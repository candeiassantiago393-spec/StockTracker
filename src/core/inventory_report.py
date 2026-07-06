"""Aggregate inventory statistics for PDF export."""
from __future__ import annotations

from datetime import datetime

from .app_settings import get_low_stock_threshold
from .stock import StockTracker


def build_inventory_report(tracker: StockTracker) -> dict:
    threshold = get_low_stock_threshold()
    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "threshold": threshold,
        "location_stats": tracker.get_location_statistics(threshold),
        "equipments_expiry": tracker.get_equipment_expiration_stats(),
        "loaned": tracker.get_loaned_equipments(),
        "low_components": tracker.get_low_stock_components(threshold),
        "low_massive": tracker.get_low_stock_massive(threshold),
        "missing_location": tracker.get_items_without_location(),
        "distribution": tracker.get_inventory_distribution(),
        "movements": tracker.get_weekly_movement_stats(weeks=8),
    }
