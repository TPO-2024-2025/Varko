from homeassistant.core import ServiceCall

import logging
_LOGGER = logging.getLogger(__name__)

async def handle_activate_intruder_detection(call: ServiceCall) -> None:
    """Handle activating the intruder detection system."""
    timeout = call.data.get("timeout", 0)
    _LOGGER.info(f"Activating intruder detection system with timeout: {timeout}s")
    # TODO: Implement intruder detection activation logic