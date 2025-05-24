import aiohttp
import asyncio
from typing import Optional, Dict, List, Union
import socket
from homeassistant.core import HomeAssistant, ServiceCall
from custom_components.varko.decorators import service, admin
from custom_components.varko.services.base_manager import BaseManager
from custom_components.varko.const import DOMAIN


class RadioBrowserAPI(BaseManager):
    __instance = None

    def __init__(self, hass: HomeAssistant):
        super().__init__(__name__, hass, f"{DOMAIN}.radio_client", [])
        self.base_urls = []
        self.session = None

    @classmethod
    async def get_instance(cls, hass: HomeAssistant):
        if cls.__instance is None:
            cls.__instance = cls(hass)
            await cls.__instance._initialize()
            await cls.__instance._setup()
        return cls.__instance

    @classmethod
    async def destroy(cls):
        if cls.__instance is not None:
            await cls.__instance._cleanup()
            cls.__instance.__del__()
            cls.__instance = None

    async def _setup(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        self.base_urls = await self._get_radiobrowser_base_urls()

    async def _cleanup(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def _get_radiobrowser_base_urls(self) -> List[str]:
        try:
            hosts = []

            async with self.session.get(
                "https://all.api.radio-browser.info/json/servers"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    for item in data:
                        host = item.get("name")
                        if host and host not in hosts:
                            hosts.append(host)

            if not hosts:
                return ["https://de1.api.radio-browser.info"]

            hosts.sort()
            return list(map(lambda x: "https://" + x, hosts))
        except Exception as e:
            self._logger.error("DNS lookup failed: %s", e)
            return ["https://de1.api.radio-browser.info"]  # fallback

    async def _fetch_json(
        self, url: str, params: Optional[Dict] = None
    ) -> Union[Dict, List]:

        for base_url in self.base_urls:
            full_url = f"{base_url}{url}"
            try:
                async with self.session.get(
                    full_url,
                    params=params,
                    headers={"User-Agent": "HomeAssistant"},
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    self._logger.debug("Request failed: %s", response.status)
            except Exception as e:
                self._logger.debug("Request error: %s", str(e))

        self._logger.error("All API servers failed")
        return {}

    async def get_station_uuid(self, name: str, countrycode: str) -> Optional[str]:
        stations = await self._fetch_json(
            "/json/stations/search", {"name": name, "countrycode": countrycode}
        )
        if stations and isinstance(stations, list):
            return stations[0].get("stationuuid")
        return None

    @service
    @admin
    async def get_list_of_stations_per_country(self, call: ServiceCall) -> List[str]:
        countrycode = call.data.get("radio_country_code")

        stations = await self._fetch_json(
            "/json/stations/search", {"countrycode": countrycode}
        )
        if stations and isinstance(stations, list):
            station_names = [station.get("name") for station in stations]

            self._logger.debug(f"Async fire: {DOMAIN}.radio_stations_list")
            self._hass.bus.async_fire(
                f"{DOMAIN}.radio_stations_list",
                {"country_code": countrycode, "stations": station_names},
            )
            return station_names
        return []
