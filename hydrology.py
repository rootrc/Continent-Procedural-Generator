import numpy as np

directions = [
    (-1,  0, 1.0), (1,  0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
    (-1, -1, np.sqrt(2)), (1, 1, np.sqrt(2)), (-1, 1, np.sqrt(2)), (1, -1, np.sqrt(2))
]

def trace_rivers(height_map, river_num):
    flow_dir = compute_d8_flow_direction(height_map)
    for (x, y) in get_top_n_high_points(height_map, river_num):
        trace_river(flow_dir, height_map, x, y)

def get_top_n_high_points(height_map, n, min_distance = 50):
    flat_indices = np.argsort((height_map).ravel())[::-1]
    selected_points = []
    for idx in flat_indices:
        x, y = np.unravel_index(idx, height_map.shape)
        if all(np.hypot(x - px, y - py) >= min_distance for px, py in selected_points):
            selected_points.append((x, y))
            if len(selected_points) == n:
                break
    return selected_points

def compute_d8_flow_direction(height_map):
    rows, cols = height_map.shape
    flow_dir = -np.ones((rows, cols), dtype=int)
    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            max_slope = -np.inf
            best_dir = -1
            current_height = height_map[x, y]
            for idx, (dx, dy, dist) in enumerate(directions):
                nx, ny = x + dx, y + dy
                neighbor_height = height_map[nx, ny]
                slope = (current_height - neighbor_height) / dist
                if slope > max_slope:
                    max_slope = slope
                    best_dir = idx
            flow_dir[x, y] = best_dir
    return flow_dir

def trace_river(flow_dir, height_map, start_x, start_y, max_length=200, river_width=2):
    rows, cols = height_map.shape
    x, y = start_x, start_y
    for _ in range(max_length):
        dir_idx = flow_dir[x, y]
        if dir_idx == -1:
            break
        dx, dy, _ = directions[dir_idx]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < rows and 0 <= ny < cols):
            break
        height_map[max(0, nx - river_width):min(rows, nx + river_width), max(0, ny - river_width):min(cols, ny + river_width)] = 0.15
        x, y = nx, ny