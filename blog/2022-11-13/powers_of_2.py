from typing import Iterator

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

if __name__ == '__main__':
  for n in (1, 2, 4, 8, 16, 32):
    order = list(middle_order_power_of_2(n))
    print(n, '->', order)
    assert sorted(order) == list(range(n))
