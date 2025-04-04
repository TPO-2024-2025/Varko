from typing import Any

from homeassistant.helpers.restore_state import RestoreEntity

from homeassistant.components.light import LightEntity, ColorMode
from homeassistant.components.mqtt import async_publish, async_subscribe
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    _LOGGER.debug("Setting up Varko lights")
    devices = entry.data.get("devices", [])

    if not devices:
        _LOGGER.warning("No devices found in config entry, lights will not be added")
    _LOGGER.debug(f"Devices in config entry: {devices}")

    light_entities = [
        VarkoLight(
            hass,
            device["device_name"],
            device["device_id"],
        )
        for device in devices
        if device.get("device_type") == "light"
    ]

    if light_entities:
        async_add_entities(light_entities, update_before_add=True)
    else:
        _LOGGER.warning("No light devices found in config entry.")


class VarkoLight(LightEntity, RestoreEntity):

    def __init__(self, hass, name, device_id):
        super().__init__()
        self._state = False
        self._attr_has_entity_name = True
        self._attr_supported_color_modes = {ColorMode.ONOFF}
        self._attr_color_mode = ColorMode.ONOFF
        self.hass = hass

        self._attr_name = name
        self._attr_unique_id = device_id
        self._command_topic = (
            f"shellies/shellycolorbulb-{device_id.upper()}/color/0/command"
        )
        self._state_topic = f"shellies/shellycolorbulb-{device_id.upper()}/color/0"

    @property
    def is_on(self):
        return self._state

    @property
    def unique_id(self) -> str | None:
        return self._attr_unique_id

    async def async_turn_on(self, **kwargs: Any) -> None:
        _LOGGER.debug("turn on called")
        await async_publish(self.hass, self._command_topic, "on")
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        _LOGGER.debug("turn off called")
        await async_publish(self.hass, self._command_topic, "off")
        self._state = False
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        _LOGGER.debug("added to hass called")
        last_state = await self.async_get_last_state()
        if last_state:
            self._state = last_state.state == "on"
            self.async_write_ha_state()

        async def state_message_received(msg):
            _LOGGER.debug("message received called")
            if msg.topic == self._state_topic:
                self._state = msg.payload == "on"
                self.async_write_ha_state()

        await async_subscribe(self.hass, self._state_topic, state_message_received)
