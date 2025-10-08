import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm

colors = [
    '#000080', '#000080', '#000080', # Ocean
    '#003581', '#003581', '#003581', # Shallow Water
    '#006A82', '#006A82', '#006A82', # Shoreline
    '#D2B48C', '#D2B48C', '#3D7171', # Beach / Swamp
    '#E4A672', '#4c9a2a', '#2A4747', # Desert / Flatland / Swamp
    '#E4A672', '#408722', '#315B34', # Desert / Flatland / Forest
    '#D2691E', '#a7754e', '#8F7A50', # Mesa / Hill
    '#5a3a3a', '#7c5a50', '#6b4a3c', # Mountain
]

height_bounds = [0.0, 0.1, 0.15, 0.2, 0.22, 0.325, 0.5, 0.55, 1.0]
moisture_bounds = [0.0, 0.4, 0.575, 1.0]

cmap = ListedColormap(colors)
bounds = np.linspace(0, len(colors), len(colors) + 1)
norm = BoundaryNorm(bounds, cmap.N)

def get_biome_indices(height_map, moisture_map):
    height_indices = np.digitize(height_map, bins = height_bounds) - 1
    moisture_indices = np.digitize(moisture_map, bins = moisture_bounds) - 1
    combined_grid = height_indices * (len(moisture_bounds) - 1) + moisture_indices
    return combined_grid

def get_cmap_norm():
    cmap = ListedColormap(colors)
    bounds = np.linspace(0, len(colors), len(colors) + 1)
    norm = BoundaryNorm(bounds, cmap.N)
    return cmap, norm