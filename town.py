import numpy as np
from scipy.ndimage import distance_transform_edt
import name_generation

def generate_towns(height_map, moisture_map, num_towns):
    town_locations = generate_town_locations(height_map, moisture_map, num_towns)
    town_names = name_generation.generate_town_names(num_towns)
    return town_locations, town_names

def generate_town_locations(height_map, moisture_map, num_towns, min_dist = 30):
    flat_indices = np.argsort(get_location_score(height_map, moisture_map).ravel())[::-1]
    coords = np.column_stack(np.unravel_index(flat_indices, height_map.shape))

    town_locations = []

    for y, x in coords:
        if len(town_locations) >= num_towns:
            break
        if all(np.hypot(x - tx, y - ty) >= min_dist for (ty, tx) in town_locations):
            town_locations.append((y, x))
    return town_locations

def get_location_score(height_map, moisture_map):
    land_mask = height_map > 0.22
    mountain_mask = height_map > 0.65
    wet_mask = moisture_map > 0.7
    dry_mask = moisture_map < 0.3
    valid_mask = land_mask & ~mountain_mask & ~wet_mask & ~dry_mask

    height_score = 1 - np.abs(height_map - 0.4)
    moisture_score = 1 - np.abs(moisture_map - 0.5)
    
    water_mask = height_map < 0.2
    distance_to_water = distance_transform_edt(~water_mask)
    max_distance = np.max(distance_to_water[land_mask])
    water_proximity_score = 0.05 * (1 - (distance_to_water / max_distance))

    return (height_score + moisture_score + water_proximity_score) * valid_mask