#include <iostream>
using namespace std;

struct CDLLNode {
    int data;
    CDLLNode* next;
    CDLLNode* prev;
};

class CircularDoublyLinkedList {
private:
    CDLLNode* head;

public:
    CircularDoublyLinkedList() : head(NULL) {}

    bool isEmpty() {
        return head == NULL;
    }

    void insertAtBeginning(int data) {
        CDLLNode* newNode = new CDLLNode{data, NULL, NULL};
        if (!head) {
            newNode->next = newNode->prev = newNode;
            head = newNode;
            return;
        }

        CDLLNode* last = head->prev;
        newNode->next = head;
        newNode->prev = last;
        head->prev = newNode;
        last->next = newNode;
        head = newNode;
    }

    void append(int data) {
        CDLLNode* newNode = new CDLLNode{data, NULL, NULL};
        if (!head) {
            newNode->next = newNode->prev = newNode;
            head = newNode;
            return;
        }

        CDLLNode* last = head->prev;
        newNode->next = head;
        head->prev = newNode;
        newNode->prev = last;
        last->next = newNode;
    }

    void display() {
        if (!head) {
            cout << "empty" << endl;
            return;
        }

        CDLLNode* temp = head;
        do {
            cout << temp->data << " <-> ";
            temp = temp->next;
        } while (temp != head);
        cout << "head" << endl;
    }

    int count() {
        if (!head) return 0;
        int c = 0;
        CDLLNode* temp = head;
        do {
            c++;
            temp = temp->next;
        } while (temp != head);
        return c;
    }
};
