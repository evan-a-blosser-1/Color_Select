"""Color Select

        This is a color selection tool that has built in palettes:
            - Basic color palette
            - Colorblind color palette (In settings)
            
        The user can select a color from the basic color palette or 
        use the color picker to select a color from the screen.
        
    Author: Evan Blosser
    Githhub: evan-a-blosser-1
    Date: 2021-09-28
"""
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import ImageGrab, Image, ImageTk
import markdown
import os
modes = ["Space Mode", "Forest Mode", "Loki Mode"]
current_mode_index = 0
selected_colors = []  

themes = {
    "Space Mode": {
        "bg_color": "#333333",
        "font_color": "cyan",
        "button_color": "#555555",
        "background_image": "img/dark_background_image.png"
    },
    "Forest Mode": {
        "bg_color": "#228B22",
        "font_color": "white",
        "button_color": "#6B8E23",
        "background_image": "img/background_image.png"
    },
    "Loki Mode": {
        "bg_color": "#4B0082",
        "font_color": "gold",
        "button_color": "#400080",
        "background_image": "img/Loki_Mode.png"
    }
}

colorblind_palette = ['#332288', '#117733', '#44AA99', '#88CCEE', '#DDCC77', '#CC6677', '#AA4499', '#882255']

def pick_color():
    color_code = colorchooser.askcolor(title="Choose a color")[1]
    if color_code:
        selected_colors.append(color_code)
        update_color_boxes()

def grab_screen_color(event):
    x, y = event.x_root, event.y_root
    screen = ImageGrab.grab()
    color = screen.getpixel((x, y))
    color_code = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
    selected_colors.append(color_code)
    update_color_boxes()

def start_color_picker():
    picker_window = tk.Toplevel(root)
    picker_window.attributes('-fullscreen', True)
    picker_window.attributes('-alpha', 0.002)  
    picker_window.config(cursor="crosshair")

    def on_click(event):
        grab_screen_color(event)
        picker_window.destroy()
    picker_window.bind("<Button-1>", on_click)  

def update_color_boxes():
    for i in range(10):
        if i < len(selected_colors):
            color_boxes[i].config(bg=selected_colors[i], text=selected_colors[i])
        else:
            color_boxes[i].config(bg="white", text="")

def save_colors():
    file_path = filedialog.asksaveasfilename(defaultextension=".tdt", filetypes=[("Text files", "*.tdt")])
    if file_path:
        with open(file_path, 'w') as file:
            for color in selected_colors:
                file.write(color + '\n')

def load_colorblind_palette():
    global selected_colors
    selected_colors = colorblind_palette.copy()
    update_color_boxes()

def show_about():
    about_file_path = "info/about.txt"
    if os.path.exists(about_file_path):
        with open(about_file_path, 'r') as file:
            about_content = file.read()
        about_window = tk.Toplevel(root)
        about_window.title("About")
        about_window.geometry("400x300")
        about_text = tk.Text(about_window, wrap="word")
        about_text.insert("1.0", about_content)
        about_text.config(state="disabled")  
        about_text.pack(padx=10, pady=10, fill="both", expand=True)
    else:
        messagebox.showerror("Error", "About file not found.")

def show_license():
    license_file_path = "info/MIT_license.txt"
    if os.path.exists(license_file_path):
        with open(license_file_path, 'r') as file:
            license_content = file.read()
        license_window = tk.Toplevel(root)
        license_window.title("License")
        license_window.geometry("400x300")
        license_text = tk.Text(license_window, wrap="word")
        license_text.insert("1.0", license_content)
        license_text.config(state="disabled") 
        license_text.pack(padx=10, pady=10, fill="both", expand=True)
    else:
        messagebox.showerror("Error", "License file not found.")

def switch_theme(mode):
    global current_mode_index
    current_mode_index = modes.index(mode)
    theme = themes[mode]
    background_image = Image.open(theme["background_image"])
    background_photo = ImageTk.PhotoImage(background_image, height=500, width=400)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")
    canvas.image = background_photo  
    pick_color_button.config(bg=theme["button_color"], fg=theme["font_color"])
    start_picker_button.config(bg=theme["button_color"], fg=theme["font_color"])


root = tk.Tk()
root.title("Personalized Color Picker Tool")
root.geometry("400x500")
root.resizable(False, False)  
background_image = Image.open(themes[modes[current_mode_index]]["background_image"])
canvas = tk.Canvas(root, width=400, height=500)
canvas.pack(fill="both", expand=True)
background_photo = ImageTk.PhotoImage(background_image)
canvas.create_image(0, 0, image=background_photo, anchor="nw")
canvas.image = background_photo 
pick_color_button = tk.Button(root, text="Pick a Color", command=pick_color, font=("Arial", 12), bg=themes[modes[current_mode_index]]["button_color"], fg=themes[modes[current_mode_index]]["font_color"])
canvas.create_window(200, 50, window=pick_color_button)
start_picker_button = tk.Button(root, text="Start Color Picker", command=start_color_picker, font=("Arial", 12), bg=themes[modes[current_mode_index]]["button_color"], fg=themes[modes[current_mode_index]]["font_color"])
canvas.create_window(200, 100, window=start_picker_button)
color_boxes = []
for row in range(5):
    for col in range(2):
        label = tk.Label(root, text="", bg="white", width=10, height=2, font=("Arial", 12))
        canvas.create_window(100 + col * 150, 250 + row * 50, window=label)  
        color_boxes.append(label)
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Settings", menu=file_menu)
themes_menu = tk.Menu(file_menu, tearoff=0)
file_menu.add_cascade(label="Themes", menu=themes_menu)
for mode in modes:
    themes_menu.add_command(label=mode, command=lambda m=mode: switch_theme(m))
file_menu.add_command(label="Save Colors", command=save_colors)
file_menu.add_command(label="Load Colorblind Palette", command=load_colorblind_palette)
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=help_menu)
help_menu.add_command(label="Colorblind Palette", command=show_about)
help_menu.add_command(label="License", command=show_license)
root.mainloop()
