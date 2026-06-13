import os
import random
import networkx as nx

def generate_and_save_graphs(base_dir=".dataset", dense_sizes=range(50, 301, 50), sparse_sizes=range(100, 1501, 100), seed=42):
    """
    Генерирует разреженные и плотные графы и сохраняет их в файлы.
    """
    sparse_dir = os.path.join(base_dir, "sparse")
    dense_dir = os.path.join(base_dir, "dense")
    os.makedirs(sparse_dir, exist_ok=True)
    os.makedirs(dense_dir, exist_ok=True)
    
    for n in sparse_sizes:
        # --- 1. Разреженный граф (Sparse) ---
        # Используем модель Барбаши-Альберт для получения связного разреженного графа
        G_sparse = nx.barabasi_albert_graph(n, 2, seed=seed)
        
        for u, v in G_sparse.edges():
            G_sparse[u][v]['weight'] = random.randint(1, 10)
            
        filename_sparse = f"graph_n{n}_sparse.txt"
        save_graph_to_file(G_sparse, os.path.join(sparse_dir, filename_sparse))
    
    for n in dense_sizes:
        # --- 2. Плотный граф (Dense) ---
        # Используем модель Эрдёша-Реньи с высокой вероятностью соединения
        p_prob = 0.5
        G_dense = nx.erdos_renyi_graph(n, p_prob, seed=seed)
        
        # Гарантируем связность 
        if not nx.is_connected(G_dense):
            T = nx.minimum_spanning_tree(G_dense)
            G_dense.add_edges_from(T.edges())
            
        # Добавляем случайные веса
        for u, v in G_dense.edges():
            G_dense[u][v]['weight'] = random.randint(1, 10)
            
        filename_dense = f"graph_n{n}_dense.txt"
        save_graph_to_file(G_dense, os.path.join(dense_dir, filename_dense))
        
def save_graph_to_file(G, filepath):
    n = G.number_of_nodes()
    m = G.number_of_edges()
    
    with open(filepath, 'w') as f:
        f.write(f"{n} {m}\n")
        for u, v, data in G.edges(data=True):
            w = data.get('weight', 1)
            f.write(f"{u} {v} {w}\n")

generate_and_save_graphs()
