#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

double findMedian(vector<int>& nums1, vector<int>& nums2) {
    int n = nums1.size();
    int m = nums2.size();
    int total = n + m;
    int idx1 = total / 2;         
    int idx2 = idx1 - 1;         
    int i = 0, j = 0;            
    int count = 0;               
    int prev = 0, curr = 0;         
    
    while (i < n && j < m) {
        if (nums1[i] <= nums2[j]) {
            curr = nums1[i];
            i++;
        } else {
            curr = nums2[j];
            j++;
        }
        if (count == idx2) {
            prev = curr;
        }
        if (count == idx1) {
            break;
        }
        count++;
    }
    while (i < n && count <= idx1) {
        curr = nums1[i];
        if (count == idx2) prev = curr;
        if (count == idx1) break;
        i++;
        count++;
    }
    while (j < m && count <= idx1) {
        curr = nums2[j];
        if (count == idx2) prev = curr;
        if (count == idx1) break;
        j++;
        count++;
    }
    if (total % 2 == 1) {
        return curr;
    } else {
        return (prev + curr) / 2.0;
    }
}

int main() {
    vector<int> A = {1, 3, 8};
    vector<int> B = { 9, 10, 11};
    cout << "Median: " << findMedian(A, B) << endl; 
    
    
    return 0;
}
