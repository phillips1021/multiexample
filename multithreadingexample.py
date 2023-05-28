import random, time, os, sys, requests, math
from concurrent.futures import ThreadPoolExecutor


def fetch_url_data_sync(url: str) -> None:
    try:
        requests.get(url, timeout=3)
    except Exception as e:
        print(e)


def fetch_sync(urls):
    for url in urls:
        fetch_url_data_sync(url)


def fetch_threaded(urls: list[str]) -> None:
    # Create a pool of 10 threads, only one will run at any time.
    with ThreadPoolExecutor(10) as executor:
        executor.map(fetch_url_data_sync, urls)


if __name__ == '__main__':
    # Read list of urls from text file
    urls_file: str = 'urls.txt'

    with open(urls_file, "r") as f:
        urls: list[str] = f.readlines()

    urls = [url.replace("\n", "") for url in urls]

    # Sample n urls from the list. The list contains 1 million urls
    n = 100
    urls = random.choices(urls, k=n)

    # Without multithreading
    start = time.perf_counter()
    fetch_sync(urls)
    print(time.perf_counter() - start)

    # With multithreading
    start = time.perf_counter()
    fetch_threaded(urls)
    print(time.perf_counter() - start)