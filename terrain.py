import numpy as np
from noise import snoise2
from scipy.ndimage import gaussian_filter

import artifact_remover
import hydrology

def generate_height_map0(width, height, scale, cx, cy, octaves, persistence, lacunarity, seed):
    height_map = np.zeros((height, width))
    nx_scale = np.random.uniform(0.8, 1.2)

    x = np.arange(width)
    y = np.arange(height)
    xx, yy = np.meshgrid(x, y)

    nx = (xx - cx) / scale
    ny = (yy - cy) / scale

    distort_noise = np.vectorize(lambda x, y: snoise2(x * 2, y * 2, octaves = 4, base = seed + 100))(nx, ny) * 0.7
    nx_distorted = nx * nx_scale + distort_noise
    ny_distorted = ny + distort_noise
    
    noise_val = np.vectorize(lambda x, y: snoise2(x, y,
                                                  octaves = octaves,
                                                  persistence = persistence,
                                                  lacunarity = lacunarity,
                                                  repeatx = width,
                                                  repeaty = height,
                                                  base = seed))(nx, ny)

    noise_val = (noise_val + 1) / 2
    distance = (np.sqrt(nx_distorted**2 + ny_distorted**2) / 2.2) ** 1.5
    height_map = noise_val - distance
    ridge_noise = 1 - np.abs(np.vectorize(lambda x, y: snoise2(x * 2, y * 2, base=seed + 200))(nx, ny))
    height_map += ridge_noise * 0.1
    height_map = np.clip(height_map, 0, 1)
    return height_map

def generate_height_map(width, height, river_num, octaves, persistence, lacunarity):
    seed = np.random.randint(1, 1000)
    scale = np.random.randint(120, 130)
    cx, cy = 0.5 * width, 0.5 * height
        
    height_map = generate_height_map0(width, height, scale, cx, cy, octaves, persistence, lacunarity, seed)

    land_mask = height_map > 0.2
    blurred = gaussian_filter(height_map * land_mask, sigma=1)
    height_map[land_mask] = blurred[land_mask]

    artifact_remover.remove_shallow_water_artifacts(height_map)
    artifact_remover.remove_deep_water_artifacts(height_map)
    
    hydrology.trace_rivers(height_map, river_num)

    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9
    height_map = np.pad(height_map, 1, mode = 'edge')
    height_map = np.array([[np.sum(kernel * height_map[i:i + 3, j:j + 3]) for j in range(height_map.shape[1] - 2)] for i in range(height_map.shape[0] - 2)])
    return height_map

def generate_moisture_map0(width, height, scale, octaves, persistence, lacunarity, seed):
    moisture_map = np.zeros((height, width))
    x = np.arange(width)
    y = np.arange(height)
    xx, yy = np.meshgrid(x, y)

    nx = xx / scale
    ny = yy / scale

    noise_val = np.vectorize(lambda x, y: snoise2(x, y,
                                                  octaves = octaves,
                                                  persistence = persistence,
                                                  lacunarity = lacunarity,
                                                  repeatx = width,
                                                  repeaty = height,
                                                  base = seed))(nx, ny)

    noise_val = (noise_val + 1) / 2
    moisture_map = noise_val
    moisture_map = np.clip(moisture_map, 0, 1)
    return moisture_map

def generate_moisture_map(width, height, octaves, persistence, lacunarity):
    seed = np.random.randint(1, 1000)
    scale = 100
    return generate_moisture_map0(width, height, scale, octaves, persistence, lacunarity, seed)