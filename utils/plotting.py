"""
Функции построения графиков сравнения classic vs quantum (Dürr–Høyer)
для алгоритмов кратчайших путей: время исполнения и число условных операций.
"""

import matplotlib.pyplot as plt


def plot_comparison_time(classic_res, quantum_res, algo_name, g_type,
                          classic_label=None, quantum_label=None, save_dir=None):
    """
    classic_res / quantum_res: {'n': [...], 'time': [...], 'ops': [...]}
    (для одного конкретного graph_type, уже отфильтрованные)
    """
    type_label = "Разреженные графы (Sparse)" if g_type == "sparse" else "Плотные графы (Dense)"
    classic_label = classic_label or f"{algo_name} Classic"
    quantum_label = quantum_label or f"{algo_name} Quantum (Dürr–Høyer)"

    plt.figure(figsize=(10, 6))
    plt.plot(classic_res['n'], classic_res['time'], marker='o', linestyle='-',
              color='darkblue', label=classic_label, linewidth=2)
    plt.plot(quantum_res['n'], quantum_res['time'], marker='o', linestyle='-',
              color='red', label=quantum_label, linewidth=2)
    plt.title(f"{algo_name}: время исполнения\n{type_label}")
    plt.xlabel('Вершины (V)')
    plt.ylabel('Время (секунды)')
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    if save_dir:
        fname = f"{save_dir}/{algo_name.lower().replace(' ', '_')}_{g_type}_time.png"
        plt.savefig(fname, dpi=120)
    plt.show()
    plt.close()


def plot_comparison_ops(classic_res, quantum_res, algo_name, g_type,
                         classic_label=None, quantum_label=None, save_dir=None):
    """
    classic_res / quantum_res: {'n': [...], 'time': [...], 'ops': [...]}
    (для одного конкретного graph_type, уже отфильтрованные)
    """
    type_label = "Разреженные графы (Sparse)" if g_type == "sparse" else "Плотные графы (Dense)"
    classic_label = classic_label or f"{algo_name} Classic"
    quantum_label = quantum_label or f"{algo_name} Quantum (Dürr–Høyer)"

    plt.figure(figsize=(10, 6))
    plt.plot(classic_res['n'], classic_res['ops'], marker='o', linestyle='-',
              color='darkblue', label=classic_label, linewidth=2)
    plt.plot(quantum_res['n'], quantum_res['ops'], marker='o', linestyle='-',
              color='red', label=quantum_label, linewidth=2)
    plt.title(f"{algo_name}: условные операции\n{type_label}")
    plt.xlabel('Вершины (V)')
    plt.ylabel('Условные операции')
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    if save_dir:
        fname = f"{save_dir}/{algo_name.lower().replace(' ', '_')}_{g_type}_ops.png"
        plt.savefig(fname, dpi=120)
    plt.show()
    plt.close()


def plot_comparison(classic_res_by_type, quantum_res_by_type, algo_name,
                     graph_types=('sparse', 'dense'), save_dir=None):
    """
    Удобная обёртка: для каждого graph_type строит оба графика (время и ops).

    classic_res_by_type / quantum_res_by_type:
        {graph_type: {'n': [...], 'time': [...], 'ops': [...]}}
    """
    for g_type in graph_types:
        c = classic_res_by_type.get(g_type)
        q = quantum_res_by_type.get(g_type)
        if not c or not c.get('n'):
            print(f"Нет данных для {g_type}, пропускаю графики")
            continue
        plot_comparison_time(c, q, algo_name, g_type, save_dir=save_dir)
        plot_comparison_ops(c, q, algo_name, g_type, save_dir=save_dir)
