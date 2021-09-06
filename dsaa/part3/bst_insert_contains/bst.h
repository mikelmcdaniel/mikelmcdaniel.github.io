#ifndef BST_H_
#define BST_H_

#include <iostream>

using std::cout;
using std::endl;

template <typename T>
class BinarySearchTree {
  struct Node {
    T value;
    Node *left, *right;
    Node(const T& value) : value(value), left(nullptr), right(nullptr) {}

    void print() {
      if (left != nullptr) {
        left->print();
      }
      cout << value << endl;
      if (right != nullptr) {
        right->print();
      }
    }

    bool contains(const T& v) {
      if (v == value) {
        return true;
      } else if (v < value) {
        if (left == nullptr) {
          return false;
        } else {
          return left->contains(v);
        }
      } else { // if (v > value)
        if (right == nullptr) {
          return false;
        } else {
          return right->contains(v);
        }
      }
    }

    bool insert(const T& new_value) {
      if (new_value == value) {
        return false;
      } else if (new_value < value) {  // Need to insert to the left
        if (left == nullptr) {
          left = new Node(new_value);
          return true;
        } else {
          return left->insert(new_value);
        }
      } else { // if (new_value > value)  Need to insert to the right
        if (right == nullptr) {
          right = new Node(new_value);
          return true;
        } else {
          return right->insert(new_value);
        }
      }
    }
  };

  Node *root;

public:
  BinarySearchTree() : root(nullptr) {}

  ~BinarySearchTree() {
    delete root;
  }

  void print() {
    if (root != nullptr) {
      root->print();
    }
  }

  bool insert(const T& value) {
    if (root == nullptr) {
      root = new Node(value);
      return true;
    } else {
      return root->insert(value);
    }
  }

  bool contains(const T& value) {
    if (root == nullptr) {
      return false;
    } else {
      return root->contains(value);
    }
  }
};

#endif /* BST_H_ */
