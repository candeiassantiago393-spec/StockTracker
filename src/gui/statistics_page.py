"""Inventory statistics — expiration, low stock, charts, and settings."""
from datetime import datetime
from pathlib import Path

from PySide6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QPieSeries,
    QValueAxis,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.app_settings import get_low_stock_threshold, set_low_stock_threshold
from src.core.stock import StockTracker

from .location_combo import format_locations_display
from .inventory_report_pdf import export_inventory_report_pdf
from .message_dialog import SiemensMessage
from . import styles

_CHART_COLORS = (
    QColor("#00CCCC"),
    QColor("#00FFB9"),
    QColor("#5B8DEF"),
    QColor("#FFB84D"),
)

_TABLE_STYLE = """
QTableWidget {
    background-color: #00183B;
    color: #FFFFFF;
    gridline-color: #2A3F5F;
    border: 1px solid #2A3F5F;
}
QHeaderView::section {
    background-color: #002A4F;
    color: #00CCCC;
    padding: 6px;
    border: 1px solid #2A3F5F;
}
"""


class StatisticsPage(QWidget):
    """Dashboard: equipment expiry, low stock lists, inventory charts."""

    def __init__(self, tracker: StockTracker, main_window) -> None:
        super().__init__()
        self.tracker = tracker
        self.main = main_window
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(*styles.TEMPLATE_PAGE_MARGINS)
        root.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("Statistics")
        title.setStyleSheet("font-size: 28px; font-weight: 600; color: #00CCCC;")
        header.addWidget(title)
        header.addStretch()

        header.addWidget(QLabel("Low stock ≤"))
        self._threshold_spin = QSpinBox()
        self._threshold_spin.setRange(0, 99999)
        self._threshold_spin.setValue(get_low_stock_threshold())
        self._threshold_spin.setMinimumWidth(80)
        header.addWidget(self._threshold_spin)
        self.btn_apply_threshold = QPushButton("APPLY")
        self.btn_apply_threshold.setMinimumWidth(80)
        self.btn_apply_threshold.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_apply_threshold.clicked.connect(self._apply_threshold)
        header.addWidget(self.btn_apply_threshold)

        self.btn_refresh = QPushButton("REFRESH")
        self.btn_refresh.setMinimumWidth(124)
        self.btn_refresh.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_refresh.clicked.connect(self.refresh)
        header.addWidget(self.btn_refresh)

        self.btn_export_pdf = QPushButton("EXPORT PDF")
        self.btn_export_pdf.setMinimumWidth(124)
        self.btn_export_pdf.setStyleSheet(styles.BTN_TEMPLATE_STYLE)
        self.btn_export_pdf.setToolTip("Export inventory report (PDF)")
        self.btn_export_pdf.clicked.connect(self._export_pdf)
        header.addWidget(self.btn_export_pdf)
        root.addLayout(header)

        body = QHBoxLayout()
        body.setSpacing(16)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        lists_host = QWidget()
        lists_layout = QVBoxLayout(lists_host)
        lists_layout.setContentsMargins(0, 0, 8, 0)
        lists_layout.setSpacing(16)

        self._summary_label = QLabel()
        self._summary_label.setWordWrap(True)
        self._summary_label.setStyleSheet("color: #B3B3BE; font-size: 13px;")
        lists_layout.addWidget(self._summary_label)

        self._locations_title = QLabel()
        self._locations_table = self._make_table(
            ("Location", "Components", "Passive", "Equipments", "Low stock", "Stock units")
        )
        lists_layout.addWidget(self._locations_title)
        lists_layout.addWidget(self._locations_table)

        self._equipments_title = QLabel()
        self._equipments_table = self._make_table(
            ("Name", "Serial", "Expiration", "Days left")
        )
        lists_layout.addWidget(self._equipments_title)
        lists_layout.addWidget(self._equipments_table)

        self._loaned_title = QLabel()
        self._loaned_table = self._make_table(
            ("Name", "Serial", "Loaned to", "Place", "Since")
        )
        lists_layout.addWidget(self._loaned_title)
        lists_layout.addWidget(self._loaned_table)

        self._components_title = QLabel()
        self._components_table = self._make_table(
            ("Component", "Supplier Ref", "Location", "Stock")
        )
        lists_layout.addWidget(self._components_title)
        lists_layout.addWidget(self._components_table)

        self._massive_title = QLabel()
        self._massive_table = self._make_table(
            ("Name", "Value", "Package", "Location", "Stock")
        )
        lists_layout.addWidget(self._massive_title)
        lists_layout.addWidget(self._massive_table)

        lists_layout.addStretch()
        scroll.setWidget(lists_host)
        body.addWidget(scroll, 3)

        charts_wrap = QWidget()
        charts_layout = QVBoxLayout(charts_wrap)
        charts_layout.setContentsMargins(0, 0, 0, 0)
        charts_layout.setSpacing(12)

        pie_title = QLabel("Inventory overview")
        pie_title.setStyleSheet("font-size: 18px; font-weight: 600; color: #00CCCC;")
        charts_layout.addWidget(pie_title)

        self._pie_chart_view = QChartView()
        self._pie_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._pie_chart_view.setMinimumHeight(200)
        charts_layout.addWidget(self._pie_chart_view, 1)

        self._legend_label = QLabel()
        self._legend_label.setWordWrap(True)
        self._legend_label.setStyleSheet("color: #FFFFFF; font-size: 13px;")
        charts_layout.addWidget(self._legend_label)

        move_title = QLabel("Stock movements (weekly)")
        move_title.setStyleSheet("font-size: 18px; font-weight: 600; color: #00CCCC;")
        charts_layout.addWidget(move_title)

        self._movement_chart_view = QChartView()
        self._movement_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._movement_chart_view.setMinimumHeight(200)
        charts_layout.addWidget(self._movement_chart_view, 1)

        loc_title = QLabel("Items per location")
        loc_title.setStyleSheet("font-size: 18px; font-weight: 600; color: #00CCCC;")
        charts_layout.addWidget(loc_title)

        self._location_chart_view = QChartView()
        self._location_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._location_chart_view.setMinimumHeight(180)
        charts_layout.addWidget(self._location_chart_view, 1)

        body.addWidget(charts_wrap, 2)
        root.addLayout(body, 1)

    def _make_table(self, columns: tuple[str, ...]) -> QTableWidget:
        table = QTableWidget(0, len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        table.setStyleSheet(_TABLE_STYLE)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setMinimumHeight(120)
        return table

    def _fill_table(self, table: QTableWidget, rows: list[tuple]) -> None:
        table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                table.setItem(row_idx, col_idx, item)
        table.resizeColumnsToContents()

    def _format_days_left(self, days_left: int | None) -> str:
        if days_left is None:
            return "—"
        if days_left < 0:
            return f"Expired ({abs(days_left)}d ago)"
        if days_left == 0:
            return "Today"
        return str(days_left)

    def _apply_threshold(self) -> None:
        value = set_low_stock_threshold(self._threshold_spin.value())
        self._threshold_spin.setValue(value)
        self.refresh()
        self.main.set_status(f"Low stock threshold set to ≤ {value}.")

    def refresh(self) -> None:
        threshold = get_low_stock_threshold()
        self._threshold_spin.setValue(threshold)
        equipments = self.tracker.get_equipment_expiration_stats()
        loaned = self.tracker.get_loaned_equipments()
        low_components = self.tracker.get_low_stock_components(threshold)
        low_massive = self.tracker.get_low_stock_massive(threshold)
        location_stats = self.tracker.get_location_statistics(threshold)
        distribution = self.tracker.get_inventory_distribution()
        movements = self.tracker.get_weekly_movement_stats(weeks=8)

        self._summary_label.setText(
            f"Low stock threshold: ≤ {threshold} units. "
            f"Equipment sorted by calibration expiration (soonest first). "
            f"Locations include multi-tag components (each location counted separately)."
        )

        self._locations_title.setText(f"Storage locations ({len(location_stats)})")
        self._fill_table(
            self._locations_table,
            [
                (
                    item.get("location") or "—",
                    item.get("components", 0),
                    item.get("passive", 0),
                    item.get("equipments", 0),
                    item.get("low_stock", 0),
                    item.get("stock_units", 0),
                )
                for item in location_stats
            ],
        )

        self._equipments_title.setText(
            f"Equipments — calibration expiration ({len(equipments)})"
        )
        self._fill_table(
            self._equipments_table,
            [
                (
                    item.get("name") or item.get("description") or "—",
                    item.get("serial_number") or "—",
                    item.get("calibration_expiration") or "—",
                    self._format_days_left(item.get("days_left")),
                )
                for item in equipments
            ],
        )

        self._loaned_title.setText(f"Equipments — on loan ({len(loaned)})")
        self._fill_table(
            self._loaned_table,
            [
                (
                    item.get("name") or item.get("description") or "—",
                    item.get("serial_number") or "—",
                    item.get("loaned_to") or "—",
                    item.get("loan_place") or "—",
                    item.get("loan_since") or "—",
                )
                for item in loaned
            ],
        )

        self._components_title.setText(
            f"Components — low stock ({len(low_components)})"
        )
        self._fill_table(
            self._components_table,
            [
                (
                    item.get("label") or "—",
                    item.get("mouser") or item.get("manufacturer_ref") or "—",
                    format_locations_display(
                        self.tracker.parse_component_locations(item.get("location", ""))
                    )
                    or "—",
                    item.get("stock", 0),
                )
                for item in low_components
            ],
        )

        self._massive_title.setText(
            f"Passive (R/C) — low stock ({len(low_massive)})"
        )
        self._fill_table(
            self._massive_table,
            [
                (
                    item.get("name") or "—",
                    item.get("value") or "—",
                    item.get("package") or "—",
                    item.get("location") or "—",
                    item.get("stock", 0),
                )
                for item in low_massive
            ],
        )

        self._update_pie_chart(distribution)
        self._update_movement_chart(movements)
        self._update_location_chart(location_stats)
        self.main.set_status("Statistics refreshed.")

    def _export_pdf(self) -> None:
        default_name = f"inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        reports_dir = Path(__file__).resolve().parents[2] / "data" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export inventory report",
            str(reports_dir / default_name),
            "PDF files (*.pdf)",
        )
        if not path:
            self.main.set_status("Export cancelled.")
            return
        try:
            saved = export_inventory_report_pdf(self.tracker, Path(path))
        except OSError as exc:
            SiemensMessage.warning(self, "Export failed", str(exc))
            self.main.set_status("Report export failed.")
            return
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices

        QDesktopServices.openUrl(QUrl.fromLocalFile(str(saved.parent)))
        self.main.set_status(f"Report exported to {saved}")
        SiemensMessage.information(
            self,
            "Export",
            f"Report saved:\n{saved}\n\nThe folder was opened in File Explorer.",
        )

    def _update_pie_chart(self, distribution: list[dict]) -> None:
        series = QPieSeries()
        legend_lines: list[str] = []
        total_count = sum(int(item.get("count") or 0) for item in distribution)

        for index, item in enumerate(distribution):
            count = int(item.get("count") or 0)
            if count <= 0:
                continue
            label = str(item.get("label") or "Item")
            stock = int(item.get("stock") or 0)
            pie_slice = series.append(f"{label} ({count})", count)
            color = _CHART_COLORS[index % len(_CHART_COLORS)]
            pie_slice.setColor(color)
            pie_slice.setLabelVisible(count > 0 and total_count > 0)
            if item.get("key") == "equipments":
                legend_lines.append(
                    f'<span style="color:{color.name()}">■</span> {label}: '
                    f"{count} item(s)"
                )
            else:
                legend_lines.append(
                    f'<span style="color:{color.name()}">■</span> {label}: '
                    f"{count} item(s), stock {stock}"
                )

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Items by category")
        chart.setTitleBrush(QColor("#00CCCC"))
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        chart.setBackgroundVisible(False)
        chart.setPlotAreaBackgroundVisible(False)
        chart.setTheme(QChart.ChartTheme.ChartThemeDark)
        if series.count() == 0:
            chart.setTitle("No inventory data yet")

        self._pie_chart_view.setChart(chart)
        self._legend_label.setText(
            "<br>".join(legend_lines) if legend_lines else "No data to display."
        )

    def _update_movement_chart(self, movements: list[dict]) -> None:
        chart = QChart()
        chart.setTheme(QChart.ChartTheme.ChartThemeDark)
        chart.setBackgroundVisible(False)
        chart.setPlotAreaBackgroundVisible(False)
        chart.setTitle("IN vs OUT (last weeks)")
        chart.setTitleBrush(QColor("#00CCCC"))

        if not movements:
            chart.setTitle("No movement history yet")
            self._movement_chart_view.setChart(chart)
            return

        set_in = QBarSet("IN")
        set_out = QBarSet("OUT")
        set_in.setColor(QColor("#00FFB9"))
        set_out.setColor(QColor("#FF6B8A"))
        categories: list[str] = []

        for entry in movements:
            categories.append(str(entry.get("label", "")))
            set_in.append(int(entry.get("in") or 0))
            set_out.append(int(entry.get("out") or 0))

        series = QBarSeries()
        series.append(set_in)
        series.append(set_out)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor("#FFFFFF"))
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelsColor(QColor("#FFFFFF"))
        max_val = max(
            [int(entry.get("in") or 0) for entry in movements]
            + [int(entry.get("out") or 0) for entry in movements]
            + [1]
        )
        axis_y.setRange(0, max_val)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self._movement_chart_view.setChart(chart)

    def _update_location_chart(self, location_stats: list[dict]) -> None:
        chart = QChart()
        chart.setTheme(QChart.ChartTheme.ChartThemeDark)
        chart.setBackgroundVisible(False)
        chart.setPlotAreaBackgroundVisible(False)
        chart.setTitle("Tagged items per location")
        chart.setTitleBrush(QColor("#00CCCC"))

        ranked = [
            item
            for item in location_stats
            if int(item.get("total_items") or 0) > 0
            and item.get("location") != StockTracker.UNASSIGNED_LOCATION
        ]
        ranked.sort(key=lambda item: int(item.get("total_items") or 0), reverse=True)
        ranked = ranked[:10]

        if not ranked:
            chart.setTitle("No locations in use yet")
            self._location_chart_view.setChart(chart)
            return

        set_components = QBarSet("Components")
        set_passive = QBarSet("Passive")
        set_equipments = QBarSet("Equipments")
        set_components.setColor(QColor("#00CCCC"))
        set_passive.setColor(QColor("#5B8DEF"))
        set_equipments.setColor(QColor("#FFB84D"))
        categories: list[str] = []

        for item in ranked:
            categories.append(str(item.get("location") or "—"))
            set_components.append(int(item.get("components") or 0))
            set_passive.append(int(item.get("passive") or 0))
            set_equipments.append(int(item.get("equipments") or 0))

        series = QBarSeries()
        series.append(set_components)
        series.append(set_passive)
        series.append(set_equipments)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor("#FFFFFF"))
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelsColor(QColor("#FFFFFF"))
        max_val = max(
            [int(item.get("total_items") or 0) for item in ranked] + [1]
        )
        axis_y.setRange(0, max_val)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self._location_chart_view.setChart(chart)
