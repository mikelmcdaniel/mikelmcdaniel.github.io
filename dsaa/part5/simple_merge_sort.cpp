#include <iostream>
#include <vector>

using std::cout;
using std::endl;
using std::string;
using std::vector;


// Overall, this algorithm is O(L + R) = O(n)
vector<string> merge(
    const vector<string>::iterator left_low, const vector<string>::iterator left_high,
    const vector<string>::iterator right_low, const vector<string>::iterator right_high) {
  // O(1)
  vector<string> result;
  auto left_position = left_low;
  auto right_position = right_low;
  // If L is the size of the left range (left_high - left_low)
  // and R is the size of the right range (right_high - right_low),
  // then this loop is O(L + R) = O(n)
  while (left_position != left_high && right_position != right_high) {
    if (*left_position < *right_position) {
      result.push_back(*left_position);
      ++left_position;
    } else {
      result.push_back(*right_position);
      ++right_position;
    }
  }
  // O(L)
  while (left_position != left_high) {
    result.push_back(*left_position);
    ++left_position;
  }
  // O(R)
  while (right_position != right_high) {
    result.push_back(*right_position);
    ++right_position;
  }
  return result;
}


// T(0) = 1
// T(1) = 1
// T(N) = 1 + N + 2 * T(N / 2)
void merge_sort(vector<string>::iterator low, vector<string>::iterator high) {
  // The few lines below are O(1)
  if (high - low <= 1) {
    return;
  }
  auto middle = low + (high - low) / 2;
  // The recursive calls to merge_sort add "2 * T(N / 2)" to T(N)
  merge_sort(low, middle);
  merge_sort(middle, high);
  // The merge step below adds O(N) steps to T(N)
  // Merge the left and right halves.
  vector<string> merged = merge(low, middle, middle, high); // O(N)
  // The copy step below adds O(N) steps to T(N)
  // Copy merged elements into [low, high); O(N)
  auto it = low;
  for (const string& value : merged) {
    *it = value;
    ++it;
  }
}


int main() {
  vector<string> words;
  words.push_back("cherry");
  words.push_back("durian");
  words.push_back("apple");
  words.push_back("egg plant");
  words.push_back("banana");

  merge_sort(words.begin(), words.end());
  for (const string& w : words) {
    cout << w << endl;
  }
  cout << endl;
  return 0;
}
