from tkinter import Scrollbar, BOTH, VERTICAL, HORIZONTAL, Y, RIGHT, X, BOTTOM
from tkinter.ttk import Treeview


class ObservationTree(Treeview):
    def __init__(self, p, selectmode='browse'):
        super().__init__(p, selectmode=selectmode)

        self.vscroll = None
        self.hscroll = None

        self['show'] = 'headings'

        self.build_columns()

        self.set_vscroll(Scrollbar(p, orient=VERTICAL, command=self.yview))
        self.get_vscroll().pack(fill=Y, side=RIGHT)
        self.set_hscroll(Scrollbar(p, orient=HORIZONTAL, command=self.xview))
        self.get_hscroll().pack(fill=X, side=BOTTOM)

        self.configure(yscrollcommand=self.get_vscroll().set, xscrollcommand=self.get_hscroll().set)

        self.pack(fill=BOTH, expand=False)

    def get_vscroll(self) -> Scrollbar:
        return self.vscroll

    def set_vscroll(self, v: Scrollbar) -> None:
        self.vscroll = v

    def get_hscroll(self) -> Scrollbar:
        return self.hscroll

    def set_hscroll(self, v: Scrollbar) -> None:
        self.hscroll = v

    def build_columns(self):
        self['columns'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
        self.heading(1, text='station')
        self.column(1, width=1, minwidth=60)
        self.heading(2, text='time')
        self.column(2, width=1, minwidth=150)
        self.heading(3, text='wind dir.')
        self.column(3, width=1, minwidth=60)
        self.heading(4, text='wind speed')
        self.column(4, width=1, minwidth=30)
        self.heading(5, text='gusts')
        self.column(5, width=1, minwidth=30)
        self.heading(6, text='wave height')
        self.column(6, width=1, minwidth=30)
        self.heading(7, text='dominant wave period')
        self.column(7, width=1, minwidth=30)
        self.heading(8, text='avg. wave period')
        self.column(8, width=1, minwidth=30)
        self.heading(9, text='mean wave direction')
        self.column(9, width=1, minwidth=30)
        self.heading(10, text='barometer')
        self.column(10, width=1, minwidth=30)
        self.heading(11, text='air temp.')
        self.column(11, width=1, minwidth=30)
        self.heading(12, text='water temp.')
        self.column(12, width=1, minwidth=30)
        self.heading(13, text='dewpoint')
        self.column(13, width=1, minwidth=30)
        self.heading(14, text='visibility')
        self.column(14, width=1, minwidth=30)
        self.heading(15, text='pressure trend')
        self.column(15, width=1, minwidth=30)
        self.heading(16, text='tide')
        self.column(16, width=1, minwidth=30)
        self.bind('<ButtonRelease-1>', None)
