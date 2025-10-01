import random
import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2

width = 512
height = 512
scale = 100.0

octaves = 8
persistence = 0.4
lacunarity = 2.0

def generate_continent(width, height, scale=100, seed=0, cx=width/2, cy=height / 2):
    heightmap = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            nx = (x - cx) / scale
            ny = (y - cy) / scale
            distance = (np.sqrt(nx**2 + ny**2) / 2.2) ** 1.2
            
            noise_val = snoise2(nx, ny,
                                octaves=octaves,
                                persistence=persistence,
                                lacunarity=lacunarity,
                                repeatx=width,
                                repeaty=height,
                                base=seed)
            noise_val = (noise_val + 1) / 2
            heightmap[y][x] = noise_val - distance
    heightmap = np.clip(heightmap, 0, 1)
    return heightmap

num_continents = 1
continent_centers = [
    (width * 0.5, height * 0.5)
]

global_map = np.zeros((height, width))

for i in range(num_continents):
    seed = np.random.randint(1, 1000)
    cx, cy = continent_centers[i]
    continent = generate_continent(width, height, scale, seed, cx, cy)
    global_map = np.add(global_map, continent)

plt.figure(figsize=(8, 8))
plt.imshow(global_map, cmap='terrain')
plt.title("Simplex Noise - Continental Shape")
plt.axis('off')
plt.tight_layout()
plt.show()