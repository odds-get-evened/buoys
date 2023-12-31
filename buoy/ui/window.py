import datetime
import os
import tkinter as tk
from threading import Thread
from tkinter import BOTH, EW, LEFT, VERTICAL, RIGHT, Y, END, HORIZONTAL, BOTTOM, X, W, TOP, N, S, E, NW
from tkinter.ttk import Notebook, Treeview

from buoy.hourly import BuoyHourly
from buoy.ui.component.observation_tree import ObservationTree


class BuoyWindow:
    def __init__(self, p=None):
        # hourly instance to grab the datas
        self.data_nb = None
        self.obs_tree = None
        self.buoys_hourly = None

        # add all Tk component fields
        self.main_nb_tab2 = None
        self.main_nb = None
        self.main_nb_tab1 = None
        self.main_frame = None

        self.win = tk.Tk() if p is None else tk.Toplevel(p)

        # add Tk StringVars
        self.loc_sv = tk.StringVar()
        self.start_hr_sv = tk.IntVar(value=1)
        self.end_hr_sv = tk.IntVar(value=6)
        self.stn_id_sv = tk.StringVar(value='41115')

        self.win.title("buoys")
        '''
        self.width = 640
        self.height = 480
        '''
        self.width = 360
        self.height = 480
        self.win.minsize(self.width, self.height)
        self.x = int((self.win.winfo_screenwidth() / 2) - (self.width / 2))
        self.y = int((self.win.winfo_screenheight() / 2) - (self.height / 2))
        self.win.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

        self.boot_up()

        self.build()

        self.post_build()

        self.win.mainloop()

    def boot_up(self):
        if os.name == 'nt':
            self.windows_boot()
        elif os.name == 'posix':
            # apple OS support
            pass
        else:
            pass

    def windows_boot(self):
        # do windows relevant stuff here
        pass

    def build(self):
        self.main_frame = tk.Frame(self.win)

        self.main_nb = Notebook(self.main_frame)
        self.main_nb_tab1 = tk.Frame(self.main_nb)
        self.main_nb_tab1.pack(expand=True, fill=BOTH)
        self.main_nb_tab2 = tk.Frame(self.main_nb)
        self.main_nb.add(self.main_nb_tab1, text='hourly')
        self.main_nb.add(self.main_nb_tab2, text='stations')
        self.main_nb.pack(expand=True, fill=BOTH)

        self.main_nb_tab1.columnconfigure(1, weight=1)

        stn_lbl = tk.Label(self.main_nb_tab1, text='station ID')
        stn_lbl.grid(row=0, column=0)

        stn_id_txt = tk.Entry(self.main_nb_tab1, textvariable=self.stn_id_sv)
        stn_id_txt.grid(row=0, column=1, sticky=EW)

        start_hr_lbl = tk.Label(self.main_nb_tab1, text='start hour')
        start_hr_lbl.grid(row=1, column=0)

        start_hr_txt = tk.Entry(self.main_nb_tab1, textvariable=self.start_hr_sv)
        start_hr_txt.grid(row=1, column=1, sticky=EW)

        end_hr_lbl = tk.Label(self.main_nb_tab1, text='ending hour')
        end_hr_lbl.grid(row=2, column=0)

        start_hr_txt = tk.Entry(self.main_nb_tab1, textvariable=self.end_hr_sv)
        start_hr_txt.grid(row=2, column=1, sticky=EW)

        get_obs_btn = tk.Button(self.main_nb_tab1, text='get observations')
        get_obs_btn.grid(row=3, column=0, columnspan=2, sticky='ew')
        get_obs_btn.bind('<ButtonRelease-1>', self.get_observations_evt)

        self.data_nb = Notebook(self.main_nb_tab1)
        self.data_nb.grid(row=4, column=0, columnspan=2, sticky=N+S+E+W)

        obs_panel = tk.Frame(background='red')
        obs_panel.pack(fill=BOTH, expand=True)
        self.data_nb.add(obs_panel, text='list')
        
        self.obs_tree = ObservationTree(obs_panel, selectmode='browse')

        vis_panel = tk.Frame(background='green')
        vis_panel.pack(fill=BOTH, expand=True)
        self.data_nb.add(vis_panel, text='chart')

        self.main_frame.pack(expand=True, fill=BOTH)

    def post_build(self):
        pass

    def get_observations_evt(self, evt):
        [self.obs_tree.delete(o) for o in self.obs_tree.get_children()]
        stn_id = self.stn_id_sv.get()
        start_hr = self.start_hr_sv.get()
        end_hr = self.end_hr_sv.get()

        self.buoys_hourly = BuoyHourly(stn_id, start_hr, end_hr)

        obs = self.buoys_hourly.get_observations()

        [(self.obs_tree.insert('', END, values=(
            o['id'],
            datetime.datetime.fromtimestamp(o['timestamp']).strftime("%c"),
            o['wind_direction'],
            o['wind_speed'],
            o['gusts'],
            o['wave_height'],
            o['dominant_wave_period'],
            o['avg_wave_period'],
            o['mean_wave_direction'],
            o['barometer'],
            o['air_temp'],
            o['water_temp'],
            o['dewpoint'],
            o['visibility'],
            o['pressure_tendency'],
            o['tide']
        )), print(o)) for o in obs]
