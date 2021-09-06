#include <iostream>
#include <string>

#include "good_my_min.h"

using std::cout;
using std::endl;
using std::string;

int main(int argc, const char* argv[]) {
  string apples = "apples", oranges = "oranges";
  cout << "my_min(2, 3) == " << my_min(2, 3) << endl;
  cout << "my_min(5, 4) == " << my_min(5, 4) << endl;
  cout << "my_min(2.2, 3.3) == " << my_min(2.2, 3.3) << endl;
  cout << "my_min(5.5, 4.4) == " << my_min(5.5, 4.4) << endl;
  cout << "my_min(apples, oranges) == " << my_min(apples, oranges) << endl;
  cout << "my_min(oranges, apples) == " << my_min(oranges, apples) << endl;
  cout << endl;
  cout << "my_max(100, 200) == " << my_max(100, 200) << endl;
  cout << "my_max(111.111, 222.222) == " << my_max(111.111, 222.222) << endl;
  return 0;
}
