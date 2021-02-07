from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from tkinter import ttk
import tkinter as tk
import matplotlib
matplotlib.use("TKAgg")


# Tkinter window switching concept from https://www.youtube.com/watch?v=jBUpjijYtCk&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=4

terms_string = "The Energy Oracle application monitors component energy use on a per-system\n\
                basis. Collected data feeds into a machine learning model which predicts\n\
                future energy usage. The Oracle is intended for use as both a commercial\n\
                and consumer product. A user could anticipate lulls in computational\n\
                overhead, and reduce power draw accordingly. This would both lower costs\n\
                and lower excess energy consumption.\n\n\
                To accomplish this, The Energy Oracle requires read/write access to the\n\
                interface of the model-specific-registers. Root privileges are needed\n\
                for this task, explaining the password prompt.\n\n\
                The entire Energy Oracle project is open source and available for\n\
                inspection to ensure full transparency. Your password is never saved by us.\n\
                (https://github.com/aservet1/energyOracle)"

LARGE_FONT = ("Helvetica", 20)
MEDIUM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

style.use("ggplot")

graph_dict = {"DRAM": "dram.txt",
              "CORE": "core.txt",
              "PACKAGE": "package.txt",
              "GPU": "gpu.txt",
              "TOTAL": "sample.txt"}

graph_obj_dict = {"DRAM": [],
                  "CORE": [],
                  "PACKAGE": [],
                  "GPU": [],
                  "TOTAL": []}

for key in graph_dict:
    f2 = Figure(figsize=(2.5, 1.25), dpi=100)
    f2plot = f2.add_subplot()
    f2plot.
    graph_obj_dict[key].append(f2)
    graph_obj_dict[key].append(f2plot)

active = graph_dict["TOTAL"]

fig = Figure(figsize=(8, 4), dpi=100)
plot = fig.add_subplot()


def animate(i, graph, path):
    data = open(path, "r").read()
    dataList = data.split('\n')
    xList = []
    yList = []
    for each in dataList:
        if len(each) > 1:
            x, y = each.split(',')
            xList.append(int(x))
            yList.append(int(y))
    graph.clear()
    graph.plot(xList, yList)


def animate_main(i):
    data = open(active, "r").read()
    dataList = data.split('\n')
    xList = []
    yList = []
    for each in dataList:
        if len(each) > 1:
            x, y = each.split(',')
            xList.append(int(x))
            yList.append(int(y))
    plot.clear()
    plot.plot(xList, yList)


class EnergyOracle(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        s = ttk.Style()
        print(s.theme_names())
        s.theme_use("alt")

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

        label = ttk.Label(self, text=terms_string, font=MEDIUM_FONT)
        label.grid(row=0, column=0, columnspan=2)

        button_agree = ttk.Button(
            self, text="Agree", command=lambda: load_graph_page())
        button_agree.grid(row=1, column=1)

        button_disagree = ttk.Button(
            self, text="Disagree", command=lambda: controller.quit())
        button_disagree.grid(row=1, column=0)

        def load_graph_page():
            controller.show_frame(GraphPage)
            controller.frame_dict[GraphPage].create_toolbar()


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent

        self.main_graph()
        self.create_buttons()

        small_graph_objects = {}

        i = 0
        for key in graph_dict:
            self.small_graph(key, i)
            i += 1

        self.focus_target("TOTAL")

    # def clear_test(self):
    #     self.focused_graph

    def create_buttons(self):

        label_dram = ttk.Label(
            self, text="DRAM USAGE", font=LARGE_FONT, background="white")
        label_dram.grid(row=0, column=5, sticky="S")
        button_dram = ttk.Button(
            self, text="FOCUS", command=lambda: self.focus_target("DRAM"))
        button_dram.grid(row=1, column=5, sticky="N")

        label_core = ttk.Label(
            self,  text="CORE USAGE", font=LARGE_FONT, background="white")
        label_core.grid(row=2, column=5, sticky="S")
        button_core = ttk.Button(
            self, text="FOCUS", command=lambda: self.focus_target("CORE"))
        button_core.grid(row=3, column=5, sticky="N")

        label_package = ttk.Label(
            self,  text="PACKAGE USAGE", font=LARGE_FONT, background="white")
        label_package.grid(row=4, column=5, sticky="S")
        button_package = ttk.Button(
            self, text="FOCUS", command=lambda: self.focus_target("PACKAGE"))
        button_package.grid(row=5, column=5, sticky="N")

        label_gpu = ttk.Label(
            self, text="GPU USAGE", font=LARGE_FONT, background="white")
        label_gpu.grid(row=6, column=5, sticky="S")
        button_gpu = ttk.Button(
            self, text="FOCUS", command=lambda: self.focus_target("GPU"))
        button_gpu.grid(row=7, column=5, sticky="N")

        label_total = ttk.Label(
            self,  text="TOTAL USAGE", font=LARGE_FONT, background="white")
        label_total.grid(row=8, column=5, sticky="S")
        button_total = ttk.Button(
            self, text="FOCUS", command=lambda: self.focus_target("TOTAL"))
        button_total.grid(row=9, column=5, sticky="N")

    def main_graph(self):
        # global fig
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().grid(row=1, column=0, rowspan=10,
                                    columnspan=4, pady=10)
        canvas.draw()

        self.focused_graph = canvas

    def create_toolbar(self):
        self.toolbarFrame = tk.Frame(self.parent)
        self.toolbarFrame.grid(row=0, column=0, columnspan=4, sticky="NW")
        self.toolbar = NavigationToolbar2Tk(
            self.focused_graph, self.toolbarFrame)

    def small_graph(self, key, row_num):
        canvas = FigureCanvasTkAgg(graph_obj_dict[key][0], self)
        canvas.get_tk_widget().grid(row=row_num * 2, column=6,
                                    rowspan=2, columnspan=1, ipadx=10, ipady=10)
        canvas.draw()

    def focus_target(self, key):

        global active
        active = graph_dict[key]


application = EnergyOracle()
application.geometry("1280x720")
animation1 = animation.FuncAnimation(fig, animate_main, interval=1000)
animation2 = animation.FuncAnimation(
    graph_obj_dict["DRAM"][0], animate, interval=1000, fargs=[graph_obj_dict["DRAM"][1], graph_dict["DRAM"]])
animation3 = animation.FuncAnimation(
    graph_obj_dict["CORE"][0], animate, interval=1000, fargs=[graph_obj_dict["CORE"][1], graph_dict["CORE"]])
animation4 = animation.FuncAnimation(
    graph_obj_dict["PACKAGE"][0], animate, interval=1000, fargs=[graph_obj_dict["PACKAGE"][1], graph_dict["PACKAGE"]])
animation5 = animation.FuncAnimation(
    graph_obj_dict["GPU"][0], animate, interval=1000, fargs=[graph_obj_dict["GPU"][1], graph_dict["GPU"]])
animation6 = animation.FuncAnimation(
    graph_obj_dict["TOTAL"][0], animate, interval=1000, fargs=[graph_obj_dict["TOTAL"][1], graph_dict["TOTAL"]])

application.mainloop()
