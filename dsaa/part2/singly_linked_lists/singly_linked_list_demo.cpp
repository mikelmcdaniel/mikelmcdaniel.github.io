#include <iostream>
#include <string>

#include "singly_linked_list.h"

using std::cout;
using std::endl;
using std::string;

int main() {
  LinkedList<string> words;
  words.push_back("apple");
  words.push_back("banana");
  words.push_back("cherry");

  words.pop_front();

  for (const string& word : words) {
    cout << word << endl;
  }

  return 0;
}
