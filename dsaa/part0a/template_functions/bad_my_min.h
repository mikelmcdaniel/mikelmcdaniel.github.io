#pragma once
// Templates should be declared and defined in the header file.
// If they are declared in the header file and defined in the .cpp file, then
// the compiler won't know how to compile the template when it sees it being
// used in another .cpp file.
template <typename T>
T my_min(const T& x, const T& y);

// my_min should not be defined in the header file because it should only be
// defined/compiled once.
int my_max(int x, int y) {
  return (x > y) ? x : y;
}

// This is correct: non-template functions should be declared but not defined in
// header files.
double my_max(double x, double y);
