from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from tkinter import ttk
import tkinter as tk
import matplotlib
import pyperclip
matplotlib.use("TKAgg")
from forecast.forecaster import Forecaster
from collections import deque
from collections import defaultdict
from forecast.influx_connection import InfluxDBConnection
from datetime import datetime, timedelta
import pandas as pd

terms_string = '''The Energy Oracle application monitors component energy use on a per-system\
basis. Collected data feeds into a machine learning model which predicts\
future energy usage. The Oracle is intended for use as both a commercial\
and consumer product. A user could anticipate lulls in computational\
overhead, and reduce power draw accordingly. This would both lower costs\
and lower excess energy consumption.\n\n
To accomplish this, The Energy Oracle requires read/write access to the\
interface of the model-specific-registers. Root privileges are needed\
for this task, explaining the password prompt.\n\n
The entire Energy Oracle project is open source and available for\
inspection to ensure full transparency. Your password is never saved by us.\n\n
(https://github.com/aservet1/energyOracle)'''

LARGE_FONT = ("Helvetica", 20)
MEDIUM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

style.use("ggplot")





active_key = "TOTAL"
graph_dict = defaultdict(deque)

max_readings = 480

host = 'localhost'
port = 8086
dbname = 'energyDB'
measurement = 'energy'

conn = InfluxDBConnection(host, port, dbname)
now = datetime.now()
readings = conn.get_readings(None, None, measurement, max_readings)
forecasts = None

for readings in readings:
    for reading in readings:
        graph_dict["TIME"].append(datetime.strptime(reading["time"], "%Y-%m-%dT%H:%M:%SZ"))
        total = 0
        for column in ["DRAM", "GPU", "PKG", "CORE"]:
            val = reading[column]
            total += val
            graph_dict[column].append(val)
        graph_dict["TOTAL"].append(total)
        

graph_obj_dict = defaultdict(list)

for key in graph_dict:
    if key != "TIME":
        f2 = Figure(figsize=(2.5, 1.25), dpi=100)
        f2plot = f2.add_subplot()
        graph_obj_dict[key].append(f2)
        graph_obj_dict[key].append(f2plot)

active = graph_dict[active_key]

fig = Figure(figsize=(8, 4), dpi=100)
plot = fig.add_subplot()



def get_prediction():
    print("Getting prediction")
    f = Forecaster(None, None, host, port, dbname, measurement)
    f.run()
    global forecasts
    forecasts = f.forecasts
    df = pd.DataFrame()
    df["ds"] = forecasts["DRAM"]["ds"].copy()
    columns = {"DRAM", "CPU", "CORE", "PKG"}
    total_stuff = []
    for a, b, c, d in zip(forecasts["DRAM"]["yhat"], forecasts["CORE"]["yhat"], forecasts["CORE"]["yhat"], forecasts["PKG"]["yhat"]):
        total_stuff.append(a + b + c + d)
    df["yhat"] = pd.Series(total_stuff)
    forecasts["TOTAL"] = df

        



get_prediction()   
    

def animate(i, graph, deq, domain):
    xList = graph_dict["TIME"]
    yList = deq
    graph.clear()
    graph.plot(xList, yList)
    graph.get_xaxis().set_visible(False)
    graph.patch.set_edgecolor('black')
    graph.patch.set_linewidth('1')


def animate_main(i):
    reading = [r for r in conn.get_last_reading(measurement)][0][0]
    now = datetime.now()
    xListPredicted = []
    yListPredicted = []
    for time, prediction in zip(forecasts[active_key]["ds"], forecasts[active_key]["yhat"]):
        if (time < now + timedelta(hours=1)) and (time > now - timedelta(hours=2)):
            xListPredicted.append(time)
            yListPredicted.append(prediction)
    xListActual = graph_dict["TIME"]
    yListActual = []
    if reading['time'] != xListActual[-1]:
        if len(xListActual) == max_readings:
            for column in {"DRAM", "GPU", "PKG", "CORE", "TOTAL", "TIME"}:
                graph_dict[column].popleft()
        graph_dict["TIME"].append(datetime.strptime(reading["time"], "%Y-%m-%dT%H:%M:%SZ"))
        total = 0
        for column in {"DRAM", "GPU", "PKG", "CORE"}:
            val = reading[column]
            total += val
            graph_dict[column].append(val)
        graph_dict["TOTAL"].append(total)
    xListActual = []
    print(xListActual, xListPredicted, yListActual, yListPredicted)
    for actual, time in zip(active, graph_dict["TIME"]):
        if time > (now - timedelta(hours=2)):
            xListActual.append(time)
            yListActual.append(actual)
    plot.clear()
    print(xListPredicted)
    plot.patch.set_edgecolor('black')
    plot.patch.set_linewidth('1')


class EnergyOracle(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        icon = tk.PhotoImage(file="gui/icon.png")
        self.iconphoto(False, icon)

        s = ttk.Style()
        s.theme_use("default")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(0, weight=5)
        container.grid_columnconfigure(0, weight=5)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=lambda: self.quit())
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frame_dict = {}

        for F in (HomePage, GraphPage, Splash):

            frame = F(container, self)
            self.frame_dict[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Splash)

    def show_frame(self, container):
        frame = self.frame_dict[container]
        frame.tkraise()

    def quit(self):
        self.destroy()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.background_image = tk.PhotoImage(file="gui/BG_name.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        tc_label = ttk.Label(self, text=terms_string,
                             font=LARGE_FONT, borderwidth=4, padding=5, relief='solid', wraplength=615)
        tc_label.pack(pady=(125, 0), ipadx=10, ipady=10)

        button_agree = ttk.Button(
            self, text="Agree", command=lambda: load_graph_page())
        button_agree.place(x=875, y=600)

        button_disagree = ttk.Button(
            self, text="Disagree", command=lambda: controller.quit())
        button_disagree.place(x=875, y=625)

        button_git = ttk.Button(self, text="Copy URL",
                                command=lambda: copy_url())
        button_git.place(x=875, y=650)

        def copy_url():
            pyperclip.copy("https://github.com/aservet1/energyOracle")

        def load_graph_page():
            controller.show_frame(GraphPage)
            controller.frame_dict[GraphPage].create_toolbar()


class Splash(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.background_image = tk.PhotoImage(file="gui/BG_name.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_start = ttk.Button(
            self, text="Start", command=lambda: controller.show_frame(HomePage))
        button_start.place(x=875, y=600)

        button_start = ttk.Button(
            self, text="Quit", command=lambda: controller.quit())
        button_start.place(x=875, y=625)


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent

        self.main_graph()
        self.create_buttons()

        small_graph_objects = {}

        i = 0
        for key in graph_dict:
            if key != "TIME":
                self.small_graph(key, i)
                i += 1

        self.focus_target("DRAM")

    # def clear_test(self):
    #     self.focused_graph

    def create_buttons(self):
        self.label_display = ttk.Label(
            self, font=LARGE_FONT, background="white")
        self.label_display.grid(row=0, column=0, sticky="S")

        self.button_start = ttk.Button(
            self, text="START SERVICE", state="enabled", command=lambda: self.start_service())
        self.button_stop = ttk.Button(
            self, text=" STOP SERVICE ", state="disabled", command=lambda: self.stop_service())
        self.button_start.grid(row=9, column=0, sticky="SW", padx=(100, 0))
        self.button_stop.grid(row=10, column=0, sticky="NW", padx=(100, 0))

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
            self,  text="PKG USAGE", font=LARGE_FONT, background="white")
        label_package.grid(row=4, column=5, sticky="S")
        button_package = ttk.Button(
            self, text="FOCUS", command=lambda: self.focus_target("PKG"))
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

    def start_service(self):
        self.button_start.configure(state="disabled")
        self.button_stop.configure(state="enabled")

    def stop_service(self):
        self.button_start.configure(state="enabled")
        self.button_stop.configure(state="disabled")

    def main_graph(self):
        # global fig
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().grid(row=0, column=0, rowspan=10,
                                    columnspan=4, sticky="NS")
        canvas.draw()

        self.focused_graph = canvas

    def create_toolbar(self):
        self.toolbarFrame = tk.Frame(self.parent)
        self.toolbarFrame.grid(row=5, column=0, columnspan=4, sticky="NW")
        self.toolbar = NavigationToolbar2Tk(
            self.focused_graph, self.toolbarFrame)

    def small_graph(self, key, row_num):
        canvas = FigureCanvasTkAgg(graph_obj_dict[key][0], self)
        canvas.get_tk_widget().grid(row=row_num * 2, column=6,
                                    rowspan=2, columnspan=1, sticky="NS")
        canvas.draw()


    def focus_target(self, key):

        global active, active_key
        active_key = key
        active = graph_dict[key]
        self.label_display.configure(text="DISPLAYING: " + key)


application = EnergyOracle()
interval = 2000
application.geometry("1280x720")
animation1 = animation.FuncAnimation(fig, animate_main, interval=interval)
animation2 = animation.FuncAnimation(
    graph_obj_dict["DRAM"][0], animate, interval=interval, fargs=[graph_obj_dict["DRAM"][1], graph_dict["DRAM"], 'DRAM'])
animation3 = animation.FuncAnimation(
    graph_obj_dict["CORE"][0], animate, interval=interval, fargs=[graph_obj_dict["CORE"][1], graph_dict["CORE"], 'CORE'])
animation4 = animation.FuncAnimation(
    graph_obj_dict["PKG"][0], animate, interval=interval, fargs=[graph_obj_dict["PKG"][1], graph_dict["PKG"], "PKG"])
animation5 = animation.FuncAnimation(
    graph_obj_dict["GPU"][0], animate, interval=interval, fargs=[graph_obj_dict["GPU"][1], graph_dict["GPU"], "GPU"])
animation6 = animation.FuncAnimation(
    graph_obj_dict["TOTAL"][0], animate, interval=interval, fargs=[graph_obj_dict["TOTAL"][1], graph_dict["TOTAL"], "TOTAL"])

application.mainloop()
conn.close()

