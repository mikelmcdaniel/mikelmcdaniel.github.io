#include "bad_my_min.h"

// This template function should be defined in the header file so that when the
// compiler sees this function being used, it can compile it. Since the function
// is defined in this .cpp file and it is not used in this .cpp file, this
// template is never actually used/compiled!
template <typename T>
T my_min(const T& x, const T& y) {
  return (x < y) ? x : y;
}

// This is correct: my_max should be defined in the .cpp file so it's compiled
// exactly once.
double my_max(double x, double y) {
  return (x > y) ? x : y;
}
