import tkinter as tk
from tkinter import ttk, messagebox
import world_generator

def generate():
    try:
        octaves = int(octaves_input.get())
        persistence = float(persistence_input.get())
        lacunarity = float(lacunarity_input.get())
        river_num = int(river_input.get())
        num_towns = int(towns_input.get())

        world_generator.generate_world(octaves, persistence, lacunarity, river_num, num_towns)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

root = tk.Tk()
root.title("Continent Procedural Generator")
root.geometry("420x500")
root.resizable(False, False)
root.configure(bg = "#f0f0f5")

style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background = "#f0f0f5")
style.configure("TLabel", background = "#f0f0f5", font = ("Segoe UI", 10))
style.configure("TButton", font = ("Segoe UI", 11, "bold"), padding = 6)
style.map("TButton", background = [("active", "#0078D7")], foreground = [("active", "white")])

ttk.Label(
    root, 
    text = "Continent Procedural Generator", 
    font = ("Segoe UI", 16, "bold"), 
    foreground = "#333"
).pack(pady = 15)

frame = ttk.Frame(root, padding = 20)
frame.pack(fill="x", expand = True)

octaves_input = tk.IntVar(value = 8)
persistence_input = tk.DoubleVar(value = 0.5)
lacunarity_input = tk.DoubleVar(value = 2)
river_input = tk.IntVar(value = 5)
towns_input = tk.IntVar(value = 12)

def slider(label, var, from_, to, resolution=1):
    row = ttk.Frame(frame)
    row.pack(fill = "x", pady = 10)
    ttk.Label(row, text = label, width = 18, anchor = "w").pack(side = "left")
    scale = tk.Scale(row, from_ = from_, to = to, orient = "horizontal",
                     variable = var, resolution = resolution, showvalue = True, length = 200)
    scale.pack(side = "left", padx = 5)

    value_label = ttk.Label(row, text = str(var.get()), width = 6)
    value_label.pack(side = "left")

    def update_label(value):
        value_label.config(text = f"{float(value):.2f}" if isinstance(var.get(), float) else f"{int(float(value))}")
    scale.config(command = update_label)
    
slider("Octaves:", octaves_input, 2, 12)
slider("Persistence:", persistence_input, 0.4, 0.6, 0.1)
slider("Lacunarity:", lacunarity_input, 1.5, 2.5, 0.1)
slider("Rivers:", river_input, 0, 10)
slider("Towns:", towns_input, 0, 40)

ttk.Button(root, text = "Generate World", command = generate).pack(pady=25)

root.mainloop()