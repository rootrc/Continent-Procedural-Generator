import terrain, town, biomes, visualize

global_width = 512
global_height = 512

octaves = 8
persistence = 0.5
lacunarity = 2.0
river_num = 5
num_towns = 12

height_map = terrain.generate_height_map(global_width, global_height, river_num, octaves, persistence, lacunarity)
moisture_map = terrain.generate_moisture_map(global_width, global_height, octaves, persistence, lacunarity)
town_locations = town.generate_town_locations(height_map, moisture_map, num_towns)

grid = biomes.get_biome_indices(height_map, moisture_map)
cmap, norm = biomes.get_cmap_norm()

visualize.draw(grid, cmap, norm, town_locations)