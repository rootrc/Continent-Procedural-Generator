import numpy as np

directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
distances = [1, np.sqrt(2), 1, np.sqrt(2), 1, np.sqrt(2), 1, np.sqrt(2)]

def get_top_n_high_points(height_map, n):
    flat_indices = np.argpartition(height_map.flatten(), -n)[-n:]
    return [np.unravel_index(i, height_map.shape) for i in flat_indices]

def compute_d8_flow_direction(height_map):
    rows, cols = height_map.shape
    flow_dir = -np.ones((rows, cols), dtype=int)
    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            max_slope = -np.inf
            best_dir = -1
            current_height = height_map[x, y]
            for idx, (dx, dy) in enumerate(directions):
                nx, ny = x + dx, y + dy
                neighbor_height = height_map[nx, ny]
                drop = current_height - neighbor_height
                slope = drop / distances[idx]
                if slope > max_slope:
                    max_slope = slope
                    best_dir = idx
            flow_dir[x, y] = best_dir
    return flow_dir

def trace_river(flow_dir, height_map, start_x, start_y, max_length=100):
    rows, cols = height_map.shape
    x, y = start_x, start_y
    for _ in range(max_length):
        dir_idx = flow_dir[x, y]
        if dir_idx == -1:
            break
        dx, dy = directions[dir_idx]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < rows and 0 <= ny < cols):
            break
        height_map[max(0, nx - 2):min(rows, nx + 2), max(0, ny - 2):min(cols, ny + 2)] = 0.15
        x, y = nx, ny