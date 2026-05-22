"""
Stock Tracker — camada de negocio (Excel + distribuidores).

Sem interface grafica. A GUI em src/gui/ consome a classe StockTracker.
"""
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from openpyxl import Workbook, load_workbook

from .suppliers import search_part
from .suppliers.base import SupplierId

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.credentials import load_secrets

DATA_DIR = PROJECT_ROOT / "data"
EXCEL_FILE = DATA_DIR / "stock.xlsx"

SHEET_COMPONENTS = "Components"
SHEET_HISTORY = "History"


class StockTracker:
    """
    Class that manages stock (Excel + Mouser API).

    Example:
        tracker = StockTracker()
        row = tracker.find_component("581-SR4M3DC12")
    """

    def __init__(self, excel_path: Optional[Path] = None, api_key: str = ""):
        self.excel_file = Path(excel_path) if excel_path else EXCEL_FILE
        self._secrets = load_secrets()
        # Compatibilidade: api_key no construtor ou MOUSER_API_KEY em secrets
        if api_key:
            self._secrets["MOUSER_API_KEY"] = api_key
        self.api_key = str(self._secrets.get("MOUSER_API_KEY", "")).strip()
        self._ensure_data_folder()

    def _ensure_data_folder(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Excel helpers
    # ------------------------------------------------------------------
    def get_workbook(self):
        try:
            return load_workbook(self.excel_file)
        except FileNotFoundError:
            wb = Workbook()
            wb.active.title = SHEET_COMPONENTS
            return wb

    def get_components_sheet(self, workbook):
        if SHEET_COMPONENTS not in workbook.sheetnames:
            sheet = workbook.create_sheet(SHEET_COMPONENTS)
        else:
            sheet = workbook[SHEET_COMPONENTS]

        if sheet.max_row == 1 and sheet["A1"].value is None:
            sheet.append([
                "ID", "Mouser Reference", "Manufacturer",
                "Manufacturer Reference", "Value", "Description", "Stock",
            ])
        return sheet

    def get_history_sheet(self, workbook):
        if SHEET_HISTORY not in workbook.sheetnames:
            history = workbook.create_sheet(SHEET_HISTORY)
        else:
            history = workbook[SHEET_HISTORY]

        if history.max_row == 1 and history["A1"].value is None:
            history.append([
                "Date", "User", "Mouser Reference",
                "Movement", "Quantity", "Stock After",
            ])
        return history

    def save_workbook(self, workbook) -> bool:
        try:
            workbook.save(self.excel_file)
            return True
        except PermissionError:
            print("ERRO: Fecha o stock.xlsx no Excel antes de guardar.")
            return False

    # ------------------------------------------------------------------
    # Search / barcode
    # ------------------------------------------------------------------
    @staticmethod
    def extract_part_number(text: str) -> str:
        text = text.strip()
        match = re.search(r"P([A-Z0-9\-]+)Q", text, re.IGNORECASE)
        if match:
            return match.group(1)
        return text

    @staticmethod
    def normalize_ref(text) -> str:
        if text is None:
            return ""
        value = str(text).strip().upper()
        return value

    def refs_match(self, query: str, *candidates) -> bool:
        q = self.normalize_ref(query)
        if not q or len(q) < 2:
            return False
        for raw in candidates:
            c = self.normalize_ref(raw)
            if not c:
                continue
            if q == c or q in c or c in q:
                return True
        return False

    @staticmethod
    def row_is_empty(row) -> bool:
        return all(
            cell.value is None or str(cell.value).strip() == ""
            for cell in row
        )

    def find_component(self, sheet, part_number: str):
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(row):
                continue
            if self.refs_match(
                part_number,
                row[1].value,
                row[2].value,
                row[3].value,
                row[5].value,
            ):
                return row
        return None

    def find_component_any(self, sheet, *queries: str):
        seen = set()
        for query in queries:
            key = self.normalize_ref(query)
            if not key or key in seen:
                continue
            seen.add(key)
            row = self.find_component(sheet, query)
            if row:
                return row
        return None

    def search_in_excel_all(self, sheet, query: str) -> list:
        """All rows matching query (Mouser ref, manufacturer, mfr ref, description)."""
        results = []
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(row):
                continue
            if self.refs_match(
                query,
                row[1].value,
                row[2].value,
                row[3].value,
                row[5].value,
            ):
                results.append(row)
        return results

    def search_in_excel(self, sheet, query: str):
        matches = self.search_in_excel_all(sheet, query)
        return matches[0] if matches else None

    def excel_autocomplete_terms(self, sheet) -> list[str]:
        """Referencias no Excel para sugestoes ao escrever (pesquisa manual)."""
        seen: set[str] = set()
        terms: list[str] = []
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(row):
                continue
            for col in (1, 2, 3):
                text = str(row[col].value or "").strip()
                if len(text) < 2:
                    continue
                key = text.upper()
                if key in seen:
                    continue
                seen.add(key)
                terms.append(text)
        return sorted(terms, key=lambda x: x.upper())

    def excel_autocomplete_mouser_refs(self, sheet) -> list[str]:
        """Referencias Mouser (coluna 1) para sugestoes no campo barcode/scan."""
        seen: set[str] = set()
        refs: list[str] = []
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(row):
                continue
            text = str(row[1].value or "").strip()
            if len(text) < 1:
                continue
            key = text.upper()
            if key in seen:
                continue
            seen.add(key)
            refs.append(text)
        return sorted(refs, key=lambda x: x.upper())

    def list_components(self, sheet) -> list:
        """Lista componentes (ignora linhas vazias)."""
        items = []
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(row):
                continue
            items.append(self.row_to_dict(row))
        return items

    def row_to_dict(self, row) -> dict:
        return {
            "mouser": row[1].value or "",
            "manufacturer": row[2].value or "",
            "manufacturer_ref": row[3].value or "",
            "description": row[5].value or "",
            "stock": row[6].value if row[6].value is not None else 0,
        }

    def component_exists(
        self, sheet, mouser_ref: str, manufacturer_ref: str = ""
    ) -> bool:
        return self.find_component_any(sheet, mouser_ref, manufacturer_ref) is not None

    def get_history_rows(
        self, workbook, component_only: bool = False, mouser_ref: str = ""
    ) -> list:
        history = self.get_history_sheet(workbook)
        rows = list(history.iter_rows(min_row=2, values_only=True))
        if component_only and mouser_ref:
            rows = [
                row for row in rows if str(row[2]).strip() == mouser_ref.strip()
            ]
        return list(reversed(rows[-20:]))

    def next_component_id(self, sheet) -> int:
        max_id = 0
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1):
            try:
                max_id = max(max_id, int(row[0].value or 0))
            except (TypeError, ValueError):
                pass
        return max_id + 1

    def add_component_row(
        self,
        sheet,
        mouser_ref: str,
        manufacturer: str = "",
        manufacturer_ref: str = "",
        description: str = "",
        stock: int = 0,
    ) -> None:
        sheet.append([
            self.next_component_id(sheet),
            mouser_ref,
            manufacturer,
            manufacturer_ref,
            "",
            description,
            stock,
        ])

    # ------------------------------------------------------------------
    # Distribuidores (Mouser, TME, ...)
    # ------------------------------------------------------------------
    def search_supplier(
        self, supplier: SupplierId, part_number: str
    ) -> Optional[dict]:
        """Pesquisa num fornecedor; devolve dict compativel com codigo existente."""
        part = search_part(supplier, part_number, self._secrets)
        return dict(part) if part else None

    def search_mouser(self, part_number: str) -> Optional[dict]:
        return self.search_supplier("mouser", part_number)

    def search_digikey(self, part_number: str) -> Optional[dict]:
        return self.search_supplier("digikey", part_number)

    def search_rs(self, part_number: str) -> Optional[dict]:
        return self.search_supplier("rs", part_number)

    def search_tme(self, part_number: str) -> Optional[dict]:
        return self.search_supplier("tme", part_number)

    def configured_suppliers(self) -> list[str]:
        from .suppliers.credentials import configured_suppliers

        return configured_suppliers(self._secrets)

    # ------------------------------------------------------------------
    # Stock movements
    # ------------------------------------------------------------------
    def add_history(self, history, user, mouser_ref, movement, qty, stock_after):
        history.append([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user,
            mouser_ref,
            movement,
            qty,
            stock_after,
        ])

    def update_stock(self, user: str, code: str, quantity: int, movement: str) -> bool:
        """
        movement: "IN" or "OUT"
        Returns True if saved successfully.
        """
        workbook = self.get_workbook()
        sheet = self.get_components_sheet(workbook)
        history = self.get_history_sheet(workbook)

        part_number = self.extract_part_number(code)
        row = self.find_component_any(sheet, part_number, code)
        if row is None:
            print("Componente nao encontrado.")
            return False

        current = int(row[6].value or 0)
        if movement == "IN":
            new_stock = current + quantity
        else:
            if current < quantity:
                print("Stock insuficiente.")
                return False
            new_stock = current - quantity

        row[6].value = new_stock
        self.add_history(
            history, user, row[1].value, movement, quantity, new_stock
        )
        return self.save_workbook(workbook)

    def add_from_mouser_and_stock_in(
        self, user: str, code: str, quantity: int
    ) -> bool:
        """
        Full flow:
        1) If component exists in Excel -> add stock (IN)
        2) If not -> search Mouser -> add row -> add stock (IN)
        """
        if quantity <= 0:
            print("Quantidade tem de ser maior que 0.")
            return False

        workbook = self.get_workbook()
        sheet = self.get_components_sheet(workbook)
        history = self.get_history_sheet(workbook)

        part_number = self.extract_part_number(code)
        row = self.find_component_any(sheet, part_number, code)

        if row is None:
            part = self.search_mouser(part_number)
            if part is None:
                print("Nao encontrado no Excel nem na Mouser.")
                return False

            mouser_ref = part.get("MouserPartNumber", part_number)
            if self.find_component_any(sheet, mouser_ref):
                row = self.find_component_any(sheet, mouser_ref)
            else:
                self.add_component_row(
                    sheet,
                    mouser_ref=mouser_ref,
                    manufacturer=part.get("Manufacturer", ""),
                    manufacturer_ref=part.get("ManufacturerPartNumber", ""),
                    description=part.get("Description", ""),
                    stock=0,
                )
                if not self.save_workbook(workbook):
                    return False
                print(f"Novo componente adicionado ao Excel: {mouser_ref}")
                workbook = self.get_workbook()
                sheet = self.get_components_sheet(workbook)
                history = self.get_history_sheet(workbook)
                row = self.find_component_any(sheet, mouser_ref, part_number, code)

        if row is None:
            print("Erro ao localizar componente apos guardar.")
            return False

        current = int(row[6].value or 0)
        new_stock = current + quantity
        row[6].value = new_stock
        self.add_history(
            history, user, row[1].value, "IN", quantity, new_stock
        )
        if self.save_workbook(workbook):
            print(f"Stock atualizado: {new_stock}")
            return True
        return False
