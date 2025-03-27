"""Component to integrate with Varko."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

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
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Varko using config flow"""

    _LOGGER.setLevel(logging.DEBUG)  # TODO: Remove after development
    _LOGGER.debug("VARKO: Started setup")

    # Register services
    for service_name, handler in SERVICES.items():
        hass.services.async_register(DOMAIN, service_name, handler)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry"""
    # Remove services when integration is unloaded
    for service_name in SERVICES:
        hass.services.async_remove(DOMAIN, service_name)
    return True
