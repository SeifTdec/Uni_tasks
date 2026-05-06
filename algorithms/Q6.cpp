#include <bits/stdc++.h>
using namespace std;

void backtrack(string &letters, vector<bool> &used, string &current) {
    if (current.size() == letters.size()) {
        cout << current << '\n';
        return;
    }

    for (int i = 0; i < (int)letters.size(); i++) {
        if (used[i]) continue;
        if (i > 0 && letters[i] == letters[i - 1] && !used[i - 1]) continue;

        used[i] = true;
        current.push_back(letters[i]);

        backtrack(letters, used, current);

        current.pop_back();
        used[i] = false;
    }
}

int main() {
    string letters = "exhausted";
    sort(letters.begin(), letters.end());

    vector<bool> used(letters.size(), false);
    string current;

    backtrack(letters, used, current);

    return 0;
}
