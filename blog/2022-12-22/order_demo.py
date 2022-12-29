from typing import Any, Iterable, Iterator, List, Sequence


def sorted_merge(iter1: Iterable, iter2: Iterable) -> Iterator:
    # Convert any iterables to iterators. (e.g. a list to an iterator)
    iter1 = iter(iter1)
    iter2 = iter(iter2)

    # Get the first items in iter1 and iter2
    x1 = next(iter1, None)
    x2 = next(iter2, None)
    # While there are items in iter1 and iter2:
    while x1 is not None and x2 is not None:
        # Yield the smaller value between iter1 and iter2, then get the next value.
        if x1 < x2:
            yield x1
            x1 = next(iter1, None)
        else:
            yield x2
            x2 = next(iter2, None)
    # Yield any remaining values in iter1 and iter2
    if x1 is not None:
        yield x1
        yield from iter1
    if x2 is not None:
        yield x2
        yield from iter2


def ordered_merge(iter1: Iterable, iter2: Iterable, num_buckets: int) -> Iterator:
    for _, x in sorted_merge(
        ((hash(x) % num_buckets, x) for x in iter1),
        ((hash(x) % num_buckets, x) for x in iter2),
    ):
        yield x


def ordered(sequence: Sequence, num_buckets: int) -> List:
    buckets: List[List] = [[] for _ in range(num_buckets)]
    for x in sequence:
        buckets[hash(x) % num_buckets].append(x)
    result = []
    for bucket in buckets:
        bucket.sort()
        result.extend(sorted(bucket))
    return result


def demo_sorted_ints(sequence, num_buckets):
    expected_result = sorted(sequence, key=lambda x: (hash(x) % num_buckets, x))
    actual_result = ordered(sequence, num_buckets)
    print(f"ordered({sequence!r}, {num_buckets!r}) == {actual_result!r}")
    assert actual_result == expected_result


def main():
    demo_sorted_ints([], 4)
    demo_sorted_ints([8, 2, 1, 5, 1, 0], 4)
    demo_sorted_ints([0, 1, 2, 1, 2, 1, 1], 4)


if __name__ == "__main__":
    main()
