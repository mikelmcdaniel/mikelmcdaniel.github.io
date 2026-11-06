import itertools
import multiprocessing
import operator
import random
import sys
from typing import Callable, Iterable, Iterator, NamedTuple


sys.setrecursionlimit(999_999)


class ParamNames(NamedTuple):
    func: str
    row_sort: str
    col_sort: str
    rcs: str
    rcs_cmp: str
    rcs_tie: str
    rcs_cmp_tie: str


class Params(NamedTuple):
    func: Callable[[int, dict, "Params"], int]
    row_sort: Callable[[tuple[int, ...] | Iterable[int] | Iterator[int]], tuple[int, ...]]
    col_sort: Callable[[tuple[int, ...] | Iterable[int] | Iterator[int], int], tuple[int, ...]]
    rcs: Callable[[tuple[int, ...]], object]
    rcs_cmp: Callable[[object, object], bool]
    rcs_tie: Callable[[tuple[int, ...]], object]
    rcs_cmp_tie: Callable[[object, object], bool]

def row_col_swap(row_max_sums, col_max_sums, params: Params):
    if params.rcs_cmp(params.rcs(row_max_sums), params.rcs(col_max_sums)):
        row_max_sums, col_max_sums = col_max_sums, row_max_sums
    elif params.rcs(row_max_sums) == params.rcs(col_max_sums) and params.rcs_cmp_tie(params.rcs_tie(row_max_sums), params.rcs_tie(col_max_sums)):
        row_max_sums, col_max_sums = col_max_sums, row_max_sums
    return row_max_sums, col_max_sums


def _matrices_with_max_sums(
        col_max_sums: tuple[int, ...], 
        row_max_sums: tuple[int, ...], 
        col: int,
        cache,
        params: Params) -> int:
    if col and col_max_sums[col - 1] == 0:
        col -= 1
        col_max_sums = col_max_sums[:col] + col_max_sums[col + 1:]
    # assert 0 not in col_max_sums
    if not row_max_sums or not col_max_sums:
        return 1
    if col >= len(col_max_sums) or not row_max_sums[0]:
        return _matrices_with_max_sums(col_max_sums, row_max_sums[1:], 0, cache, params)


    row_max_sums = params.row_sort(row_max_sums)  # Needed for reasons
    col_max_sums = params.col_sort(col_max_sums, col)
    if col == 0:
        row_max_sums, col_max_sums = row_col_swap(row_max_sums, col_max_sums, params)
    
    cache_key = (col_max_sums, row_max_sums, col)
    if not cache_key in cache:
        cache[cache_key] = sum(
            _matrices_with_max_sums(
                col_max_sums[:col] + (col_max_sums[col] - delta,) + col_max_sums[col + 1:], 
                (row_max_sums[0] - delta,) + row_max_sums[1:], 
                col + 1,
                cache,
                params)
            for delta in range(min(col_max_sums[col], row_max_sums[0]) + 1)
        )
    return cache[cache_key]


def matrices_with_max_sums(
        col_max_sums: Iterable[int] | Iterator[int], 
        row_max_sums: Iterable[int] | Iterator[int], 
        cache, 
        params: Params) -> int:
    return _matrices_with_max_sums(params.col_sort(tuple(col_max_sums), 0), params.row_sort(tuple(row_max_sums)), 0, cache=cache, params=params)


def A049088(n, cache, params: Params):
    return matrices_with_max_sums([2]*n, [2]*n, cache, params)


def A131235_row(n, cache, params: Params):
    row = []
    for k in range(n + 1):
        row.append(matrices_with_max_sums([2]*(n - k), [2]*k, cache, params))
    return row


ROW_SORTS = {
    'yes': lambda row_max_sums: tuple(sorted(row_max_sums)),
    'yesX': lambda row_max_sums: row_max_sums[:1] + tuple(sorted(row_max_sums[1:])),
    'no': lambda row_max_sums: row_max_sums,
    'reverse': lambda row_max_sums: tuple(sorted(row_max_sums, reverse=True)),
    'reverseX': lambda row_max_sums: row_max_sums[:1] + tuple(sorted(row_max_sums[1:], reverse=True)),
}
COL_SORTS = {
    'yes': lambda col_max_sums, col: tuple(sorted(col_max_sums[:col])) + tuple(sorted(col_max_sums[col:])),
    'yesX': lambda col_max_sums, col: () if not col_max_sums else tuple(sorted(col_max_sums[:col])) + (col_max_sums[col],) + tuple(sorted(col_max_sums[col + 1:])),
    'no': lambda col_max_sums, col: col_max_sums,
    'reverse': lambda col_max_sums, col: tuple(sorted(col_max_sums[:col], reverse=True)) + tuple(sorted(col_max_sums[col:], reverse=True)),
    'reverseX': lambda col_max_sums, col: () if not col_max_sums else tuple(sorted(col_max_sums[:col], reverse=True)) + (col_max_sums[col],) + tuple(sorted(col_max_sums[col + 1:], reverse=True)),
}
RCS_GETS = {
    'identity': lambda x: x,
    'sum': sum,
    'len': len,
}
RCS_CMPS = {
    'lt': operator.lt,
    'gt': operator.gt,
}
FUNCS = {
    'A049088': A049088,
    'A131235_row': A131235_row
}


def get_data_row(param_names: ParamNames):
    params = Params(*(d[name] for name, d in zip(param_names, (FUNCS, ROW_SORTS, COL_SORTS, RCS_GETS, RCS_CMPS, RCS_GETS, RCS_CMPS))))

    cache = {}
    name = "_".join([param_names.row_sort, param_names.col_sort, param_names.rcs, param_names.rcs_cmp, param_names.rcs_tie, param_names.rcs_cmp_tie])
    data: list[str | int] = [param_names.func, name]
    for n in range(1, 21):
        params.func(n, cache, params)
        data.append(len(cache))
        if len(cache) > 100_000:
            break
    return data


all_param_names: list[ParamNames] = [ParamNames(*names) for names in itertools.product(FUNCS, ROW_SORTS, COL_SORTS, RCS_GETS, RCS_CMPS, RCS_GETS, RCS_CMPS)]
all_param_names = [names for names in all_param_names if names.rcs != names.rcs_tie]
random.shuffle(all_param_names)
with multiprocessing.Pool(15) as p:
    for data in p.map(get_data_row, all_param_names, len(all_param_names) // 60):
        print(",".join(map(str, data)))
        sys.stdout.flush()