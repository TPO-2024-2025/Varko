import os
import sys
import unittest
from unittest.mock import MagicMock, AsyncMock, patch

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from custom_components.varko.services.zone_manager import ZoneManager
from custom_components.varko.const import DOMAIN


class TestZoneManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_hass = MagicMock()
        self.mock_logger = MagicMock()
        self.mock_storage = AsyncMock()
        self.mock_storage.async_load = AsyncMock(return_value={})

        self.store_patch = patch(
            "custom_components.varko.services.base_manager.Store",
            return_value=self.mock_storage,
        )
        self.store_patch.start()

        self.base_init_patch = patch.object(
            ZoneManager, "_initialize", new_callable=AsyncMock
        )
        self.mock_base_init = self.base_init_patch.start()

        self.mock_tracker = MagicMock()
        self.track_state_change_event_patch = patch(
            "custom_components.varko.services.zone_manager.async_track_state_change_event",
            return_value=self.mock_tracker,
        )
        self.mock_track_state_change_event = self.track_state_change_event_patch.start()

        self.mock_group_manager = AsyncMock()
        self.group_manager_patch = patch(
            "custom_components.varko.services.zone_manager.GroupManager.get_instance",
            return_value=self.mock_group_manager,
        )
        self.mock_group_manager_instance = self.group_manager_patch.start()

        self.zone_manager = ZoneManager(self.mock_hass)

    def tearDown(self):
        self.store_patch.stop()
        self.base_init_patch.stop()
        self.track_state_change_event_patch.stop()
        self.group_manager_patch.stop()
        ZoneManager.destroy()

    # ----------------------------------------------
    # Initialization and singleton tests
    # ----------------------------------------------

    async def test_should_get_same_instance(self):
        # arrange
        instance1 = await ZoneManager.get_instance(self.mock_hass)

        # act
        instance2 = await ZoneManager.get_instance(self.mock_hass)

        # assert
        self.assertIsInstance(instance1, ZoneManager)
        self.assertIs(instance1, instance2)

    async def test_destroy_instance(self):
        # arrange
        await ZoneManager.get_instance(self.mock_hass)

        # act
        ZoneManager.destroy()

        # assert
        self.assertIsNone(ZoneManager._ZoneManager__instance)

    async def test_default_values_initializaition(self):
        # arrange
        await self.zone_manager._initialize()

        # assert
        self.assertEqual(self.zone_manager._data["active_zone"], "zone.home")
        self.assertEqual(self.zone_manager._group_tracker, None)
        self.assertEqual(self.zone_manager._device_trackers, [])
        self.assertEqual(self.zone_manager._device_entities, [])

    # ----------------------------------------------
    # Group tracker tests
    # ----------------------------------------------

    async def test_setup_group_tracker(self):
        # arrange
        mock_tracker = MagicMock()
        self.mock_track_state_change_event.return_value = mock_tracker

        mock_clear_group = MagicMock()
        with patch.object(ZoneManager, "_clear_group_tracker", mock_clear_group):
            # act
            await self.zone_manager._setup_group_tracker()

        # assert
        self.mock_track_state_change_event.assert_called_once_with(
            self.mock_hass,
            f"{DOMAIN}.group",
            self.zone_manager._handle_group_state_change,
        )
        mock_clear_group.assert_called_once()
        self.assertEqual(self.zone_manager._group_tracker, mock_tracker)

    def test_clear_group_tracker_with_existing_tracker(self):
        # arrange
        mock_tracker = MagicMock(return_value=None)
        self.zone_manager._group_tracker = mock_tracker

        # act
        self.zone_manager._clear_group_tracker()

        # assert
        mock_tracker.assert_called_once()
        self.assertIsNone(self.zone_manager._group_tracker)

    def test_clear_group_tracker_without_existing_tracker(self):
        # arrange
        self.zone_manager._group_tracker = None

        # act
        self.zone_manager._clear_group_tracker()

        # assert
        self.assertIsNone(self.zone_manager._group_tracker)

    # ----------------------------------------------
    # Device tracker tests
    # ----------------------------------------------
    async def test_setup_device_trackers_single_person(self):
        # arrange
        self.zone_manager._data = {"active_zone": "zone.home"}
        self.mock_group_manager._data = ["person.janez"]
        self.zone_manager._device_entities = []

        mock_person_state = MagicMock()
        mock_person_state.attributes = {"device_trackers": ["device_tracker.samsungS8"]}
        self.mock_hass.states.get.return_value = mock_person_state

        mock_check_presence_in_zone = AsyncMock()
        with patch.object(
            ZoneManager, "_check_presence_in_zone", mock_check_presence_in_zone
        ):
            # act
            await self.zone_manager._setup_device_trackers()

        # assert
        self.assertEqual(
            self.zone_manager._device_entities, ["device_tracker.samsungS8"]
        )
        self.mock_track_state_change_event.assert_called_once_with(
            self.mock_hass,
            ["device_tracker.samsungS8", "zone.home"],
            self.zone_manager._handle_zone_device_state_change,
        )
        mock_check_presence_in_zone.assert_awaited_once_with(
            "zone.home",
            ["device_tracker.samsungS8"],
        )

    async def test_setup_device_trackers_multiple_people(self):
        # arrange
        self.zone_manager._data = {"active_zone": "zone.home"}
        self.mock_group_manager._data = ["person.janez", "person.marta"]
        self.zone_manager._device_entities = []

        mock_person_state_janez = MagicMock()
        mock_person_state_janez.attributes = {
            "device_trackers": ["device_tracker.samsungS8"]
        }

        mock_person_state_marta = MagicMock()
        mock_person_state_marta.attributes = {
            "device_trackers": ["device_tracker.iphone"]
        }

        self.mock_hass.states.get.side_effect = [
            mock_person_state_janez,
            mock_person_state_marta,
        ]

        mock_check_presence_in_zone = AsyncMock()
        with patch.object(
            ZoneManager, "_check_presence_in_zone", mock_check_presence_in_zone
        ):
            # act
            await self.zone_manager._setup_device_trackers()

        # assert
        self.assertEqual(
            self.zone_manager._device_entities,
            ["device_tracker.samsungS8", "device_tracker.iphone"],
        )
        self.mock_track_state_change_event.assert_called_once_with(
            self.mock_hass,
            ["device_tracker.samsungS8", "device_tracker.iphone", "zone.home"],
            self.zone_manager._handle_zone_device_state_change,
        )
        mock_check_presence_in_zone.assert_awaited_once_with(
            "zone.home",
            ["device_tracker.samsungS8", "device_tracker.iphone"],
        )

    async def test_setup_device_trackers_no_active_zone(self):
        # arrange
        self.zone_manager._data = {"active_zone": None}
        self.mock_group_manager._data = ["person.janez"]
        self.zone_manager._device_entities = []

        # act
        with self.assertLogs(level="WARNING") as log:
            await self.zone_manager._setup_device_trackers()

        # assert
        self.assertEqual(self.zone_manager._device_entities, [])
        self.mock_hass.states.get.assert_not_called()
        self.mock_track_state_change_event.assert_not_called()
        self.assertIn("No active zone to track.", log.output[0])

    async def test_setup_device_trackers_person_does_not_exist(self):
        # arrange
        self.zone_manager._data = {"active_zone": "zone.home"}
        self.mock_group_manager._data = ["person.janez"]
        self.zone_manager._device_entities = []

        mock_person_state = MagicMock()
        mock_person_state.attributes = {"device_trackers": ["device_tracker.samsungS8"]}
        self.mock_hass.states.get.return_value = None  # Simulate person not existing

        # act
        with self.assertLogs(level="WARNING") as log:
            await self.zone_manager._setup_device_trackers()

        # assert
        self.assertEqual(self.zone_manager._device_entities, [])
        self.mock_hass.states.get.assert_called_once_with("person.janez")
        self.mock_track_state_change_event.assert_not_called()
        self.assertIn("Person person.janez does not exist.", log.output[0])

    async def test_setup_device_trackers_invalid_device_tracker_format(self):
        # arrange
        self.zone_manager._data = {"active_zone": "zone.home"}
        self.mock_group_manager._data = ["person.janez"]
        self.zone_manager._device_entities = []

        mock_person_state = MagicMock()
        mock_person_state.attributes = {"device_trackers": 123}
        self.mock_hass.states.get.return_value = mock_person_state

        with self.assertLogs(level="WARNING") as log:
            # act
            await self.zone_manager._setup_device_trackers()

        # assert
        self.assertEqual(self.zone_manager._device_entities, [])
        self.mock_hass.states.get.assert_called_once_with("person.janez")
        self.mock_track_state_change_event.assert_not_called()
        self.assertIn(
            "Invalid device tracker format for person.janez: 123", log.output[0]
        )

    async def test_setup_device_trackers_no_people(self):
        # arrange
        self.zone_manager._data = {"active_zone": "zone.home"}
        self.mock_group_manager._data = []
        self.zone_manager._device_entities = []

        # act
        with self.assertLogs(level="WARNING") as log:
            await self.zone_manager._setup_device_trackers()

        # assert
        self.assertEqual(self.zone_manager._device_entities, [])
        self.mock_hass.states.get.assert_not_called()
        self.mock_track_state_change_event.assert_not_called()
        self.assertIn(
            "No device trackers found for the users or no users present.", log.output[0]
        )

    def test_clear_device_trackers(self):
        # arrange
        self.zone_manager._device_trackers = [MagicMock(), MagicMock()]
        self.zone_manager._device_entities = [
            "device_tracker.samsungS8",
            "device_tracker.iphone",
        ]

        # act
        self.zone_manager._clear_device_trackers()

        # assert
        for tracker in self.zone_manager._device_trackers:
            tracker.assert_called_once()
        self.assertEqual(self.zone_manager._device_trackers, [])
        self.assertEqual(self.zone_manager._device_entities, [])

    def test_clear_device_trackers_no_trackers(self):
        # arrange
        self.zone_manager._device_trackers = []
        self.zone_manager._device_entities = [
            "device_tracker.samsungS8",
            "device_tracker.iphone",
        ]

        # act
        self.zone_manager._clear_device_trackers()

        # assert
        self.assertEqual(self.zone_manager._device_trackers, [])
        self.assertEqual(self.zone_manager._device_entities, [])

    # ----------------------------------------------
    # Callback methods tests
    # ----------------------------------------------
    async def test_handle_group_state_change(self):
        # arrange
        mock_setup_device_trackers = AsyncMock()
        with patch.object(
            ZoneManager, "_setup_device_trackers", mock_setup_device_trackers
        ):
            # act
            await self.zone_manager._handle_group_state_change(None)

        # assert
        mock_setup_device_trackers.assert_awaited_once()

    async def test_handle_zone_device_state_change_zone_event(self):
        # arrange
        self.zone_manager._data = {"active_zone": "zone.home"}
        self.zone_manager._device_entities = [
            "device_tracker.samsungS8",
            "device_tracker.iphoneX",
        ]

        event = MagicMock()
        event.data = {"entity_id": "zone.home"}

        mock_check_presence_in_zone = AsyncMock()
        with patch.object(
            ZoneManager, "_check_presence_in_zone", mock_check_presence_in_zone
        ):
            # act
            await self.zone_manager._handle_zone_device_state_change(event)

        # assert
        mock_check_presence_in_zone.assert_awaited_once_with(
            "zone.home",
            ["device_tracker.samsungS8", "device_tracker.iphoneX"],
        )

    async def test_handle_zone_device_state_change_device_event(self):
        # arrange
        self.zone_manager._data = {"active_zone": "zone.home"}
        self.zone_manager._device_entities = [
            "device_tracker.samsungS8",
            "device_tracker.iphoneX",
        ]

        event = MagicMock()
        event.data = {"entity_id": "device_tracker.samsungS8"}

        mock_check_presence_in_zone = AsyncMock()
        with patch.object(
            ZoneManager, "_check_presence_in_zone", mock_check_presence_in_zone
        ):
            # act
            await self.zone_manager._handle_zone_device_state_change(event)

        # assert
        mock_check_presence_in_zone.assert_awaited_once_with(
            "zone.home",
            ["device_tracker.samsungS8"],
        )

    # -----------------------------------------------
    # Check presence in zone tests
    # -----------------------------------------------
    async def test_check_presence_in_zone_device_in_zone(self):
        # arrange
        zone_entity_id = "zone.home"
        tracking_entities = ["device_tracker.samsungS8"]

        mock_zone_state = MagicMock()
        mock_zone_state.attributes = {"radius": 100, "longitude": 0, "latitude": 0}

        mock_device_state = MagicMock()
        mock_device_state.attributes = {"longitude": 0, "latitude": 0}

        self.mock_hass.states.get.side_effect = [
            mock_zone_state,
            mock_device_state,
        ]

        mock_service_call = AsyncMock()
        self.mock_hass.services.async_call = mock_service_call

        # act
        with self.assertLogs(level="INFO") as log:
            await self.zone_manager._check_presence_in_zone(
                zone_entity_id, tracking_entities
            )

        # assert
        self.assertIn(
            "Device device_tracker.samsungS8 is in the zone zone.home.", log.output[0]
        )

    async def test_check_presence_in_zone_device_not_in_zone(self):
        # arrange
        zone_entity_id = "zone.home"
        tracking_entities = ["device_tracker.samsungS8"]

        mock_zone_state = MagicMock()
        mock_zone_state.attributes = {"radius": 100, "longitude": 0, "latitude": 0}

        mock_device_state = MagicMock()
        mock_device_state.attributes = {"longitude": 1, "latitude": 1}

        self.mock_hass.states.get.side_effect = [
            mock_zone_state,
            mock_device_state,
        ]

        mock_service_call = AsyncMock()
        self.mock_hass.services.async_call = mock_service_call

        # act
        with self.assertLogs(level="INFO") as log:
            await self.zone_manager._check_presence_in_zone(
                zone_entity_id, tracking_entities
            )

        # assert
        self.assertIn(
            "Device device_tracker.samsungS8 is not in the zone zone.home.",
            log.output[0],
        )

    async def test_check_presence_in_zone_no_zone(self):
        # arrange
        zone_entity_id = None
        tracking_entities = ["device_tracker.samsungS8"]

        # act
        with self.assertLogs(level="WARNING") as log:
            await self.zone_manager._check_presence_in_zone(
                zone_entity_id, tracking_entities
            )

        # assert
        self.assertIn("No zone entity ID provided.", log.output[0])

    async def test_check_presence_in_zone_no_tracking_entities(self):
        # arrange
        zone_entity_id = "zone.home"
        tracking_entities = []

        # act
        with self.assertLogs(level="WARNING") as log:
            await self.zone_manager._check_presence_in_zone(
                zone_entity_id, tracking_entities
            )

        # assert
        self.assertIn("No device trackers provided.", log.output[0])

    async def test_check_presence_in_zone_zone_does_not_exist(self):
        # arrange
        zone_entity_id = "zone.home"
        tracking_entities = ["device_tracker.samsungS8"]

        self.mock_hass.states.get.return_value = None

        # act
        with self.assertLogs(level="WARNING") as log:
            await self.zone_manager._check_presence_in_zone(
                zone_entity_id, tracking_entities
            )

        # assert
        self.assertIn(f"Zone entity ID {zone_entity_id} does not exist.", log.output[0])

    # -----------------------------------------------
    # Service tests
    # -----------------------------------------------
    async def test_select_activation_zone(self):
        # arrange
        mock_call = MagicMock()
        mock_call.context.user_id = None
        mock_call.data = {"zone_entity_id": "zone.home"}

        mock_setup_device_trackers = AsyncMock()
        with patch.object(
            ZoneManager, "_setup_device_trackers", mock_setup_device_trackers
        ):
            # act
            await self.zone_manager.select_activation_zone(mock_call)

        # assert
        mock_setup_device_trackers.assert_awaited_once()
        self.assertEqual(self.zone_manager._data["active_zone"], "zone.home")

    async def test_select_activation_zone_no_zone_entity_id(self):
        # arrange
        mock_call = MagicMock()
        mock_call.context.user_id = None
        mock_call.data = {}

        # act
        with self.assertLogs(level="WARNING") as log:
            await self.zone_manager.select_activation_zone(mock_call)

        # assert
        self.assertIn("No zone entity ID provided.", log.output[0])

    async def test_select_activation_zone_zone_does_not_exist(self):
        # arrange
        mock_call = MagicMock()
        mock_call.context.user_id = None
        mock_call.data = {"zone_entity_id": "zone.non_existent"}

        self.mock_hass.states.get.return_value = None

        # act
        with self.assertLogs(level="WARNING") as log:
            await self.zone_manager.select_activation_zone(mock_call)

        # assert
        self.assertIn("Zone entity ID zone.non_existent does not exist.", log.output[0])
