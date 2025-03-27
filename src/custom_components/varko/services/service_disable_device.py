from homeassistant.core import ServiceCall

import logging
_LOGGER = logging.getLogger(__name__)

async def handle_disable_device(call: ServiceCall) -> None:
    """Handle disabling a device from simulation."""
    device_id = call.data.get("device_id")
    _LOGGER.debug(f"Disabling device from simulation: {device_id}")
    # TODO: Implement device disabling logic