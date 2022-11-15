from typing import Iterator

def phi_order(n: int) -> Iterator[int]:
  phi = (5**0.5 + 1) / 2
  for i in range(n):
    yield round(i * n * phi) % n

if __name__ == '__main__':
  for n in range(1, 30):
    order = list(phi_order(n))
    print(f'{n:2d} {str(sorted(order) == list(range(n))):5s} {order}')
