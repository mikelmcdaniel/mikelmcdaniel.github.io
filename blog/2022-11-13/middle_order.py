import collections

from typing import Iterator, Tuple


# O(n) time and O(n) space
def middle_order_queue(n: int) -> Iterator[int]:
  """Return all the numbers in [0, n) in middle order using a queue.

  The queue contains a list of ranges, starting with [0, n). For each range, we
  yield the mid-point and add on the left and right subranges of numbers that
  have not been yielded yet.

  This takes O(n) space because the queue size will have roughly n / 2 elements
  at it's peak size.
  """
  # q is a queue of ranges of numbers that have not been yielded yet.
  # The lo(wer) bound is inclusive and the hi(gher) bound is exclusive.
  q = collections.deque([(0, n)])
  # This loop will iterate at most 2 * n times.
  # Each iteration is O(1) time.
  # During the last iterations, q will have O(n / 2) = O(n) pairs in it!
  while q:
    lo, hi = q.popleft()
    if lo == hi:
      continue
    mid = (lo + hi) // 2
    yield mid
    q.append((lo, mid))
    q.append((mid + 1, hi))


def _middle_order_recursive(lo: int, hi: int) -> Iterator[int]:
  """Return all the numbers in [lo, hi) in middle order using recursion.

  First, we yield the mid point of [lo, hi), then we process the mid points of
  [lo, mid) and [mid + 1, hi) in an interleaved.

  This uses O(hi - lo) space because each recursive generator call creates 2
  generators (one for the left half and one for the left half), with a total
  depth of roughly log(hi - lo, 2).
  """
  if lo == hi:
    return
  mid = (lo + hi) // 2
  yield mid
  # Note that because we recure on the left and right halves simultaneously,
  # this use O(n) space in the worst case!
  left = _middle_order_recursive(lo, mid)
  right = _middle_order_recursive(mid + 1, hi)
  # Note that since len(list(right)) <= len(list(left)), we must put right
  # in zip first. zip(left, right) would not work because zip would call
  # next(left) first then call next(right) and realize that there were no
  # elements next *and* zip would not return the element from left so we would
  # have no easy way to get that element!
  for r, l in zip(right, left):
    yield l
    yield r
  yield from left


# O(n) time and O(n) space.
def middle_order_recursive(n: int) -> Iterator[int]:
  return _middle_order_recursive(0, n)


def is_power_of_2(n: int) -> bool:
  return n & (n - 1) == 0

# O(n) time and O(1) space
def middle_order_power_of_2(n: int) -> Iterator[int]:
  assert is_power_of_2(n)
  step = n
  # This loop runs O(log(n)) times
  # Each loop yields O(n / step) times
  # If we up all the numbers yielded, then we get 1 + 2 + 4 + ... + 2**log(n, 2)
  # which is just n. This also matches what we expect since we should yield each
  # number in [0, n) exactly once.
  while step > 1:
    start = step // 2
    yield from range(start, n, step)
    step = start
  yield 0


def power_of_2_ge(n: int) -> int:
  x = 1
  while True:
    if x >= n:
      return x
    x <<= 1


# O(n) time and O(n) space
def middle_order_seen_power_of_2_ge(n: int) -> Iterator[int]:
  """Return all the numbers in [0, n) in middle order.

  Here, we calculate the smallest power of 2 that is >= n, then call
  middle_order_power_of_2 and use a set to ensure we only yield each number one
  time.

  This takes O(n) space because the set will contain all numbers in [0, n).
  """
  seen_nums = set()  # Note: Instead of using a set, we could use a bitset
  n2 = power_of_2_ge(n)
  for x in middle_order_power_of_2(n2):
    x = n * x // n2
    if x not in seen_nums:
      yield x
      seen_nums.add(x)


def _middle_order_ranges(n: int) -> Iterator[Tuple[int, int]]:
  """Yield all left and right ranges in [0, n) in middle order using recursion.

  This strategy is actually the same as the queue strategy in disguise! Instead
  of maintaining a queue in memory, we use recursion to see what our earlier
  ranges are that we need to process.

  Each range is then processed by yielding the left and right sub-ranges.

  Since we only recurse once *and* only iterate over 1/2 of the numbers in the
  recursive call as what we yield, this function uses O(n + n/2 + n/4 + ...) =
  O(n) time and O(log2(n)) space.
  """
  yield 0, n
  # This loop will execute at most n / 2 times
  for lo, hi in _middle_order_ranges(n):
    mid = (lo + hi) // 2
    if not mid:  # Without this if-statement, we would recurse infinitely
      return
    if mid + 1 != hi:
      yield mid + 1, hi
    if lo != mid:
      yield lo, mid


# O(n) time and O(log(n)) space!
def middle_order_ranges(n: int) -> Iterator[int]:
  for lo, hi in _middle_order_ranges(n):
    yield (lo + hi) // 2


if __name__ == '__main__':
  for n in (5, 8, 9, 10, 20, 21):
    for middle_order in (
        middle_order_queue,
        middle_order_recursive,
        middle_order_seen_power_of_2_ge,
        middle_order_ranges):
      order = list(middle_order(n))
      print(f'{middle_order.__name__:>31s}({n:>2d}) -> {order}')
      assert sorted(order) == list(range(n))
