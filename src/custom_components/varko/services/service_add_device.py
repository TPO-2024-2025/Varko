from homeassistant.config_entries import ConfigEntry
from homeassistant.core import ServiceCall
from homeassistant.helpers.entity_platform import async_get_platforms

from ..const import DOMAIN
from ..light import VarkoLight
import logging

_LOGGER = logging.getLogger(__name__)


async def handle_add_device(call: ServiceCall) -> None:
    """Handle adding a device to the presence simulation system."""
    device_type = call.data.get("device_type")
    device_name = call.data.get("device_name")
    device_id = call.data.get("device_id")

    new_device = {
        "device_type": device_type,
        "device_name": device_name,
        "device_id": device_id,
    }

    hass = call.hass
    entry: ConfigEntry | None = next(
        (config_entry for config_entry in hass.config_entries.async_entries(DOMAIN)),
        None,
    )
    if not entry:
        _LOGGER.error("No valid config entry found for Varko")
        return

    devices = entry.data.get("devices", [])
    devices.append(new_device)
    hass.config_entries.async_update_entry(entry, data={"devices": devices})
    hass.data[DOMAIN][entry.entry_id]["devices"].append(new_device)

    platforms = async_get_platforms(hass, DOMAIN)
    light_platform = next((p for p in platforms if p.domain == "light"), None)
    if light_platform:
        await light_platform.async_add_entities(
            [VarkoLight(hass, device_name, device_id)]
        )
        _LOGGER.debug(f"Added {device_name} as a light device.")
    else:
        _LOGGER.warning("Light platform not found. Device was not added.")
