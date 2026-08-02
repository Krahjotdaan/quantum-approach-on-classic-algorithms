import random
import numpy as np


def grover_multi_mark(marked_mask: np.ndarray, initial_state: np.ndarray,
                       num_iterations: int) -> np.ndarray:
    state = initial_state.copy()
    for _ in range(num_iterations):
        state[marked_mask] *= -1 
        mean = np.mean(state)
        state = 2 * mean - state 
    return state


def durr_hoyer_argmin(scores, candidates, ops_counter=None, rng=random):
    if not candidates:
        return -1
    if len(candidates) == 1:
        if ops_counter is not None:
            ops_counter[0] += 1
        return candidates[0]

    n_items = len(scores)
    n_qubits = int(np.ceil(np.log2(max(n_items, 2))))
    N = 2 ** n_qubits
    initial_state = np.ones(N) / np.sqrt(N)

    y = rng.choice(candidates)
    max_rounds = max(1, int(np.ceil(np.sqrt(N))))

    for _ in range(max_rounds):
        target_val = scores[y] if y < n_items else float('inf')

        marked_mask = np.zeros(N, dtype=bool)
        for i in candidates:
            if scores[i] < target_val:
                marked_mask[i] = True

        num_marked = int(marked_mask.sum())
        if num_marked == 0:
            break

        m = 1.0
        lam = 6.0 / 5.0
        found = False
        measured_index = None
        max_attempts = int(np.ceil(2 * np.sqrt(N / max(num_marked, 1)))) + 5

        for _ in range(max_attempts):
            cap = max(1, int(np.ceil(m)))
            num_iters = rng.randint(0, cap - 1) if cap > 1 else 0

            if ops_counter is not None:
                ops_counter[0] += max(num_iters, 1)

            state = grover_multi_mark(marked_mask, initial_state, num_iters)
            probs = np.abs(state) ** 2
            probs = probs / probs.sum()
            measured_index = int(np.random.choice(N, p=probs))

            if measured_index < n_items and marked_mask[measured_index]:
                found = True
                break
            m = min(m * lam, np.sqrt(N))

        if found and measured_index is not None:
            y = measured_index

    return y
