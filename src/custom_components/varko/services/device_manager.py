from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

from custom_components.varko.decorators import service, admin
from custom_components.varko.light import VarkoLight
from custom_components.varko.services.base_manager import BaseManager
from custom_components.varko.const import (
    DOMAIN,
    DEVICE_TYPE,
    DEVICE_ID,
    DEVICE_NAME,
    IS_ENABLED,
    ENTITY,
    ENTITY_ID,
)


class DeviceManager(BaseManager):
    _instance = None

    def __init__(self, hass: HomeAssistant):
        super().__init__(__name__, hass, f"{DOMAIN}.devices", [])

    @classmethod
    async def get_instance(cls, hass: HomeAssistant):
        if cls._instance is None:
            cls._instance = cls(hass)
            await cls._instance.initialize()
        return cls._instance

    @service
    @admin
    async def add_device(self, call: ServiceCall):
        entity_id = call.data.get(ENTITY)
        device_type = call.data.get(DEVICE_TYPE)
        device_name = call.data.get(DEVICE_NAME)
        is_enabled = call.data.get(IS_ENABLED, True)
        device_id = call.data.get(DEVICE_ID)

        if any(device[DEVICE_ID] == device_id for device in self.data):
            self.logger.warning(f"Device with {device_id} already exists.")
            return

        if any(
            device.get(ENTITY_ID) == entity_id
            for device in self.data
            if ENTITY_ID in device
        ):
            self.logger.warning(f"Entity with {entity_id} already exists.")
            return

        new_device = {
            DEVICE_TYPE: device_type,
            DEVICE_NAME: device_name,
            IS_ENABLED: is_enabled,
            DEVICE_ID: device_id,
        }

        if entity_id:
            new_device[ENTITY_ID] = entity_id

        self.data.append(new_device)
        await self.store.async_save(self.data)

        entry = next(
            (entry for entry in self.hass.config_entries.async_entries(DOMAIN)),
            None,
        )
        if entry:
            devices = entry.data.get("devices", [])
            devices.append(new_device)
            self.hass.config_entries.async_update_entry(
                entry, data={"devices": devices}
            )
        else:
            self.logger.error("No config entry found for Varko.")
            return

        self.hass.data[DOMAIN][entry.entry_id]["devices"].append(new_device)

        if not entity_id:
            platforms = async_get_platforms(self.hass, DOMAIN)
            light_platform = next((p for p in platforms if p.domain == "light"), None)

            if light_platform:
                await light_platform.async_add_entities(
                    [VarkoLight(self.hass, device_name, device_id, entry.entry_id)],
                )
                self.logger.debug(f"Added {device_name} as a light device.")
            else:
                self.logger.warning("Light platform not found. Device was not added.")
        else:
            self.logger.debug(
                f"Added {device_name} linked to existing entity {entity_id}."
            )

    @service
    @admin
    async def remove_device(self, call: ServiceCall):
        entity_id = call.data.get(ENTITY)

        entity_registry = async_get_entity_registry(self.hass)
        entity_entry = entity_registry.async_get(entity_id)

        if not entity_entry:
            self.logger.error(f"Entity {entity_id} not found in registry")
            return

        device_id = entity_entry.unique_id

        device_to_remove = next(
            (device for device in self.data if device[DEVICE_ID] == device_id), None
        )

        if not device_to_remove:
            device_to_remove = next(
                (device for device in self.data if device.get(ENTITY_ID) == entity_id),
                None,
            )

        if not device_to_remove:
            self.logger.warning(
                f"Device or entity {entity_id} not found in Varko data."
            )
            return

        if ENTITY_ID in device_to_remove:
            filter_key = ENTITY_ID
            filter_value = device_to_remove[ENTITY_ID]
        else:
            filter_key = DEVICE_ID
            filter_value = device_to_remove[DEVICE_ID]

        self.data = [
            device for device in self.data if device.get(filter_key) != filter_value
        ]
        await self.store.async_save(self.data)

        entry = next(
            (entry for entry in self.hass.config_entries.async_entries(DOMAIN)),
            None,
        )
        if entry:
            devices = [
                d
                for d in entry.data.get("devices", [])
                if d.get(filter_key) != filter_value
            ]
            self.hass.config_entries.async_update_entry(
                entry, data={"devices": devices}
            )

            if (
                DOMAIN in self.hass.data
                and entry.entry_id in self.hass.data[DOMAIN]
                and "devices" in self.hass.data[DOMAIN][entry.entry_id]
            ):
                self.hass.data[DOMAIN][entry.entry_id]["devices"] = [
                    d
                    for d in self.hass.data[DOMAIN][entry.entry_id]["devices"]
                    if d.get(filter_key) != filter_value
                ]
        else:
            self.logger.error("No config entry found for Varko.")
            return

        if ENTITY_ID not in device_to_remove:
            entity_entry_id = entity_registry.async_get_entity_id(
                "light", DOMAIN, device_id
            )

            if entity_entry_id:
                entity_registry.async_remove(entity_entry_id)
                self.logger.debug(
                    f"Removed entity {entity_entry_id} (device ID: {device_id})."
                )
            else:
                self.logger.warning(f"No entity found for device ID {device_id}.")
        else:
            self.logger.debug(
                f"Device {device_id} linked to existing entity {device_to_remove[ENTITY_ID]}, skipping entity removal."
            )

    @service
    @admin
    async def enable_device(self, call: ServiceCall):
        entity_id = call.data.get(ENTITY)

        entity_registry = async_get_entity_registry(self.hass)
        entity_entry = entity_registry.async_get(entity_id)

        if not entity_entry:
            self.logger.error(f"Entity {entity_id} not found in registry")
            return

        device_id = entity_entry.unique_id

        device_to_enable = next(
            (device for device in self.data if device[DEVICE_ID] == device_id), None
        )

        if not device_to_enable:
            device_to_enable = next(
                (device for device in self.data if device.get(ENTITY_ID) == entity_id),
                None,
            )

        if not device_to_enable:
            self.logger.warning(
                f"Device or entity {entity_id} not found in Varko data."
            )
            return

        if device_to_enable.get(IS_ENABLED, True):
            self.logger.warning(f"Device {device_id} already enabled")
            return

        device_to_enable[IS_ENABLED] = True

        if ENTITY_ID in device_to_enable:
            filter_key = ENTITY_ID
            filter_value = device_to_enable[ENTITY_ID]
        else:
            filter_key = DEVICE_ID
            filter_value = device_to_enable[DEVICE_ID]

        entry = next(
            (entry for entry in self.hass.config_entries.async_entries(DOMAIN)),
            None,
        )
        if entry:
            for device in entry.data.get("devices", []):
                if device.get(filter_key) == filter_value:
                    device[IS_ENABLED] = True
                    break
            self.hass.config_entries.async_update_entry(
                entry, data={"devices": entry.data["devices"]}
            )
            if (
                DOMAIN in self.hass.data
                and entry.entry_id in self.hass.data[DOMAIN]
                and "devices" in self.hass.data[DOMAIN][entry.entry_id]
            ):
                for device in self.hass.data[DOMAIN][entry.entry_id]["devices"]:
                    if device.get(filter_key) == filter_value:
                        device[IS_ENABLED] = True
                        break

        await self.store.async_save(self.data)
        self.logger.debug(f"Enabled device {device_id} (Entity {entity_id}).")

    @service
    @admin
    async def disable_device(self, call: ServiceCall):
        entity_id = call.data.get(ENTITY)

        entity_registry = async_get_entity_registry(self.hass)
        entity_entry = entity_registry.async_get(entity_id)
        if not entity_entry:
            self.logger.error(f"Entity {entity_id} not found in registry")
            return

        device_id = entity_entry.unique_id

        device_to_disable = next(
            (device for device in self.data if device[DEVICE_ID] == device_id), None
        )

        if not device_to_disable:
            device_to_disable = next(
                (device for device in self.data if device.get(ENTITY_ID) == entity_id),
                None,
            )

        if not device_to_disable:
            self.logger.warning(
                f"Device or entity {entity_id} not found in Varko data."
            )
            return

        if not device_to_disable.get(IS_ENABLED, True):
            self.logger.warning(f"Device {device_id} already disabled.")
            return

        device_to_disable[IS_ENABLED] = False

        if ENTITY_ID in device_to_disable:
            filter_key = ENTITY_ID
            filter_value = device_to_disable[ENTITY_ID]
        else:
            filter_key = DEVICE_ID
            filter_value = device_to_disable[DEVICE_ID]

        entry = next((e for e in self.hass.config_entries.async_entries(DOMAIN)), None)

        if entry:
            for device in entry.data.get("devices", []):
                if device.get(filter_key) == filter_value:
                    device[IS_ENABLED] = False
                    break
            self.hass.config_entries.async_update_entry(
                entry, data={"devices": entry.data["devices"]}
            )
            if (
                DOMAIN in self.hass.data
                and entry.entry_id in self.hass.data[DOMAIN]
                and "devices" in self.hass.data[DOMAIN][entry.entry_id]
            ):
                for device in self.hass.data[DOMAIN][entry.entry_id]["devices"]:
                    if device.get(filter_key) == filter_value:
                        device[IS_ENABLED] = False
                        break

        await self.store.async_save(self.data)
        self.logger.debug(f"Disabled device {device_id} (Entity {entity_id}).")

    async def control_device(self, device_id: str, command: str):
        normalized_command = command.upper()

        device = next(
            (device for device in self.data if device[DEVICE_ID] == device_id), None
        )
        if not device:
            self.logger.error(f"Device {device_id} not found in store data")
            return

        entity_id = device.get(ENTITY_ID)
        if not entity_id:
            entity_registry = async_get_entity_registry(self.hass)
            entity_id = entity_registry.async_get_entity_id("light", DOMAIN, device_id)
            if not entity_id:
                self.logger.error(f"No entity found for device {device_id}")
                return

        state = self.hass.states.get(entity_id)
        if not state:
            self.logger.error(f"Entity {entity_id} not available in states")
            return

        try:
            if normalized_command == "ON":
                self.logger.debug(f"async_turn_on should be called")
                await self.hass.services.async_call(
                    "light", "turn_on", {"entity_id": entity_id}, blocking=True
                )
            elif normalized_command == "OFF":
                self.logger.debug(f"async_turn_off should be called")
                await self.hass.services.async_call(
                    "light", "turn_off", {"entity_id": entity_id}, blocking=True
                )
            else:
                raise ValueError(f"Invalid command: {command}")
        except Exception as e:
            self.logger.error(f"Error controlling {device_id}: {str(e)}")
