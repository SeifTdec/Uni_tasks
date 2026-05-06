#include <bits/stdc++.h>
using namespace std;
bool dfs(int u, int targetK, int sum,
         vector<vector<pair<int,int>>> &adj,
         vector<bool> &visited) {
    if (sum > targetK) return true;
    visited[u] = true;

    for (auto &edge : adj[u]) {
        int v = edge.first;
        int w = edge.second;

        if (!visited[v]) {
            if (dfs(v, targetK, sum + w, adj, visited))
                return true;
        }
    }
    visited[u] = false; 
    return false;
}

int main() {
    int n = 9; // nodes 0..8
    vector<vector<pair<int,int>>> adj(n);

    auto addEdge = [&](int u, int v, int w) {
        adj[u].push_back({v, w});
        adj[v].push_back({u, w}); 
    };

    addEdge(0, 1, 4);
    addEdge(0, 7, 8);
    addEdge(1, 2, 8);
    addEdge(1, 7, 11);
    addEdge(2, 3, 7);
    addEdge(2, 8, 2);
    addEdge(2, 5, 4);
    addEdge(3, 4, 9);
    addEdge(3, 5, 14);
    addEdge(4, 5, 10);
    addEdge(5, 6, 2);
    addEdge(6, 7, 1);
    addEdge(6, 8, 6);
    addEdge(7, 8, 7);

    vector<int> tests = {20, 30, 60};

    for (int K : tests) {
        vector<bool> visited(n, false);
        bool ok = dfs(0, K, 0, adj, visited);
        cout << "K = " << K << " -> " << (ok ? "YES" : "NO") << '\n';
    }

    return 0;
}
