"""Component to integrate with Varko."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.panel_custom import async_register_panel
from homeassistant.components.http import StaticPathConfig
from homeassistant.const import Platform

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

from .services import (
    service_add_device,
    service_remove_device,
    service_enable_device,
    service_disable_device,
    service_activate_intruder_detection,
    service_deactivate_intruder_detection,
    service_activate_presence_simulation,
    service_deactivate_presence_simulation,
    service_add_activation_zone,
    service_remove_activation_zone,
    service_send_notification,
)

SERVICES = {
    # Device management services
    "add_device": service_add_device.handle_add_device,
    "remove_device": service_remove_device.handle_remove_device,
    "enable_device": service_enable_device.handle_enable_device,
    "disable_device": service_disable_device.handle_disable_device,
    # System activation services
    "activate_intruder_detection": service_activate_intruder_detection.handle_activate_intruder_detection,
    "deactivate_intruder_detection": service_deactivate_intruder_detection.handle_deactivate_intruder_detection,
    "activate_presence_simulation": service_activate_presence_simulation.handle_activate_presence_simulation,
    "deactivate_presence_simulation": service_deactivate_presence_simulation.handle_deactivate_presence_simulation,
    # Location zone management services
    "add_activation_zone": service_add_activation_zone.handle_add_activation_zone,
    "remove_activation_zone": service_remove_activation_zone.handle_remove_activation_zone,
    # Notification service
    "send_notification": service_send_notification.handle_send_notification,
}


async def async_setup(hass, config):
    """Set up the Varko component"""

    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                "/local/varko_panel.js",
                "/config/custom_components/varko/www/varko_panel.js",
                True,
            )
        ]
    )

    await async_register_panel(
        hass,
        frontend_url_path="varko-panel",
        module_url="/local/varko_panel.js",
        sidebar_title="Varko",
        sidebar_icon="mdi:home-lock",
        webcomponent_name="varko-panel",
        require_admin=True,
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Varko using config flow"""

    _LOGGER.setLevel(logging.DEBUG)  # TODO: Remove after development
    _LOGGER.debug("VARKO: Started setup")
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "config": entry.data,
        "devices": [],
    }
    # Register services
    for service_name, handler in SERVICES.items():
        hass.services.async_register(DOMAIN, service_name, handler)

    await hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, [Platform.LIGHT])
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry"""
    # Remove services when integration is unloaded
    for service_name in SERVICES:
        hass.services.async_remove(DOMAIN, service_name)

    unload_ok = await hass.config_entries.async_forward_entry_unload(
        entry, Platform.LIGHT
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
