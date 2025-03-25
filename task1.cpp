#include <iostream>
using namespace std;

class Node {
    public:
        int data;
        Node* next;
        Node(int val) : data(val), next(NULL) {}
};

class LinkedList {
    private:
        Node* head;
    public:
        LinkedList() : head(NULL) {}

        bool isEmpty() {
            return head == NULL;
        }

        void insertBegin(int val) {
            Node* newNode = new Node(val);
            newNode->next = head;
            head = newNode;
        }

        void insertBefore(int target, int val) {
            if (head == NULL) return;

            if (head->data == target) {
                insertBegin(val);
                return;
            }

            Node* current = head;
            Node* prev = NULL;

            while (current != NULL && current->data != target) {
                prev = current;
                current = current->next;
            }

            if (current != NULL) {
                Node* newNode = new Node(val);
                prev->next = newNode;
                newNode->next = current;
            }
        }

        void append(int val) {
            Node* newNode = new Node(val);

            if (head == NULL) {
                head = newNode;
                return;
            }

            Node* current = head;
            while (current->next != NULL) {
                current = current->next;
            }
            current->next = newNode;
        }

        bool search(int val) {
            Node* current = head;
            while (current != NULL) {
                if (current->data == val) {
                    return true;
                }
                current = current->next;
            }
            return false;
        }

        void display() {
            Node* current = head;
            while (current != NULL) {
                cout << current->data << " ";
                current = current->next;
            }
            cout << "\n";
        }

        int count() {
            int count = 0;
            Node* current = head;
            while (current != NULL) {
                count++;
                current = current->next;
            }
            return count;
        }

        ~LinkedList() {
            Node* current = head;
            while (current != NULL) {
                Node* nextNode = current->next;
                delete current;
                current = nextNode;
            }
        }
};

int main() {
    LinkedList list;
    list.insertBegin(5);   
    list.insertBegin(8);   
    list.insertBefore(5, 3);
    list.append(7); 
    cout << "Elements in the list: ";
    list.display();   
    cout << "Search for 5: " << (list.search(5) ? "Found" : "Not Found") << "\n"; 
    cout << "Search for 10: " << (list.search(10) ? "Found" : "Not Found") << "\n"; 
    cout << "Elements: " << list.count() <<"\n"; 
    return 0;
}