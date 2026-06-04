from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal, Optional

class LeadBaseContactForm(BaseModel):
    # ── Core form fields ──────────────────────────────────────────────────────
    name: str
    email: EmailStr

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


class LeadContactRequest(LeadBaseContactForm):
    phone: str
    viewings_per_week: Literal["1-10", "11-30", "31-50", "50+"]
    agent_type: Literal["solo", "agency"]

    @field_validator("phone")
    @classmethod
    def phone_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Phone must not be empty")
        return v


class Lead44ContactRequest(LeadBaseContactForm):
    project_type: str = Field(alias='projectType')
    budget: str
    message: str

class LeadContactResponse(BaseModel):
    success: bool
    message: str
