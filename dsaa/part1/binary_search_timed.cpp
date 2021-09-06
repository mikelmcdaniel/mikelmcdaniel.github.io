#include <algorithm>
#include <chrono>
#include <iostream>
#include <fstream>
#include <random>
#include <string>
#include <vector>

using std::cout;
using std::endl;
using std::ifstream;
using std::string;
using std::vector;

vector<string> read_lines(const string& filepath, const long max_lines=-1) {
  ifstream f(filepath);
  vector<string> lines;
  for(string line; getline(f, line); ) {
    lines.push_back(line);
    if (max_lines > 0 && lines.size() >= max_lines) {
      break;
    }
  }
  return lines;
}

vector<string> get_random_words(const vector<string>& words, const int sample_size) {
    std::default_random_engine dre;
    std::uniform_int_distribution<int> uniform_dist(0, words.size() - 1);
    vector<string> random_words;
    for (int i = 0; i < sample_size; ++i) {
      random_words.push_back(words[uniform_dist(dre)]);
    }
    return random_words;
}

bool _contains_word_bs(
    const vector<string>& words, const string& word, int low, int high) {
  // Base case: Could not find the word
  if (low == high) {
    return false;
  }
  // Bonus question: We can also calculate `middle = (low + high) / 2`.
  //   When is calculating `middle = low + (high - low) / 2` better?
  const int middle = low + (high - low) / 2;
  const string& mid_word = words[middle];
  if (mid_word == word) {
    // Base case: Found the word!
    return true;
  } else if (word < mid_word) {
    high = middle;
  } else {  // if (word > mid_word)
    low = middle + 1;
  }
  // Recursive case: We've narrowed down the search to the left or right half.
  // Note that instead of recursing here, we could just as easily put the code
  //   in this function in a loop.
  return _contains_word_bs(words, word, low, high);
}

bool contains_word_bs(const vector<string>& words, const string& word) {
  return _contains_word_bs(words, word, 0, words.size());
}

// Returns the number of seconds to search for all `sample_words` in `words`.
double time_contains_word_bs(const vector<string>& words, const vector<string>& sample_words) {
  auto start_time = std::chrono::steady_clock::now();
  for (const string& w : sample_words) {
    contains_word_bs(words, w);
  }
  auto end_time = std::chrono::steady_clock::now();
  std::chrono::duration<double> elapsed_seconds = end_time - start_time;
  return elapsed_seconds.count();
}

// Returns the number of seconds to search for all `sample_words` in `words`.
double time_std_find(const vector<string>& words, const vector<string>& sample_words) {
  auto start_time = std::chrono::steady_clock::now();
  for (const string& w : sample_words) {
    std::binary_search(words.begin(), words.end(), w);
  }
  auto end_time = std::chrono::steady_clock::now();
  std::chrono::duration<double> elapsed_seconds = end_time - start_time;
  return elapsed_seconds.count();
}

int main(int argc, const char* argv[]) {
  const int sample_size = 100000;
  const char* words_filename = argc > 1 ? argv[1] : "words.txt";
  // Output a CSV that can be graphed.
  cout << "\"Number of words\",contains_word_bs,std::binary_search\n";
  for (int n = 1; n < 1000000; n *= 2) {
      vector<string> words = read_lines(words_filename, n);
      std::sort(words.begin(), words.end());
      vector<string> random_words = get_random_words(words, sample_size);
      cout
          << words.size() << ","
          << time_contains_word_bs(words, random_words) << ","
          << time_std_find(words, random_words) << '\n';
  }
  return 0;
}
