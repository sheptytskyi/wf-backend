from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal, Optional


class LeadContactRequest(BaseModel):
    # ── Core form fields ──────────────────────────────────────────────────────
    name: str
    phone: str
    email: EmailStr
    viewings_per_week: Literal["1-10", "11-30", "31-50", "50+"]
    agent_type: Literal["solo", "agency"]

    # ── UTM parameters ────────────────────────────────────────────────────────
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None

    # ── Meta / Facebook identifiers ───────────────────────────────────────────
    fbclid: Optional[str] = None
    fbp: Optional[str] = None
    fbc: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name must not be empty")
        return v

    @field_validator("phone")
    @classmethod
    def phone_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Phone must not be empty")
        return v


class LeadContactResponse(BaseModel):
    success: bool
    message: str
