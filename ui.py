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

graph_dict = {"DRAM": [[1, 2, 3], [1, 2, 3]],
              "CORE": [[1, 2, 3], [3, 2, 1]],
              "PACKAGE": [[1, 2, 3], [6, 8, 1]],
              "GPU": [[1, 2, 3], [5, 5, 5]],
              "TOTAL": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        [5, 1, 6, 8, 2, 4, 6, 1, 3, 8]]}


# def animate_graph


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

        self.main_graph()
        self.create_buttons()

        i = 0
        for key in graph_dict:
            self.small_graph(key, i)
            i += 1

    def create_buttons(self):

        label_dram = ttk.Label(self, text="DRAM usage")
        label_dram.grid(row=0, column=5, sticky="S")
        button_dram = ttk.Checkbutton(
            self, text="FOCUS", takefocus=0, command=lambda: self.focus_target("DRAM"))
        button_dram.grid(row=1, column=5, sticky="N")

        label_core = ttk.Label(self, text="CORE usage")
        label_core.grid(row=2, column=5, sticky="S")
        button_core = ttk.Checkbutton(
            self, text="FOCUS",  takefocus=0, command=lambda: self.focus_target("CORE"))
        button_core.grid(row=3, column=5, sticky="N")

        label_package = ttk.Label(self, text="PACKAGE usage")
        label_package.grid(row=4, column=5, sticky="S")
        button_package = ttk.Checkbutton(
            self, text="FOCUS",  takefocus=0, command=lambda: self.focus_target("PACKAGE"))
        button_package.grid(row=5, column=5, sticky="N")

        label_gpu = ttk.Label(self, text="GPU usage")
        label_gpu.grid(row=6, column=5, sticky="S")
        button_gpu = ttk.Checkbutton(
            self, text="FOCUS",  takefocus=0, command=lambda: self.focus_target("GPU"))
        button_gpu.grid(row=7, column=5, sticky="N")

        label_total = ttk.Label(self, text="TOTAL usage")
        label_total.grid(row=8, column=5, sticky="S")
        button_total = ttk.Checkbutton(
            self, text="FOCUS",  takefocus=0, command=lambda: self.focus_target("TOTAL"))
        button_total.grid(row=9, column=5, sticky="N")

    def main_graph(self):
        f = Figure(figsize=(10, 6), dpi=100)
        plot = f.add_subplot()
        plot.plot(graph_dict["TOTAL"][0], graph_dict["TOTAL"][1])
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().grid(row=0, column=0, rowspan=11,
                                    columnspan=4, pady=10, sticky="NSEW")
        self.focused_graph = canvas

    def small_graph(self, key, row_num):
        f2 = Figure(figsize=(2, 1), dpi=100)
        plot = f2.add_subplot()
        plot.plot(graph_dict[key][0], graph_dict[key][1])
        canvas = FigureCanvasTkAgg(f2, self)
        canvas.get_tk_widget().grid(row=row_num * 2, column=6, rowspan=2, columnspan=1, ipadx=10, ipady=50,
                                    sticky="NS")

    def focus_target(self, key):
        self.focused_graph.get_tk_widget().grid_forget()
        f = Figure(figsize=(10, 6), dpi=100)
        plot = f.add_subplot()
        plot.plot(graph_dict[key][0], graph_dict[key][1])
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().grid(row=0, column=0, rowspan=10,
                                    columnspan=4, pady=10, sticky="NSEW")
        self.focused_graph = canvas


application = EnergyOracle()
application.mainloop()
