import logging
from datetime import datetime, UTC

import httpx

from src.core.config import settings
from src.leads.schemas import LeadContactRequest

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def _fmt(value: str | None, fallback: str = "—") -> str:
    """Return value if truthy, otherwise the fallback dash."""
    return value if value else fallback


def _build_message(lead: LeadContactRequest) -> str:
    agent_label = "Solo Agent" if lead.agent_type == "solo" else "Agency Team"
    utc_time = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

    # ── Core contact info ─────────────────────────────────────────────────────
    lines = [
        "🏠 <b>New WatchFlat Early Access Request</b>",
        "",
        f"🕒 <b>Submitted:</b> {utc_time}",
        f"👤 <b>Name:</b> {lead.name}",
        f"📞 <b>Phone:</b> {lead.phone}",
        f"📧 <b>Email:</b> {lead.email}",
        f"📅 <b>Viewings/week:</b> {lead.viewings_per_week}",
        f"🏢 <b>Type:</b> {agent_label}",
    ]

    # ── UTM attribution block (only shown if at least one field is present) ───
    has_utm = any([
        lead.utm_source, lead.utm_medium, lead.utm_campaign,
        lead.utm_content, lead.utm_term,
    ])
    if has_utm:
        lines += [
            "",
            "📊 <b>UTM Attribution</b>",
            f"  • Source:   {_fmt(lead.utm_source)}",
            f"  • Medium:   {_fmt(lead.utm_medium)}",
            f"  • Campaign: {_fmt(lead.utm_campaign)}",
            f"  • Content:  {_fmt(lead.utm_content)}",
            f"  • Term:     {_fmt(lead.utm_term)}",
        ]

    # ── Meta / Facebook identifiers (only shown if present) ───────────────────
    has_meta = any([lead.fbclid, lead.fbp, lead.fbc])
    if has_meta:
        lines += [
            "",
            "🎯 <b>Meta Identifiers</b>",
            f"  • fbclid: {_fmt(lead.fbclid)}",
            f"  • fbp:    {_fmt(lead.fbp)}",
            f"  • fbc:    {_fmt(lead.fbc)}",
        ]

    return "\n".join(lines)


async def send_lead_to_telegram(lead: LeadContactRequest) -> bool:
    """
    Send the lead contact data as a formatted Telegram message.
    Returns True on success, False if Telegram is mis-configured or the call fails.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not token or not chat_id:
        logger.warning(
            "Telegram notification skipped: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not configured."
        )
        return False

    url = TELEGRAM_API_URL.format(token=token)
    payload = {
        "chat_id": chat_id,
        "text": _build_message(lead),
        "parse_mode": "HTML",
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            logger.info("Telegram notification sent for lead: %s", lead.email)
            return True
    except httpx.HTTPStatusError as exc:
        logger.error(
            "Telegram API returned error %s: %s",
            exc.response.status_code,
            exc.response.text,
        )
    except httpx.RequestError as exc:
        logger.error("Failed to reach Telegram API: %s", exc)

    return False
