from custom_components.varko.decorators import admin, service
from custom_components.varko.services.base_manager import BaseManager
from custom_components.varko.services.group_manager import GroupManager
from custom_components.varko.services.state_manager import StateManager
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.components.zone import in_zone
from custom_components.varko.const import DOMAIN

class ZoneManager(BaseManager):
    __instance = None

    def __init__(self, hass):
        super().__init__(
            __name__,
            hass,
            f"{DOMAIN}.zone",
            {
                "active_zone": "zone.home",
            },
        )
        self._group_tracker = None
        self._device_trackers = []
        self._device_entities = []

    @classmethod
    async def get_instance(cls, hass):
        if cls.__instance is None:
            cls.__instance = cls(hass)
            await cls.__instance._initialize()
            await cls.__instance._setup_group_tracker()
            await cls.__instance._setup_device_trackers()
        return cls.__instance

    @classmethod
    def destroy(cls):
        if cls.__instance is not None:
            cls.__instance._clear_group_tracker()
            cls.__instance._clear_device_trackers()
            cls.__instance.__del__()
            cls.__instance = None

    async def _setup_group_tracker(self):
        self._clear_group_tracker()

        self._group_tracker = async_track_state_change_event(
            self._hass,
            f"{DOMAIN}.group",
            self._handle_group_state_change,
        )

    async def _setup_device_trackers(self):
        self._clear_device_trackers()

        zone_entity_id = self._data.get("active_zone")
        if not zone_entity_id:
            self._logger.warning("No active zone to track.")
            return

        group_manager = await GroupManager.get_instance(self._hass)
        people = group_manager._data

        for person in people:
            person_state = self._hass.states.get(person)
            if not person_state:
                self._logger.warning(f"Person {person} does not exist.")
                continue

            devices = person_state.attributes.get("device_trackers")
            if isinstance(devices, list):
                self._device_entities.extend(devices)
            elif isinstance(devices, str):
                self._device_entities.append(devices)
            else:
                self._logger.warning(
                    f"Invalid device tracker format for {person}: {devices}"
                )
                continue

        if not self._device_entities:
            self._logger.warning("No device trackers found for the users.")
            return

        entities_to_track = self._device_entities + [zone_entity_id]
        self._logger.debug(f"Tracking entities: {entities_to_track}")

        self._device_trackers.append(
            async_track_state_change_event(
                self._hass,
                entities_to_track,
                self._handle_zone_device_state_change,
            )
        )

        await self._check_presence_in_zone(zone_entity_id, self._device_entities)

    def _clear_device_trackers(self):
        for tracker in self._device_trackers:
            tracker()
        self._device_trackers = []
        self._device_entities = []

    def _clear_group_tracker(self):
        if self._group_tracker:
            self._group_tracker()
            self._group_tracker = None

    async def _handle_group_state_change(self, _):
        await self._setup_device_trackers()

    async def _handle_zone_device_state_change(self, event):
        entity_id = event.data.get("entity_id")
        zone_entity_id = self._data.get("active_zone")

        # if the zone has changed, check all device trackers
        if entity_id == zone_entity_id:
            await self._check_presence_in_zone(
                zone_entity_id,
                self._device_entities,
            )
        # if state of a device tracker has changed, check only that device tracker
        else:
            await self._check_presence_in_zone(
                zone_entity_id,
                [entity_id],
            )

    async def _check_presence_in_zone(self, zone_entity_id, tracking_entities):
        if not zone_entity_id:
            self._logger.warning("No zone entity ID provided.")
            return

        if not tracking_entities:
            self._logger.warning("No device trackers provided.")
            return

        zone_state = self._hass.states.get(zone_entity_id)
        if not zone_state:
            self._logger.warning(f"Zone entity ID {zone_entity_id} does not exist.")
            return

        any_device_in_zone = False

        for device_tracker in tracking_entities:
            device_state = self._hass.states.get(device_tracker)
            if not device_state:
                self._logger.warning(f"Device tracker {device_tracker} does not exist.")
                continue

            if in_zone(
                zone_state,
                device_state.attributes.get("latitude"),
                device_state.attributes.get("longitude"),
            ):
                self._logger.info(
                    f"Device {device_tracker} is in the zone {zone_entity_id}."
                )
                any_device_in_zone = True
            else:
                self._logger.info(
                    f"Device {device_tracker} is not in the zone {zone_entity_id}."
                )

        if any_device_in_zone:
            self._logger.info(
                f"At least one device tracker is in the zone {zone_entity_id}. Setting system state to idle."
            )
            await self._hass.services.async_call(
                DOMAIN,
                "set_state_idle",
            )

        else:
            self._logger.info(
                f"No device trackers are in the zone {zone_entity_id}. Setting system state to ready."
            )
            await self._hass.services.async_call(
                DOMAIN,
                "set_state_ready",
            )

    @service
    @admin
    async def select_activation_zone(self, call):
        self._logger.debug("Service call to select activation zone: %s", call.data)

        zone_entity_id = call.data.get("zone_entity_id")

        if not zone_entity_id:
            self._logger.error("No zone entity ID provided.")
            return

        if not self._hass.states.get(zone_entity_id):
            self._logger.error(f"Zone entity ID {zone_entity_id} does not exist.")
            return

        self._data["active_zone"] = zone_entity_id
        await self._store.async_save(self._data)
        await self._setup_device_trackers()

        self._logger.info(f"Selected activation zone: {zone_entity_id}")
