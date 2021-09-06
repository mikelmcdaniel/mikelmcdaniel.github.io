#pragma once

template <typename T>
T my_min(const T& x, const T& y) {
  return (x < y) ? x : y;
}

int my_max(int x, int y);
double my_max(double x, double y);
