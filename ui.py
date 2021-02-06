from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from tkinter import ttk
import tkinter as tk
import matplotlib
matplotlib.use("TKAgg")


# Tkinter window switching concept from https://www.youtube.com/watch?v=jBUpjijYtCk&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=4


LARGE_FONT = ("Helvetica", 12)
MEDIUM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

style.use("ggplot")


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

    def animate(self, graph):
        graph.clear()
        graph.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                   [5, 1, 6, 8, 2, 4, 6, 1, 3, 8])

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

        focused = self.main_graph()
        for i in range(5):
            self.small_graph(i)

    def main_graph(self):
        f = Figure(figsize=(10, 6), dpi=100)
        plot = f.add_subplot()
        plot.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                  [5, 1, 6, 8, 2, 4, 6, 1, 3, 8])
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().grid(row=0, column=0, rowspan=10,
                                    columnspan=4, pady=10, sticky="NSEW")
        return f

    def small_graph(self, row_num):
        f2 = Figure(figsize=(2, 1), dpi=100)
        plot = f2.add_subplot()
        plot.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                  [5, 1, 6, 8, 2, 4, 6, 1, 3, 8])
        canvas = FigureCanvasTkAgg(f2, self)
        canvas.get_tk_widget().grid(row=row_num, column=8, rowspan=1, columnspan=1, ipadx=10, ipady=50,
                                    sticky="NS")
        return f2

    def focus_graph(self, graph_to_focus, key):
        graph_to_focus.clear()
        plot = graph_to_focus.add_subplot()
        plot.plot(graph_dict[key])


application = EnergyOracle()
application.mainloop()
