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
        self.websession = websession
        self.host = host
        self.url = f"http://{self.host}/"
        self._connection_failed = False
        self._dataparse_failed = False
        self.success_init = False

    async def async_connect(self):
        """Test the router is accessible."""
        data = await self.async_get_skyhub_data()
        self.success_init = data is not None

    async def async_get_skyhub_data(self):
        """Retrieve data from Sky Hub and return parsed result."""
        parseddata = None
        try:
            async with getattr(self.websession, "get")(
                self.url,
            ) as response:
                if response.status == HTTP_OK:
                    if self._connection_failed:
                        self._log_message(
                            "Connection restored to router",
                            unset_error=True,
                            level=INFO,
                            error_type=CONNECTION_ERROR,
                        )
                    responsedata = await response.text()
                    # responsedata = TEST_RESPONSE
                    parseddata = await self._async_parse_skyhub_response(responsedata)
                    if self._dataparse_failed:
                        self._log_message(
                            "Response data from Sky Hub corrected",
                            unset_error=True,
                            level=INFO,
                            error_type=DATA_ERROR,
                        )
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
            if not self.success_init:
                message = f"Error parsing data at startup for {self.host}, is this a Sky Router?"
            else:
                message = f"Invalid response from Sky Hub: {err}"
            self._log_message(
                message,
                level=ERROR,
                error_type=DATA_ERROR,
            )
            return

    async def _async_parse_skyhub_response(self, data_str):
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
                raise RuntimeError(
                    f"Error: MAC address {dvc[1]} not in correct format."
                )

            mac = dvc[1]
            name = dvc[0]
            connection = dvc[2]
            devices.append(_Device(mac, name, connection))
        return devices

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
        return {"mac": self.mac}
