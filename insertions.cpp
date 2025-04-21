#include <iostream>
using namespace std;

int main() {
    int arr[6];
    cout << "Enter numbers: " << endl;
    for (int i = 0; i < 6; ++i) {
        cin >> arr[i];
    }
    for (int i = 1; i < 6; ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }

    cout << "Sorted array: ";
    for (int i = 0; i < 6; ++i) {
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}
