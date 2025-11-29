import asyncio

from metaboutique import build, data


def main():
    asyncio.run(data.fetch_shop_links())
