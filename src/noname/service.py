import logging
import httpx

from src.leads.service import TELEGRAM_API_URL
from src.noname.message_builder import TelegramMessageBuilder
from src.noname.schema import ProjectRequest
from src.core.config import settings

logger = logging.getLogger(__name__)


def _build_nn_message(lead: ProjectRequest):
    return TelegramMessageBuilder.build(lead)


async def send_nn_lead_to_telegram(lead: ProjectRequest) -> bool:
    """
    Send the lead contact data as a formatted Telegram message.
    Returns True on success, False if Telegram is mis-configured or the call fails.
    """
    token = settings.TELEGRAM_BOT_TOKEN_NN
    chat_id = settings.TELEGRAM_CHAT_ID_NN

    if not token or not chat_id:
        logger.warning(
            "Telegram notification skipped: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not configured."
        )
        return False

    url = TELEGRAM_API_URL.format(token=token)
    payload = {
        "chat_id": chat_id,
        "text": _build_nn_message(lead),
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