"""Python module for accessing SkyQ hub."""
import asyncio
import logging
import re
from dataclasses import dataclass, field

import aiohttp

from .const import CONNECTION_ERROR, DATA_ERROR, MAC_REGEX  # , TEST_RESPONSE

_LOGGER = logging.getLogger(__name__)

HTTP_OK = 200

ERROR = logging.ERROR
INFO = logging.INFO


class SkyQHub:
    """SkyQ_Hub is the instantiation of the SkyQ Hub."""

    def __init__(self, websession: aiohttp.ClientSession, host: str):
        """Initialize the hub."""
        self._websession = websession
        self._host = host
        self._url = f"http://{self._host}/"
        self._ssid = None
        self._mac = None
        self._ipaddr = None
        self._connection_failed = False
        self._dataparse_failed = False
        self._success_init = False
        self._available = False

    @property
    def available(self):
        """Return ssid."""
        return self._available

    @property
    def ssid(self):
        """Return ssid."""
        return self._ssid

    @property
    def success_init(self):
        """Return sucess_status."""
        return self._success_init

    @property
    def wan_ip(self):
        """Return wan ip address."""
        return self._ipaddr

    @property
    def wan_mac(self):
        """Return wan mac address."""
        return self._mac

    @property
    def url(self):
        """Return host url."""
        return self._url

    async def async_connect(self):
        """Test the router is accessible."""
        devices = await self.async_get_skyhub_data()
        self._success_init = devices is not None

    async def async_get_skyhub_data(self):
        """Retrieve data from Sky Hub and return parsed result."""
        parseddata = None
        self._available = False
        try:
            async with getattr(self._websession, "get")(
                self._url,
            ) as response:
                if response.status == HTTP_OK:
                    self._available = True
                    if self._connection_failed:
                        self._log_message(
                            "Connection restored to router",
                            unset_error=True,
                            level=INFO,
                            error_type=CONNECTION_ERROR,
                        )
                    responsedata = await response.text()
                    # responsedata = TEST_RESPONSE
                    parseddata, ssid, ipaddr, mac = _parse_skyhub_response(responsedata)
                    if self._dataparse_failed:
                        self._log_message(
                            "Response data from Sky Hub corrected",
                            unset_error=True,
                            level=INFO,
                            error_type=DATA_ERROR,
                        )
                    else:
                        self._ssid = ssid
                        self._mac = mac
                        self._ipaddr = ipaddr
                    return parseddata

        except asyncio.TimeoutError:
            self._log_message(
                "Connection to the router timed out",
                level=ERROR,
                error_type=CONNECTION_ERROR,
            )
            return
        except aiohttp.client_exceptions.ClientConnectorError as err:
            self._log_message(
                f"Connection to the router failed: {err}",
                level=ERROR,
                error_type=CONNECTION_ERROR,
            )
            return
        except (OSError, RuntimeError) as err:
            message = (
                f"Invalid response from Sky Hub: {err}"
                if self.success_init
                else f"Error parsing data at startup for {self._host}, is this a Sky Router?"
            )

            self._log_message(
                message,
                level=ERROR,
                error_type=DATA_ERROR,
            )
            return

    def _log_message(
        self, log_message, unset_error=False, level=ERROR, error_type=None
    ):
        if error_type == CONNECTION_ERROR:
            if self._connection_failed and not unset_error:
                _LOGGER.debug(log_message)
                return
            self._connection_failed = not unset_error
        if error_type == DATA_ERROR:
            if self._dataparse_failed and not unset_error:
                _LOGGER.debug(log_message)
                return
            self._dataparse_failed = not unset_error
        if level == ERROR:
            _LOGGER.error(log_message)
        if level == INFO:
            _LOGGER.info(log_message)
        return


@dataclass
class _Device:
    mac: str = field(init=True, repr=True, compare=True)
    name: str = field(init=True, repr=True, compare=True)
    connection: str = field(init=True, repr=True, compare=True)

    def asdict(self):
        """Convert to dictionary."""
        return {"mac": self.mac, "connection": self.connection}


def _parse_skyhub_response(data_str):
    """Parse the Sky Hub data format."""
    pattmatch = re.search("attach_dev = '(.*)'", data_str)
    if pattmatch is None:
        raise OSError(
            "Error: Impossible to fetch data from Sky Hub. Try to reboot the router."
        )
    patt = pattmatch.group(1)

    dev = [patt1.split(",") for patt1 in patt.split("<lf>")]

    devices = []
    for dvc in dev:
        if not MAC_REGEX.match(dvc[1]):
            raise RuntimeError(f"Error: MAC address {dvc[1]} not in correct format.")

        mac = dvc[1]
        name = dvc[0]
        connection = dvc[2]
        devices.append(_Device(mac, name, connection))
    ssid = re.search("sky_WirelessAllSSIDs = '(.*)'", data_str).group(1)
    wanmatch = re.search("wanDslLinkConfig = '(.*)'", data_str).group(1).split("_")
    ipaddr = wanmatch[5]
    mac = wanmatch[6]
    return devices, ssid, ipaddr, mac
