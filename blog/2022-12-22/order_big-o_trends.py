import collections
import functools
import itertools
import math
import operator
import time

from typing import Any, Iterable, Iterator, List, Sequence, Tuple


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
    buckets = [[] for _ in range(num_buckets)]
    for x in sequence:
        buckets[hash(x) % num_buckets].append(x)
    result = []
    for bucket in buckets:
        bucket.sort()
        result.extend(bucket)
    return result


def fact(n):
    return functools.reduce(operator.mul, range(2, n + 1), 1)


def choose(n, k):
    return fact(n) // fact(n - k) // fact(k)


__log_fact_cache = []


def log_fact(n):
    try:
        return __log_fact_cache[n]
    except IndexError:
        while n >= len(__log_fact_cache):
            __log_fact_cache.append(math.lgamma(len(__log_fact_cache) + 1))
        return __log_fact_cache[n]
    # return math.lgamma(n + 1)


__log_choose_cache = []


def log_choose(n, k):
    try:
        return __log_choose_cache[n][k]
    except IndexError:
        while n >= len(__log_choose_cache):
            __log_choose_cache.append([])
        sub_cache = __log_choose_cache[n]
        while k >= len(sub_cache):
            sub_cache.append(
                log_fact(n) - (log_fact(n - len(sub_cache)) + log_fact(len(sub_cache)))
            )
        return __log_choose_cache[n][k]
    # assert n >= k
    # return log_fact(n) - (log_fact(n - k) + log_fact(k))


# __ascending_partitions_counter = collections.defaultdict(int)
# __ascending_partitions_cache = {}
#
#
# def _cached_ascending_partitions(
#     num_elements: int,
#     num_buckets: int,
#     max_in_cur_bucket: int,
#     empty_list: List[int],
# ) -> Iterator[Tuple[List[int], int]]:
#     # assert not empty_list
#     if num_buckets == 0:
#         return iter([(empty_list, 0)])
#
#     cache_key = (num_elements, num_buckets)
#     __ascending_partitions_counter[cache_key] += 1
#     if cache_key in __ascending_partitions_cache:
#         return itertools.takewhile(
#             lambda p_and_lnp: p_and_lnp[0][-1] <= max_in_cur_bucket,
#             __ascending_partitions_cache[cache_key],
#         )
#     elif __ascending_partitions_counter[cache_key] > 100:
#         result = []
#         for p, lnp in _ascending_partitions(
#             num_elements,
#             num_buckets,
#             num_elements,  # NOTE
#             [],
#         ):
#             result.append((list(p), lnp))
#         __ascending_partitions_cache[cache_key] = result
#         return _cached_ascending_partitions(
#             num_elements,
#             num_buckets,
#             max_in_cur_bucket,
#             empty_list,
#         )
#     return _ascending_partitions(
#         num_elements,
#         num_buckets,
#         max_in_cur_bucket,
#         empty_list,
#     )


# def _ascending_partitions(
#     num_elements: int,
#     num_buckets: int,
#     max_in_cur_bucket: int,
#     empty_list: List[int],
# ) -> Iterator[Tuple[List[int], int]]:
#     if num_buckets == 0:
#         yield empty_list, 0
#         return
#     min_in_cur_bucket = (num_elements + num_buckets - 1) // num_buckets
#     for num_in_cur_bucket in range(min_in_cur_bucket, max_in_cur_bucket + 1):
#         num_elements_remaining = num_elements - num_in_cur_bucket
#         for p, lnp in _ascending_partitions(
#             num_elements_remaining,
#             num_buckets - 1,
#             min(num_elements_remaining, num_in_cur_bucket),
#             empty_list,
#         ):
#             p.append(num_in_cur_bucket)
#             yield p, lnp + log_choose(num_elements, num_in_cur_bucket)
#             p.pop()


# def _ascending_partitions(
#     num_elements: int,
#     num_buckets: int,
#     max_in_cur_bucket: int,
#     empty_list: List[int],
#     m: float,
# ) -> Iterator[Tuple[List[int], int]]:
#     if num_buckets == 0:
#         yield empty_list, m
#         return
#     min_in_cur_bucket = (num_elements + num_buckets - 1) // num_buckets
#     for num_in_cur_bucket in range(min_in_cur_bucket, max_in_cur_bucket + 1):
#         num_elements_remaining = num_elements - num_in_cur_bucket
#         empty_list.append(num_in_cur_bucket)
#         yield from _ascending_partitions(
#             num_elements_remaining,
#             num_buckets - 1,
#             min(num_elements_remaining, num_in_cur_bucket),
#             empty_list,
#             m + log_choose(num_elements, num_in_cur_bucket)
#         )
#         empty_list.pop()


def add_to_partition(partition, num_in_cur_bucket):
    if not partition or partition[-1][0] != num_in_cur_bucket:
        partition.append([num_in_cur_bucket, 1])
    else:
        partition[-1][1] += 1


def pop_partition(partition):
    partition[-1][1] -= 1
    if partition[-1][1] == 0:
        partition.pop()


def _descending_partitions(
    num_elements: int,
    num_buckets: int,
    max_in_cur_bucket: int,
    partition_so_far: List[Tuple[int, int]],
    log_num_partitions: float,
) -> Iterator[Tuple[List[Tuple[int, int]], int]]:
    if num_buckets == 0:
        assert num_elements == 0
        yield partition_so_far, log_num_partitions
        return
    if max_in_cur_bucket == 0:
        partition_so_far.append((0, num_buckets))
        yield partition_so_far, log_num_partitions
        partition_so_far.pop()
        return
    min_in_cur_bucket = (num_elements + num_buckets - 1) // num_buckets
    for num_in_cur_bucket in range(min_in_cur_bucket, max_in_cur_bucket + 1):
        # min_repetitions = num_elements // num_in_cur_bucket #1  # TODO: This is wrong
        min_repetitions = max(
            num_elements + num_buckets - num_in_cur_bucket * num_buckets, 1
        )
        max_repetitions = num_elements // num_in_cur_bucket
        for repitions in range(min_repetitions, max_repetitions + 1):
            num_elements_remaining = num_elements - repitions * num_in_cur_bucket
            # add_to_partition(partition_so_far, num_in_cur_bucket)
            partition_so_far.append((num_in_cur_bucket, repitions))
            # assert num_elements_remaining < num_in_cur_bucket
            yield from _descending_partitions(
                num_elements_remaining,
                num_buckets - repitions,
                min(num_elements_remaining, num_in_cur_bucket - 1),
                partition_so_far,
                log_num_partitions
                + sum(
                    # log_choose(num_elements, num_in_cur_bucket)
                    log_choose(num_elements - x * num_in_cur_bucket, num_in_cur_bucket)
                    for x in range(repitions)
                ),
            )
            # pop_partition(partition_so_far)
            partition_so_far.pop()


def unordered_partitions(num_elements: int, num_buckets: int) -> Iterator[List[int]]:
    for partition, count in _descending_partitions(
        num_elements, num_buckets, num_elements, [], 0.0
    ):
        log_num_partitions = count + log_fact(num_buckets)  # * fact(num_buckets)
        for _, log_bucket_count in partition:
            # num_partitions //= fact(bucket_count)
            log_num_partitions -= log_fact(log_bucket_count)
        yield partition, log_num_partitions


def approx_num_ops_to_sort(n: int, base: int = 2) -> float:
    return n * math.log(n, base) if n > 1 else 1


def average_approx_num_ops_to_order(num_elements, num_buckets) -> float:
    log_total_partitions = num_elements * math.log(num_buckets)
    ops = 0
    num_unique_partitions = 0
    for partition, log_num_partitions in unordered_partitions(
        num_elements, num_buckets
    ):
        num_unique_partitions += 1
        ops += sum(
            num_k * approx_num_ops_to_sort(k) for k, num_k in partition
        ) * math.exp(log_num_partitions - log_total_partitions)
    return ops, num_unique_partitions


# def ratio_num_bins_with_balls(n, num_balls):
#     if n < num_balls:
#         return 0
#     return choose(n, num_balls) * (n - 1)**(n - num_balls) / n**(n - 1)


# def ratio_num_bins_with_balls(n, num_balls):
#     if n < num_balls or n <= 1:
#         return 0
#     return math.exp(log_choose(n, num_balls) + (n - num_balls) * math.log(n - 1) - (n - 1) * math.log(n))


def prod(iterable):
    return functools.reduce(operator.mul, iterable, 1)


def num_bins_with_balls(num_elements, objs_in_bucket, num_buckets):
    try:
        return (
            num_buckets
            * (num_buckets - 1) ** (num_elements - objs_in_bucket)
            * choose(num_elements, objs_in_bucket)
        )
    except ZeroDivisionError:
        return 0


def ratio_num_bins_with_balls(num_elements, objs_in_bucket, num_buckets):
    try:
        log_num_buckets = math.log(num_buckets)
        # return num_buckets * (num_buckets - 1)**(num_elements - objs_in_bucket) * choose(num_elements, objs_in_bucket) / num_buckets**num_elements
        return math.exp(
            log_num_buckets
            + math.log(num_buckets - 1) * (num_elements - objs_in_bucket)
            + log_choose(num_elements, objs_in_bucket)
            - log_num_buckets * num_elements
        )
    except (ZeroDivisionError, ValueError):
        return 0


def main():
    # max_n = 10  # 1_000_000
    # for n in range(1, max_n + 1):
    #     counts = collections.defaultdict(int)
    #     # total_np = 0
    #     for p, lnp in unordered_partitions(n, n):
    #         np = int(round(math.exp(lnp)))
    #         # total_np += np
    #         for c, r in p:
    #             if c == 0:
    #                 continue
    #             # counts[c, r] += np
    #             counts[c] += r * np
    #     # print(n, total_np, n**n)
    #     print(n, sorted(counts.items()))
    # return
    with open("/home/mikel/Desktop/output_4.csv", "w") as f:
        f.write("num_elements,num_buckets,approx_ops_base_2,approx_ops_base_e\n")
        for num_elements in range(10_000, max_n + 1, 10_000):
            print(f"{num_elements=}")
            for num_buckets in range(10_000, max_n + 1, 10_000):
                # bucket_counts = [(b, num_bins_with_balls(num_elements, b, num_buckets)) for b in range(1, num_elements + 1)]
                # bucket_counts = [(b, c) for b, c in bucket_counts if c > 0]
                # print(num_elements, bucket_counts)
                expected_2 = sum(
                    ratio_num_bins_with_balls(num_elements, b, num_buckets)
                    * approx_num_ops_to_sort(b, 2)
                    for b in range(num_elements + 1)
                )
                expected_e = sum(
                    ratio_num_bins_with_balls(num_elements, b, num_buckets)
                    * approx_num_ops_to_sort(b, math.e)
                    for b in range(num_elements + 1)
                )
                f.write(f"{num_elements},{num_buckets},{expected_2},{expected_e}\n")
    return
    if True:
        # with open('/home/mikel/Desktop/output_TWO.csv', 'a') as f:
        #     f.write('num_elements,num_buckets,num_unique_partitions,approx_ops,seconds_to_calculate\n')
        for num_elements_exp in range(111):
            for num_buckets_exp in range(num_elements_exp + 2):
                num_elements = 2 ** num_elements_exp
                num_buckets = 2 ** num_buckets_exp
                start_time = time.time()
                approx_ops, num_unique_partitions = average_approx_num_ops_to_order(
                    num_elements, num_buckets
                )
                seconds_to_calculate = time.time() - start_time
                print(
                    f"{num_elements=} {num_buckets=} {num_unique_partitions=} {seconds_to_calculate=}"
                )
                print("average order ops:", approx_ops)
                print("average sort ops:", approx_num_ops_to_sort(num_elements))
                print()
            #     f.write(f'{num_elements},{num_buckets},{num_unique_partitions},{approx_ops},{seconds_to_calculate}\n')
            # f.flush()


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()')
    main()
