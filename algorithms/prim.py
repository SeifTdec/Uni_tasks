import heapq
from collections import defaultdict

def prims_algorithm(graph, start=0):
    visited = set()
    min_heap = [(0, start, -1)]  
    mst_edges = []
    total_cost = 0

    while min_heap:
        cost, u, parent = heapq.heappop(min_heap)

        if u in visited:
            continue

        visited.add(u)
        total_cost += cost

        if parent != -1:
            mst_edges.append((parent, u, cost))

        for neighbor, weight in graph[u]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (weight, neighbor, u))

    return mst_edges, total_cost

graph = defaultdict(list)
edges = [
    (0, 1, 2), (0, 3, 6),
    (1, 2, 3), (1, 3, 8), (1, 4, 5),
    (2, 4, 7),
    (3, 4, 9)
]

for u, v, w in edges:
    graph[u].append((v, w))
    graph[v].append((u, w))  

mst, cost = prims_algorithm(graph, start=0)

print("MST Edges:")
for u, v, w in mst:
    print(f"  {u} -- {v}  (weight: {w})")
print(f"Total MST Cost: {cost}")
