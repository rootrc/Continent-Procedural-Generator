import numpy as np
from collections import deque

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def remove_shallow_water_artifacts(height_map):
    rows, cols = height_map.shape
    visited = np.zeros((rows, cols), dtype=bool)
    for i in range(rows):
        for j in range(cols):
            if not visited[i, j] and height_map[i, j] < 0.2:
                water_artifacts = remove_shallow_water_artifacts_bfs(height_map, i, j, visited, rows, cols)
                for (x, y) in water_artifacts:
                    height_map[x, y] = 0

def remove_shallow_water_artifacts_bfs(height_map, x, y, visited, rows, cols):
    water_artifacts = []
    queue = deque([(x, y)])
    visited[x, y] = True
    water_artifacts.append((x, y))
    while queue:
        cx, cy = queue.popleft()
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if  not (0 <= nx < rows and 0 <= ny < cols) or visited[nx, ny]:
                continue
            if height_map[nx, ny] >= 0.2:
                return []
            if 0.1 < height_map[nx, ny] < 0.2:
                visited[nx, ny] = True
                water_artifacts.append((nx, ny))
                queue.append((nx, ny))
    return water_artifacts

def remove_deep_water_artifacts(height_map):
    rows, cols = height_map.shape
    visited = np.zeros((rows, cols), dtype=bool)
    for i in range(rows):
        for j in range(cols):
            if not visited[i, j] and height_map[i, j] < 0.1:
                water_artifacts = remove_deep_water_artifacts_bfs(height_map, i, j, visited, rows, cols)
                for (x, y) in water_artifacts:
                    height_map[x, y] = 0.125

def remove_deep_water_artifacts_bfs(height_map, x, y, visited, rows, cols):
    water_artifacts = []
    queue = deque([(x, y)])
    visited[x, y] = True
    water_artifacts.append((x, y))
    cnt = 1
    while queue:
        cx, cy = queue.popleft()
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if not (0 <= nx < rows and 0 <= ny < cols) or visited[nx, ny]:
                continue
            if height_map[nx, ny] < 0.1:
                visited[nx, ny] = True
                water_artifacts.append((nx, ny))
                queue.append((nx, ny))
                cnt += 1
    if (cnt < 1000):
        return water_artifacts
    return []