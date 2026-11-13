import cProfile
import collections
import functools
import itertools
import math
import operator
import time

from typing import Any, Iterable, Iterator, List, Sequence, Tuple


def approx_num_ops_to_sort(k: int, base: float = 2) -> float:
    return 1 if k < 2 else k * math.log(k, base)


def approx_num_ops_to_order(partition: List[Tuple[int, int]], base: float = 2) -> float:
    return sum(d * approx_num_ops_to_sort(k, base) for k, d in partition)


__log_fact_cache: List[float] = []  # __log_fact_cache[n] == log_fact(n)


def log_fact(n):
    try:
        return __log_fact_cache[n]
    except IndexError:
        pass
    while n >= len(__log_fact_cache):
        __log_fact_cache.append(math.lgamma(n + 1))
    return __log_fact_cache[n]


__log_choose_cache: List[
    List[float]
] = []  # __log_choose_cache[n][k] == log_choose(n, k)


def log_choose(n, k):
    try:
        return __log_choose_cache[n][k]
    except IndexError:
        pass
    while n >= len(__log_choose_cache):
        __log_choose_cache.append([])
    __log_choose_cache_n = __log_choose_cache[n]
    while k >= len(__log_choose_cache_n):
        sub_k = len(__log_choose_cache_n)
        __log_choose_cache_n.append(log_fact(n) - log_fact(n - sub_k) - log_fact(sub_k))
    return __log_choose_cache[n][k]


def _descending_partitions(
    num_elements: int,
    num_buckets: int,
    max_in_cur_bucket: int,
    partition_so_far: List[Tuple[int, int]],
    log_num_partitions: float,
) -> Iterator[Tuple[List[Tuple[int, int]], float]]:
    """Yields all partitions in descending order with num_elements in num_buckets such that every bucket has
    max_in_cur_bucket or fewer elements.
    """
    if num_buckets == 0:
        assert num_elements == 0
        yield partition_so_far, log_num_partitions
        return
    if max_in_cur_bucket == 0:
        partition_so_far.append((0, num_buckets))
        yield partition_so_far, log_num_partitions
        partition_so_far.pop()
        return
    # min_in_cur_bucket is the fewest number of elements we can have in our current bucket such that it is still
    # possible to put num_elements elements in num_buckets.
    min_in_cur_bucket = (num_elements + num_buckets - 1) // num_buckets
    for num_in_cur_bucket in range(min_in_cur_bucket, max_in_cur_bucket + 1):
        min_repetitions = max(
            num_elements + num_buckets - num_in_cur_bucket * num_buckets, 1
        )
        max_repetitions = num_elements // num_in_cur_bucket
        for repitions in range(min_repetitions, max_repetitions + 1):
            num_elements_remaining = num_elements - repitions * num_in_cur_bucket
            partition_so_far.append((num_in_cur_bucket, repitions))
            yield from _descending_partitions(
                num_elements_remaining,
                num_buckets - repitions,
                min(num_elements_remaining, num_in_cur_bucket - 1),
                partition_so_far,
                # We multiply the number of possible partitions we've seen so far by the number of ways we can log_choose
                # num_in_cur_bucket elements from num_elements.
                log_num_partitions
                + sum(
                    log_choose(num_elements - x * num_in_cur_bucket, num_in_cur_bucket)
                    for x in range(repitions)
                ),
            )
            partition_so_far.pop()


def partitions(
    num_elements: int, num_buckets: int
) -> Iterator[Tuple[List[Tuple[int, int]], float]]:
    for partition, log_num_duplicates in _descending_partitions(
        num_elements, num_buckets, num_elements, [], 0.0
    ):
        log_num_duplicates += log_fact(num_buckets)
        for num_in_bucket, num_buckets_with_x_elements in partition:
            log_num_duplicates -= log_fact(num_buckets_with_x_elements)
        yield partition, log_num_duplicates


def main():
    max_n = 9
    for num_elements in range(1, max_n + 1):
        num_buckets = num_elements
        bucket_counts: Dict[int, int] = collections.defaultdict(int)
        bucket_counts[0] = 0
        for partition, log_num_duplicates in partitions(num_elements, num_buckets):
            num_duplicates = int(round(math.exp(log_num_duplicates)))
            for k, num_buckets_with_k_elements in partition:
                bucket_counts[k] += num_buckets_with_k_elements * num_duplicates
        for k, num_buckets_with_k_elements in sorted(bucket_counts.items()):
            print(f"{k}: {num_buckets_with_k_elements // num_elements:<10d} ", end="")
        print()


if __name__ == "__main__":
    main()
