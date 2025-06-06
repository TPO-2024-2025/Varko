import asyncio
import random
from datetime import datetime, time
from zoneinfo import ZoneInfo

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, ServiceCall

from custom_components.varko.const import (
    DEVICE_ID,
    DEVICE_NAME,
    DEVICE_TYPE,
    DOMAIN,
    FRIGATE_MQTT_PERSON_TOPIC,
    STATE_ACTIVE,
    STATE_ENTITY_ID,
    STATE_IDLE,
    STATE_READY,
)
from custom_components.varko.decorators import admin, service
from custom_components.varko.services.base_manager import BaseManager
from custom_components.varko.services.device_manager import DeviceManager
from custom_components.varko.services.group_manager import GroupManager


class State:
    """Base State interface"""

    def __init__(self, manager: "StateManager"):
        self._manager = manager

    async def set_state_idle(self):
        raise NotImplementedError

    async def set_state_ready(self):
        raise NotImplementedError

    async def set_state_active(self):
        raise NotImplementedError


class IdleState(State):
    """State when system is inactive"""

    async def set_state_idle(self):
        self._manager._logger.warning("System is already IDLE")

    async def set_state_ready(self):
        self._manager._logger.info("Setting system state to READY")
        self._manager._state = ReadyState(self._manager)

    async def set_state_active(self):
        self._manager._logger.info("Setting system state to ACTIVE")
        self._manager._state = ActiveState(self._manager)

        # Start presence simulation
        self._manager._start_presence_simulation()


class ReadyState(State):
    """State when system is ready to start interventions"""

    async def set_state_idle(self):
        self._manager._logger.info("Setting system state to IDLE")
        self._manager._state = IdleState(self._manager)

    async def set_state_ready(self):
        self._manager._logger.warning("System is already READY")

    async def set_state_active(self):
        self._manager._logger.info("Setting system state to ACTIVE")
        self._manager._state = ActiveState(self._manager)

        # Start presence simulation
        self._manager._start_presence_simulation()
        await self._manager._send_notification("System is now active.")


class ActiveState(State):
    """State when system is doing interventions"""

    async def set_state_idle(self):
        self._manager._logger.info("Setting system state to IDLE")
        self._manager._state = IdleState(self._manager)

        # Stop presence simulation
        self._manager._stop_presence_simulation()

    async def set_state_ready(self):
        self._manager._logger.info("Setting system state to READY")
        self._manager._state = ReadyState(self._manager)

        # Stop presence simulation
        self._manager._stop_presence_simulation()
        await self._manager._send_notification("System is now ready.")

    async def set_state_active(self):
        self._manager._logger.info("Resetting ACTIVE system state")

        # Restart presence simulation
        self._manager._start_presence_simulation()


class StateManager(BaseManager):
    __instance = None

    def __init__(self, hass: HomeAssistant):
        super().__init__(__name__, hass, f"{DOMAIN}.state", [])

        # Start in idle state
        self._state: State = IdleState(self)
        # Set Home Assistant state
        self._hass.states.async_set(STATE_ENTITY_ID, STATE_IDLE)

        # Presence simulation duration from Home Assistant Settings
        self._presence_simulation_duration_minutes = hass.config_entries.async_entries(
            DOMAIN
        )[0].data.get("presence_simulation_duration_minutes", 30)
        # Define presence simulation task
        self._presence_simulation_timer: asyncio.Task | None = None
        self._presence_simulation_stop_event = asyncio.Event()

        self._mqtt_frigate_subscription = None

    @classmethod
    async def get_instance(cls, hass: HomeAssistant):
        if cls.__instance is None:
            cls.__instance = cls(hass)
            await cls.__instance._initialize()
            await cls.__instance._setup_mqtt()
        return cls.__instance

    @classmethod
    def destroy(cls):
        if cls.__instance is not None:
            cls.__instance._clear_mqtt()
            cls.__instance.__del__()
            cls.__instance = None

    @service
    @admin
    async def set_state_idle(self, call: ServiceCall) -> None:
        """Set system to idle state."""
        await self._state.set_state_idle()
        self._hass.states.async_set(STATE_ENTITY_ID, STATE_IDLE)

    @service
    @admin
    async def set_state_ready(self, call: ServiceCall) -> None:
        caller_id = call.context.user_id

        if not caller_id and self._state == ActiveState(self):
            self._logger.debug(
                "Internal set_state_ready called while system is active, skipping"
            )
            return

        """Set system to ready state."""
        await self._state.set_state_ready()
        self._hass.states.async_set(STATE_ENTITY_ID, STATE_READY)

    @service
    @admin
    async def set_state_active(self, call: ServiceCall) -> None:
        """Set system to active state."""

        await self._state.set_state_active()
        self._hass.states.async_set(STATE_ENTITY_ID, STATE_ACTIVE)

    def _start_presence_simulation(self):
        self._logger.info("Started presence simulation")

        self._presence_simulation_stop_event.clear()
        # Reset current presence simulation
        if (
            self._presence_simulation_timer
            and not self._presence_simulation_timer.done()
        ):
            self._presence_simulation_timer.cancel()
            self._logger.debug("Cancelled existing presence simulation timer")
        # Start presence simulation
        self._presence_simulation_timer = asyncio.create_task(
            self._presence_simulation_task()
        )

    def _stop_presence_simulation(self):
        self._logger.info("Stopped presence simulation")

        self._presence_simulation_stop_event.set()
        # Turn off all actual devices
        asyncio.create_task(self._turn_off_all_devices())

        if (
            self._presence_simulation_timer
            and not self._presence_simulation_timer.done()
        ):
            self._presence_simulation_timer.cancel()
            self._logger.debug("Cancelled presence simulation timer")
            self._presence_simulation_timer = None

    async def _turn_off_all_devices(self):
        device_manager = await DeviceManager.get_instance(self._hass)
        for device in device_manager._data:
            device_id = device.get("device_id")
            if not device_id:
                continue
            try:
                if device.get(DEVICE_TYPE) == "media_player":
                    await device_manager.control_device(device_id, "STOP_MEDIA")

                await device_manager.control_device(device_id, "OFF")
                self._logger.debug(
                    f"Turned off device {device_id} during simulation stop"
                )
            except Exception as e:
                self._logger.error(f"Error turning off device {device_id}: {e}")

    async def _presence_simulation_task(self):
        try:
            await self._presence_simulation()
            self._logger.info(
                "Presence simulation timer expired, setting state to READY"
            )
            await self.set_state_ready(None)
        except asyncio.CancelledError:
            self._logger.debug("Presence simulation timer cancelled")

    async def _presence_simulation(self):
        # TODO: Use environment info (time of day etc) to determine which devices to turn on first / turn on at all
        device_manager = await DeviceManager.get_instance(self._hass)
        devices = device_manager._data

        timezone = ZoneInfo(self._hass.config.time_zone)
        time_now = datetime.now(timezone).time()

        time_morning = time(6, 0)
        time_evening = time(22, 0)

        for device in devices:
            device_type = device.get(DEVICE_TYPE)
            if device_type == "light" and time_morning <= time_now < time_evening:
                self._logger.info("Skipping light device during daytime")
                continue
            elif device_type == "media_player" and (
                time_now < time_morning or time_now >= time_evening
            ):
                self._logger.info("Skipping media_player device during nighttime")
                continue

            device_id = device.get(DEVICE_ID)
            device_name = device.get(DEVICE_NAME, "Unknown device")
            if not device_id:
                self._logger.warning(
                    f"Device {device_name} missing device_id, skipping"
                )
                continue

            self._logger.info(f"Turning on device '{device_name}' ({device_id})")
            try:
                await device_manager.control_device(device_id, "ON")

                if device_type == "media_player":
                    await device_manager.control_device(device_id, "PLAY_MEDIA")
            except Exception as e:
                self._logger.error(f"Error turning on device {device_id}: {e}")

            # Wait random interval between devices turning on
            stopped = await self._wait_or_stop(random.uniform(3, 8))
            if stopped:
                self._logger.info("Presence simulation stopped early")
                return

        # Wait for the full simulation duration or until stop event is set
        await self._wait_or_stop(self._presence_simulation_duration_minutes * 60)

    async def _wait_or_stop(self, delay):
        try:
            await asyncio.wait_for(
                self._presence_simulation_stop_event.wait(), timeout=delay
            )
            return True
        except asyncio.TimeoutError:
            return False

    async def _setup_mqtt(self):
        try:
            self._mqtt_frigate_subscription = await mqtt.async_subscribe(
                self._hass,
                FRIGATE_MQTT_PERSON_TOPIC,
                self._handle_person_detection,
                qos=1,
            )
            self._logger.info("MQTT subscription to frigate/+/person established")
        except Exception as e:
            self._logger.error(f"Failed to set up MQTT subscription: {e}")

    async def _handle_person_detection(self, msg: mqtt.ReceiveMessage):

        if not msg.payload:
            self._logger.warning("Received empty payload from MQTT")
            return

        if msg.payload == "1":
            # Ignore activation if called when system is in IDLE state
            is_idle = isinstance(self._state, IdleState)
            if is_idle:
                return

            await self._hass.services.async_call(
                DOMAIN,
                "set_state_active",
            )

    def _clear_mqtt(self):
        if self._mqtt_frigate_subscription:
            self._mqtt_frigate_subscription()
            self._mqtt_frigate_subscription = None
            self._logger.info("MQTT subscription to frigate/+/person cleared")

    async def _send_notification(self, message: str):
        group_manager = await GroupManager.get_instance(self._hass)
        people = group_manager._data

        devices = []
        for person in people:
            person_state = self._hass.states.get(person)
            if not person_state:
                self._logger.warning(f"Person {person} does not exist.")
                continue

            new_devices = person_state.attributes.get("device_trackers")
            if isinstance(new_devices, list):
                devices.extend(new_devices)
            elif isinstance(new_devices, str):
                devices.append(new_devices)

        for device in devices:
            self._logger.debug(f"Sending notification to {device}")
            await self._hass.services.async_call(
                "notify",
                f"mobile_app_{device.split('.')[1]}",
                {
                    "title": "Varko",
                    "message": message,
                },
                blocking=True,
            )
