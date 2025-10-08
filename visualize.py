from matplotlib import pyplot as plt

def draw(grid, cmap, norm, town_locations):
    plt.figure(figsize = (8, 8))
    plt.imshow(grid, cmap, norm)
    for y, x in town_locations:
        plt.plot(x, y, 'wo', markersize = 4, markeredgecolor = 'black', label = 'Town' if (y, x) == town_locations[0] else "")
    plt.legend()
    plt.title("Simplex Noise - Continental Shape")
    plt.axis('off')
    plt.tight_layout()
    plt.show()