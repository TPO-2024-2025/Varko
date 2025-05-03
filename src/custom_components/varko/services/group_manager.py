from homeassistant.core import HomeAssistant, ServiceCall

from custom_components.varko.const import DOMAIN
from custom_components.varko.decorators import admin, service
from custom_components.varko.services.base_manager import BaseManager


class GroupManager(BaseManager):
    __instance = None

    def __init__(self, hass: HomeAssistant):
        super().__init__(__name__, hass, f"{DOMAIN}.group", [])

    @classmethod
    async def get_instance(cls, hass: HomeAssistant):
        if cls.__instance is None:
            cls.__instance = cls(hass)
            await cls.__instance._initialize()
        return cls.__instance

    @classmethod
    def destroy(cls):
        if cls.__instance is not None:
            cls.__instance.__del__()
            cls.__instance = None

    @service
    @admin
    async def add_person(self, call: ServiceCall):
        person = call.data.get("person")

        members = set(self._data)
        if person in members:
            self._logger.warning(f"Person {person} already exists in the group.")
            return

        members.add(person)

        self._data = list(members)
        await self._store.async_save(self._data)
        self._logger.info(f"Added {person} to the group.")

        self.__publish_state_changed(members)

    @service
    @admin
    async def remove_person(self, call: ServiceCall):
        person = call.data.get("person")

        members = set(self._data)
        if person not in members:
            self._logger.warning(f"Person {person} does not exist in the group.")
            return

        members.remove(person)

        self._data = list(members)
        await self._store.async_save(self._data)
        self._logger.info(f"Removed {person} from the group.")

        self.__publish_state_changed(members)

    def __publish_state_changed(self, members: set):
        self._hass.states.async_set(
            f"{DOMAIN}.group",
            str(len(members)),
        )
