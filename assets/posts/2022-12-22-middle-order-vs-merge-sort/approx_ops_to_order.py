import collections
import functools
import itertools
import math
import operator
import time

from typing import Any, Iterable, Iterator, List, Sequence, Tuple


def approx_num_ops_to_sort(k: int) -> float:
    return 1 if k < 2 else k * math.log2(k)


def approx_num_ops_to_order(partition: List) -> float:
    return sum(approx_num_ops_to_sort(len(bucket)) for bucket in partition)


def _partitions(elements, buckets):
    if not elements:
        yield buckets
        return
    # For each bucket, place the first element in that bucket then yield all
    # partitions of remaining elements.
    for b in buckets:
        b.append(elements[0])
        yield from _partitions(elements[1:], buckets)
        b.pop()


def partitions(elements, num_buckets):
    return _partitions(elements, tuple([] for _ in range(num_buckets)))


def nice_partition_str(partition):
    return f"[[{'], ['.join(''.join(bucket) for bucket in partition)}]]"


def main():
    elements = ["A", "B", "C"]
    num_elements = len(elements)
    num_buckets = 2
    num_partitions = num_buckets ** num_elements
    for partition in partitions(elements, num_buckets):
        approx_ops = approx_num_ops_to_order(partition)
        print(
            f"{nice_partition_str(partition)} takes approximately {approx_ops} operations order."
        )
    approx_avg_ops = (
        sum(approx_num_ops_to_order(p) for p in partitions(elements, num_buckets))
        / num_partitions
    )
    print(
        f"Ordering {num_elements} elements in {num_buckets} buckets takes {approx_avg_ops} operations on average."
    )


if __name__ == "__main__":
    main()
