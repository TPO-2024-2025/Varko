import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from custom_components.varko.const import DOMAIN


class BaseManager:
    def __init__(
        self, module_name: str, hass: HomeAssistant, store_key: str, data_default
    ):
        self._logger = logging.getLogger(module_name)
        self._hass = hass
        self._store = Store(hass, 1, store_key)
        self._data = data_default
        self.__services = []

        self.__register_services()

    def __del__(self):
        self.__unregister_services()

    async def _initialize(self):
        data = await self._store.async_load()
        if data is None:
            self._logger.info(f"Creating new store for {self._store.key}")
        else:
            self._logger.info(f"Loading data from store {self._store.key}")
            self._data = data

    def __register_services(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, "_is_service") and attr._is_service:
                self._logger.debug(f"Registering service: {attr_name}")
                self.__services.append(attr_name)
                self._hass.services.async_register(DOMAIN, attr_name, attr)

    def __unregister_services(self):
        for service in self.__services:
            self._logger.debug(f"Unregistering service: {service}")
            self._hass.services.async_remove(DOMAIN, service)
        self.__services = []
