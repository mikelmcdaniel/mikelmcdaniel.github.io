import collections
import functools
import itertools
import math
import operator
import time

from typing import Any, Dict, Iterable, Iterator, List, Sequence, Tuple


def approx_num_ops_to_sort(k: int) -> float:
    return 1 if k < 2 else k * math.log2(k)


def approx_num_ops_to_order(partition: List[int]) -> float:
    return sum(approx_num_ops_to_sort(k) for k in partition)


def fact(n):
    return functools.reduce(operator.mul, range(2, n + 1), 1)


def choose(n, k):
    return fact(n) // fact(n - k) // fact(k)


def _descending_partitions(
    num_elements: int,
    num_buckets: int,
    max_in_cur_bucket: int,
    partition_so_far: List[int],
    num_partitions: int,
) -> Iterator[Tuple[List[int], int]]:
    """Yields all partitions in descending order with num_elements in num_buckets such that every bucket has
    max_in_cur_bucket or fewer elements.
    """
    if num_buckets == 0:
        assert num_elements == 0
        # print(f'{num_elements=} {num_buckets=} {max_in_cur_bucket=} {partition_so_far=} {num_partitions=}')
        yield partition_so_far, num_partitions
        return
    # min_in_cur_bucket is the fewest number of elements we can have in our current bucket such that it is still
    # possible to put num_elements elements in num_buckets.
    min_in_cur_bucket = (num_elements + num_buckets - 1) // num_buckets
    for num_in_cur_bucket in range(min_in_cur_bucket, max_in_cur_bucket + 1):
        num_elements_remaining = num_elements - num_in_cur_bucket
        partition_so_far.append(num_in_cur_bucket)
        yield from _descending_partitions(
            num_elements_remaining,
            num_buckets - 1,
            min(num_elements_remaining, num_in_cur_bucket),
            partition_so_far,
            # We multiply the number of possible partitions we've seen so far by the number of ways we can choose
            # num_in_cur_bucket elements from num_elements.
            num_partitions * choose(num_elements, num_in_cur_bucket),
        )
        partition_so_far.pop()


def partitions(num_elements: int, num_buckets: int) -> Iterator[Tuple[List[int], int]]:
    for partition, num_duplicates in _descending_partitions(
        num_elements, num_buckets, num_elements, [], 1
    ):
        # Since we are are only looking at descending partitions, we need to account for all the different ways that a
        # descending partition can be reordered. For example, [3, 1] can also be [1, 3] and [2, 2] is already unique.
        # In general there are N! ways to order N elements, so we multiply by num_buckets! and divide by
        # partition.count(num_in_bucket)! to account for buckets with the same number of elements.
        num_duplicates *= fact(num_buckets)
        # bucket_counts[k] is the number of buckets that have k elements in them
        bucket_counts: Dict[int, int] = collections.defaultdict(int)
        for num_in_bucket in partition:
            bucket_counts[num_in_bucket] += 1
        for num_buckets_with_x_elements in bucket_counts.values():
            num_duplicates //= fact(num_buckets_with_x_elements)
        yield partition, num_duplicates


def main():
    num_elements = 3
    num_buckets = 2
    num_partitions = num_buckets ** num_elements
    for partition, num_duplicates in partitions(num_elements, num_buckets):
        approx_ops = approx_num_ops_to_order(partition)
        print(
            f"{partition} occurs {num_duplicates} times and takes approximately {approx_ops} operations to order."
        )
    approx_avg_ops = (
        sum(
            d * approx_num_ops_to_order(p)
            for p, d in partitions(num_elements, num_buckets)
        )
        / num_partitions
    )
    print(
        f"Ordering {num_elements} elements in {num_buckets} buckets takes {approx_avg_ops} operations on average."
    )


if __name__ == "__main__":
    main()
