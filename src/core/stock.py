###############################################################################
# 1. Module Level Documentation
###############################################################################
"""
Stock Tracker — business layer (Excel inventory + distributor APIs).

No GUI code in this module. The PySide6 layer in `src/gui/` uses `StockTracker`.
See `docs/PROJETO_STOCKTRACKER.md` for data model and SCAN flow.
"""

###############################################################################
# 2. Imports
###############################################################################
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from openpyxl import Workbook, load_workbook

from .suppliers import search_part, supplier_label
from .suppliers.base import SupplierId

###############################################################################
# 3. Constants and Global Variables
###############################################################################
_SUPPLIER_SEARCH_ORDER: tuple[SupplierId, ...] = (
    "mouser",
    "tme",
    "rs",
    "digikey",
    "robert_mauser",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.credentials import load_secrets

DATA_DIR = PROJECT_ROOT / "data"
EXCEL_FILE = DATA_DIR / "stock.xlsx"

SHEET_COMPONENTS = "Components"
SHEET_HISTORY = "History"
SHEET_MATERIALS = "Materials"

###############################################################################
# 4. StockTracker class
###############################################################################


class StockTracker:
    """
    Class:
        Manages component inventory in Excel and optional distributor catalog lookup.
    Args:
        excel_path (Path | None): Override path to workbook; default `data/stock.xlsx`.
        api_key (str): Optional Mouser key; otherwise loaded from `config/secrets.py`.
    Example:
        tracker = StockTracker()
        wb = tracker.get_workbook()
        sheet = tracker.get_components_sheet(wb)
        row = tracker.find_component(sheet, "581-SR4M3DC12")
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
                "ID", "Supplier Reference", "Manufacturer",
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
                "Date", "User", "Supplier Reference",
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

    def ensure_workbook_sheets(self) -> bool:
        """Create Components, Materials and History sheets if missing, then save."""
        workbook = self.get_workbook()
        self.get_components_sheet(workbook)
        self.get_history_sheet(workbook)
        self.get_materials_sheet(workbook)
        self._order_workbook_sheets(workbook)
        self._remove_default_sheet(workbook)
        return self.save_workbook(workbook)

    @staticmethod
    def _order_workbook_sheets(workbook) -> None:
        order = (SHEET_COMPONENTS, SHEET_MATERIALS, SHEET_HISTORY)
        for target_idx, name in enumerate(order):
            if name not in workbook.sheetnames:
                continue
            current_idx = workbook.sheetnames.index(name)
            offset = target_idx - current_idx
            if offset:
                workbook.move_sheet(name, offset)

    @staticmethod
    def _remove_default_sheet(workbook) -> None:
        if "Sheet" not in workbook.sheetnames:
            return
        sheet = workbook["Sheet"]
        if sheet.max_row <= 1 and not sheet["A1"].value:
            workbook.remove(sheet)

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

    def excel_autocomplete_supplier_refs(self, sheet) -> list[str]:
        """Supplier references (column 1) for barcode/scan autocomplete."""
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

    def excel_autocomplete_mouser_refs(self, sheet) -> list[str]:
        """Backward-compatible alias."""
        return self.excel_autocomplete_supplier_refs(sheet)

    @staticmethod
    def part_supplier_reference(part: dict, fallback: str = "") -> str:
        return str(
            part.get("supplier_part_number")
            or part.get("MouserPartNumber")
            or fallback
        ).strip()

    @staticmethod
    def part_manufacturer(part: dict) -> str:
        return str(part.get("manufacturer") or part.get("Manufacturer") or "")

    @staticmethod
    def part_manufacturer_reference(part: dict) -> str:
        return str(
            part.get("manufacturer_part_number")
            or part.get("ManufacturerPartNumber")
            or ""
        )

    @staticmethod
    def part_description(part: dict) -> str:
        return str(part.get("description") or part.get("Description") or "")

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

    def _find_by_manufacturer_pair(
        self, sheet, manufacturer: str, manufacturer_ref: str
    ):
        manufacturer_n = self.normalize_ref(manufacturer)
        manufacturer_ref_n = self.normalize_ref(manufacturer_ref)
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(row):
                continue
            row_manufacturer = self.normalize_ref(row[2].value)
            row_manufacturer_ref = self.normalize_ref(row[3].value)
            if (
                row_manufacturer == manufacturer_n
                and row_manufacturer_ref == manufacturer_ref_n
            ):
                return row
        return None

    def add_manual_component(
        self,
        user: str,
        supplier_reference: str = "",
        manufacturer: str = "",
        manufacturer_reference: str = "",
        description: str = "",
        initial_stock: int = 0,
    ) -> tuple[bool, str]:
        supplier_reference = str(supplier_reference).strip()
        manufacturer = str(manufacturer).strip()
        manufacturer_reference = str(manufacturer_reference).strip()
        description = str(description).strip()

        if initial_stock < 0:
            return False, "Initial stock cannot be negative."
        if not supplier_reference and not (manufacturer and manufacturer_reference):
            return (
                False,
                "Provide Supplier Reference OR both Manufacturer and Manufacturer Reference.",
            )

        workbook = self.get_workbook()
        sheet = self.get_components_sheet(workbook)
        history = self.get_history_sheet(workbook)

        if supplier_reference:
            if self.find_component_any(sheet, supplier_reference):
                return False, "A component with this supplier reference already exists."
        elif self._find_by_manufacturer_pair(sheet, manufacturer, manufacturer_reference):
            return (
                False,
                "A component with this Manufacturer + Manufacturer Reference already exists.",
            )

        self.add_component_row(
            sheet,
            mouser_ref=supplier_reference,
            manufacturer=manufacturer,
            manufacturer_ref=manufacturer_reference,
            description=description,
            stock=initial_stock,
        )

        if initial_stock > 0:
            history_ref = supplier_reference or manufacturer_reference or "MANUAL"
            self.add_history(history, user, history_ref, "IN", initial_stock, initial_stock)

        if not self.save_workbook(workbook):
            return False, "Close stock.xlsx in Excel before saving."

        return True, "Manual component added successfully."

    def update_component(
        self,
        row,
        supplier_reference: str = "",
        manufacturer: str = "",
        manufacturer_reference: str = "",
        description: str = "",
    ) -> tuple[bool, str]:
        supplier_reference = str(supplier_reference).strip()
        manufacturer = str(manufacturer).strip()
        manufacturer_reference = str(manufacturer_reference).strip()
        description = str(description).strip()

        if not supplier_reference and not (manufacturer and manufacturer_reference):
            return (
                False,
                "Provide Supplier Reference OR both Manufacturer and Manufacturer Reference.",
            )

        workbook = self.get_workbook()
        sheet = self.get_components_sheet(workbook)
        target_row = row[0].row

        for other in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(other) or other[0].row == target_row:
                continue
            if supplier_reference and self.normalize_ref(
                other[1].value
            ) == self.normalize_ref(supplier_reference):
                return False, "Another component already uses this supplier reference."
            if (
                manufacturer
                and manufacturer_reference
                and self.normalize_ref(other[2].value)
                == self.normalize_ref(manufacturer)
                and self.normalize_ref(other[3].value)
                == self.normalize_ref(manufacturer_reference)
            ):
                return (
                    False,
                    "Another component already uses this Manufacturer + Manufacturer Reference.",
                )

        row[1].value = supplier_reference
        row[2].value = manufacturer
        row[3].value = manufacturer_reference
        row[5].value = description

        if not self.save_workbook(workbook):
            return False, "Close stock.xlsx in Excel before saving."

        return True, "Component updated successfully."

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

    def search_suppliers_order(self) -> list[SupplierId]:
        """Fornecedores configurados, por ordem de pesquisa (APIs estaveis primeiro)."""
        configured = set(self.configured_suppliers())
        return [s for s in _SUPPLIER_SEARCH_ORDER if s in configured]

    def search_any_supplier(
        self, part_number: str
    ) -> tuple[Optional[dict], Optional[SupplierId]]:
        """Pesquisa em cada distribuidor configurado ate encontrar resultado."""
        for supplier in self.search_suppliers_order():
            part = self.search_supplier(supplier, part_number)
            if part is not None:
                return part, supplier
        return None, None

    def configured_supplier_labels(self) -> str:
        return ", ".join(supplier_label(s) for s in self.search_suppliers_order())

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

    def add_from_supplier_and_stock_in(
        self,
        user: str,
        code: str,
        quantity: int,
        supplier: SupplierId | None = None,
    ) -> bool:
        """
        Full flow:
        1) If component exists in Excel -> add stock (IN)
        2) If not -> search distributor API(s) -> add row -> add stock (IN)
        """
        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return False

        workbook = self.get_workbook()
        sheet = self.get_components_sheet(workbook)
        history = self.get_history_sheet(workbook)

        part_number = self.extract_part_number(code)
        row = self.find_component_any(sheet, part_number, code)

        if row is None:
            if supplier is not None:
                part = self.search_supplier(supplier, part_number)
            else:
                part, _found = self.search_any_supplier(part_number)
            if part is None:
                print("Not found in Excel or distributor catalog.")
                return False

            supplier_ref = self.part_supplier_reference(part, part_number)
            manufacturer_ref = self.part_manufacturer_reference(part)
            if self.find_component_any(sheet, supplier_ref, manufacturer_ref):
                row = self.find_component_any(
                    sheet, supplier_ref, manufacturer_ref, part_number, code
                )
            else:
                self.add_component_row(
                    sheet,
                    mouser_ref=supplier_ref,
                    manufacturer=self.part_manufacturer(part),
                    manufacturer_ref=manufacturer_ref,
                    description=self.part_description(part),
                    stock=0,
                )
                if not self.save_workbook(workbook):
                    return False
                print(f"New component added to Excel: {supplier_ref}")
                workbook = self.get_workbook()
                sheet = self.get_components_sheet(workbook)
                history = self.get_history_sheet(workbook)
                row = self.find_component_any(
                    sheet, supplier_ref, manufacturer_ref, part_number, code
                )

        if row is None:
            print("Could not locate component after save.")
            return False

        current = int(row[6].value or 0)
        new_stock = current + quantity
        row[6].value = new_stock
        self.add_history(
            history, user, row[1].value, "IN", quantity, new_stock
        )
        if self.save_workbook(workbook):
            print(f"Stock updated: {new_stock}")
            return True
        return False

    def add_from_mouser_and_stock_in(
        self, user: str, code: str, quantity: int
    ) -> bool:
        """Pesquisa em todos os distribuidores configurados (nome legado)."""
        return self.add_from_supplier_and_stock_in(user, code, quantity)

    # ------------------------------------------------------------------
    # Materials (calibration tracking)
    # ------------------------------------------------------------------
    def get_materials_sheet(self, workbook):
        if SHEET_MATERIALS not in workbook.sheetnames:
            sheet = workbook.create_sheet(SHEET_MATERIALS)
        else:
            sheet = workbook[SHEET_MATERIALS]

        if sheet.max_row == 0 or (
            sheet.max_row == 1 and sheet["A1"].value is None
        ):
            headers = [
                "ID",
                "Supplier Reference",
                "Serial Number",
                "Description",
                "Calibration Date",
                "Calibration Expiration Date",
            ]
            if sheet.max_row == 0:
                sheet.append(headers)
            else:
                for col, value in enumerate(headers, start=1):
                    sheet.cell(row=1, column=col, value=value)
        else:
            self._migrate_materials_sheet(sheet)
        return sheet

    @staticmethod
    def _migrate_materials_sheet(sheet) -> None:
        """Upgrade legacy Materials sheets to the current column layout."""
        if str(sheet["A1"].value or "").strip() != "ID":
            return
        b1 = str(sheet["B1"].value or "").strip()
        if b1 == "Description":
            sheet.insert_cols(2)
            sheet["B1"] = "Supplier Reference"
            b1 = "Supplier Reference"
        c1 = str(sheet["C1"].value or "").strip()
        if b1 == "Supplier Reference" and c1 == "Description":
            sheet.insert_cols(3)
            sheet["C1"] = "Serial Number"

    @staticmethod
    def normalize_date(text) -> str:
        """Return YYYY-MM-DD or empty string."""
        if text is None:
            return ""
        value = str(text).strip()
        if not value:
            return ""
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return value

    @staticmethod
    def validate_date(text: str) -> tuple[bool, str]:
        raw = str(text or "").strip()
        if not raw:
            return True, ""
        normalized = StockTracker.normalize_date(raw)
        try:
            datetime.strptime(normalized, "%Y-%m-%d")
            return True, normalized
        except ValueError:
            return False, ""

    def search_materials_all(self, sheet, query: str) -> list:
        """All material rows matching supplier reference or description."""
        results = []
        q = self.normalize_ref(query)
        if not q:
            return results
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(row):
                continue
            supplier_ref = self.normalize_ref(row[1].value)
            serial = self.normalize_ref(row[2].value)
            desc = self.normalize_ref(row[3].value)
            if (
                q in supplier_ref
                or supplier_ref in q
                or q in serial
                or serial in q
                or q in desc
                or desc in q
            ):
                results.append(row)
        return results

    def find_material_by_supplier_ref(self, sheet, supplier_ref: str):
        key = self.normalize_ref(supplier_ref)
        if not key:
            return None
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(row):
                continue
            if self.normalize_ref(row[1].value) == key:
                return row
        return None

    def material_row_to_dict(self, row) -> dict:
        return {
            "id": row[0].value or "",
            "supplier_reference": row[1].value or "",
            "serial_number": row[2].value or "",
            "description": row[3].value or "",
            "calibration_date": self.normalize_date(row[4].value),
            "calibration_expiration": self.normalize_date(row[5].value),
        }

    def next_material_id(self, sheet) -> int:
        max_id = 0
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1):
            try:
                max_id = max(max_id, int(row[0].value or 0))
            except (TypeError, ValueError):
                pass
        return max_id + 1

    def add_material(
        self,
        description: str = "",
        supplier_reference: str = "",
        serial_number: str = "",
        calibration_date: str = "",
        calibration_expiration: str = "",
    ) -> tuple[bool, str]:
        description = str(description).strip()
        supplier_reference = str(supplier_reference).strip()
        serial_number = str(serial_number).strip()
        if not description and not supplier_reference and not serial_number:
            return False, "Provide Description, Supplier Reference or Serial Number."

        ok, calib = self.validate_date(calibration_date)
        if not ok:
            return False, "Invalid calibration date (use YYYY-MM-DD)."
        ok, expiry = self.validate_date(calibration_expiration)
        if not ok:
            return False, "Invalid expiration date (use YYYY-MM-DD)."

        workbook = self.get_workbook()
        sheet = self.get_materials_sheet(workbook)
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(row):
                continue
            if supplier_reference and self.normalize_ref(
                row[1].value
            ) == self.normalize_ref(supplier_reference):
                return False, "A material with this supplier reference already exists."
            if serial_number and self.normalize_ref(
                row[2].value
            ) == self.normalize_ref(serial_number):
                return False, "A material with this serial number already exists."
            if description and self.normalize_ref(
                row[3].value
            ) == self.normalize_ref(description):
                return False, "A material with this description already exists."

        sheet.append([
            self.next_material_id(sheet),
            supplier_reference,
            serial_number,
            description,
            calib,
            expiry,
        ])
        if not self.save_workbook(workbook):
            return False, "Close stock.xlsx in Excel before saving."
        return True, "Material added successfully."

    def update_material(
        self,
        row,
        description: str = "",
        supplier_reference: str = "",
        serial_number: str = "",
        calibration_date: str = "",
        calibration_expiration: str = "",
    ) -> tuple[bool, str]:
        description = str(description).strip()
        supplier_reference = str(supplier_reference).strip()
        serial_number = str(serial_number).strip()
        if not description and not supplier_reference and not serial_number:
            return False, "Provide Description, Supplier Reference or Serial Number."

        ok, calib = self.validate_date(calibration_date)
        if not ok:
            return False, "Invalid calibration date (use YYYY-MM-DD)."
        ok, expiry = self.validate_date(calibration_expiration)
        if not ok:
            return False, "Invalid expiration date (use YYYY-MM-DD)."

        workbook = self.get_workbook()
        sheet = self.get_materials_sheet(workbook)
        target_row = row[0].row
        ref_norm = self.normalize_ref(supplier_reference)
        serial_norm = self.normalize_ref(serial_number)
        desc_norm = self.normalize_ref(description)

        for other in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(other) or other[0].row == target_row:
                continue
            if supplier_reference and self.normalize_ref(other[1].value) == ref_norm:
                return False, "Another material already uses this supplier reference."
            if serial_number and self.normalize_ref(other[2].value) == serial_norm:
                return False, "Another material already uses this serial number."
            if description and self.normalize_ref(other[3].value) == desc_norm:
                return False, "Another material already uses this description."

        row[1].value = supplier_reference
        row[2].value = serial_number
        row[3].value = description
        row[4].value = calib
        row[5].value = expiry

        if not self.save_workbook(workbook):
            return False, "Close stock.xlsx in Excel before saving."
        return True, "Material updated successfully."

    def get_material_rows(
        self,
        workbook,
        material_only: bool = False,
        supplier_reference: str = "",
        description: str = "",
    ) -> list:
        """Rows for materials table dialog (last 20, newest first)."""
        sheet = self.get_materials_sheet(workbook)
        ref_filter = self.normalize_ref(supplier_reference) if material_only else ""
        desc_filter = self.normalize_ref(description) if material_only else ""
        rows: list[tuple] = []
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if self.row_is_empty(row):
                continue
            if material_only and (ref_filter or desc_filter):
                row_ref = self.normalize_ref(row[1].value)
                row_desc = self.normalize_ref(row[3].value)
                if ref_filter and row_ref != ref_filter:
                    continue
                if desc_filter and row_desc != desc_filter:
                    continue
            data = self.material_row_to_dict(row)
            rows.append((
                data["id"],
                data["supplier_reference"],
                data["serial_number"],
                data["description"],
                data["calibration_date"],
                data["calibration_expiration"],
            ))
        return list(reversed(rows[-20:]))
