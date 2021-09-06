#pragma once

template <typename T>
class TemplateVector {
  int capacity, size_;
  T* values;

public:
  int ops_counter;

  TemplateVector() : capacity(1), size_(0), ops_counter(0) {
    values = new T[capacity];
  }
  ~TemplateVector() {
    delete[] values;
  }

  void push_back(const T& value) {
    ++ops_counter;
    if (size_ >= capacity) {
      // Create a new bigger
      ops_counter += 2 * capacity + 3;
      const int new_capacity = 2 * capacity;
      T *new_lines = new T[new_capacity];
      // Copy everything to the big array
      for (int i = 0; i < size_; ++i) {
        ++ops_counter;
        new_lines[i] = values[i];
      }
      // Delete old array
      ops_counter += capacity;
      delete[] values;
      // Make lines point to new array
      ops_counter += 2;
      values = new_lines;
      capacity = new_capacity;
    }
    ++ops_counter;
    values[size_] = value;
    ++ops_counter;
    ++size_;
  }

  T* begin() {
    return values; // same as &strs[0]
  }

  T* end() {
    return values + size_; // same as &strs[size]
  }

  T& operator[](int index) {
    return values[index];
  }

  int size() {
    return size_;
  }
};
