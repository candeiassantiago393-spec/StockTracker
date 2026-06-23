"""
Calibration expiration email alerts for equipment inventory.

Runs when the Stock Tracker GUI starts (and daily while open). Sends SMTP email
when an equipment calibration date is within the configured window.
"""
from __future__ import annotations

import json
import smtplib
import ssl
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from typing import TYPE_CHECKING

from .stock import DATA_DIR, StockTracker

if TYPE_CHECKING:
    from collections.abc import Mapping

ALERTS_STATE_FILE = DATA_DIR / "calibration_alerts_sent.json"
DEFAULT_ALERT_TO = "candeiassantiago393@gmail.com"
DEFAULT_ALERT_DAYS = 30


@dataclass
class CalibrationAlertResult:
    """Outcome of a calibration alert check."""

    sent_count: int = 0
    failures: list[str] = field(default_factory=list)
    expiring_count: int = 0
    smtp_configured: bool = False


def _parse_iso_date(value: str) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def _alert_days(secrets: Mapping[str, object]) -> int:
    raw = secrets.get("CALIBRATION_ALERT_DAYS", DEFAULT_ALERT_DAYS)
    try:
        days = int(raw)
    except (TypeError, ValueError):
        days = DEFAULT_ALERT_DAYS
    return max(1, days)


def _alert_recipient(secrets: Mapping[str, object]) -> str:
    return str(secrets.get("CALIBRATION_ALERT_TO", DEFAULT_ALERT_TO)).strip()


def _smtp_settings(secrets: Mapping[str, object]) -> dict[str, str | int] | None:
    host = str(secrets.get("SMTP_HOST", "")).strip()
    user = str(secrets.get("SMTP_USER", "")).strip()
    password = str(secrets.get("SMTP_PASSWORD", "")).replace(" ", "").strip()
    if not host or not user or not password:
        return None
    port_raw = secrets.get("SMTP_PORT", 465)
    try:
        port = int(port_raw)
    except (TypeError, ValueError):
        port = 465
    security = str(secrets.get("SMTP_SECURITY", "")).strip().lower()
    if security not in {"ssl", "starttls", "auto"}:
        security = "ssl" if port == 465 else "starttls"
    from_addr = str(secrets.get("SMTP_FROM", user)).strip() or user
    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "from_addr": from_addr,
        "security": security,
    }


def _smtp_attempts(smtp: Mapping[str, str | int]) -> list[tuple[str, int, str]]:
    host = str(smtp["host"])
    port = int(smtp["port"])
    security = str(smtp["security"])
    if security == "ssl":
        return [(host, port if port != 587 else 465, "ssl")]
    if security == "starttls":
        return [(host, port if port != 465 else 587, "starttls")]
    return [
        (host, port, "ssl" if port == 465 else "starttls"),
        (host, 465, "ssl"),
        (host, 587, "starttls"),
    ]


def _deliver_smtp_message(
    message: EmailMessage,
    smtp: Mapping[str, str | int],
) -> None:
    context = ssl.create_default_context()
    errors: list[str] = []
    seen: set[tuple[str, int, str]] = set()

    for host, port, mode in _smtp_attempts(smtp):
        key = (host, port, mode)
        if key in seen:
            continue
        seen.add(key)
        try:
            if mode == "ssl":
                with smtplib.SMTP_SSL(host, port, timeout=60, context=context) as server:
                    server.login(str(smtp["user"]), str(smtp["password"]))
                    server.send_message(message)
            else:
                with smtplib.SMTP(host, port, timeout=60) as server:
                    server.ehlo()
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(str(smtp["user"]), str(smtp["password"]))
                    server.send_message(message)
            return
        except OSError as exc:
            errors.append(f"{host}:{port} ({mode}): {exc}")

    detail = "; ".join(errors) if errors else "unknown SMTP error"
    raise OSError(detail)


def _load_state() -> dict:
    if not ALERTS_STATE_FILE.is_file():
        return {"last_sent": {}}
    try:
        data = json.loads(ALERTS_STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"last_sent": {}}
    if not isinstance(data, dict):
        return {"last_sent": {}}
    last_sent = data.get("last_sent")
    if not isinstance(last_sent, dict):
        data["last_sent"] = {}
    return data


def _save_state(state: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ALERTS_STATE_FILE.write_text(
        json.dumps(state, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _iter_expiring_equipment(
    tracker: StockTracker,
    *,
    alert_days: int,
) -> list[dict]:
    workbook = tracker.get_workbook()
    sheet = tracker.get_equipments_sheet(workbook)
    today = date.today()
    deadline = today + timedelta(days=alert_days)
    expiring: list[dict] = []

    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
        if tracker.row_is_empty(row):
            continue
        data = tracker.equipment_row_to_dict(row)
        expiry = _parse_iso_date(data.get("calibration_expiration", ""))
        if expiry is None or expiry > deadline:
            continue
        days_left = (expiry - today).days
        expiring.append(
            {
                **data,
                "expiration_date": expiry.isoformat(),
                "days_left": days_left,
            }
        )
    return expiring


def _equipment_alert_key(equipment: Mapping[str, object]) -> str:
    eq_id = str(equipment.get("id", "")).strip() or "?"
    expiry = str(equipment.get("expiration_date", "")).strip()
    return f"{eq_id}:{expiry}"


def _already_sent_today(state: dict, equipment: Mapping[str, object]) -> bool:
    key = _equipment_alert_key(equipment)
    last = str(state.get("last_sent", {}).get(key, "")).strip()
    return last == date.today().isoformat()


def _mark_sent_today(state: dict, equipment: Mapping[str, object]) -> None:
    key = _equipment_alert_key(equipment)
    state.setdefault("last_sent", {})[key] = date.today().isoformat()


def _format_expiry_message(days_left: int, expiration_date: str) -> str:
    if days_left < 0:
        return f"A calibração expirou em {expiration_date}."
    if days_left == 0:
        return f"A calibração expira hoje ({expiration_date})."
    if days_left == 1:
        return f"A calibração expira amanhã ({expiration_date})."
    return f"A calibração expira a {expiration_date} (faltam {days_left} dias)."


def _build_email_subject(equipment: Mapping[str, object]) -> str:
    name = str(equipment.get("name", "")).strip() or "Equipamento"
    expiry = str(equipment.get("expiration_date", "")).strip()
    return f"[Stock Tracker] Calibração a expirar — {name} ({expiry})"


def _build_email_body(equipment: Mapping[str, object]) -> str:
    days_left = int(equipment.get("days_left", 0))
    expiration_date = str(equipment.get("expiration_date", "")).strip()
    lines = [
        "Alerta de calibração — Stock Tracker",
        "",
        _format_expiry_message(days_left, expiration_date),
        "",
        "Informações do equipamento:",
        f"  ID: {equipment.get('id', '')}",
        f"  Nome: {equipment.get('name', '')}",
        f"  Referência fornecedor: {equipment.get('supplier_reference', '')}",
        f"  Número de série: {equipment.get('serial_number', '')}",
        f"  Descrição: {equipment.get('description', '')}",
        f"  Data de calibração: {equipment.get('calibration_date', '')}",
        f"  Data de expiração: {expiration_date}",
        f"  Localização: {equipment.get('location', '')}",
        "",
        "Este email foi enviado automaticamente pelo Stock Tracker.",
    ]
    return "\n".join(lines)


def send_calibration_alert_email(
    equipment: Mapping[str, object],
    *,
    secrets: Mapping[str, object],
) -> tuple[bool, str]:
    smtp = _smtp_settings(secrets)
    if smtp is None:
        return False, "SMTP not configured (set SMTP_HOST, SMTP_USER, SMTP_PASSWORD in secrets.py)."

    recipient = _alert_recipient(secrets)
    if not recipient:
        return False, "CALIBRATION_ALERT_TO is empty."

    message = EmailMessage()
    message["Subject"] = _build_email_subject(equipment)
    message["From"] = str(smtp["from_addr"])
    message["To"] = recipient
    message.set_content(_build_email_body(equipment))

    try:
        _deliver_smtp_message(message, smtp)
    except OSError as exc:
        return False, f"SMTP error: {exc}"

    return True, f"Email sent to {recipient}."


def run_calibration_alert_check(
    tracker: StockTracker,
    *,
    secrets: Mapping[str, object] | None = None,
) -> CalibrationAlertResult:
    """
    Find equipment with calibration expiring soon and send alert emails.

    Sends at most one email per equipment per calendar day while still in the
    alert window (default: 30 days before expiration, including expired items).
    """
    active_secrets = secrets if secrets is not None else tracker._secrets
    result = CalibrationAlertResult(
        smtp_configured=_smtp_settings(active_secrets) is not None
    )
    alert_days = _alert_days(active_secrets)
    expiring = _iter_expiring_equipment(tracker, alert_days=alert_days)
    result.expiring_count = len(expiring)
    if not expiring:
        return result

    state = _load_state()
    state_changed = False

    for equipment in expiring:
        if _already_sent_today(state, equipment):
            continue
        ok, detail = send_calibration_alert_email(
            equipment,
            secrets=active_secrets,
        )
        if ok:
            _mark_sent_today(state, equipment)
            state_changed = True
            result.sent_count += 1
        else:
            label = str(equipment.get("name", "")).strip() or str(equipment.get("id", ""))
            result.failures.append(f"{label}: {detail}")

    if state_changed:
        _save_state(state)

    return result
