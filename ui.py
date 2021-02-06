import matplotlib


import tkinter as tk
from tkinter import ttk

# Tkinter window switching concept from https://www.youtube.com/watch?v=jBUpjijYtCk&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=4


LARGE_FONT = ("Helvetica", 12)
MEDIUM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

#ttk.Style().configure("default", font=MEDIUM_FONT)


class EnergyOracle(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(0, weight=5)
        container.grid_columnconfigure(0, weight=5)

        self.frame_dict = {}

        for F in (HomePage, GraphPage):

            frame = F(container, self)
            self.frame_dict[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, container):
        frame = self.frame_dict[container]
        frame.tkraise()

    def quit(self):
        self.destroy()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Terms and Conditions", font=LARGE_FONT)
        label.pack(pady=15, padx=15)

        button_agree = ttk.Button(
            self, text="Agree", command=lambda: controller.show_frame(GraphPage))
        button_agree.pack(pady=15, padx=15)

        button_disagree = ttk.Button(
            self, text="Disagree", command=lambda: controller.quit())
        button_disagree.pack(pady=15, padx=15)


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=15, padx=15)


application = EnergyOracle()
application.mainloop()
