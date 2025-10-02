import random
import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2

global_width = 512
global_height = 512

octaves = 6
persistence = 0.5
lacunarity = 2.0

def generate_continent(width, height, scale, seed, cx = global_width/2, cy = global_height/2):
    heightmap = np.zeros((height, width))
    nx_scale = np.random.uniform(0.8, 1.2)

    x = np.arange(width)
    y = np.arange(height)
    xx, yy = np.meshgrid(x, y)

    nx = (xx - cx) / scale
    ny = (yy - cy) / scale

    distort_noise = np.vectorize(lambda x, y: snoise2(x * 2, y * 2, octaves = 3, base = seed + 100))(nx, ny) * 0.3
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
    distance = (np.sqrt(nx_distorted**2 + ny_distorted**2) / 2.2) ** 1.3
    heightmap = noise_val - distance

    heightmap = np.clip(heightmap, 0, 1)
    return heightmap

num_continents = 5

global_map = np.zeros((global_height, global_width))

for i in range(num_continents):
    seed = np.random.randint(1, 1000)
    cx, cy = np.random.uniform(0.1, 0.9) * global_width, np.random.uniform(0.1, 0.9) * global_height
    scale = np.random.randint(50, 100)
    continent = generate_continent(global_width, global_height, scale, seed, cx, cy)
    global_map += continent
    
global_map = np.clip(global_map, 0, 1)

plt.figure(figsize = (8, 8))
plt.imshow(global_map, cmap = 'terrain')
plt.title("Simplex Noise - Continental Shape")
plt.axis('off')
plt.tight_layout()
plt.show()