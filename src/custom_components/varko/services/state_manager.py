import asyncio
import random
from homeassistant.core import HomeAssistant, ServiceCall

from custom_components.varko.const import (
    DOMAIN,
    STATE_ACTIVE,
    STATE_ENTITY_ID,
    STATE_IDLE,
    STATE_READY,
)
from custom_components.varko.decorators import admin, service
from custom_components.varko.services.base_manager import BaseManager
from custom_components.varko.services.device_manager import DeviceManager


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

        # Start presence detection
        self._manager.start_presence_detection()

    async def set_state_active(self):
        self._manager._logger.info("Setting system state to ACTIVE")
        self._manager._state = ActiveState(self._manager)

        # Start presence detection & simulation
        self._manager.start_presence_detection()
        self._manager.start_presence_simulation()


class ReadyState(State):
    """State when system is ready to start interventions"""

    async def set_state_idle(self):
        self._manager._logger.info("Setting system state to IDLE")
        self._manager._state = IdleState(self._manager)

        # Stop presence detection
        self._manager.stop_presence_detection()

    async def set_state_ready(self):
        self._manager._logger.warning("System is already READY")

    async def set_state_active(self):
        self._manager._logger.info("Setting system state to ACTIVE")
        self._manager._state = ActiveState(self._manager)

        # Start presence simulation
        self._manager.start_presence_simulation()


class ActiveState(State):
    """State when system is doing interventions"""

    async def set_state_idle(self):
        self._manager._logger.info("Setting system state to IDLE")
        self._manager._state = IdleState(self._manager)

        # Stop presence detection & simulation
        self._manager.stop_presence_detection()
        self._manager.stop_presence_simulation()

    async def set_state_ready(self):
        self._manager._logger.info("Setting system state to READY")
        self._manager._state = ReadyState(self._manager)

        # Stop presence simulation
        self._manager.stop_presence_simulation()

    async def set_state_active(self):
        self._manager._logger.info("Resetting ACTIVE system state")

        # Restart presence simulation
        self._manager.start_presence_simulation()


class StateManager(BaseManager):
    __instance = None

    def __init__(self, hass: HomeAssistant):
        super().__init__(__name__, hass, f"{DOMAIN}.state", [])

        # Start in idle state
        self._state: State = IdleState(self)
        # Set Home Assistant state
        self._hass.states.async_set(STATE_ENTITY_ID, STATE_IDLE)

        self._presence_detection_enabled: bool = False

        # Presence simulation duration from Home Assistant Settings
        self._presence_simulation_duration_minutes = hass.config_entries.async_entries(
            DOMAIN
        )[0].data.get("presence_simulation_duration_minutes", 30)
        # Define presence simulation task
        self._presence_simulation_timer: asyncio.Task | None = None
        self._presence_simulation_stop_event = asyncio.Event()

    @classmethod
    async def get_instance(cls, hass: HomeAssistant):
        if cls.__instance is None:
            cls.__instance = cls(hass)
            await cls.__instance._initialize()
        return cls.__instance

    @service
    @admin
    async def set_state_idle(self, call: ServiceCall) -> None:
        """Set system to idle state."""
        await self._state.set_state_idle()
        self._hass.states.async_set(STATE_ENTITY_ID, STATE_IDLE)

    @service
    @admin
    async def set_state_ready(self, call: ServiceCall) -> None:
        """Set system to ready state."""
        await self._state.set_state_ready()
        self._hass.states.async_set(STATE_ENTITY_ID, STATE_READY)

    @service
    @admin
    async def set_state_active(self, call: ServiceCall) -> None:
        """Set system to active state."""
        await self.set_state_active_execute()

    async def internal_set_state_active(self):
        """Set system to active state from internal system."""
        # Ignore activation if presence detection disabled
        if not self._presence_detection_enabled:
            return
        await self.set_state_active_execute()

    async def set_state_active_execute(self):
        await self._state.set_state_active()
        self._hass.states.async_set(STATE_ENTITY_ID, STATE_ACTIVE)

    def start_presence_detection(self):
        self._presence_detection_enabled = True
        self._logger.info("Started presence detection")

    def stop_presence_detection(self):
        self._presence_detection_enabled = False
        self._logger.info("Stopped presence detection")

    def start_presence_simulation(self):
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
            self.presence_simulation_task()
        )

    def stop_presence_simulation(self):
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
                await device_manager.control_device(device_id, "OFF")
                self._logger.debug(
                    f"Turned off device {device_id} during simulation stop"
                )
            except Exception as e:
                self._logger.error(f"Error turning off device {device_id}: {e}")

    async def presence_simulation_task(self):
        try:
            await self.presence_simulation()
            self._logger.info(
                "Presence simulation timer expired, setting state to READY"
            )
            await self.set_state_ready(None)
        except asyncio.CancelledError:
            self._logger.debug("Presence simulation timer cancelled")

    async def presence_simulation(self):
        # TODO: Use environment info (time of day etc) to determine which devices to turn on first / turn on at all
        device_manager = await DeviceManager.get_instance(self._hass)
        devices = device_manager._data

        for device in devices:
            device_id = device.get("device_id")
            device_name = device.get("device_name", "Unknown device")
            if not device_id:
                self._logger.warning(
                    f"Device {device_name} missing device_id, skipping"
                )
                continue

            self._logger.info(f"Turning on device '{device_name}' ({device_id})")
            try:
                await device_manager.control_device(device_id, "ON")
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
