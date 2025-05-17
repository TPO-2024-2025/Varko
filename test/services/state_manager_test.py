import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch, call

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from custom_components.varko.const import (
    DOMAIN,
    STATE_ACTIVE,
    STATE_ENTITY_ID,
    STATE_IDLE,
    STATE_READY,
)
from custom_components.varko.services.state_manager import (
    StateManager,
    IdleState,
    ReadyState,
    ActiveState,
)


class TestStateManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_hass = MagicMock()

        self.store_patch = patch(
            "custom_components.varko.services.base_manager.Store",
            return_value=MagicMock(),
        )
        self.mock_store = self.store_patch.start()

        self.init_patch = patch.object(
            StateManager, "_initialize", new_callable=AsyncMock
        )
        self.mock_init = self.init_patch.start()

        self.mqtt_patch = patch.object(
            StateManager, "_setup_mqtt", new_callable=AsyncMock
        )
        self.mock_mqtt = self.mqtt_patch.start()

        self.state_manager = StateManager(self.mock_hass)

        self.state_manager._start_presence_simulation = MagicMock()
        self.state_manager._stop_presence_simulation = MagicMock()

        mock_entry = MagicMock()
        mock_entry.data = {"presence_simulation_duration_minutes": 15}
        self.mock_hass.config_entries.async_entries.return_value = [mock_entry]

        self.device_manager_patch = patch(
            "custom_components.varko.services.state_manager.DeviceManager.get_instance",
            new_callable=AsyncMock,
        )
        self.mock_device_manager_get = self.device_manager_patch.start()

        device_manager_instance = AsyncMock()
        device_manager_instance._data = [
            {"device_id": "device1", "device_name": "Light 1"},
            {"device_id": "device2", "device_name": "Light 2"},
        ]
        device_manager_instance.control_device = AsyncMock()
        self.mock_device_manager_get.return_value = device_manager_instance

    def tearDown(self):
        self.store_patch.stop()
        self.init_patch.stop()
        self.mqtt_patch.stop()
        self.device_manager_patch.stop()

        StateManager.destroy()

    # -------------------------------------------------------------------------
    # Initialization and Singleton Tests
    # -------------------------------------------------------------------------

    async def test_initialization_state(self):
        # assert
        self.assertIsInstance(self.state_manager._state, IdleState)
        self.mock_hass.states.async_set.assert_called_once_with(
            STATE_ENTITY_ID, STATE_IDLE
        )

    async def test_should_get_same_instance(self):
        # arrange
        instance1 = await StateManager.get_instance(self.mock_hass)

        # act
        instance2 = await StateManager.get_instance(self.mock_hass)

        # assert
        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, StateManager)

    async def test_destroy_instance(self):
        # arrange
        await StateManager.get_instance(self.mock_hass)

        # act
        StateManager.destroy()

        # assert
        self.assertIsNone(StateManager._StateManager__instance)

    # -------------------------------------------------------------------------
    # State Transition Tests - All combinations
    # -------------------------------------------------------------------------

    # Idle -> Idle
    async def test_idle_to_idle_transition(self):
        # arrange
        self.state_manager._state = IdleState(self.state_manager)
        mock_call = MagicMock()
        mock_call.context.user_id = None

        # act
        await self.state_manager.set_state_idle(mock_call)

        # assert
        self.mock_hass.states.async_set.assert_called_with(STATE_ENTITY_ID, STATE_IDLE)

    # Idle -> Ready
    async def test_idle_to_ready_transition(self):
        # arrange
        self.state_manager._state = IdleState(self.state_manager)
        mock_call = MagicMock()
        mock_call.context.user_id = None

        # act
        await self.state_manager.set_state_ready(mock_call)

        # assert
        self.assertIsInstance(self.state_manager._state, ReadyState)
        self.mock_hass.states.async_set.assert_called_with(STATE_ENTITY_ID, STATE_READY)

    # Idle -> Active
    async def test_idle_to_active_transition(self):
        # arrange
        self.state_manager._state = IdleState(self.state_manager)
        self.state_manager._start_presence_simulation = MagicMock()
        mock_call = MagicMock()
        mock_call.context.user_id = None

        # act
        await self.state_manager.set_state_active(mock_call)

        # assert
        self.assertIsInstance(self.state_manager._state, ActiveState)
        self.mock_hass.states.async_set.assert_called_with(
            STATE_ENTITY_ID, STATE_ACTIVE
        )
        self.state_manager._start_presence_simulation.assert_called_once()

    # Ready -> Idle
    async def test_ready_to_idle_transition(self):
        # arrange
        self.state_manager._state = ReadyState(self.state_manager)
        mock_call = MagicMock()
        mock_call.context.user_id = None

        # act
        await self.state_manager.set_state_idle(mock_call)

        # assert
        self.assertIsInstance(self.state_manager._state, IdleState)
        self.mock_hass.states.async_set.assert_called_with(STATE_ENTITY_ID, STATE_IDLE)

    # Ready -> Ready
    async def test_ready_to_ready_transition(self):
        # arrange
        self.state_manager._state = ReadyState(self.state_manager)
        mock_call = MagicMock()
        mock_call.context.user_id = None

        # act
        await self.state_manager.set_state_ready(mock_call)

        # assert
        self.assertIsInstance(self.state_manager._state, ReadyState)
        # Warning should be logged but can't easily verify in this test setup

    # Ready -> Active
    async def test_ready_to_active_transition(self):
        # arrange
        self.state_manager._state = ReadyState(self.state_manager)
        self.state_manager._start_presence_simulation = MagicMock()
        mock_call = MagicMock()
        mock_call.context.user_id = None
        self.state_manager._send_notification = AsyncMock()

        # act
        await self.state_manager.set_state_active(mock_call)

        # assert
        self.assertIsInstance(self.state_manager._state, ActiveState)
        self.mock_hass.states.async_set.assert_called_with(
            STATE_ENTITY_ID, STATE_ACTIVE
        )
        self.state_manager._start_presence_simulation.assert_called_once()
        self.state_manager._send_notification.assert_called_with(
            "System is now active."
        )

    # Active -> Idle
    async def test_active_to_idle_transition(self):
        # arrange
        self.state_manager._state = ActiveState(self.state_manager)
        self.state_manager._stop_presence_simulation = MagicMock()
        mock_call = MagicMock()
        mock_call.context.user_id = None

        # act
        await self.state_manager.set_state_idle(mock_call)

        # assert
        self.assertIsInstance(self.state_manager._state, IdleState)
        self.mock_hass.states.async_set.assert_called_with(STATE_ENTITY_ID, STATE_IDLE)
        self.state_manager._stop_presence_simulation.assert_called_once()

    # Active -> Ready
    async def test_active_to_ready_transition(self):
        # arrange
        self.state_manager._state = ActiveState(self.state_manager)
        self.state_manager._stop_presence_simulation = MagicMock()
        mock_call = MagicMock()
        mock_call.context.user_id = None
        self.state_manager._send_notification = AsyncMock()

        # act
        await self.state_manager.set_state_ready(mock_call)

        # assert
        self.assertIsInstance(self.state_manager._state, ReadyState)
        self.mock_hass.states.async_set.assert_called_with(STATE_ENTITY_ID, STATE_READY)
        self.state_manager._stop_presence_simulation.assert_called_once()
        self.state_manager._send_notification.assert_called_with("System is now ready.")

    # Active -> Active
    async def test_active_to_active_transition(self):
        # arrange
        self.state_manager._state = ActiveState(self.state_manager)
        self.state_manager._start_presence_simulation = MagicMock()
        mock_call = MagicMock()
        mock_call.context.user_id = None

        # act
        await self.state_manager.set_state_active(mock_call)

        # assert
        self.assertIsInstance(self.state_manager._state, ActiveState)
        self.mock_hass.states.async_set.assert_called_with(
            STATE_ENTITY_ID, STATE_ACTIVE
        )
        self.state_manager._start_presence_simulation.assert_called_once()

    # -------------------------------------------------------------------------
    # MQTT Tests
    # -------------------------------------------------------------------------

    async def test_setup_mqtt(self):
        # Arrange
        self.mqtt_patch.stop()
        with patch(
            "custom_components.varko.services.state_manager.mqtt.async_subscribe",
            new_callable=AsyncMock,
        ) as mock_subscribe:
            # Act
            await self.state_manager._setup_mqtt()

            # Assert
            mock_subscribe.assert_called_once()

    def test_clear_mqtt(self):
        # arrange
        subscription_mock = MagicMock()
        self.state_manager._mqtt_frigate_subscription = subscription_mock

        # act
        self.state_manager._clear_mqtt()

        # assert
        subscription_mock.assert_called_once()
        self.assertIsNone(self.state_manager._mqtt_frigate_subscription)

    async def test_handle_person_detection_with_payload(self):
        # arrange
        self.state_manager._state = ReadyState(self.state_manager)
        msg = MagicMock()
        msg.payload = "1"
        self.mock_hass.services.async_call = AsyncMock()

        # act
        await self.state_manager._handle_person_detection(msg)

        # assert
        self.mock_hass.services.async_call.assert_called_once_with(
            DOMAIN,
            "set_state_active",
        )

    async def test_handle_person_detection_with_empty_payload(self):
        # arrange
        msg = MagicMock()
        msg.payload = ""
        self.state_manager._hass.services.async_call = AsyncMock()

        # act
        await self.state_manager._handle_person_detection(msg)

        # assert
        self.state_manager._hass.services.async_call.assert_not_called()

    async def test_handle_person_detection_in_idle_state(self):
        # arrange
        self.state_manager._state = IdleState(self.state_manager)
        msg = MagicMock()
        msg.payload = "1"
        self.state_manager._hass.services.async_call = AsyncMock()

        # act
        await self.state_manager._handle_person_detection(msg)

        # assert
        self.state_manager._hass.services.async_call.assert_not_called()

    # -------------------------------------------------------------------------
    # Presence Simulation Tests
    # -------------------------------------------------------------------------

    async def test_start_presence_simulation(self):
        # arrange
        self.state_manager._presence_simulation_timer = MagicMock()
        self.state_manager._presence_simulation_timer.done.return_value = False

        with patch("asyncio.create_task") as mock_create_task:
            # act
            self.state_manager._start_presence_simulation()

            # assert
            self.assertFalse(
                self.state_manager._presence_simulation_stop_event.is_set()
            )

    async def test_stop_presence_simulation(self):
        # arrange
        mock_timer = MagicMock()
        mock_timer.done.return_value = False
        self.state_manager._presence_simulation_timer = mock_timer
        self.state_manager._turn_off_all_devices = AsyncMock()

        self.state_manager._stop_presence_simulation = (
            StateManager._stop_presence_simulation.__get__(self.state_manager)
        )

        # act
        self.state_manager._stop_presence_simulation()

        # assert
        self.assertTrue(self.state_manager._presence_simulation_stop_event.is_set())

    async def test_turn_off_all_devices(self):
        # arrange
        device_manager_instance = AsyncMock()
        device_manager_instance.control_device = AsyncMock()
        device_manager_instance._data = [
            {"device_id": "device1", "device_name": "Light 1"},
            {"device_id": "device2", "device_name": "Light 2"},
        ]
        self.mock_device_manager_get.return_value = device_manager_instance

        # act
        await self.state_manager._turn_off_all_devices()

        # assert
        self.mock_device_manager_get.assert_called_once()
        device_manager_instance.control_device.assert_has_calls(
            [call("device1", "OFF"), call("device2", "OFF")]
        )

    async def test_presence_simulation_task_completion(self):
        # arrange
        self.state_manager._presence_simulation = AsyncMock()
        self.state_manager.set_state_ready = AsyncMock()

        # act
        await self.state_manager._presence_simulation_task()

        # assert
        self.state_manager._presence_simulation.assert_called_once()
        self.state_manager.set_state_ready.assert_called_once_with(None)

    async def test_presence_simulation(self):
        # arrange
        device_manager_instance = self.mock_device_manager_get.return_value
        self.state_manager._presence_simulation_duration_minutes = 15
        self.state_manager._wait_or_stop = AsyncMock(side_effect=[False, False, False])

        # act
        await self.state_manager._presence_simulation()

        # assert
        device_manager_instance.control_device.assert_has_awaits(
            [call("device1", "ON"), call("device2", "ON")]
        )
        self.state_manager._wait_or_stop.assert_has_awaits(
            [
                call(unittest.mock.ANY),
                call(unittest.mock.ANY),
                call(15 * 60),
            ]
        )

    async def test_presence_simulation_early_stop(self):
        # arrange
        self.state_manager._wait_or_stop = AsyncMock(side_effect=[True])
        device_manager_instance = self.mock_device_manager_get.return_value
        device_manager_instance.control_device.reset_mock()

        # act
        await self.state_manager._presence_simulation()

        # assert
        device_manager_instance.control_device.assert_called_with("device1", "ON")
        self.assertEqual(device_manager_instance.control_device.call_count, 1)
        self.state_manager._wait_or_stop.assert_called_once()
