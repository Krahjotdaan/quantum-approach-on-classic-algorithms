from quantum_core import durr_hoyer_argmin


def adj_to_matrix(adj_list):
    n = len(adj_list)
    INF = float('inf')
    mat = [[INF] * n for _ in range(n)]
    for i in range(n):
        mat[i][i] = 0
    for u in range(n):
        for v, w in adj_list[u]:
            if w < mat[u][v]:
                mat[u][v] = w
    return mat


def floyd_warshall_classic(matrix):
    n = len(matrix)
    dist = [row[:] for row in matrix]
    ops = 0
    for k in range(n):
        for i in range(n):
            if dist[i][k] == float('inf'):
                continue
            for j in range(n):
                ops += 1
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
    return dist, ops


def floyd_warshall_quantum(matrix):
    n = len(matrix)
    dist = [row[:] for row in matrix]
    if n == 0:
        return dist, 0

    ops_counter = [0]

    for k in range(n):
        for i in range(n):
            if dist[i][k] == float('inf'):
                continue

            for _sub in range(n):
                scores = []
                candidates = []
                for j in range(n):
                    val = dist[i][k] + dist[k][j]
                    scores.append(val)
                    if val < dist[i][j]:
                        candidates.append(j)

                if not candidates:
                    break

                best_j = durr_hoyer_argmin(scores, candidates, ops_counter)
                if best_j == -1:
                    break

                new_dist = dist[i][k] + dist[k][best_j]
                if new_dist < dist[i][best_j]:
                    dist[i][best_j] = new_dist

    return dist, ops_counter[0]
