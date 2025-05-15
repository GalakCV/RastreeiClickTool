import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
from itertools import cycle

running = False
coords_cycle = None
wait_time = 0
coords = {}

BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4a7a8c"
TEXT_COLOR = "#333333"
HIGHLIGHT_COLOR = "#2d5f73"

def update_coordinates():
    x, y = pyautogui.position()
    coord_label.config(text=f"Coordenadas do Cursor: X={x}, Y={y}")
    Window.after(100, update_coordinates)

def collect_coordinates():
    global coords, coords_cycle, wait_time
    try:
        coords = {
            "PreOpen": (int(x_entry0.get()), int(y_entry0.get())),
            "OpenPort": (int(x_entry1.get()), int(y_entry1.get())),
            "Param1": (int(x_entry2.get()), int(y_entry2.get())),
            "SetParam1": (int(x_entry3.get()), int(y_entry3.get())),
            "Param2": (int(x_entry4.get()), int(y_entry4.get())),
            "SetParam2": (int(x_entry5.get()), int(y_entry5.get()))
        }
        wait_time = int(wait_entry.get())
        coords_cycle = cycle(coords.items())
        return True
    except ValueError:
        messagebox.showerror("Erro", "Insira apenas números válidos.")
        return False

def start_countdown(seconds):
    if seconds > 0 and running:
        countdown_label.config(text=f"Iniciando novo ciclo em: {seconds}s")
        Window.after(1000, lambda: start_countdown(seconds - 1))
    else:
        countdown_label.config(text="")
        if running:
            move_smoothly()

def move_smoothly():
    global running
    if running and coords_cycle:
        name, (x, y) = next(coords_cycle)
        pyautogui.moveTo(x, y, duration=0.2)
        pyautogui.click(clicks=1)

        if name == "SetParam2":
            start_countdown(wait_time)
        else:
            Window.after(1000, move_smoothly)

def start_loop():
    global running
    if not running and collect_coordinates():
        running = True
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        move_smoothly()

def stop_loop(event=None):
    global running
    running = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    countdown_label.config(text="Loop parado")

def Create_Window():
    global Window, coord_label, countdown_label
    global x_entry0, y_entry0, x_entry1, y_entry1, x_entry2, y_entry2
    global x_entry3, y_entry3, x_entry4, y_entry4, x_entry5, y_entry5
    global start_button, stop_button, wait_entry

    Window = tk.Tk()
    Window.title("Click Automation")
    Window.geometry("500x600")
    Window.configure(bg=BG_COLOR)

    title = tk.Label(Window, text="Automação de Cliques", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
    title.pack(pady=10)

    coord_label = tk.Label(Window, text="", font=("Arial", 10), bg=BG_COLOR)
    coord_label.pack(pady=5)

    def create_entry_group(label_text):
        frame = tk.Frame(Window, bg=BG_COLOR)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, bg=BG_COLOR).pack(side=tk.LEFT, padx=5)
        x = ttk.Entry(frame, width=5)
        x.pack(side=tk.LEFT)
        y = ttk.Entry(frame, width=5)
        y.pack(side=tk.LEFT, padx=5)
        return x, y

    x_entry0, y_entry0 = create_entry_group("0. PreOpen")
    x_entry1, y_entry1 = create_entry_group("1. OpenPort")
    x_entry2, y_entry2 = create_entry_group("2. Param1")
    x_entry3, y_entry3 = create_entry_group("3. SetParam1")
    x_entry4, y_entry4 = create_entry_group("4. Param2")
    x_entry5, y_entry5 = create_entry_group("5. SetParam2")

    wait_frame = tk.Frame(Window, bg=BG_COLOR)
    wait_frame.pack(pady=10)
    tk.Label(wait_frame, text="Tempo entre ciclos (s):", bg=BG_COLOR).pack(side=tk.LEFT)
    wait_entry = ttk.Entry(wait_frame, width=5)
    wait_entry.insert(0, "5")
    wait_entry.pack(side=tk.LEFT, padx=5)

    countdown_label = tk.Label(Window, text="", font=("Arial", 12), fg="red", bg=BG_COLOR)
    countdown_label.pack(pady=10)

    btn_frame = tk.Frame(Window, bg=BG_COLOR)
    btn_frame.pack(pady=15)

    start_button = ttk.Button(btn_frame, text="Iniciar", command=start_loop)
    start_button.pack(side=tk.LEFT, padx=10)

    stop_button = ttk.Button(btn_frame, text="Parar", command=stop_loop, state=tk.DISABLED)
    stop_button.pack(side=tk.LEFT, padx=10)

    footer = tk.Label(Window, text="Criado por GalakCV", font=("Arial", 8, "italic"), fg="red", bg=BG_COLOR)
    footer.pack(side=tk.BOTTOM, pady=10)

    Window.bind("<F12>", stop_loop)
    update_coordinates()
    Window.mainloop()

Create_Window()
