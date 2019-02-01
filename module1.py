import Tkinter as tk
import Tkconstants, tkFileDialog
import ttk
import os
import time
import json
import pandas as pd


LARGE_FONT = ('Verdanna', 12)
LARGE_FONT_BOLD = ('Verdanna', 12, 'bold')
NORM_FONT = ('Verdanna', 10)
NORM_FONT_BOLD = ('Verdanna', 10, 'bold')
SMALL_FONT = ('Verdanna', 8)

section_rows = {
    'metadata': 0,
    'files': 1,
    'dirs': 2,
    'checks': 3,
    'surfaces': 4,
    'run_button': 5,
    }


class QaqcApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.config_file = 'Z:\qaqc\qaqc_config.json'
        self.load_config()

        # show splash screen
        self.withdraw()
        splash = Splash(self)

        tk.Tk.wm_title(self, 'cBLUE')
        tk.Tk.iconbitmap(self, 'cBLUE_icon.ico')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save settings',
                             command=lambda: self.save_config())
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff=0)
        exchangeChoice.add_command(label='About', command=self.show_about)
        menubar.add_cascade(label='Help', menu=exchangeChoice)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        for F in (MainGuiPage,):  # makes it easy to add "pages" in future
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(MainGuiPage)

        # after splash screen, show main GUI
        time.sleep(1)
        splash.destroy()
        self.deiconify()

    def load_config(self):
        if os.path.isfile(self.config_file):
            with open(self.config_file) as cf:
                self.controller_configuration = json.load(cf)
        else:
           print("configuration file doesn't exist")

    def save_config(self):
        config = 'cblue_configuration.json'
        print('saving {}...\n{}'.format(config, self.controller_configuration))
        with open(config, 'w') as fp:
            json.dump(self.controller_configuration, fp)

    @staticmethod
    def show_about():
        about = tk.Toplevel()
        tk.Toplevel.iconbitmap(about, 'cBLUE_icon.ico')
        about.wm_title('About cBLUE')
        splash_img = tk.PhotoImage(file='cBLUE_splash.gif')
        label = tk.Label(about, image=splash_img)
        label.pack()
        b1 = ttk.Button(about, text='Ok', command=about.destroy)
        b1.pack()
        about.mainloop()

    @staticmethod
    def popupmsg(msg):
        popup = tk.Tk()
        popup.wm_title('!')
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side='top', fill='x', pady=10)
        b1 = ttk.Button(popup, text='Ok', command=popup.destroy)
        b1.pack()
        popup.mainloop()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        splash_img = tk.PhotoImage(file='Z:\qaqc\qaqc.gif', master=self)
        label = tk.Label(self, image=splash_img)
        label.pack()
        self.update()


class MainGuiPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        self.parent = parent  # container made in QaqcApp ?
        self.controller = controller  # QaqcApp ?
        
        print self.parent
        print self.controller.controller_configuration

        #  Build the GUI
        self.control_panel_width = 30
        self.build_gui()


    def build_gui(self):

        self.build_metadata()
        self.build_files()
            
        
    def build_metadata(self):
        """
        build metadata section
        """

        meta_frame = ttk.Frame(self)
        meta_frame.grid(row=section_rows['metadata'], sticky=tk.NSEW)

        label = tk.Label(meta_frame, text='Populate Metadata', font=LARGE_FONT_BOLD)
        label.grid(row=0, columnspan=3, pady=(10, 0), sticky=tk.W)

        def get_wkt_ids():
            wkts_file = 'Z:\qaqc\wkts_NAD83_2011_UTM.csv'
            wkts_df = pd.read_csv(wkts_file)
            wkt_ids = wkts_df.iloc[:, 1]
            return tuple(wkt_ids)

        def get_proj_names():
            with open('Z:\qaqc\project_list.txt', 'r') as f:
               project_ids = [s.strip() for s in f.readlines()]
            print project_ids
            return tuple(project_ids)

        metadata = {
            'project_name': ['Project Name', None],
            'hor_datum': ['Horizontal Datum', None],
            'tile_size': ['Tile Size (m)', None],
            'exp_classes': ['Expected Classes (comma sep.)', None],
            }

        m = 'project_name'
        row = 1
        meta_label = tk.Label(meta_frame, text=metadata[m][0])
        meta_label.grid(column=0, row=row, sticky=tk.W)
        proj_name_var = tk.StringVar()
        proj_name_var.set("(Select Project ID)")
        metadata[m][1] = tk.OptionMenu(meta_frame, proj_name_var, *get_proj_names())
        metadata[m][1].grid(column=1, row=row, sticky=tk.EW)

        m = 'hor_datum'
        row = 2
        meta_label = tk.Label(meta_frame, text=metadata[m][0])
        meta_label.grid(column=0, row=row, sticky=tk.W)
        wkt_var = tk.StringVar()
        wkt_var.set("(Select WKT ID)")
        metadata[m][1] = tk.OptionMenu(meta_frame, wkt_var, *get_wkt_ids())
        metadata[m][1].grid(column=1, row=row, sticky=tk.EW)

        m = 'tile_size'
        row = 3
        meta_label = tk.Label(meta_frame, text=metadata[m][0])
        meta_label.grid(column=0, row=row, sticky=tk.W)
        metadata[m][1] = tk.Entry(meta_frame, width=30)
        metadata[m][1].grid(column=1, row=row, sticky=tk.EW)

        m = 'exp_classes'
        row = 4
        meta_label = tk.Label(meta_frame, text=metadata[m][0])
        meta_label.grid(column=0, row=row, sticky=tk.W)
        metadata[m][1] = tk.Entry(meta_frame, width=30)
        metadata[m][1].grid(column=1, row=row, sticky=tk.EW)


    def build_files(self):
        '''Files'''

        files_frame = ttk.Frame(self)
        files_frame.grid(row=section_rows['files'], sticky=tk.NSEW)

        label = tk.Label(files_frame, text='Select Files', font=LARGE_FONT_BOLD)
        label.grid(row=0, columnspan=3, pady=(10, 0), sticky=tk.W)

        def get_file():
            return tkFileDialog.askopenfilename()

        def file0_clicked():
            files_to_set['contractor_shp'][1].configure(text=get_file())
        def file1_clicked():
            files_to_set['dz_classes_template'][1].configure(text=get_file())
        def file1_clicked():
            files_to_set['dz_export_settings'][1].configure(text=get_file())
        def file1_clicked():
            files_to_set['dz_mxd'][1].configure(text=get_file())

        files_to_set = {
            'contractor_shp': ['Contractor Tile Shapefile', None, file0_clicked, '.shp'],
            'dz_classes_template': ['Dz Classes Template', None, file1_clicked, '.lyr'],
            'dz_export_settings': ['Dz Export Settings', None, file1_clicked, '.xml'],
            'dz_mxd': ['QAQC ArcGIS Map', None, file1_clicked, '.mxd'],
            }

        for i, d in enumerate(files_to_set, 1):
            check_label = tk.Label(files_frame, text=files_to_set[d][0])
            check_label.grid(column=0, row=i, sticky=tk.W)

            btn = tk.Button(files_frame, text="...", command=files_to_set[d][2])
            btn.grid(column=1, row=i, sticky=tk.W)

            files_to_set[d][1] = tk.Label(files_frame, 
                                       text='(Select {} file)'.format(files_to_set[d][3]))
            files_to_set[d][1].grid(column=2, row=i, sticky=tk.W)
    
if __name__ == "__main__":
    app = QaqcApp()
    app.geometry('400x800')
    app.mainloop()  # tk functionality

