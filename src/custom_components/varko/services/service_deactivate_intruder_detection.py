from homeassistant.core import ServiceCall

import logging
_LOGGER = logging.getLogger(__name__)

async def handle_deactivate_intruder_detection(call: ServiceCall) -> None:
    """Handle deactivating the intruder detection system."""
    _LOGGER.info("Deactivating intruder detection system")
    # TODO: Implement intruder detection deactivation logic