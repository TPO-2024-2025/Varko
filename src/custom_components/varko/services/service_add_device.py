from homeassistant.core import ServiceCall

import logging

_LOGGER = logging.getLogger(__name__)


async def handle_add_device(call: ServiceCall) -> None:
    """Handle adding a device to the presence simulation system."""
    device_id = call.data.get("device_id")
    _LOGGER.debug(f"Adding device to simulation system: {device_id}")
    # TODO: Implement device registration logic
