import tkinter as tk

from Controllers.main_controller import MainController

if __name__ == '__main__':
    print("BeeFit started!")
    root = tk.Tk()
    root.withdraw()
    app = MainController(root)
    root.mainloop()
