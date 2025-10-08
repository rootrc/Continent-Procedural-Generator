import numpy as np
from scipy.ndimage import distance_transform_edt

def generate_towns(height_map, moisture_map, num_towns):
    town_locations = generate_town_locations(height_map, moisture_map, num_towns)
    town_names = generate_town_names(num_towns)
    return town_locations, town_names

def generate_town_locations(height_map, moisture_map, num_towns):
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

syllable_sets = {
    "prefixes": ["Al", "Bel", "Car", "Dor", "Eld", "Fen", "Gal", "Har", "Ith", "Jar", "Kor", "Lor", "Mor", "Nor", "Or", "Pel", "Quel", "Riv", "Sar", "Tor", "Ul", "Val", "Wyn", "Xan", "Yar", "Zel"],
    "middles": ["a", "e", "i", "o", "u", "ae", "io", "ar", "el", "or", "an", "in", "un", "eth", "ir", "il"],
    "suffixes": ["dale", "ford", "heim", "hold", "mere", "mont", "peak", "reach", "rest", "rock", "stead", "ton", "vale", "watch", "wick", "wood"]
}

def generate_town_names(num_towns):
    syllables = syllable_sets.get("default", syllable_sets)
    town_names = []
    for _ in range(num_towns):
        name = np.random.choice(syllables["prefixes"])
        if np.random.rand() > 0.5:
            name += np.random.choice(syllables["middles"])
        name += np.random.choice(syllables["suffixes"])
        town_names.append(name)
    return np.array(town_names)