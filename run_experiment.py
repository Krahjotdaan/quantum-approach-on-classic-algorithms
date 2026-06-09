import os
import re
import time
import matplotlib.pyplot as plt
import numpy as np
from load_graph import *  

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


def run_experiment(algorithms_dict, graph_types=['sparse', 'dense'], base_dir=".dataset"):
    results = {}
    
    for algo_name in algorithms_dict.keys():
        results[algo_name] = {t: [] for t in graph_types}
    
    for g_type in graph_types:
        dir_path = os.path.join(base_dir, g_type)
        if not os.path.exists(dir_path):
            print(f"Папка {dir_path} не найдена.")
            continue
            
        available_sizes = sorted([int(f.split('_')[1][1:]) for f in os.listdir(dir_path) 
                                  if f.startswith('graph_n') and f.endswith('.txt')])
        
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
    
    algo_colors =  ['red', 'darkblue']
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
    
    algo_colors = ['red', 'darkblue']
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


def plot_speedup_ratio(results, ref_algo_name, test_algo_name, graph_types=['sparse', 'dense']):
    colors = {'sparse': 'green', 'dense': 'red'}
    
    for g_type in graph_types:
        plt.figure(figsize=(10, 6))
        
        if g_type in results[ref_algo_name] and g_type in results[test_algo_name]:
            raw_ref = results[ref_algo_name][g_type]
            raw_test = results[test_algo_name][g_type]
            
            ratios_by_n = {}
            
            for d_ref in raw_ref:
                n = d_ref['n']
                ops_r = d_ref['ops']
                
                candidates = [d_t for d_t in raw_test if d_t['n'] == n]
                
                if not candidates: continue
                
                for d_t in candidates:
                    ops_t = d_t['ops']
                    ratio = ops_r / ops_t if ops_t > 0 else 1.0
                    
                    if n not in ratios_by_n:
                        ratios_by_n[n] = []
                    ratios_by_n[n].append(ratio)
            
            ns_sorted = sorted(ratios_by_n.keys())
            avg_ratios = [np.mean(ratios_by_n[n]) for n in ns_sorted]
            
            label = f"{'Разреженный' if g_type=='sparse' else 'Плотный'}"
            plt.plot(ns_sorted, avg_ratios, marker='s', linestyle='--', 
                     color=colors.get(g_type, 'blue'), label=label, linewidth=2)
            
            plt.axhline(y=1, color='black', linestyle=':', linewidth=1)
            type_label = "Разреженные графы" if g_type == 'sparse' else "Плотные графы"
            plt.title(f"Выигрыш {test_algo_name} над {ref_algo_name}\n({type_label})")
            plt.xlabel('Вершины (V)')
            plt.ylabel('Коэффициент ускорения (Classic Ops / Quantum Ops)')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        else:
            print(f"Нет данных для построения графика ускорения ({g_type}).")
