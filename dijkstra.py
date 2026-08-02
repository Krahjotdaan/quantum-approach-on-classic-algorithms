import heapq
from quantum_core import durr_hoyer_argmin


def dijkstra_classic_heap(adj_list, start_node):
    n = len(adj_list)
    dist = [float('inf')] * n
    dist[start_node] = 0
    pq = [(0, start_node)]
    ops = 0
    while pq:
        d, u = heapq.heappop(pq)
        ops += 1
        if d > dist[u]:
            continue
        for v, w in adj_list[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
                ops += 1
    return dist, ops


def dijkstra_quantum(adj_list, start_node):
    n = len(adj_list)
    dist = [float('inf')] * n
    visited = [False] * n
    dist[start_node] = 0

    ops_counter = [0]

    for _ in range(n):
        candidates = [i for i in range(n) if not visited[i]]
        u = durr_hoyer_argmin(dist, candidates, ops_counter)
        if u == -1 or dist[u] == float('inf'):
            break
        visited[u] = True

        for v, w in adj_list[u]:
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    return dist, ops_counter[0]
