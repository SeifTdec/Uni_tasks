#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high]; 
    int i = (low - 1); 

    for (int j = low; j <= high - 1; j++) {
        if (arr[j] <= pivot) {
            i++; 
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return (i + 1);
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

int main() {
    vector<int> data = {12, 4, 5, 6, 7, 3, 1, 15};
    
    cout << "Unsorted array: ";
    for (int x : data) cout << x << " ";
    
    quickSort(data, 0, data.size() - 1);
    
    cout << "\nSorted array:   ";
    for (int x : data) cout << x << " ";
    
    return 0;
}
