from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class LandingPageDetails(BaseSchema):
    design_status: Optional[str] = None
    languages: Optional[str] = None
    need_analytics: Optional[bool] = None
    need_crm: Optional[bool] = None


class CorporateWebsiteDetails(BaseSchema):
    pages_count: Optional[str] = None
    need_cms: Optional[str] = None
    need_multilingual: Optional[str] = None


class TelegramBotDetails(BaseSchema):
    bot_purpose: Optional[str] = None
    expected_users: Optional[str] = None
    need_payment: Optional[str] = None
    need_crm: Optional[str] = None
    need_admin_panel: Optional[str] = None


class WebAppDetails(BaseSchema):
    application_type: Optional[str] = None
    expected_users: Optional[str] = None
    require_auth: Optional[str] = None
    require_admin_panel: Optional[str] = None
    third_party_integrations: Optional[str] = None
    required_integrations_list: Optional[str] = None


class CRMDetails(BaseSchema):
    employees_count: Optional[str] = None
    main_processes: Optional[str] = None
    need_reporting: Optional[str] = None


class AutomationDetails(BaseSchema):
    process_to_automate: Optional[str] = None
    current_tools: Optional[str] = None
    people_involved: Optional[str] = None


class AIDetails(BaseSchema):
    ai_functionality: Optional[str] = None
    need_integration: Optional[str] = None


class ServiceDetails(BaseSchema):
    landing_page: LandingPageDetails
    corporate_website: CorporateWebsiteDetails
    telegram_bot: TelegramBotDetails
    web_app: WebAppDetails
    crm: CRMDetails
    automation: AutomationDetails
    ai: AIDetails


class ProjectRequest(BaseSchema):
    selected_services: list[str]

    industry: str
    industry_custom: Optional[str] = None
    business_size: str
    company_name: str

    goals: list[str]
    project_description: str

    service_details: ServiceDetails

    budget_range: str
    project_timeline: str

    website_exists: str
    website_url: Optional[str] = None

    references: Optional[str] = None
    lead_source: Optional[str] = None
    business_impact: Optional[str] = None

    full_name: str
    email: EmailStr
    telegram: Optional[str] = None
    phone: Optional[str] = None
    preferred_contact_method: str