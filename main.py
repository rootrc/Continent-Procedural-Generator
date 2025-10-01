import random
import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2

width = 512
height = 512

octaves = 6
persistence = 0.4
lacunarity = 2.0

def generate_continent(width, height, scale, seed, cx = width/2, cy = height/2):
    heightmap = np.zeros((height, width))
    nx_scale = np.random.randint(25, 100) / 50

    x = np.arange(width)
    y = np.arange(height)
    xx, yy = np.meshgrid(x, y)

    nx = (xx - cx) / scale
    ny = (yy - cy) / scale

    distort_noise = np.vectorize(lambda x, y: snoise2(x * 2, y * 2, octaves = 2, base = seed + 100))(nx, ny) * 0.3
    nx_distorted = nx * nx_scale + distort_noise
    ny_distorted = ny + distort_noise

    distance = (np.sqrt(nx_distorted**2 + ny_distorted**2) / 2.2) ** 1.2

    noise_val = np.vectorize(lambda x, y: snoise2(x, y,
                                                  octaves = octaves,
                                                  persistence = persistence,
                                                  lacunarity = lacunarity,
                                                  repeatx = width,
                                                  repeaty = height,
                                                  base = seed))(nx, ny)

    noise_val = (noise_val + 1) / 2
    heightmap = noise_val - distance
    heightmap = np.clip(heightmap, 0, 1)
    return heightmap

num_continents = 5

global_map = np.zeros((height, width))

for i in range(num_continents):
    seed = np.random.randint(1, 1000)
    cx, cy = np.random.randint(10, 90) / 100 * width, np.random.randint(10, 90) / 100 * height
    scale = np.random.randint(50, 100)
    continent = generate_continent(width, height, scale, seed, cx, cy)
    global_map = np.add(global_map, continent)

plt.figure(figsize = (8, 8))
plt.imshow(global_map, cmap = 'terrain')
plt.title("Simplex Noise - Continental Shape")
plt.axis('off')
plt.tight_layout()
plt.show()