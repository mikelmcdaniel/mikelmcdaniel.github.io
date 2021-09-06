#pragma once

// Compromise Search is a compromise between Binary Search and Linear Search:
//   We use Binary Search until we get to small_size elements, then we switch to Linear Search.
//   Binary Search between low and high until the gap betwenlow and high is <= small_size,
//   then use std::find on the range (from low to high).
// For example,
// vector<string> words = {"aaa", "bbb", "ccc", "ddd", "eee"};
// cout << *compromise_search(words.begin(), words.end(), "bbb", 3) << endl;
// will print "bbb\n".
// compromise_search will
// - calculate the middle
// - see that "bbb" < "ccc" (and update the upper bound)
// - see that the remaining range (from "aaa" to "ccc" exclusive)
//   has <= small_size (3) elements
// - use std::find to search through the remaining range
//   (from "aaa" to "ccc" exclusive)
//
// RandomAccessIt is a random-access iterator, like vector<string>::begin().
// low is inclusive and high is exclusive.
template<class RandomAccessIt, class T>
RandomAccessIt compromise_search(
    RandomAccessIt low, RandomAccessIt high, const T& value, int small_size) {
  auto original_high = high;
  while (high - low > small_size) {
    auto middle = low + (high - low) / 2;
    if (*middle == value) {
      return middle;
    } else if (value < *middle) {
      high = middle;
    } else { // if (value > middle_value)
      low = middle + 1;
    }
  }
  auto it = std::find(low, high, value);
  // If we didn't find anything between low and high,
  // then return the original_high iterator.
  if (it == high) {
    return original_high;
  } else {
    return it;
  }
}
