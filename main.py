import auto_update
auto_update.check_update()

import tkinter as tk
from ui.main_window import MainWindow

if __name__ == "__main__":
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except:
        pass

    app = MainWindow(root)
    root.mainloop()