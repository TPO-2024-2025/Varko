from homeassistant.core import ServiceCall

import logging
_LOGGER = logging.getLogger(__name__)

async def handle_remove_activation_zone(call: ServiceCall) -> None:
    """Handle removing a location zone from system activation."""
    zone_id = call.data.get("zone_id")
    _LOGGER.debug(f"Removing activation zone: {zone_id}")
    # TODO: Implement zone removal logic