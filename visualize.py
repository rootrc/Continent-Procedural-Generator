from matplotlib import pyplot as plt

def draw(grid, cmap, norm, continent_name, town_locations, town_names):
    plt.figure(figsize = (8, 8))
    plt.imshow(grid, cmap, norm)
    for i, (y, x) in enumerate(town_locations):
        if i == 0:
            plt.plot(x, y, 'w*', markersize = 8, markeredgecolor = 'black', label = 'Captial')
        else:
            plt.plot(x, y, 'wo', markersize = 4, markeredgecolor = 'black', label = 'Town' if (y, x) == town_locations[1] else "")
        plt.text(x + 5, y, town_names[i], fontsize=6, color = 'white', bbox=dict(facecolor='black', alpha=0.5, boxstyle='round,pad=0.2'))
    plt.legend()
    plt.title("The Continent of " + continent_name)  
    plt.text(10, 10, 'N', fontsize = 14, color = 'white', fontweight = 'bold')
    plt.arrow(10, 25, 0, -10, head_width = 5, head_length = 5, fc = 'white', ec = 'white')
    plt.axis('off')
    plt.tight_layout()
    plt.show()