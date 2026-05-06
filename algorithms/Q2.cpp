#include <bits/stdc++.h>
using namespace std;

void printPath(const vector<int>& path) {
    cout << "[ ";
    for (int i = 0; i < (int)path.size(); i++) {
        cout << path[i];
        if (i + 1 < (int)path.size()) cout << ", ";
    }
    cout << " ]\n";
}

void dfs(const vector<vector<int>>& grid, int r, int c, vector<int>& path) {
    int m = grid.size();
    int n = grid[0].size();

    path.push_back(grid[r][c]);

    if (r == m - 1 && c == n - 1) {
        printPath(path);
        path.pop_back();
        return;
    }
    if (r + 1 < m) {
        dfs(grid, r + 1, c, path);
    }
    if (c + 1 < n) {
        dfs(grid, r, c + 1, path);
    }
    if (r + 1 < m && c + 1 < n) {
        dfs(grid, r + 1, c + 1, path);
    }

    path.pop_back();
}

int main() {
    int m, n;
    cin >> m >> n;
    vector<vector<int>> grid(m, vector<int>(n));
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            cin >> grid[i][j];
        }
    }
    vector<int> path;
    dfs(grid, 0, 0, path);

    return 0;
}
