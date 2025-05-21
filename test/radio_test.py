import os
import sys
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import asyncio
import socket
import aiohttp

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from custom_components.varko.radio import RadioBrowserAPI
from custom_components.varko.const import DOMAIN


class TestRadio(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_hass = MagicMock()
        self.mock_logger = MagicMock()

        self.init_patch = patch.object(
            RadioBrowserAPI, "_initialize", new_callable=AsyncMock
        )
        self.mock_init = self.init_patch.start()

        self.radio_browser_api = RadioBrowserAPI(self.mock_hass)

    async def asyncTearDown(self):
        self.init_patch.stop()
        await RadioBrowserAPI.destroy()

    # ----------------------------------------------
    # Initialization and singleton tests
    # ----------------------------------------------

    async def test_should_get_same_instance(self):
        # arrange
        instance1 = await RadioBrowserAPI.get_instance(self.mock_hass)

        # act
        instance2 = await RadioBrowserAPI.get_instance(self.mock_hass)

        # assert
        self.assertIsInstance(instance1, RadioBrowserAPI)
        self.assertIs(instance1, instance2)

    async def test_destroy_instance(self):
        # arrange
        await RadioBrowserAPI.get_instance(self.mock_hass)

        # act
        await RadioBrowserAPI.destroy()

        # assert
        self.assertIsNone(RadioBrowserAPI._RadioBrowserAPI__instance)

    async def test_default_values_initialization(self):
        # arrange
        await self.radio_browser_api._initialize()

        # assert
        self.assertEqual(self.radio_browser_api.base_urls, [])
        self.assertIsNone(self.radio_browser_api.session)

    async def test_setup(self):
        # arrange
        await self.radio_browser_api._initialize()

        # act
        await self.radio_browser_api._setup()

        # assert
        self.assertIsNotNone(self.radio_browser_api.session)
        self.assertGreater(len(self.radio_browser_api.base_urls), 0)
        await self.radio_browser_api._cleanup()

    async def test_cleanup(self):
        # arrange
        await self.radio_browser_api._initialize()
        await self.radio_browser_api._setup()

        # act
        await self.radio_browser_api._cleanup()

        # assert
        self.assertIsNone(self.radio_browser_api.session)

    async def test_get_radiobrowser_base_urls_success(self):
        # arrange
        mock_event_loop = MagicMock()
        getaddrinfo_result = [
            (None, None, None, None, ("192.168.1.1", 80)),
            (None, None, None, None, ("192.168.1.2", 80)),
        ]

        with patch.object(asyncio, "get_event_loop", return_value=mock_event_loop):
            mock_event_loop.getaddrinfo = AsyncMock(return_value=getaddrinfo_result)
            with patch.object(
                socket,
                "gethostbyaddr",
                side_effect=[
                    ("de1.api.radio-browser.info", [], []),
                    ("de2.api.radio-browser.info", [], []),
                ],
            ):

                # act
                result = await self.radio_browser_api._get_radiobrowser_base_urls()

            # assert
            self.assertEqual(
                result,
                [
                    "https://de1.api.radio-browser.info",
                    "https://de2.api.radio-browser.info",
                ],
            )

    async def test_get_radiobrowser_base_urls_dns_fail(self):
        # arrange
        mock_event_loop = MagicMock()

        with patch.object(asyncio, "get_event_loop", return_value=mock_event_loop):
            mock_event_loop.getaddrinfo.side_effect = Exception("DNS lookup failed")

            # act
            result = await self.radio_browser_api._get_radiobrowser_base_urls()

        # assert
        self.assertEqual(
            result,
            ["https://de1.api.radio-browser.info"],
        )

    async def test_fetch_json_success(self):
        # arrange
        self.radio_browser_api.session = aiohttp.ClientSession()
        self.radio_browser_api.base_urls = ["https://de1.api.radio-browser.info"]

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"station": "test"})

        with patch.object(self.radio_browser_api.session, "get") as mock_get:
            mock_get.return_value.__aenter__.return_value = mock_response

            # act
            result = await self.radio_browser_api._fetch_json("/json/stations")

        # assert
        self.assertEqual(result, {"station": "test"})
        await self.radio_browser_api.session.close()

    async def test_fetch_json_non_200_status(self):
        # arrange
        self.radio_browser_api.session = aiohttp.ClientSession()
        self.radio_browser_api.base_urls = ["https://de1.api.radio-browser.info"]

        mock_response = AsyncMock()
        mock_response.status = 404
        mock_response.json = AsyncMock(return_value={"error": "Not Found"})

        with patch.object(self.radio_browser_api.session, "get") as mock_get:
            mock_get.return_value.__aenter__.return_value = mock_response

            # act
            result = await self.radio_browser_api._fetch_json("/json/stations")

        # assert
        self.assertEqual(result, {})

        await self.radio_browser_api.session.close()

    async def test_fetch_json_raises_exception(self):
        # arrange
        self.radio_browser_api.session = aiohttp.ClientSession()
        self.radio_browser_api.base_urls = ["https://de1.api.radio-browser.info"]

        with patch.object(
            self.radio_browser_api.session,
            "get",
            side_effect=Exception("Connection error"),
        ):

            # act
            result = await self.radio_browser_api._fetch_json("/json/stations")

        # assert
        self.assertEqual(result, {})

        await self.radio_browser_api.session.close()

    async def test_get_station_uuid_success(self):
        # arrange
        stations = [
            {
                "stationuuid": "12345",
                "name": "Test Station",
                "countrycode": "DE",
            }
        ]

        self.radio_browser_api._fetch_json = AsyncMock(return_value=stations)

        # act
        result = await self.radio_browser_api.get_station_uuid("Test Station", "DE")

        # assert
        self.assertEqual(result, "12345")
        self.radio_browser_api._fetch_json.assert_called_once_with(
            "/json/stations/search", {"name": "Test Station", "countrycode": "DE"}
        )

    async def test_get_station_uuid_stations_none(self):
        # arrange
        self.radio_browser_api._fetch_json = AsyncMock(return_value=None)

        # act
        result = await self.radio_browser_api.get_station_uuid("Test Station", "DE")

        # assert
        self.assertIsNone(result)
        self.radio_browser_api._fetch_json.assert_called_once_with(
            "/json/stations/search", {"name": "Test Station", "countrycode": "DE"}
        )

    async def test_get_station_uuid_stations_empty_list(self):
        # arrange
        self.radio_browser_api._fetch_json = AsyncMock(return_value=[])

        # act
        result = await self.radio_browser_api.get_station_uuid("Test Station", "DE")

        # assert
        self.assertIsNone(result)
        self.radio_browser_api._fetch_json.assert_called_once_with(
            "/json/stations/search", {"name": "Test Station", "countrycode": "DE"}
        )

    async def test_get_station_uuid_stations_not_a_list(self):
        # arrange
        self.radio_browser_api._fetch_json = AsyncMock(return_value={})

        # act
        result = await self.radio_browser_api.get_station_uuid("Test Station", "DE")

        # assert
        self.assertIsNone(result)
        self.radio_browser_api._fetch_json.assert_called_once_with(
            "/json/stations/search", {"name": "Test Station", "countrycode": "DE"}
        )

    async def test_get_list_of_stations_per_country_success(self):
        # arrange
        mock_call = MagicMock()
        mock_call.context.user_id = None
        mock_call.data = {"radio_country_code": "SI"}

        mock_stations = [
            {"name": "Radio 1", "countrycode": "SI"},
            {"name": "Radio Aktual", "countrycode": "SI"},
        ]

        self.radio_browser_api._fetch_json = AsyncMock(return_value=mock_stations)

        # act
        result = await self.radio_browser_api.get_list_of_stations_per_country(
            mock_call
        )

        # assert
        self.assertEqual(result, ["Radio 1", "Radio Aktual"])
        self.radio_browser_api._hass.bus.async_fire.assert_called_once_with(
            "varko.radio_stations_list",
            {
                "country_code": "SI",
                "stations": ["Radio 1", "Radio Aktual"],
            },
        )

    async def test_get_list_of_stations_per_country_no_stations(self):
        # arrange
        mock_call = MagicMock()
        mock_call.context.user_id = None
        mock_call.data = {"radio_country_code": "SI"}

        self.radio_browser_api._fetch_json = AsyncMock(return_value=[])

        # act
        result = await self.radio_browser_api.get_list_of_stations_per_country(
            mock_call
        )

        # assert
        self.assertEqual(result, [])
        self.radio_browser_api._hass.bus.async_fire.assert_not_called()

    async def test_get_list_of_stations_per_country_stations_not_a_list(self):
        # arrange
        mock_call = MagicMock()
        mock_call.context.user_id = None
        mock_call.data = {"radio_country_code": "SI"}

        self.radio_browser_api._fetch_json = AsyncMock(return_value={})

        # act
        result = await self.radio_browser_api.get_list_of_stations_per_country(
            mock_call
        )

        # assert
        self.assertEqual(result, [])
        self.radio_browser_api._hass.bus.async_fire.assert_not_called()
