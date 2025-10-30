import name_generation
import terrain, town, biomes, visualize

global_width = 512
global_height = 512

def generate_world(octaves, persistence, lacunarity, river_num, town_num):
    height_map = terrain.generate_height_map(global_width, global_height, river_num, octaves, persistence, lacunarity)
    moisture_map = terrain.generate_moisture_map(global_width, global_height, octaves, persistence, lacunarity)
    continent_name = name_generation.generate_continent_name()
    town_locations, town_names = town.generate_towns(height_map, moisture_map, town_num)

    grid = biomes.get_biome_indices(height_map, moisture_map)
    cmap, norm = biomes.get_cmap_norm()

    visualize.draw(grid, cmap, norm, continent_name, town_locations, town_names)