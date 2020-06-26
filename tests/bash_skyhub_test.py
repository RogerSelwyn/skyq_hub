"""Sky Q Hub test script."""
import asyncio
import sys

import aiohttp

from pyskyqhub.skyq_hub import SkyQHub


async def main(host):
    """Run the main test process."""
    async with aiohttp.ClientSession() as session:
        skyhub = SkyQHub(session, host)

        print("-----> Initialising")
        data = await skyhub.async_connect()
        print(f"Connected succesfully: {skyhub.success_init}")

        if skyhub.success_init:
            print("-----> Getting data")
            data = await skyhub.async_get_skyhub_data()
            print(data)


asyncio.run(main(sys.argv[1]))
