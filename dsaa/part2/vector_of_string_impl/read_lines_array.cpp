#include <iostream>  // std::cout, std::endl
#include <exception>  // std::exception
#include <fstream>  // std::ifstream
#include <string>  // std::string
#include <utility>  // std::pair, std::make_pair
#include <vector>  // std::vector

using std::cout;
using std::endl;
using std::exception;
using std::ifstream;
using std::make_pair;
using std::pair;
using std::string;
using std::vector;


// It's good to subclass on an existing exception type when you write a library
// so people using your code can choose to catch the specific exception type.
class read_lines_exception : public exception {
  string what_str;
public:
  read_lines_exception(const string& what_str) : what_str(what_str) {}
  const char* what() const noexcept override {
    return what_str.c_str();
  }
};


// Returns an array of lines (strings) and the number of lines.
// If we just returned the pointer to the strings, then the caller wouldn't know
// how many lines we read fromt he file, so we return both.
pair<string*, int> read_lines_array(const string& filepath) {
  ifstream f(filepath);
  // We don't know how many lines are in the file, so we need an array that we
  // can resize somehow... Arrays don't really support resizing but if we create
  // an array and need more space, we can create a new[] bigger array, copy
  // everything to the new array, then delete[] the old array.
  //
  // No matter how big we make the original array, it might have to get bigger,
  // so let's just start with a capacity (number of lines we can fit) of 1.
  int lines_capacity = 1;
  // We also need to keep track of how many lines we have so far.
  int lines_size = 0;
  string *lines = new string[lines_capacity];
  if (f.fail()) {
    throw read_lines_exception("Could not open file " + filepath);
  }
  for(string line; getline(f, line); ) {
    // Now we need to add the line to our array
    // It's possible that there's no more space, so we need to check that first.
    if (lines_size >= lines_capacity) {
      // "Resize" lines by creating a new array, copying all the lines to the
      // new array, then deleting the old array.
      // Create a new array with more capacity.
      const int new_lines_capacity = lines_capacity * 2;
      string *new_lines = new string[new_lines_capacity];
      // Copy existing lines
      for (int i = 0; i < lines_capacity; ++i) {
        new_lines[i] = lines[i];
      }
      // Delete old lines
      delete[] lines;
      // Update lines/capacity to point to the new lines/capacity.
      lines = new_lines;
      lines_capacity = new_lines_capacity;
    }
    // Add the line to our array.
    lines[lines_size] = line;
    ++lines_size;
  }
  if (f.bad()) {
    throw read_lines_exception("Failed to read all lines in " + filepath);
  }
  return make_pair(lines, lines_size);
}


class StringVector {
  // We need to keep track of how much room is in the array (capacity)
  // and the number of elements in the array (size_).
  int capacity, size_;
  string *strs;

public:
  StringVector() : capacity(1), size_(0) {
    strs = new string[capacity];
  }

  // Don't forget to delete dynamically allocated arrays when we're done using
  // them! Alternatively, use an std::unique_ptr.
  ~StringVector() {
    delete[] strs;
  }

  void push_back(const string& str) {
    if (size_ >= capacity) {
      const int new_capacity = 2 * capacity;
      string *new_strs = new string[new_capacity];
      for (int i = 0; i < size_; ++i) {
        new_strs[i] = strs[i];
      }
      delete[] strs;
      strs = new_strs;
      capacity = new_capacity;
    }
    strs[size_] = str;
    ++size_;
  }

  string& operator[](int index) {
    return strs[index];
  }

  int size() {
    return size_;
  }

  string* begin() {
    return strs;  // same as &strs[0]
  }

  string* end() {
    return strs + size_;  // same as &strs[size_]
  }
};


StringVector read_lines_string_vector(const string& filepath) {
  ifstream f(filepath);
  StringVector lines;
  if (f.fail()) {
    throw read_lines_exception("Could not open file " + filepath);
  }
  for(string line; getline(f, line); ) {
    lines.push_back(line);
  }
  if (f.bad()) {
    throw read_lines_exception("Failed to read all lines in " + filepath);
  }
  return lines;
}


template<typename T>
class TemplateVector {
  int capacity, size_;
  T *values;

public:
  TemplateVector() : capacity(1), size_(0) {
    values = new T[capacity];
  }

  ~TemplateVector() {
    delete[] values;
  }

  void push_back(const T& value) {
    if (size_ >= capacity) {
      const int new_capacity = 2 * capacity;
      T *new_values = new T[new_capacity];
      for (int i = 0; i < size_; ++i) {
        new_values[i] = values[i];
      }
      delete[] values;
      values = new_values;
      capacity = new_capacity;
    }
    values[size_] = value;
    ++size_;
  }

  T& operator[](int index) {
    return values[index];
  }

  int size() {
    return size_;
  }

  T* begin() {
    return values;  // same as &values[0]
  }

  T* end() {
    return values + size_;  // same as &values[size_]
  }
};


TemplateVector<string> read_lines_template_vector(const string& filepath) {
  ifstream f(filepath);
  TemplateVector<string> lines;
  if (f.fail()) {
    throw read_lines_exception("Could not open file " + filepath);
  }
  for(string line; getline(f, line); ) {
    lines.push_back(line);
  }
  if (f.bad()) {
    throw read_lines_exception("Failed to read all lines in " + filepath);
  }
  return lines;
}


vector<string> read_lines_std_vector(const string& filepath) {
  ifstream f(filepath);
  vector<string> lines;
  if (f.fail()) {
    throw read_lines_exception("Could not open file " + filepath);
  }
  for(string line; getline(f, line); ) {
    lines.push_back(line);
  }
  if (f.bad()) {
    throw read_lines_exception("Failed to read all lines in " + filepath);
  }
  return lines;
}


int main(int argc, const char *argv[]) {
  string filepath = argc > 1 ?  argv[1] : "truth.txt";

  auto lines_and_size = read_lines_array(filepath);
  string* lines = lines_and_size.first;
  int num_lines = lines_and_size.second;
  cout << "read_lines_array:" << endl;
  for (int i = 0; i < num_lines; ++i) {
    cout << lines[i] << endl;
  }
  cout << endl;
  delete[] lines;

  cout << "read_lines_string_vector:" << endl;
  for (const string& line : read_lines_string_vector(filepath)) {
    cout << line << endl;
  }
  cout << endl;

  cout << "read_lines_template_vector:" << endl;
  for (const string& line : read_lines_template_vector(filepath)) {
    cout << line << endl;
  }
  cout << endl;

  cout << "read_lines_std_vector:" << endl;
  for (const string& line : read_lines_std_vector(filepath)) {
    cout << line << endl;
  }
  return 0;
}
