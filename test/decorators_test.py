import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from custom_components.varko.decorators import service
from custom_components.varko.decorators import admin


class ServiceTest(unittest.TestCase):
    def test_should_add_is_service_attribute(self):
        # arrange
        @service
        def mock_handler():
            pass

        # act & assert
        self.assertTrue(hasattr(mock_handler, "_is_service"))
        self.assertTrue(getattr(mock_handler, "_is_service"))


class AdminTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_allow_internal_call(self):
        # arrange
        mock_call = MagicMock()
        mock_call.context.user_id = None

        @admin
        async def mock_handler(self, call):
            return "success"

        # act
        result = await mock_handler(MagicMock(), mock_call)

        # assert
        self.assertEqual(result, "success")

    async def test_should_allow_admin_call(self):
        # arrange
        mock_manager = MagicMock()
        mock_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock(is_admin=True, name="AdminUser")
        )
        mock_call = MagicMock()
        mock_call.context.user_id = "admin_user"

        @admin
        async def mock_handler(self, call):
            return "success"

        # act
        result = await mock_handler(mock_manager, mock_call)

        # assert
        self.assertEqual(result, "success")

    async def test_should_error_when_user_not_found(self):
        mock_manager = MagicMock()
        mock_manager._hass.auth.async_get_user = AsyncMock(return_value=None)
        mock_call = MagicMock()
        mock_call.context.user_id = "unknown_user"

        @admin
        async def mock_handler(self, call):
            return "success"

        with self.assertRaises(Exception) as context:
            await mock_handler(mock_manager, mock_call)

        self.assertIn("Unauthorized", str(context.exception))

    async def test_should_error_when_user_is_not_admin(self):
        mock_manager = MagicMock()
        mock_manager._hass.auth.async_get_user = AsyncMock(
            return_value=MagicMock(is_admin=False, name="RegularUser")
        )
        mock_call = MagicMock()
        mock_call.context.user_id = "regular_user"

        @admin
        async def mock_handler(self, call):
            return "success"

        with self.assertRaises(Exception) as context:
            await mock_handler(mock_manager, mock_call)

        self.assertIn("Unauthorized", str(context.exception))
