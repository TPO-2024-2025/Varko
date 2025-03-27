from homeassistant.core import ServiceCall

import logging

_LOGGER = logging.getLogger(__name__)


async def handle_enable_device(call: ServiceCall) -> None:
    """Handle enabling a device for use in simulation."""
    device_id = call.data.get("device_id")
    _LOGGER.debug(f"Enabling device for simulation: {device_id}")
    # TODO: Implement device enabling logic
