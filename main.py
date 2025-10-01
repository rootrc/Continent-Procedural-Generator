import random
import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2

# Map settings
width = 512
height = 512
scale = 150.0

# Simplex noise parameters
octaves = 8
persistence = 0.4
lacunarity = 2.0

cnt = 0
sum = 0

def generate_continent(width, height, scale=100, threshold=0.3, seed=0):
    # Create array for height map
    heightmap = np.zeros((height, width))

    # Generate noise with radial falloff for "continental" shapes
    for y in range(height):
        for x in range(width):
            nx = (x - width / 2) / scale
            ny = (y - height / 2) / scale
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


# Display as image
plt.figure(figsize=(6, 6))
threshold = 0.35
seed = np.random.randint(1, 100)
heightmap = generate_continent(width, height, scale, threshold, seed)
plt.imshow(heightmap, cmap = 'terrain')  # 'terrain' colormap gives a natural look
plt.title("Simplex Noise - Continental Shape")
plt.axis('off')
plt.tight_layout()
plt.show()