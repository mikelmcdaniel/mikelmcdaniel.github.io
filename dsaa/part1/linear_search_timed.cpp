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

bool contains_word_linear(const vector<string>& words, const string& word) {
  for (const auto& w : words) {
    if (w == word) {
      return true;
    }
  }
  return false;
}

// Returns the number of seconds to search for all `sample_words` in `words`.
double time_contains_word_linear(const vector<string>& words, const vector<string>& sample_words) {
  auto start_time = std::chrono::steady_clock::now();
  for (const string& w : sample_words) {
    contains_word_linear(words, w);
  }
  auto end_time = std::chrono::steady_clock::now();
  std::chrono::duration<double> elapsed_seconds = end_time - start_time;
  return elapsed_seconds.count();
}

// Returns the number of seconds to search for all `sample_words` in `words`.
double time_std_find(const vector<string>& words, const vector<string>& sample_words) {
  auto start_time = std::chrono::steady_clock::now();
  for (const string& w : sample_words) {
    std::find(words.begin(), words.end(), w);
  }
  auto end_time = std::chrono::steady_clock::now();
  std::chrono::duration<double> elapsed_seconds = end_time - start_time;
  return elapsed_seconds.count();
}

int main(int argc, const char* argv[]) {
  const int sample_size = 10000;
  const char* words_filename = argc > 1 ? argv[1] : "words.txt";
  // Output a CSV that can be graphed.
  cout << "\"Number of words\",contains_word_linear,std::find\n";
  for (int n = 1; n < 1000000; n *= 2) {
      vector<string> words = read_lines(words_filename, n);
      vector<string> random_words = get_random_words(words, sample_size);
      cout
          << words.size() << ","
          << time_contains_word_linear(words, random_words) << ","
          << time_std_find(words, random_words) << '\n';
  }
  return 0;
}
