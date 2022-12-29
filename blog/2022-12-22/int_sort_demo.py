from typing import Any, Iterable, Iterator, List, Optional, Sequence


def sorted_non_negative_ints(ints: Iterable[int]) -> List[int]:
    # counts[i] is the number of times we've seen the int i
    counts: List[int] = []
    for i in ints:
        if i < 0:
            raise ValueError(f"sorted_non_negative_ints got a negative int: {i}")
        while i >= len(counts):  # Grow counts until it's big enough!
            counts.append(0)
        counts[i] += 1

    result = []
    for i, count in enumerate(counts):
        for _ in range(count):
            result.append(i)
    return result


def demo_sorted_ints(sequence):
    expected_result = sorted(sequence)
    actual_result = sorted_non_negative_ints(sequence)
    print(f"sorted_non_negative_ints({sequence!r}) == {actual_result!r}")
    assert actual_result == expected_result


def main():
    demo_sorted_ints([])
    demo_sorted_ints([8, 2, 1, 5, 1, 0])
    demo_sorted_ints([0, 1, 2, 1, 2, 1, 1])


if __name__ == "__main__":
    main()
