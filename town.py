import numpy as np

def find_town_locations(height_map, moisture_map, num_towns):
    flat_indices = np.argsort(get_location_score(height_map, moisture_map).ravel())[::-1]
    coords = np.column_stack(np.unravel_index(flat_indices, height_map.shape))

    town_locations = []
    min_dist = 30

    for y, x in coords:
        if len(town_locations) >= num_towns:
            break
        if all(np.hypot(x - tx, y - ty) >= min_dist for (ty, tx) in town_locations):
            town_locations.append((y, x))

    return town_locations

def get_location_score(height_map, moisture_map):
    land_mask = height_map > 0.2
    mountain_mask = height_map > 0.65
    wet_mask = moisture_map > 0.7
    dry_mask = moisture_map < 0.3
    valid_mask = land_mask & ~mountain_mask & ~wet_mask & ~dry_mask

    height_score = 1 - np.abs(height_map - 0.4)
    moisture_score = 1 - np.abs(moisture_map - 0.5)

    return (height_score + moisture_score) * valid_mask