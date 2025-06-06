"""Component to integrate with Varko."""

import logging

from homeassistant.components.http import StaticPathConfig
from homeassistant.components.panel_custom import async_register_panel
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from custom_components.varko.services.group_manager import GroupManager
from custom_components.varko.services.state_manager import StateManager

from .const import DOMAIN
from .services.device_manager import DeviceManager
from .services.zone_manager import ZoneManager

from custom_components.varko.radio import RadioBrowserAPI

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the Varko component"""

    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                "/local/varko_panel.js",
                "/config/custom_components/varko/www/varko_panel.js",
                True,
            ),
            StaticPathConfig(
                "/local/varko_panel.css",
                "/config/custom_components/varko/www/varko_panel.css",
                True,
            ),
            StaticPathConfig(
                "/local/varko_panel.html",
                "/config/custom_components/varko/www/varko_panel.html",
                True,
            ),
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

    await DeviceManager.get_instance(hass)
    await StateManager.get_instance(hass)
    await GroupManager.get_instance(hass)
    await ZoneManager.get_instance(hass)
    await RadioBrowserAPI.get_instance(hass)

    await hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, [Platform.LIGHT])
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry"""
    unload_ok = await hass.config_entries.async_forward_entry_unload(
        entry, Platform.LIGHT
    )

    StateManager.destroy()
    DeviceManager.destroy()
    GroupManager.destroy()
    ZoneManager.destroy()
    await RadioBrowserAPI.destroy()

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
