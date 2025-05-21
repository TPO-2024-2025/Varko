from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

from custom_components.varko.const import (
    DEVICE_ID,
    DEVICE_NAME,
    DEVICE_TYPE,
    DOMAIN,
    ENTITY,
    ENTITY_ID,
    RADIO_STATION_UUID,
    IS_ENABLED,
)
from custom_components.varko.decorators import admin, service
from custom_components.varko.light import VarkoLight
from custom_components.varko.services.base_manager import BaseManager
from custom_components.varko.radio import RadioBrowserAPI


class DeviceManager(BaseManager):
    __instance = None

    def __init__(self, hass: HomeAssistant):
        super().__init__(__name__, hass, f"{DOMAIN}.devices", [])

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
    async def add_light_device(self, call: ServiceCall):
        entity_id = call.data.get(ENTITY)
        device_name = call.data.get(DEVICE_NAME)
        is_enabled = call.data.get(IS_ENABLED, True)
        device_id = call.data.get(DEVICE_ID)

        if any(device[DEVICE_ID] == device_id for device in self._data):
            self._logger.warning(f"Device with {device_id} already exists.")
            return

        if any(
            device.get(ENTITY_ID) == entity_id
            for device in self._data
            if ENTITY_ID in device
        ):
            self._logger.warning(f"Entity with {entity_id} already exists.")
            return

        new_device = {
            DEVICE_TYPE: "light",
            DEVICE_NAME: device_name,
            IS_ENABLED: is_enabled,
            DEVICE_ID: device_id,
        }

        if entity_id:
            new_device[ENTITY_ID] = entity_id

        self._data.append(new_device)
        await self._store.async_save(self._data)

        entry = next(
            (entry for entry in self._hass.config_entries.async_entries(DOMAIN)),
            None,
        )
        if entry:
            devices = entry.data.get("devices", [])
            devices.append(new_device)
            self._hass.config_entries.async_update_entry(
                entry, data={"devices": devices}
            )
        else:
            self._logger.error("No config entry found for Varko.")
            return

        self._hass.data[DOMAIN][entry.entry_id]["devices"].append(new_device)

        if not entity_id:
            platforms = async_get_platforms(self._hass, DOMAIN)
            light_platform = next((p for p in platforms if p.domain == "light"), None)

            if light_platform:
                await light_platform.async_add_entities(
                    [VarkoLight(self._hass, device_name, device_id, entry.entry_id)],
                )
                self._logger.debug(f"Added {device_name} as a light device.")
            else:
                self._logger.warning("Light platform not found. Device was not added.")
        else:
            self._logger.debug(
                f"Added {device_name} linked to existing entity {entity_id}."
            )

    @service
    @admin
    async def add_media_device(self, call: ServiceCall):
        entity_id = call.data.get(ENTITY)
        is_enabled = call.data.get(IS_ENABLED, True)

        if any(
            device.get(ENTITY_ID) == entity_id
            for device in self._data
            if ENTITY_ID in device
        ):
            self._logger.warning(f"Entity with {entity_id} already exists.")
            return

        entity_registry = async_get_entity_registry(self._hass)
        entity_entry = entity_registry.async_get(entity_id)
        if not entity_entry:
            self._logger.error(f"Entity {entity_id} not found in registry")
            return

        new_device = {
            DEVICE_TYPE: "media_player",
            IS_ENABLED: is_enabled,
            DEVICE_ID: entity_entry.unique_id,
            ENTITY_ID: entity_id,
            RADIO_STATION_UUID: None,
        }

        self._data.append(new_device)
        await self._store.async_save(self._data)

        entry = next(
            (entry for entry in self._hass.config_entries.async_entries(DOMAIN)),
            None,
        )
        if entry:
            devices = entry.data.get("devices", [])
            devices.append(new_device)
            self._hass.config_entries.async_update_entry(
                entry, data={"devices": devices}
            )
        else:
            self._logger.error("No config entry found for Varko.")
            return

        self._hass.data[DOMAIN][entry.entry_id]["devices"].append(new_device)
        self._logger.debug(
            f"Added {entity_id} as a media player device. (is_enabled: {is_enabled})"
        )

    @service
    @admin
    async def remove_device(self, call: ServiceCall):
        entity_id = call.data.get(ENTITY)

        entity_registry = async_get_entity_registry(self._hass)
        entity_entry = entity_registry.async_get(entity_id)

        if not entity_entry:
            self._logger.error(f"Entity {entity_id} not found in registry")
            return

        device_id = entity_entry.unique_id

        device_to_remove = next(
            (device for device in self._data if device[DEVICE_ID] == device_id), None
        )

        if not device_to_remove:
            device_to_remove = next(
                (device for device in self._data if device.get(ENTITY_ID) == entity_id),
                None,
            )

        if not device_to_remove:
            self._logger.warning(
                f"Device or entity {entity_id} not found in Varko data."
            )
            return

        if ENTITY_ID in device_to_remove:
            filter_key = ENTITY_ID
            filter_value = device_to_remove[ENTITY_ID]
        else:
            filter_key = DEVICE_ID
            filter_value = device_to_remove[DEVICE_ID]

        self._data = [
            device for device in self._data if device.get(filter_key) != filter_value
        ]
        await self._store.async_save(self._data)

        entry = next(
            (entry for entry in self._hass.config_entries.async_entries(DOMAIN)),
            None,
        )
        if entry:
            devices = [
                d
                for d in entry.data.get("devices", [])
                if d.get(filter_key) != filter_value
            ]
            self._hass.config_entries.async_update_entry(
                entry, data={"devices": devices}
            )

            if (
                DOMAIN in self._hass.data
                and entry.entry_id in self._hass.data[DOMAIN]
                and "devices" in self._hass.data[DOMAIN][entry.entry_id]
            ):
                self._hass.data[DOMAIN][entry.entry_id]["devices"] = [
                    d
                    for d in self._hass.data[DOMAIN][entry.entry_id]["devices"]
                    if d.get(filter_key) != filter_value
                ]
        else:
            self._logger.error("No config entry found for Varko.")
            return

        if ENTITY_ID not in device_to_remove:
            entity_entry_id = entity_registry.async_get_entity_id(
                "light", DOMAIN, device_id
            )

            if entity_entry_id:
                entity_registry.async_remove(entity_entry_id)
                self._logger.debug(
                    f"Removed entity {entity_entry_id} (device ID: {device_id})."
                )
            else:
                self._logger.warning(f"No entity found for device ID {device_id}.")
        else:
            self._logger.debug(
                f"Device {device_id} linked to existing entity {device_to_remove[ENTITY_ID]}, skipping entity removal."
            )

    @service
    @admin
    async def enable_device(self, call: ServiceCall):
        entity_id = call.data.get(ENTITY)

        entity_registry = async_get_entity_registry(self._hass)
        entity_entry = entity_registry.async_get(entity_id)

        if not entity_entry:
            self._logger.error(f"Entity {entity_id} not found in registry")
            return

        device_id = entity_entry.unique_id

        device_to_enable = next(
            (device for device in self._data if device[DEVICE_ID] == device_id), None
        )

        if not device_to_enable:
            device_to_enable = next(
                (device for device in self._data if device.get(ENTITY_ID) == entity_id),
                None,
            )

        if not device_to_enable:
            self._logger.warning(
                f"Device or entity {entity_id} not found in Varko data."
            )
            return

        if device_to_enable.get(IS_ENABLED, True):
            self._logger.warning(f"Device {device_id} already enabled")
            return

        device_to_enable[IS_ENABLED] = True

        if ENTITY_ID in device_to_enable:
            filter_key = ENTITY_ID
            filter_value = device_to_enable[ENTITY_ID]
        else:
            filter_key = DEVICE_ID
            filter_value = device_to_enable[DEVICE_ID]

        entry = next(
            (entry for entry in self._hass.config_entries.async_entries(DOMAIN)),
            None,
        )
        if entry:
            for device in entry.data.get("devices", []):
                if device.get(filter_key) == filter_value:
                    device[IS_ENABLED] = True
                    break
            self._hass.config_entries.async_update_entry(
                entry, data={"devices": entry.data["devices"]}
            )
            if (
                DOMAIN in self._hass.data
                and entry.entry_id in self._hass.data[DOMAIN]
                and "devices" in self._hass.data[DOMAIN][entry.entry_id]
            ):
                for device in self._hass.data[DOMAIN][entry.entry_id]["devices"]:
                    if device.get(filter_key) == filter_value:
                        device[IS_ENABLED] = True
                        break

        await self._store.async_save(self._data)
        self._logger.debug(f"Enabled device {device_id} (Entity {entity_id}).")

    @service
    @admin
    async def disable_device(self, call: ServiceCall):
        entity_id = call.data.get(ENTITY)

        entity_registry = async_get_entity_registry(self._hass)
        entity_entry = entity_registry.async_get(entity_id)
        if not entity_entry:
            self._logger.error(f"Entity {entity_id} not found in registry")
            return

        device_id = entity_entry.unique_id

        device_to_disable = next(
            (device for device in self._data if device[DEVICE_ID] == device_id), None
        )

        if not device_to_disable:
            device_to_disable = next(
                (device for device in self._data if device.get(ENTITY_ID) == entity_id),
                None,
            )

        if not device_to_disable:
            self._logger.warning(
                f"Device or entity {entity_id} not found in Varko data."
            )
            return

        if not device_to_disable.get(IS_ENABLED, True):
            self._logger.warning(f"Device {device_id} already disabled.")
            return

        device_to_disable[IS_ENABLED] = False

        if ENTITY_ID in device_to_disable:
            filter_key = ENTITY_ID
            filter_value = device_to_disable[ENTITY_ID]
        else:
            filter_key = DEVICE_ID
            filter_value = device_to_disable[DEVICE_ID]

        entry = next((e for e in self._hass.config_entries.async_entries(DOMAIN)), None)

        if entry:
            for device in entry.data.get("devices", []):
                if device.get(filter_key) == filter_value:
                    device[IS_ENABLED] = False
                    break
            self._hass.config_entries.async_update_entry(
                entry, data={"devices": entry.data["devices"]}
            )
            if (
                DOMAIN in self._hass.data
                and entry.entry_id in self._hass.data[DOMAIN]
                and "devices" in self._hass.data[DOMAIN][entry.entry_id]
            ):
                for device in self._hass.data[DOMAIN][entry.entry_id]["devices"]:
                    if device.get(filter_key) == filter_value:
                        device[IS_ENABLED] = False
                        break

        await self._store.async_save(self._data)
        self._logger.debug(f"Disabled device {device_id} (Entity {entity_id}).")

    @service
    @admin
    async def choose_radio_station(self, call: ServiceCall):
        radio_country_code = call.data.get("radio_country_code")
        station_name = call.data.get("station_name")

        radio_api = await RadioBrowserAPI.get_instance(self._hass)
        station_uuid = await radio_api.get_station_uuid(
            station_name, radio_country_code
        )

        media_players = [
            device for device in self._data if device[DEVICE_TYPE] == "media_player"
        ]

        if not media_players:
            self._logger.warning("No media players found in Varko data.")
            return

        for device in media_players:
            device[RADIO_STATION_UUID] = station_uuid

        await self._store.async_save(self._data)

        self._logger.debug(
            f"Updated media players with station UUID {station_uuid} for {station_name} in {radio_country_code}"
        )

    async def control_device(self, device_id: str, command: str):
        normalized_command = command.upper()

        device = next(
            (device for device in self._data if device[DEVICE_ID] == device_id), None
        )

        if not device:
            self._logger.error(f"Device {device_id} not found in store data")
            return

        entity_id = device.get(ENTITY_ID)
        if not entity_id:
            entity_registry = async_get_entity_registry(self._hass)
            entity_id = entity_registry.async_get_entity_id("light", DOMAIN, device_id)
            if not entity_id:
                self._logger.error(f"No entity found for device {device_id}")
                return

        state = self._hass.states.get(entity_id)
        if not state:
            self._logger.error(f"Entity {entity_id} not available in states")
            return

        try:
            if normalized_command == "ON":
                self._logger.debug(f"async_turn_on should be called")
                if device.get(DEVICE_TYPE) == "light":
                    await self._hass.services.async_call(
                        "light", "turn_on", {"entity_id": entity_id}, blocking=True
                    )
                elif device.get(DEVICE_TYPE) == "media_player":
                    await self._hass.services.async_call(
                        "media_player",
                        "turn_on",
                        {"entity_id": entity_id},
                        blocking=True,
                    )
            elif normalized_command == "OFF":
                self._logger.debug(f"async_turn_off should be called")
                if device.get(DEVICE_TYPE) == "light":
                    await self._hass.services.async_call(
                        "light", "turn_off", {"entity_id": entity_id}, blocking=True
                    )
                elif device.get(DEVICE_TYPE) == "media_player":
                    await self._hass.services.async_call(
                        "media_player",
                        "turn_off",
                        {"entity_id": entity_id},
                        blocking=True,
                    )
            elif normalized_command == "PLAY_MEDIA":
                if device.get(DEVICE_TYPE) != "media_player":
                    self._logger.error(f"Device {device_id} is not a media player")
                    return

                if device.get(RADIO_STATION_UUID) is None:
                    radio_api = await RadioBrowserAPI.get_instance(self._hass)
                    default_station_uuid = await radio_api.get_station_uuid(
                        "Radio Slovenija", "SI"
                    )
                    device[RADIO_STATION_UUID] = default_station_uuid
                    await self._store.async_save(self._data)

                selected_station_uuid = device.get(RADIO_STATION_UUID)

                self._logger.debug(f"async_media_play should be called")
                await self._hass.services.async_call(
                    "media_player",
                    "play_media",
                    {
                        "entity_id": entity_id,
                        "media_content_id": f"media-source://radio_browser/{selected_station_uuid}",
                        "media_content_type": "music",
                    },
                    blocking=True,
                )
            elif normalized_command == "STOP_MEDIA":
                if device.get(DEVICE_TYPE) != "media_player":
                    self._logger.error(f"Device {device_id} is not a media player")
                    return

                self._logger.debug(f"async_media_stop should be called")
                await self._hass.services.async_call(
                    "media_player",
                    "media_stop",
                    {"entity_id": entity_id},
                    blocking=True,
                )
            else:
                raise ValueError(f"Invalid command: {command}")
        except Exception as e:
            self._logger.error(f"Error controlling {device_id}: {str(e)}")
