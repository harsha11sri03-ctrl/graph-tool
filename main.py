from tkinter import Tk
from tkinter.filedialog import askopenfilename
from file_loader import load_file
from plotter import plot_bar

# Hide tkinter window
Tk().withdraw()

file_path = askopenfilename(title="Select File")

if not file_path:
    print("No file selected")
    exit()

df = load_file(file_path)

plot_bar(df)