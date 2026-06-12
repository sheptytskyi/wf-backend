import logging

from fastapi import APIRouter, BackgroundTasks, status

from src.leads.schemas import Lead44ContactRequest, LeadContactRequest, LeadContactResponse
from src.leads.service import send_44_lead_to_telegram, send_lead_to_telegram
from src.noname.schema import ProjectRequest
from src.noname.service import send_nn_lead_to_telegram

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post(
    "/contact",
    response_model=LeadContactResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit early access request",
    description=(
        "Accepts the landing page lead contact form and dispatches "
        "a Telegram notification in the background."
    ),
)
async def submit_contact(
    payload: LeadContactRequest,
    background_tasks: BackgroundTasks,
) -> LeadContactResponse:
    background_tasks.add_task(send_lead_to_telegram, payload)
    logger.info("Lead contact received from: %s — queued Telegram notification.", payload.email)
    return LeadContactResponse(
        success=True,
        message="Thank you! We'll be in touch shortly.",
    )


@router.post(
    "/44/contact",
    response_model=LeadContactResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit early access request",
    description=(
        "Accepts the landing page lead contact form and dispatches "
        "a Telegram notification in the background."
    ),
)
async def submit_contact(
    payload: Lead44ContactRequest,
    background_tasks: BackgroundTasks,
) -> LeadContactResponse:
    background_tasks.add_task(send_44_lead_to_telegram, payload)
    logger.info("Lead contact received from: %s — queued Telegram notification.", payload.email)
    return LeadContactResponse(
        success=True,
        message="Thank you! We'll be in touch shortly.",
    )


@router.post(
    "/nn/contact",
    response_model=LeadContactResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit early access request",
    description=(
        "Accepts the landing page lead contact form and dispatches "
        "a Telegram notification in the background."
    ),
)
async def submit_contact(
    payload: ProjectRequest,
    background_tasks: BackgroundTasks,
) -> LeadContactResponse:
    background_tasks.add_task(send_nn_lead_to_telegram, payload)
    logger.info("Lead contact received from: %s — queued Telegram notification.", payload.email)
    return LeadContactResponse(
        success=True,
        message="Thank you! We'll be in touch shortly.",
    )