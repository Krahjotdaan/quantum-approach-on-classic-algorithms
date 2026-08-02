from quantum_core import durr_hoyer_argmin


def bellman_ford_classic(n, edges, start=0):
    dist = [float('inf')] * n
    dist[start] = 0
    ops = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            ops += 1
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    return dist, ops


def bellman_ford_quantum(n, edges, start=0):
    dist = [float('inf')] * n
    dist[start] = 0
    E = len(edges)
    if E == 0:
        return dist, 0

    ops_counter = [0]

    # ВАЖНО: в отличие от классического Bellman-Ford, здесь за один "раунд"
    # релаксируется только ОДНО (самое выгодное) ребро, а не все рёбра сразу.
    # Поэтому n-1 раундов недостаточно для гарантированной сходимости --
    # используем цикл "пока есть кандидаты с gain > 0", с защитным пределом
    # (n-1)*E, чтобы отразить, что каждое ребро в худшем случае может
    # потребоваться релаксировать до n-1 раз, как в классике.
    max_rounds = (n - 1) * E
    for _round in range(max_rounds):
        scores = []
        candidates = []
        for i, (u, v, w) in enumerate(edges):
            if dist[u] == float('inf'):
                scores.append(float('inf'))
                continue
            new_dist = dist[u] + w
            if dist[v] == float('inf'):
                scores.append(-1e18 + new_dist)
                candidates.append(i)
                continue
            gain = dist[v] - new_dist
            scores.append(-gain) 
            if gain > 0:
                candidates.append(i)

        if not candidates:
            break

        best_idx = durr_hoyer_argmin(scores, candidates, ops_counter)
        if best_idx == -1:
            break

        u, v, w = edges[best_idx]
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w

    return dist, ops_counter[0]
