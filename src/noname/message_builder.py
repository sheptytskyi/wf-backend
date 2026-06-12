from typing import Any

from src.noname.schema import ProjectRequest


class TelegramMessageBuilder:
    YES_VALUES = {"yes", "true", "1"}

    @staticmethod
    def yes_no(value: Any) -> str:
        if isinstance(value, bool):
            return "✅ Так" if value else "❌ Ні"

        if isinstance(value, str):
            return "✅ Так" if value.lower() in TelegramMessageBuilder.YES_VALUES else "❌ Ні"

        return str(value)

    @staticmethod
    def add_field(lines: list[str], label: str, value: Any) -> None:
        if value not in (None, "", [], {}):
            lines.append(f"• {label}: {value}")

    @classmethod
    def build(cls, request: ProjectRequest) -> str:
        lines: list[str] = []

        lines.extend(
            [
                "🚀 <b>Нова заявка з сайту</b>",
                "",
                "👤 <b>Контактна інформація</b>",
            ]
        )

        cls.add_field(lines, "Ім'я", request.full_name)
        cls.add_field(lines, "Компанія", request.company_name)
        cls.add_field(lines, "Email", request.email)
        cls.add_field(lines, "Telegram", request.telegram)
        cls.add_field(lines, "Телефон", request.phone)
        cls.add_field(lines, "Спосіб зв'язку", request.preferred_contact_method)

        lines.extend(
            [
                "",
                "🏢 <b>Бізнес</b>",
            ]
        )

        cls.add_field(lines, "Індустрія", request.industry)
        cls.add_field(lines, "Розмір компанії", request.business_size)

        if request.selected_services:
            lines.extend(
                [
                    "",
                    "🛠 <b>Послуги</b>",
                ]
            )

            for service in request.selected_services:
                lines.append(f"• {service}")

        if request.goals:
            lines.extend(
                [
                    "",
                    "🎯 <b>Цілі проєкту</b>",
                ]
            )

            for goal in request.goals:
                lines.append(f"• {goal}")

        if request.project_description:
            lines.extend(
                [
                    "",
                    "📝 <b>Опис проєкту</b>",
                    request.project_description,
                ]
            )

        service_blocks: list[str] = []

        if request.service_details.landing_page:
            lp = request.service_details.landing_page
            values = [
                lp.design_status,
                lp.languages,
                lp.need_analytics,
                lp.need_crm,
            ]

            if any(v not in (None, "") for v in values):
                block = ["🌐 <b>Landing Page</b>"]
                cls.add_field(block, "Дизайн", lp.design_status)
                cls.add_field(block, "Мови", lp.languages)

                if lp.need_analytics is not None:
                    block.append(
                        f"• Аналітика: {cls.yes_no(lp.need_analytics)}"
                    )

                if lp.need_crm is not None:
                    block.append(
                        f"• CRM інтеграція: {cls.yes_no(lp.need_crm)}"
                    )

                service_blocks.extend(block)
                service_blocks.append("")

        if request.service_details.telegram_bot:
            bot = request.service_details.telegram_bot
            values = bot.model_dump().values()

            if any(v not in (None, "") for v in values):
                block = ["🤖 <b>Telegram Bot</b>"]

                cls.add_field(block, "Призначення", bot.bot_purpose)
                cls.add_field(block, "Очікувана кількість користувачів", bot.expected_users)
                cls.add_field(block, "Оплата", cls.yes_no(bot.need_payment))
                cls.add_field(block, "CRM інтеграція", cls.yes_no(bot.need_crm))
                cls.add_field(block, "Адмін-панель", cls.yes_no(bot.need_admin_panel))

                service_blocks.extend(block)
                service_blocks.append("")

        if request.service_details.web_app:
            app = request.service_details.web_app
            values = app.model_dump().values()

            if any(v not in (None, "") for v in values):
                block = ["💻 <b>Web Application</b>"]

                cls.add_field(block, "Тип застосунку", app.application_type)
                cls.add_field(block, "Користувачі", app.expected_users)
                cls.add_field(block, "Авторизація", app.require_auth)
                cls.add_field(block, "Адмін-панель", app.require_admin_panel)
                cls.add_field(block, "Інтеграції", app.third_party_integrations)
                cls.add_field(block, "Список інтеграцій", app.required_integrations_list)

                service_blocks.extend(block)
                service_blocks.append("")

        if service_blocks:
            lines.extend(
                [
                    "",
                    "⚙️ <b>Деталі послуг</b>",
                    "",
                    *service_blocks,
                ]
            )

        lines.extend(
            [
                "",
                "💰 <b>Бюджет та терміни</b>",
            ]
        )

        cls.add_field(lines, "Бюджет", request.budget_range)
        cls.add_field(lines, "Термін", request.project_timeline)

        lines.extend(
            [
                "",
                "🌐 <b>Поточний сайт</b>",
            ]
        )

        cls.add_field(lines, "Сайт існує", request.website_exists)
        cls.add_field(lines, "URL", request.website_url)

        if request.references:
            lines.extend(
                [
                    "",
                    "📚 <b>Референси</b>",
                    request.references,
                ]
            )

        cls.add_field(lines, "Джерело ліда", request.lead_source)

        if request.business_impact:
            lines.extend(
                [
                    "",
                    "🔥 <b>Бізнес-вплив</b>",
                    request.business_impact,
                ]
            )

        return "\n".join(lines)