from homeassistant.core import ServiceCall

import logging
_LOGGER = logging.getLogger(__name__)

async def handle_send_notification(call: ServiceCall) -> None:
    """Handle sending a notification about system status or detected intruders."""
    message = call.data.get("message")
    severity = call.data.get("severity", "info")
    image_url = call.data.get("image_url")
    recipients = call.data.get("recipients", [])
    
    message = f"Sending {severity} notification: {message}"
    if image_url:
        message += f" with image: {image_url}"
    if recipients:
        message += f", to recipients: {recipients}"
    _LOGGER.debug(message)
    # TODO: Implement notification sending logic