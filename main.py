import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from noise import snoise2

global_width = 512
global_height = 512

octaves = 8
persistence = 0.5
lacunarity = 2.0

def generate_height_map(width, height, scale, seed, cx = global_width/2, cy = global_height/2):
    height_map = np.zeros((height, width))
    nx_scale = np.random.uniform(0.8, 1.2)

    x = np.arange(width)
    y = np.arange(height)
    xx, yy = np.meshgrid(x, y)

    nx = (xx - cx) / scale
    ny = (yy - cy) / scale

    distort_noise = np.vectorize(lambda x, y: snoise2(x * 2, y * 2, octaves = 3, base = seed + 100))(nx, ny) * 0.7
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
    
    height_map = np.clip(height_map, 0, 1)
    return height_map

def generate_mositure_map(width, height, scale, seed):
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

seed = np.random.randint(1, 1000)
scale = np.random.randint(130, 140)
cx, cy = np.random.uniform(0.4, 0.6) * global_width, np.random.uniform(0.4, 0.6) * global_height
    
height_map = generate_height_map(global_width, global_height, scale, seed)
kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9
height_map = np.pad(height_map, 1, mode = 'edge')
height_map = np.array([[np.sum(kernel * height_map[i:i + 3, j:j + 3]) for j in range(height_map.shape[1] - 2)] for i in range(height_map.shape[0] - 2)])

seed = np.random.randint(1, 1000)
scale = 100
moisture_map = generate_mositure_map(global_width, global_height, scale, seed)

colors = ['#000080', # Dry    Ocean
          '#000080', # Moist  Ocean
          '#000080', # Wet    Ocean
          '#003581', # Dry    Shallow Water
          '#003581', # Moist  Shallow Water
          "#003581", # Wet    Shallow Water
          '#006A82', # Dry    Shoreline
          '#006A82', # Moist  Shoreline
          '#006A82', # Wet    Shoreline
          '#D2B48C', # Dry    Beach
          '#D2B48C', # Moist  Beach
          "#3D7171", # Wet    Swamp
          '#E4A672', # Dry    Desert
          '#4c9a2a', # Moist  Flatland-1
          "#2A4747", # Wet    Swamp
          '#E4A672', # Dry    Desert
          "#408722", # Moist  Flatland-2
          "#315B34", # Wet    Forest
          '#D2691E', # Dry    Mesa
          '#a7754e', # Moist  Hill
          '#8F7A50', # Wet    Hill
          '#5a3a3a', # Dry    Mountain
          '#7c5a50', # Moist  Mountain
          '#6b4a3c', # Wet    Mountain
        ]
cmap = ListedColormap(colors)

height_bounds = [0.0, 0.10, 0.15, 0.2, 0.22, 0.325, 0.475, 0.525, 1.0]
moisture_bounds = [0.0, 0.4, 0.575, 1.0]

height_indices = np.digitize(height_map, bins=height_bounds) - 1
moisture_indices = np.digitize(moisture_map, bins=moisture_bounds) - 1

combined_grid = height_indices * (len(moisture_bounds) - 1) + moisture_indices

bounds = np.linspace(0, len(colors), len(colors) + 1)
norm = BoundaryNorm(bounds, cmap.N)

plt.figure(figsize = (8, 8))
plt.imshow(combined_grid, cmap=cmap, norm=norm)
plt.title("Simplex Noise - Continental Shape")
plt.axis('off')
plt.tight_layout()
plt.show()