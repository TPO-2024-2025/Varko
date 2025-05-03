import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from custom_components.varko.const import DOMAIN
from custom_components.varko.decorators import service
from custom_components.varko.services.base_manager import BaseManager


class TestBaseManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_hass = MagicMock()

        self.mock_store = MagicMock()

        self.store_patch = patch(
            "custom_components.varko.services.base_manager.Store",
            return_value=self.mock_store,
        )
        self.store_patch.start()

        self.base_manager = BaseManager(
            module_name=DOMAIN,
            hass=self.mock_hass,
            store_key="test_store",
            data_default={},
        )

    def tearDown(self):
        self.store_patch.stop()

    async def test_should_initialize_with_default(self):
        # arrange
        self.mock_store.async_load = AsyncMock(return_value=None)

        # act
        await self.base_manager._initialize()

        # assert
        self.assertEqual(self.base_manager._data, {})

    async def test_should_initialize_with_stored_value(self):
        # arrange
        self.mock_store.async_load = AsyncMock(return_value={"key": "value"})

        # act
        await self.base_manager._initialize()

        # assert
        self.assertEqual(self.base_manager._data, {"key": "value"})

    def test_should_register_services(self):
        # arrange
        @service
        def some_service():
            pass

        setattr(self.base_manager, "some_service", some_service)

        # act
        self.base_manager._BaseManager__register_services()

        # assert
        self.mock_hass.services.async_register.assert_called_with(
            DOMAIN, "some_service", some_service
        )

    def test_should_unregister_services(self):
        # arrange
        setattr(self.base_manager, "_BaseManager__services", ["some_service"])

        # act
        self.base_manager._BaseManager__unregister_services()

        # assert
        self.mock_hass.services.async_remove.assert_called_with(DOMAIN, "some_service")
