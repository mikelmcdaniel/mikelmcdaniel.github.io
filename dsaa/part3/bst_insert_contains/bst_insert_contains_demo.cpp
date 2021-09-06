#include <iostream>

#include "bst.h"

using namespace std;

int main() {
  BinarySearchTree<int> bst;
  bst.insert(11);
  bst.insert(55);
  bst.insert(99);

  bst.print();
  cout << endl;

  for (int x : {0, 11, 33, 55, 88, 99, 1000}) {
    cout << "bst.contains(" << x << ") == " << bst.contains(x) << endl;
  }

	return 0;
}
