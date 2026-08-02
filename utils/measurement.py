"""
Замер времени и числа операций для алгоритма по всем файлам датасета,
используется внутри shortest_ways.ipynb.
"""

import os
import re
import time

from utils.load_graph import load_graph_from_file, get_edges_from_adj


def list_dataset_files(base_dir, graph_types=('sparse', 'dense')):
    """Возвращает {graph_type: [(n, filepath), ...]} отсортированный по n."""
    files_by_type = {}
    pattern = re.compile(r"graph_n(\d+)_")
    for g_type in graph_types:
        dir_path = os.path.join(base_dir, g_type)
        if not os.path.exists(dir_path):
            files_by_type[g_type] = []
            continue
        found = []
        for fname in os.listdir(dir_path):
            m = pattern.search(fname)
            if m and fname.endswith(".txt"):
                found.append((int(m.group(1)), os.path.join(dir_path, fname)))
        found.sort(key=lambda x: x[0])
        files_by_type[g_type] = found
    return files_by_type


def measure_algorithm(algo_func, files_by_type, prepare_input, max_n=None):
    """
    algo_func(*args) -> (dist, ops)
    prepare_input(adj, n, edges) -> кортеж args для algo_func

    Возвращает {graph_type: {'n': [...], 'time': [...], 'ops': [...]}}
    """
    results = {}
    for g_type, files in files_by_type.items():
        ns, times, ops_list = [], [], []
        for n, filepath in files:
            if max_n is not None and n > max_n:
                continue
            adj, n_ver, m_edg = load_graph_from_file(filepath)
            edges = get_edges_from_adj(adj)
            args = prepare_input(adj, n_ver, edges)

            start_t = time.perf_counter()
            _, ops = algo_func(*args)
            elapsed = time.perf_counter() - start_t

            ns.append(n_ver)
            times.append(elapsed)
            ops_list.append(ops)

        results[g_type] = {'n': ns, 'time': times, 'ops': ops_list}
    return results


# --- Обёртки над prepare_input для каждого алгоритма ---

def dijkstra_input(adj, n, edges):
    return (adj, 0)


def bellman_ford_input(adj, n, edges):
    return (n, edges)


def floyd_warshall_input(adj, n, edges):
    from floyd_warshall import adj_to_matrix
    return (adj_to_matrix(adj),)
