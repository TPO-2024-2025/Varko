"""Config flow for Varko integration."""

from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class VarkoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Varko integration."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            "presence_simulation_duration_minutes", default=30
                        ): int,
                    }
                ),
                description_placeholders={
                    "presence_simulation_duration_minutes": "Duration in minutes presence simulation should be on for before automatically turning itself off"
                },
            )

        return self.async_create_entry(title="Varko", data=user_input)
