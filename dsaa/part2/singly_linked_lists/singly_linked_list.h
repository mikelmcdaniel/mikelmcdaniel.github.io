#include <exception>

template <typename T>
struct LinkedListNode {
  T value;
  LinkedListNode<T> *next;

  LinkedListNode(const T& value) : value(value), next(nullptr) {}
};

template <typename T>
class LinkedList {
  LinkedListNode<T> *head, *tail;

  class Iterator {
    LinkedListNode<T> *cur;
  public:
    Iterator(LinkedListNode<T> * cur) : cur(cur) {}
    // Check for inequality
    bool operator!=(const Iterator& other) {
      return cur != other.cur;
    }
    // Increment (e.g. ++it)
    Iterator& operator++() {
      cur = cur->next;
      return *this;
    }
    // Dereference (e.g. *it)
    T& operator*() {
      return cur->value;
    }
  };

public:
  LinkedList() : head(nullptr), tail(nullptr) {}

  ~LinkedList() {
    for(LinkedListNode<T> *cur = head, *next; cur != nullptr; cur = next) {
      next = cur->next;
      delete cur;
    }
  }

  void pop_front() {
    // Let's assume head != nullptr
    // TODO: Sublcass std::exception and throw an exception with a proper error message.
    if (head == nullptr) {
      throw std::exception();
    }
    LinkedListNode<T> *old_head = head;
    head = head->next;
    delete old_head;
  }

  void push_back(const T& value) {
    LinkedListNode<T> *new_node = new LinkedListNode<T>(value);
    if (tail == nullptr) {  // if the list is empty
      head = tail = new_node;
    } else {
      tail->next = new_node;
      tail = new_node;
    }
  }

  Iterator begin() {
    return Iterator(head);
  }

  Iterator end() {
    return Iterator(nullptr);
  }
};
