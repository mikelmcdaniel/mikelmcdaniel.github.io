from typing import Any, Iterable, Iterator, List, Sequence


def merge(iter1: Iterable, iter2: Iterable) -> Iterator:
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


def merge_sorted(sequence: Sequence, low: int = 0, high: int = None) -> Sequence:
    if high is None:
        high = len(sequence)
    if high - low <= 1:
        return sequence[low:high]
    middle = low + (high - low) // 2
    left = merge_sorted(sequence, low, middle)
    right = merge_sorted(sequence, middle, high)
    return list(merge(left, right))


def demo_merge(input1, input2, expected_result):
    actual_result = list(merge(input1, input2))
    print(f"merge({input1!r}, {input2!r}) == {actual_result!r}")
    assert actual_result == expected_result


def demo_merge_sorted(sequence):
    expected_result = sorted(sequence)
    actual_result = merge_sorted(sequence)
    print(f"merge_sorted({sequence!r}) == {actual_result!r}")
    assert actual_result == expected_result


def main():
    demo_merge([], [], [])
    demo_merge([], [0, 2, 5], [0, 2, 5])
    demo_merge([1, 2, 3, 6], [], [1, 2, 3, 6])
    demo_merge([1, 2, 3, 6], [0, 2, 5], [0, 1, 2, 2, 3, 5, 6])
    demo_merge_sorted([])
    demo_merge_sorted([8, 2, 1, 5, 0])


if __name__ == "__main__":
    main()
