import functools

from homeassistant.core import ServiceCall
from homeassistant.exceptions import Unauthorized

from custom_components.varko.services.base_manager import BaseManager


def service(handler):
    setattr(handler, "_is_service", True)
    return handler


def admin(handler):
    @functools.wraps(handler)
    async def wrapper(self: BaseManager, call: ServiceCall):
        if not call.context.user_id:
            self.logger.error(f"Unknown access attempt to service {call.service}")
            raise Unauthorized()

        caller = await self.hass.auth.async_get_user(call.context.user_id)
        if caller is None:
            self.logger.warning(f"User {call.context.user_id} not found.")
            raise Unauthorized()

        if not caller.is_admin:
            self.logger.error(
                f"Unauthorized access attempt to service {call.service} by {caller.name}"
            )
            raise Unauthorized()

        return await handler(self, call)

    return wrapper
