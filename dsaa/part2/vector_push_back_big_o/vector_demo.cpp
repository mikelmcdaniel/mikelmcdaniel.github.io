#include <iostream>  // std::cout, std::endl
#include <chrono>
#include <vector>

#include "template_vector.h"

using namespace std;


class SimpleTimer {
  std::chrono::time_point<std::chrono::steady_clock> start_time;

public:
  void start() {
    start_time = std::chrono::steady_clock::now();
  }

  // Return the number of seconds since .start() was called
  double elapsed_seconds() const {
    std::chrono::duration<double> diff(std::chrono::steady_clock::now() - start_time);
    return diff.count();
  }
};


int main(int argc, const char *argv[]) {
  TemplateVector<int> vec;
  SimpleTimer timer;
  cout << "n,ops_counter,elapsed_seconds" << endl;
  timer.start();
  for (int i = 0; i < 100000; ++i) {
    vec.push_back(i);
    // Only print out one in every thousand lines so the output isn't huge
    if (i % 1000 == 0) {
      cout
          << vec.size() << "," << vec.ops_counter << ","
          << timer.elapsed_seconds() << endl;
    }
  }
  return 0;
}
