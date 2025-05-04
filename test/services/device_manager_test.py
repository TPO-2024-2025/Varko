import unittest
from unittest.mock import MagicMock, patch, AsyncMock

from homeassistant.helpers.entity_registry import RegistryEntry

from custom_components.varko.services.device_manager import DeviceManager
from custom_components.varko.const import DOMAIN
from custom_components.varko.light import VarkoLight


class TestDeviceManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_hass = MagicMock()
        self.mock_store = MagicMock()
        self.mock_logger = MagicMock()

        self.store_patch = patch(
            "custom_components.varko.services.base_manager.Store",
            return_value=self.mock_store,
        )

        self.store_patch.start()

        self.base_init_patch = patch.object(
            DeviceManager, "_initialize", new_callable=AsyncMock
        )
        self.mock_base_init = self.base_init_patch.start()

        self.device_manager = DeviceManager(self.mock_hass)

    def tearDown(self):
        self.store_patch.stop()
        self.base_init_patch.stop()

        DeviceManager.destroy()

    async def test_should_get_same_instance(self):
        # arrange
        instance1 = await DeviceManager.get_instance(self.mock_hass)

        # act
        instance2 = await DeviceManager.get_instance(self.mock_hass)

        # assert
        self.assertIsInstance(instance1, DeviceManager)
        self.assertIs(instance1, instance2)

    async def test_destroy_instance(self):
        # arrange
        await DeviceManager.get_instance(self.mock_hass)

        # act
        DeviceManager.destroy()

        # assert
        self.assertIsNone(DeviceManager._DeviceManager__instance)

    async def test_should_add_existing_device(self):
        # ---------------- Arrange ----------------

        # Mock service call with device data
        call = MagicMock()
        call.data = {
            "device_id": "fcf4b2",
            "device_type": "light",
            "device_name": "myLight",
            "is_enabled": True,
            "entity": "light.light",
        }

        # Allow access through auth check
        self.device_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        # Mock configuration entry and its devices
        mock_entry = MagicMock()
        entry_id = "mock_entry_id"
        mock_entry.entry_id = entry_id
        mock_entry.data = {"devices": []}
        self.device_manager._hass.config_entries.async_entries.return_value = [
            mock_entry
        ]

        # Prepare hass.data structure for the domain
        self.device_manager._hass.data = {DOMAIN: {entry_id: {"devices": []}}}

        # Mock store
        self.device_manager._store.async_save = AsyncMock()

        # ---------------- Act ----------------

        await self.device_manager.add_device(call)

        # ---------------- Assert ----------------

        # Check internal state updated
        self.assertEqual(len(self.device_manager._data), 1)

        # Check store saved
        self.mock_store.async_save.assert_called_once()

        # Check config entry updated
        self.assertEqual(mock_entry.data["devices"][0]["device_id"], "fcf4b2")

        # Check hass.data updated
        hass_devices = self.device_manager._hass.data[DOMAIN][entry_id]["devices"]
        self.assertEqual(len(hass_devices), 1)
        self.assertEqual(hass_devices[0]["device_id"], "fcf4b2")

    async def test_should_add_new_device(self):
        # ---------------- Arrange ----------------

        # Mock service call with device data without entity field
        call = MagicMock()
        call.data = {
            "device_id": "fcf4b2",
            "device_type": "light",
            "device_name": "myLight",
            "is_enabled": True,
        }

        # Allow access through auth check
        self.device_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        # Mock configuration entry and its devices
        mock_entry = MagicMock()
        entry_id = "mock_entry_id"
        mock_entry.entry_id = entry_id
        mock_entry.data = {"devices": []}
        self.device_manager._hass.config_entries.async_entries.return_value = [
            mock_entry
        ]

        # Prepare hass.data structure for the domain
        self.device_manager._hass.data = {DOMAIN: {entry_id: {"devices": []}}}

        # Mock persistence layer
        self.device_manager._store.async_save = AsyncMock()

        # Mock platforms
        mock_platform = MagicMock()
        mock_platform.domain = "light"
        mock_platform.async_add_entities = AsyncMock()

        # ---------------- Act ----------------

        with patch(
            "custom_components.varko.services.device_manager.async_get_platforms",
            return_value=[mock_platform],
        ):
            await self.device_manager.add_device(call)

        # ---------------- Assert ----------------

        # Check that async_add_entities was called once with a VarkoLight instance
        mock_platform.async_add_entities.assert_called_once()
        added_entities = mock_platform.async_add_entities.call_args[0][0]
        self.assertEqual(len(added_entities), 1)
        self.assertIsInstance(added_entities[0], VarkoLight)
        self.assertEqual(added_entities[0].unique_id, "fcf4b2")
        self.assertEqual(added_entities[0].name, "myLight")

    async def test_should_not_add_device_with_existing_device_id(self):
        # ---------------- Arrange ----------------

        # Mock service call with device data
        call = MagicMock()
        call.data = {
            "device_id": "fcf4b2",
            "device_type": "light",
            "device_name": "myLight",
            "is_enabled": True,
        }

        # Allow access through auth check
        self.device_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        # Mock configuration entry with an existing device
        mock_entry = MagicMock()
        entry_id = "mock_entry_id"
        mock_entry.entry_id = entry_id
        mock_entry.data = {
            "devices": [
                {
                    "device_id": "fcf4b2",  # Already exists
                    "device_type": "light",
                    "device_name": "myLight",
                    "is_enabled": True,
                }
            ]
        }
        self.device_manager._hass.config_entries.async_entries.return_value = [
            mock_entry
        ]

        # Prepare hass.data structure with existing device
        self.device_manager._hass.data = {
            DOMAIN: {entry_id: {"devices": [mock_entry.data["devices"][0]]}}
        }

        # Store also includes the device
        self.device_manager._data = [mock_entry.data["devices"][0]]
        # Mock persistence layer
        self.device_manager._store.async_save = AsyncMock()

        # ---------------- Act ----------------

        await self.device_manager.add_device(call)

        # ---------------- Assert ----------------

        # Ensure no new device was added
        self.assertEqual(len(self.device_manager._data), 1)

        # async_save should NOT be called
        self.mock_store.async_save.assert_not_called()

        # Ensure hass.data still only has one device
        hass_devices = self.device_manager._hass.data[DOMAIN][entry_id]["devices"]
        self.assertEqual(len(hass_devices), 1)
        self.assertEqual(hass_devices[0]["device_id"], "fcf4b2")

    async def test_should_not_add_device_with_existing_entity_id(self):
        # ---------------- Arrange ----------------

        # Mock service call with device data
        call = MagicMock()
        call.data = {
            "device_id": "fcf4b2",
            "device_type": "light",
            "device_name": "myLight",
            "is_enabled": True,
            "entity": "light.light",
        }

        # Allow access through auth check
        self.device_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        # Mock configuration entry with an existing device
        mock_entry = MagicMock()
        entry_id = "mock_entry_id"
        mock_entry.entry_id = entry_id
        mock_entry.data = {
            "devices": [
                {
                    "device_id": "abcd",
                    "device_type": "light",
                    "device_name": "myLight",
                    "is_enabled": True,
                    "entity_id": "light.light",  # Already exists
                }
            ]
        }
        self.device_manager._hass.config_entries.async_entries.return_value = [
            mock_entry
        ]

        # Prepare hass.data structure with existing device
        self.device_manager._hass.data = {
            DOMAIN: {entry_id: {"devices": [mock_entry.data["devices"][0]]}}
        }

        # Store also includes the device
        self.device_manager._data = [mock_entry.data["devices"][0]]
        # Mock persistence layer
        self.device_manager._store.async_save = AsyncMock()

        # ---------------- Act ----------------

        await self.device_manager.add_device(call)

        # ---------------- Assert ----------------

        # Ensure no new device was added
        self.assertEqual(len(self.device_manager._data), 1)

        # async_save should NOT be called
        self.mock_store.async_save.assert_not_called()

        # Ensure hass.data still only has one device
        hass_devices = self.device_manager._hass.data[DOMAIN][entry_id]["devices"]
        self.assertEqual(len(hass_devices), 1)
        self.assertEqual(hass_devices[0]["entity_id"], "light.light")

    async def test_should_remove_existing_device(self):
        # ---------------- Arrange ----------------
        # Setup mock device data
        device_id = "abc123"
        entity_id = "light.test_light"
        device_name = "Test Light"

        # Device entry in internal _data
        device = {
            "device_id": device_id,
            "device_name": device_name,
        }

        # Set up the service call
        call = MagicMock()
        call.data = {"entity": entity_id}

        # Setup DeviceManager state
        self.device_manager._data = [device]
        self.device_manager._store.async_save = AsyncMock()
        # Allow access through auth check
        self.device_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )
        # Mock config entry
        mock_entry = MagicMock()
        entry_id = "mock_entry_id"
        mock_entry.entry_id = entry_id
        mock_entry.data = {"devices": [device]}
        self.device_manager._hass.config_entries.async_entries = MagicMock(
            return_value=[mock_entry]
        )
        self.device_manager._hass.config_entries.async_update_entry = MagicMock()

        # Setup hass.data structure
        self.device_manager._hass.data = {DOMAIN: {entry_id: {"devices": [device]}}}

        # Patch entity registry
        mock_registry = MagicMock()
        mock_entity_entry = RegistryEntry(
            entity_id=entity_id,
            unique_id=device_id,
            platform="varko",
            config_entry_id=entry_id,
        )
        mock_registry.async_get.return_value = mock_entity_entry
        mock_registry.async_get_entity_id.return_value = entity_id
        mock_registry.async_remove = MagicMock()

        with patch(
            "custom_components.varko.services.device_manager.async_get_entity_registry",
            return_value=mock_registry,
        ):
            # ---------------- Act ----------------
            await self.device_manager.remove_device(call)

        # ---------------- Assert ----------------
        # _data should be empty now
        self.assertEqual(len(self.device_manager._data), 0)

        # Data saved
        self.device_manager._store.async_save.assert_awaited_once_with([])

        # Config entry updated
        self.device_manager._hass.config_entries.async_update_entry.assert_called_once()
        updated_data = (
            self.device_manager._hass.config_entries.async_update_entry.call_args[1][
                "data"
            ]
        )
        self.assertEqual(updated_data["devices"], [])

        # Entity was removed
        mock_registry.async_remove.assert_called_once_with(entity_id)

    async def test_should_remove_device_linked_to_existing_entity(self):
        # ---------------- Arrange ----------------
        # Setup mock device data
        device_id = "abc123"
        entity_id = "light.test_light"
        device_name = "Linked Light"

        # Device entry WITH an entity_id
        device = {
            "device_id": device_id,
            "device_name": device_name,
            "entity_id": entity_id,
        }

        # Set up the service call
        call = MagicMock()
        call.data = {"entity": entity_id}

        # Setup DeviceManager state
        self.device_manager._data = [device]
        self.device_manager._store.async_save = AsyncMock()
        self.device_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        # Mock config entry
        mock_entry = MagicMock()
        entry_id = "mock_entry_id"
        mock_entry.entry_id = entry_id
        mock_entry.data = {"devices": [device]}
        self.device_manager._hass.config_entries.async_entries = MagicMock(
            return_value=[mock_entry]
        )
        self.device_manager._hass.config_entries.async_update_entry = MagicMock()

        # Setup hass.data structure
        self.device_manager._hass.data = {DOMAIN: {entry_id: {"devices": [device]}}}

        # Patch entity registry
        mock_registry = MagicMock()
        mock_entity_entry = RegistryEntry(
            entity_id=entity_id,
            unique_id=device_id,
            platform="varko",
            config_entry_id=entry_id,
        )
        mock_registry.async_get.return_value = mock_entity_entry
        mock_registry.async_remove = MagicMock()

        with patch(
            "custom_components.varko.services.device_manager.async_get_entity_registry",
            return_value=mock_registry,
        ):
            # ---------------- Act ----------------
            await self.device_manager.remove_device(call)

        # ---------------- Assert ----------------
        # _data should be empty now
        self.assertEqual(len(self.device_manager._data), 0)

        # Data saved
        self.device_manager._store.async_save.assert_awaited_once_with([])

        # Config entry updated
        self.device_manager._hass.config_entries.async_update_entry.assert_called_once()
        updated_data = (
            self.device_manager._hass.config_entries.async_update_entry.call_args[1][
                "data"
            ]
        )
        self.assertEqual(updated_data["devices"], [])

        # Entity should NOT be removed
        mock_registry.async_remove.assert_not_called()

    async def test_should_enable_disabled_device(self):
        # ---------------- Arrange ----------------
        device_id = "abc123"
        entity_id = "light.test_light"
        device_name = "Disabled Light"

        # Device is initially disabled
        device = {
            "device_id": device_id,
            "device_name": device_name,
            "is_enabled": False,
            "entity_id": entity_id,
        }

        call = MagicMock()
        call.data = {"entity": entity_id}

        self.device_manager._data = [device]
        self.device_manager._store.async_save = AsyncMock()
        self.device_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        mock_entry = MagicMock()
        entry_id = "mock_entry_id"
        mock_entry.entry_id = entry_id
        mock_entry.data = {"devices": [device]}
        self.device_manager._hass.config_entries.async_entries = MagicMock(
            return_value=[mock_entry]
        )
        self.device_manager._hass.config_entries.async_update_entry = MagicMock()

        self.device_manager._hass.data = {DOMAIN: {entry_id: {"devices": [device]}}}

        mock_registry = MagicMock()
        mock_entity_entry = RegistryEntry(
            entity_id=entity_id,
            unique_id=device_id,
            platform="varko",
            config_entry_id=entry_id,
        )
        mock_registry.async_get.return_value = mock_entity_entry

        with patch(
            "custom_components.varko.services.device_manager.async_get_entity_registry",
            return_value=mock_registry,
        ):
            # ---------------- Act ----------------
            await self.device_manager.enable_device(call)

        # ---------------- Assert ----------------
        # Device in _data should be enabled
        self.assertTrue(self.device_manager._data[0]["is_enabled"])

        # Device in config entry should be enabled
        updated_devices = (
            self.device_manager._hass.config_entries.async_update_entry.call_args[1][
                "data"
            ]["devices"]
        )
        self.assertTrue(updated_devices[0]["is_enabled"])

        # Device in hass.data should be enabled
        self.assertTrue(
            self.device_manager._hass.data[DOMAIN][entry_id]["devices"][0]["is_enabled"]
        )

        # Data saved
        self.device_manager._store.async_save.assert_awaited_once()

    async def test_should_not_enable_already_enabled_device(self):
        # ---------------- Arrange ----------------
        device_id = "abc123"
        entity_id = "light.test_light"
        device_name = "Already Enabled Light"

        # Device is already enabled
        device = {
            "device_id": device_id,
            "device_name": device_name,
            "is_enabled": True,
            "entity_id": entity_id,
        }

        call = MagicMock()
        call.data = {"entity": entity_id}

        self.device_manager._data = [device]
        self.device_manager._store.async_save = AsyncMock()
        self.device_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        mock_entry = MagicMock()
        entry_id = "mock_entry_id"
        mock_entry.entry_id = entry_id
        mock_entry.data = {"devices": [device.copy()]}
        self.device_manager._hass.config_entries.async_entries = MagicMock(
            return_value=[mock_entry]
        )
        self.device_manager._hass.config_entries.async_update_entry = MagicMock()

        self.device_manager._hass.data = {
            DOMAIN: {entry_id: {"devices": [device.copy()]}}
        }

        mock_registry = MagicMock()
        mock_entity_entry = RegistryEntry(
            entity_id=entity_id,
            unique_id=device_id,
            platform="varko",
            config_entry_id=entry_id,
        )
        mock_registry.async_get.return_value = mock_entity_entry

        with patch(
            "custom_components.varko.services.device_manager.async_get_entity_registry",
            return_value=mock_registry,
        ):
            # ---------------- Act ----------------
            await self.device_manager.enable_device(call)

        # ---------------- Assert ----------------
        # No update should have occurred
        self.device_manager._hass.config_entries.async_update_entry.assert_not_called()
        self.device_manager._store.async_save.assert_not_awaited()

        # is_enabled should still be True
        self.assertTrue(self.device_manager._data[0]["is_enabled"])

    async def test_should_disable_enabled_device(self):
        # ---------------- Arrange ----------------
        device_id = "abc123"
        entity_id = "light.test_light"
        device_name = "Disabled Light"

        # Device is initially enabled
        device = {
            "device_id": device_id,
            "device_name": device_name,
            "is_enabled": True,
            "entity_id": entity_id,
        }

        call = MagicMock()
        call.data = {"entity": entity_id}

        self.device_manager._data = [device]
        self.device_manager._store.async_save = AsyncMock()
        self.device_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        mock_entry = MagicMock()
        entry_id = "mock_entry_id"
        mock_entry.entry_id = entry_id
        mock_entry.data = {"devices": [device]}
        self.device_manager._hass.config_entries.async_entries = MagicMock(
            return_value=[mock_entry]
        )
        self.device_manager._hass.config_entries.async_update_entry = MagicMock()

        self.device_manager._hass.data = {DOMAIN: {entry_id: {"devices": [device]}}}

        mock_registry = MagicMock()
        mock_entity_entry = RegistryEntry(
            entity_id=entity_id,
            unique_id=device_id,
            platform="varko",
            config_entry_id=entry_id,
        )
        mock_registry.async_get.return_value = mock_entity_entry

        with patch(
            "custom_components.varko.services.device_manager.async_get_entity_registry",
            return_value=mock_registry,
        ):
            # ---------------- Act ----------------
            await self.device_manager.disable_device(call)

        # ---------------- Assert ----------------
        # Device in _data should be disabled
        self.assertFalse(self.device_manager._data[0]["is_enabled"])

        # Device in config entry should be disabled
        updated_devices = (
            self.device_manager._hass.config_entries.async_update_entry.call_args[1][
                "data"
            ]["devices"]
        )
        self.assertFalse(updated_devices[0]["is_enabled"])

        # Device in hass.data should be disabled
        self.assertFalse(
            self.device_manager._hass.data[DOMAIN][entry_id]["devices"][0]["is_enabled"]
        )

        # Data saved
        self.device_manager._store.async_save.assert_awaited_once()

    async def test_should_not_disable_already_disabled_device(self):
        # ---------------- Arrange ----------------
        device_id = "abc123"
        entity_id = "light.test_light"
        device_name = "Already Disabled Light"

        # Device is initially disabled
        device = {
            "device_id": device_id,
            "device_name": device_name,
            "is_enabled": False,
            "entity_id": entity_id,
        }

        call = MagicMock()
        call.data = {"entity": entity_id}

        self.device_manager._data = [device]
        self.device_manager._store.async_save = AsyncMock()
        self.device_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        mock_entry = MagicMock()
        entry_id = "mock_entry_id"
        mock_entry.entry_id = entry_id
        mock_entry.data = {"devices": [device]}
        self.device_manager._hass.config_entries.async_entries = MagicMock(
            return_value=[mock_entry]
        )
        self.device_manager._hass.config_entries.async_update_entry = MagicMock()

        self.device_manager._hass.data = {
            DOMAIN: {entry_id: {"devices": [device.copy()]}}
        }

        mock_registry = MagicMock()
        mock_entity_entry = RegistryEntry(
            entity_id=entity_id,
            unique_id=device_id,
            platform="varko",
            config_entry_id=entry_id,
        )
        mock_registry.async_get.return_value = mock_entity_entry

        with patch(
            "custom_components.varko.services.device_manager.async_get_entity_registry",
            return_value=mock_registry,
        ):
            # ---------------- Act ----------------
            await self.device_manager.disable_device(call)

        # ---------------- Assert ----------------
        # State should remain unchanged
        self.assertFalse(self.device_manager._data[0]["is_enabled"])
        self.device_manager._hass.config_entries.async_update_entry.assert_not_called()
        self.device_manager._store.async_save.assert_not_awaited()

    async def test_control_device_turns_on_light(self):
        device_id = "abc123"
        entity_id = "light.test_light"

        device = {
            "device_id": device_id,
            "device_name": "Test Light",
            "is_enabled": True,
            "entity_id": entity_id,
        }

        self.device_manager._data = [device]

        # Simulate state existing
        self.device_manager._hass.states.get = MagicMock(return_value=MagicMock())

        # Mock service call
        self.device_manager._hass.services.async_call = AsyncMock()

        await self.device_manager.control_device(device_id, "on")

        self.device_manager._hass.services.async_call.assert_awaited_once_with(
            "light", "turn_on", {"entity_id": entity_id}, blocking=True
        )

    async def test_control_device_turns_off_light(self):
        device_id = "abc123"
        entity_id = "light.test_light"

        device = {
            "device_id": device_id,
            "device_name": "Test Light",
            "is_enabled": True,
            "entity_id": entity_id,
        }

        self.device_manager._data = [device]
        self.device_manager._hass.states.get = MagicMock(return_value=MagicMock())
        self.device_manager._hass.services.async_call = AsyncMock()

        await self.device_manager.control_device(device_id, "off")

        self.device_manager._hass.services.async_call.assert_awaited_once_with(
            "light", "turn_off", {"entity_id": entity_id}, blocking=True
        )

    async def test_control_device_device_not_found(self):
        device_id = "missing123"

        self.device_manager._data = []  # No devices in the store

        # Patch logger to capture logs
        with patch.object(self.device_manager._logger, "error") as mock_log:
            # Mock service call to ensure it's NOT called
            self.device_manager._hass.services.async_call = AsyncMock()

            await self.device_manager.control_device(device_id, "on")

            # Assert async_call was not made
            self.device_manager._hass.services.async_call.assert_not_awaited()

            # Assert the correct error was logged
            mock_log.assert_called_once_with(
                "Device missing123 not found in store data"
            )
