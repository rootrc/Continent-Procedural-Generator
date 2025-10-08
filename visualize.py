from matplotlib import pyplot as plt

def draw(grid, cmap, norm, town_locations, town_names):
    plt.figure(figsize = (8, 8))
    plt.imshow(grid, cmap, norm)
    for i, (y, x) in enumerate(town_locations):
        plt.plot(x, y, 'wo', markersize = 4, markeredgecolor = 'black', label = 'Town' if (y, x) == town_locations[0] else "")
        plt.text(x + 5, y, town_names[i], fontsize=6, color='white', bbox=dict(facecolor='black', alpha=0.5, boxstyle='round,pad=0.2'))
    plt.legend()
    plt.title("Simplex Noise - Continental Shape")  
    plt.axis('off')
    plt.tight_layout()
    plt.show()