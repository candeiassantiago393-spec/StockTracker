"""Open stock.xlsx in Excel, optionally focused on a sheet cell."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def excel_cell_url(
    excel_path: Path, sheet_name: str, row: int, *, column: str = "B"
) -> str:
    """Build a file:/// URL that opens Excel on the given sheet and cell."""
    uri = excel_path.resolve().as_posix()
    cell = f"{str(column or 'B').strip().upper()}{int(row)}"
    sheet = str(sheet_name or "").strip()
    return f"file:///{uri}#'{sheet}'!{cell}"


def _focus_excel_cell_com(
    excel_path: Path, sheet_name: str, row: int, *, column: str = "B"
) -> bool:
    """Activate an open workbook and select a cell (Windows + Excel installed)."""
    if sys.platform != "win32":
        return False
    try:
        import win32com.client  # type: ignore[import-untyped]
    except ImportError:
        return False

    target = Path(excel_path).resolve()
    cell = f"{str(column or 'B').strip().upper()}{int(row)}"

    try:
        try:
            excel = win32com.client.GetActiveObject("Excel.Application")
        except Exception:
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = True

        workbook = None
        target_key = str(target).lower()
        for book in excel.Workbooks:
            try:
                if str(Path(book.FullName).resolve()).lower() == target_key:
                    workbook = book
                    break
            except Exception:
                continue

        if workbook is None:
            workbook = excel.Workbooks.Open(str(target))

        worksheet = workbook.Worksheets(sheet_name)
        worksheet.Activate()
        worksheet.Range(cell).Select()
        excel.Visible = True
        excel.WindowState = -4137  # xlNormal
        return True
    except Exception:
        return False


def launch_excel(
    excel_path: Path,
    *,
    sheet_name: str | None = None,
    row: int | None = None,
    column: str = "B",
) -> None:
    """Open stock.xlsx; jump to sheet/cell when provided."""
    path = Path(excel_path).resolve()

    if sheet_name and row:
        if _focus_excel_cell_com(path, sheet_name, row, column=column):
            return
        if sys.platform == "win32":
            os.startfile(excel_cell_url(path, sheet_name, row, column=column))
            return

    os.startfile(str(path))
