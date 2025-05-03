import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from custom_components.varko.const import DOMAIN
from custom_components.varko.services.group_manager import GroupManager


class TestGroupManager(unittest.IsolatedAsyncioTestCase):
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
            GroupManager, "_initialize", new_callable=AsyncMock
        )
        self.mock_base_init = self.base_init_patch.start()

        self.group_manager = GroupManager(self.mock_hass)

    def tearDown(self):
        self.store_patch.stop()
        self.base_init_patch.stop()

        GroupManager.destroy()

    async def test_should_get_same_instance(self):
        # arrange
        instance1 = await GroupManager.get_instance(self.mock_hass)

        # act
        instance2 = await GroupManager.get_instance(self.mock_hass)

        # assert
        self.assertIsInstance(instance1, GroupManager)
        self.assertIs(instance1, instance2)

    async def test_destroy_instance(self):
        # arrange
        await GroupManager.get_instance(self.mock_hass)

        # act
        GroupManager.destroy()

        # assert
        self.assertIsNone(GroupManager._GroupManager__instance)

    async def test_should_add_new_member(self):
        # arrange
        self.group_manager._data = []
        call = MagicMock()
        call.data = {"person": "test_user"}
        self.group_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )
        self.group_manager._store.async_save = AsyncMock()

        # act
        await self.group_manager.add_person(call)

        # assert
        self.assertEqual(self.group_manager._data, ["test_user"])
        self.mock_store.async_save.assert_called_once_with(["test_user"])
        self.mock_hass.states.async_set.assert_called_once_with(f"{DOMAIN}.group", "1")

    async def test_should_not_add_existing_member(self):
        # arrange
        self.group_manager._data = ["test_user"]
        call = MagicMock()
        call.data = {"person": "test_user"}
        self.group_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        # act
        await self.group_manager.add_person(call)

        # assert
        self.assertEqual(self.group_manager._data, ["test_user"])

    async def test_should_remove_member(self):
        # arrange
        self.group_manager._data = ["test_user"]
        call = MagicMock()
        call.data = {"person": "test_user"}
        self.group_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )
        self.group_manager._store.async_save = AsyncMock()

        # act
        await self.group_manager.remove_person(call)

        # assert
        self.assertEqual(self.group_manager._data, [])
        self.mock_store.async_save.assert_called_once_with([])
        self.mock_hass.states.async_set.assert_called_once_with(f"{DOMAIN}.group", "0")

    async def test_should_not_remove_non_existing_member(self):
        # arrange
        self.group_manager._data = []
        call = MagicMock()
        call.data = {"person": "test_user"}
        self.group_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock()
        )

        # act
        await self.group_manager.remove_person(call)

        # assert
        self.assertEqual(self.group_manager._data, [])
