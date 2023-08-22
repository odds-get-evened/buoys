import os
import tkinter as tk
from tkinter import BOTH, EW, LEFT, VERTICAL, RIGHT, Y
from tkinter.ttk import Notebook, Treeview

from buoy.hourly import BuoyHourly


class BuoyWindow:
    def __init__(self, p=None):
        # hourly instance to grab the datas
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

        obs_panel = tk.Frame(self.main_nb_tab1)
        obs_panel.grid(row=4, column=0, sticky='ew')

        obs_tree = Treeview(obs_panel, selectmode='browse')
        obs_tree.pack(expand=True, fill=BOTH, side=LEFT)
        obs_tree['show'] = 'headings'
        obs_tree['columns'] = (1, 2)
        obs_tree.heading(1, text='time')
        obs_tree.heading(2, text='station ID')
        obs_tree.bind('<ButtonRelease-1>', None)

        obs_tree_scroll = tk.Scrollbar(obs_panel, orient=VERTICAL, command=obs_tree.yview)
        obs_tree.configure(yscrollcommand=obs_tree_scroll.set)
        obs_tree_scroll.pack(side=RIGHT, expand=False, fill=Y)

        self.main_frame.pack(expand=True, fill=BOTH)

    def post_build(self):
        pass

    def get_observations_evt(self, evt):
        print(f"station ID: {self.stn_id_sv.get()}")
        stn_id = self.stn_id_sv.get()
        start_hr = self.start_hr_sv.get()
        end_hr = self.end_hr_sv.get()

        self.buoys_hourly = BuoyHourly(stn_id, start_hr, end_hr)

        obs = self.buoys_hourly.get_observations()
        [print(i) for i in obs]
