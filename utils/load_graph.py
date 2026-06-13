def load_graph_from_file(filepath):
    """
    Загружает граф из файла и возвращает:
    1. Список смежности вида: adj_list[u] = [(v, weight), ...]
    2. Количество вершин (n)
    3. Количество ребер (m)
    """
    adj_list = {}
    n = 0
    m = 0
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
        if not lines:
            return [], 0, 0
            
        parts = lines[0].split()
        n = int(parts[0])
        m = int(parts[1])
        
        for i in range(n):
            adj_list[i] = []
            
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 3:
                u = int(parts[0])
                v = int(parts[1])
                w = int(parts[2])
                
                adj_list[u].append((v, w))
                adj_list[v].append((u, w))
                
    adj_array = [adj_list[i] for i in range(n)]
    
    return adj_array, n, m


def get_edges_from_adj(adj_list):
    """Конвертация списка смежности в список ребер для Краскала"""
    edges = []
    seen = set()
    for u, neighbors in enumerate(adj_list):
        for v, w in neighbors:
            if (v, u) not in seen:
                edges.append((u, v, w))
                seen.add((u, v))
    return edges
