import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from custom_components.varko.const import DOMAIN


class BaseManager:
    def __init__(
        self, module_name: str, hass: HomeAssistant, store_key: str, data_default
    ):
        self.logger = logging.getLogger(module_name)
        self.hass = hass
        self.store = Store(hass, 1, store_key)
        self.data = data_default

        self._register_services()

    async def initialize(self):
        data = await self.store.async_load()
        if data is None:
            self.logger.info(f"Creating new store for {self.store.key}")
        else:
            self.logger.info(f"Loading data from store {self.store.key}")
            self.data = data

    def _register_services(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, "_is_service") and attr._is_service:
                self.logger.debug(f"Registering service: {attr.__name__}")
                self.hass.services.async_register(
                    DOMAIN,
                    attr.__name__,
                    attr,
                )
