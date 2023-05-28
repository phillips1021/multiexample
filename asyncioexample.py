import asyncio
import random, string, time, os, sys, requests, math
from aiohttp import ClientSession, ClientResponseError


async def fetch_url_data_async(session: ClientSession, url: str) -> None:
    # fetch url
    try:
        async with session.get(url, timeout=3) as response:
            # This is a time consuming task hence await
            await response.read()
    except Exception as e:
        print(e)


async def fetch_async(urls: list[str]):
    tasks = []
    async with ClientSession() as session:
        for url in urls:
            tasks.append(fetch_url_data_async(session, url))

        # All tasks submitted to event loop and then event loop
        # schedules these tasks
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    # Read list of urls from text file
    urls_file: str = 'urls.txt'

    with open(urls_file, "r") as f:
        urls: list[str] = f.readlines()

    urls = [url.replace("\n", "") for url in urls]

    # Sample n urls from the list. The list contains 1 million urls
    n: int = 100
    urls = random.choices(urls, k=n)

    # asyncio version
    start = time.perf_counter()
    asyncio.run(fetch_async(urls))
    print(time.perf_counter() - start)

    # normal version no asyncio or multithreading
    # start = time.perf_counter()
    # fetch_sync(urls)
    # print(time.perf_counter() - start)
    #
    # # multithreading
    # start = time.perf_counter()
    # fetch_threaded(urls)
    # print(time.perf_counter() - start)