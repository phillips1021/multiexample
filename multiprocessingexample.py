import random, os, sys, math
import time
from concurrent.futures import ProcessPoolExecutor


def square_array(arr: list[int]) -> list[int]:
    return [x ** 2 for x in arr]


def square_array_in_parallel(arr: list[int], n: int = 4, m: int = 1000) -> list[int]:
    """
    n: number of processes
    m: number of sub-arrays the array is divided into
    """

    # The original array is divided into m sub-arrays and are processed
    # in parallel.
    # batch is the size of one sub-array
    batch: int = int(math.ceil(len(arr) / m))

    with ProcessPoolExecutor(n) as executor:
        res: list[list[int]] = \
            executor.map(square_array,
                         [arr[i * batch:min((i + 1) * batch, len(arr))] for i in range(m)])

    # Merge the processed sub-arrays after finding their squares
    out: list[int] = []
    for x in res:
        out += x

    return out


if __name__ == '__main__':
    # An integer array of size 100 million with integers from 1 to 1000
    arr: list[int] = random.choices(range(1, 1000), k=100000000)

    # Without parallel processing
    start = time.perf_counter()
    square_array(arr)
    print(time.perf_counter() - start)

    # With parallel processing
    start = time.perf_counter()
    square_array_in_parallel(arr)
    print(time.perf_counter() - start)