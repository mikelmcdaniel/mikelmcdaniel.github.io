#include <cmath>
#include <iostream>
#include <string>
#include <vector>

#include "compromise_search.h"

using namespace std;

int main() {
  vector<string> words = {"apple", "banana", "mango", "tangerine", "zuchini"};
  vector<string> words_to_search = {
      "apple", "mango", "zuchini", "aaa", "bbb", "yyy", "zzz"};
  for (const string& w : words_to_search) {
    for (int small_size = 0; small_size <= words.size(); ++small_size) {
      auto word_iterator = compromise_search(words.begin(), words.end(), w, small_size);
      cout
          << w << " was"
          << (word_iterator == words.end() ? " not" : "")
          << " found" << endl;
    }
    cout << endl;
  }
  cout << endl;
  return 0;
}
