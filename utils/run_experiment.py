import os
import re
import time
import matplotlib.pyplot as plt
import numpy as np
from utils.load_graph import *  


PROJECT_ROOT = os.path.join(os.path.dirname(os.getcwd()), 'impovement-on-algos-by-quantum-approach')
BASE_DIR = os.path.join(PROJECT_ROOT, ".dataset")

def get_available_sizes(base_dir, graph_type):
    dir_path = os.path.join(base_dir, graph_type)
    if not os.path.exists(dir_path):
        return []
    
    sizes = set()
    pattern = re.compile(r"graph_n(\d+)_")
    
    for filename in os.listdir(dir_path):
        match = pattern.search(filename)
        if match:
            sizes.add(int(match.group(1)))
            
    return sorted(list(sizes))


def run_experiment(algorithms_dict, graph_types=['sparse', 'dense'], base_dir=BASE_DIR):
    results = {}
    
    for algo_name in algorithms_dict.keys():
        results[algo_name] = {t: [] for t in graph_types}
    
    for g_type in graph_types:
        dir_path = os.path.join(base_dir, g_type)
        if not os.path.exists(dir_path):
            print(f"Папка {dir_path} не найдена.")
            continue
            
        pattern = re.compile(r"graph_n(\d+)_")
        available_sizes = sorted([
            int(match.group(1)) 
            for f in os.listdir(dir_path) 
            if f.startswith('graph_n') and f.endswith('.txt') 
            and (match := pattern.search(f))
        ])
        
        for n in available_sizes:
            target_files = [f for f in os.listdir(dir_path) if f.startswith(f"graph_n{n}_")]
            
            if not target_files: continue
                
            for fname in target_files:
                filepath = os.path.join(dir_path, fname)
                try:
                    adj_list, n_ver, m_edg = load_graph_from_file(filepath)
                    edges = get_edges_from_adj(adj_list)
                    
                    for algo_name, algo_func in algorithms_dict.items():
                        start_t = time.perf_counter()
                        _, ops = algo_func(adj_list, n_ver, edges)
                        end_t = time.perf_counter()
                        
                        elapsed = end_t - start_t
                        
                        results[algo_name][g_type].append({
                            'n': n_ver,
                            'ops': ops,
                            'time': elapsed,
                            'file': fname
                        })
                        
                except Exception as e:
                    print(f"Ошибка {filepath}: {e}")
                
    return results


def plot_time(results, graph_types=['sparse', 'dense']):
    num_algos = len(results)
    if num_algos == 0: 
        return
    
    algo_colors =  ['red', 'darkblue', 'coral', 'lightblue', 'gold', 'black']
    algo_names = list(results.keys())

    for g_type in graph_types:
        plt.figure(figsize=(12, 6))
        plotted_anything = False
        
        for idx, algo_name in enumerate(algo_names):
            raw_data = results[algo_name].get(g_type, [])
            if not raw_data:
                continue
            
            ns_unique = sorted(set(d['n'] for d in raw_data))
            medians = []
            p25 = []
            p75 = []
            
            for n in ns_unique:
                times = [d['time'] for d in raw_data if d['n'] == n]
                if times:
                    medians.append(np.median(times))
                    p25.append(np.percentile(times, 25))
                    p75.append(np.percentile(times, 75))
            
            color = algo_colors[idx % len(algo_colors)]
            plt.plot(ns_unique, medians, marker='o', linestyle='-', 
                     color=color, label=algo_name, linewidth=2)
            plt.fill_between(ns_unique, p25, p75, alpha=0.3, color=color)
            plotted_anything = True
        
        if plotted_anything:
            type_label = "Разреженные графы (Sparse)" if g_type == 'sparse' else "Плотные графы (Dense)"
            plt.title(f"Время выполнения\n{type_label}")
            plt.xlabel('Вершины (V)')
            plt.ylabel('Время (секунды)')
            plt.legend(loc='upper left', fontsize=10)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        else:
            print(f"Нет данных для типа графа: {g_type}")


def plot_results(results, graph_types=['sparse', 'dense'], title_prefix="Сравнение алгоритмов"):
    num_algos = len(results)
    if num_algos == 0: 
        return
    
    algo_colors = ['red', 'darkblue', 'coral', 'lightblue', 'gold', 'black']
    algo_names = list(results.keys())

    for g_type in graph_types:
        plt.figure(figsize=(10, 6))
        plotted_anything = False
        
        for idx, algo_name in enumerate(algo_names):
            data = results[algo_name].get(g_type, [])
            if not data:
                continue
            
            ns = [d['n'] for d in data]
            ops = [d['ops'] for d in data]
            
            label = algo_name
            color = algo_colors[idx % len(algo_colors)]
            
            plt.plot(ns, ops, marker='o', linestyle='-', 
                     color=color, label=label, linewidth=2)
            plotted_anything = True
        
        if plotted_anything:
            type_label = "Разреженные графы (Sparse)" if g_type == 'sparse' else "Плотные графы (Dense)"
            plt.title(f"{title_prefix}\n{type_label}")
            plt.xlabel('Вершины (V)')
            plt.ylabel('Условные операции')
            plt.legend(loc='upper left', fontsize=10)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        else:
            print(f"Нет данных для типа графа: {g_type}")
