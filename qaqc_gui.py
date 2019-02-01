from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import json
import pandas as pd
 
LARGE_FONT = ('Verdanna', 12)
LARGE_FONT_BOLD = ('Verdanna', 12, 'bold')
NORM_FONT = ('Verdanna', 10)
NORM_FONT_BOLD = ('Verdanna', 10, 'bold')
SMALL_FONT = ('Verdanna', 8)

window = Tk()
window.title("RSD Lidar QAQC")
window.geometry('375x800')

section_rows = {
    'metadata': 0,
    'files': 1,
    'dirs': 2,
    'checks': 3,
    'surfaces': 4,
    'run_button': 5,
    }

##################################################################### 
'''Metadata'''

meta_frame = Frame(window)
meta_frame.grid(row=section_rows['metadata'], sticky=NSEW)

label = Label(meta_frame, text='Populate Metadata', font=LARGE_FONT_BOLD)
label.grid(row=0, columnspan=3, pady=(10, 0), sticky=W)

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
meta_label = Label(meta_frame, text=metadata[m][0])
meta_label.grid(column=0, row=row, sticky=W)
proj_name_var = StringVar()
proj_name_var.set("(Select Project ID)")
metadata[m][1] = OptionMenu(meta_frame, proj_name_var, *get_proj_names())
metadata[m][1].grid(column=1, row=row, sticky=EW)

m = 'hor_datum'
row = 2
meta_label = Label(meta_frame, text=metadata[m][0])
meta_label.grid(column=0, row=row, sticky=W)
wkt_var = StringVar()
wkt_var.set("(Select WKT ID)")
metadata[m][1] = OptionMenu(meta_frame, wkt_var, *get_wkt_ids())
metadata[m][1].grid(column=1, row=row, sticky=EW)

m = 'tile_size'
row = 3
meta_label = Label(meta_frame, text=metadata[m][0])
meta_label.grid(column=0, row=row, sticky=W)
metadata[m][1] = Entry(meta_frame, width=30)
metadata[m][1].grid(column=1, row=row, sticky=EW)

m = 'exp_classes'
row = 4
meta_label = Label(meta_frame, text=metadata[m][0])
meta_label.grid(column=0, row=row, sticky=W)
metadata[m][1] = Entry(meta_frame, width=30)
metadata[m][1].grid(column=1, row=row, sticky=EW)


#####################################################################
'''Files'''

files_frame = Frame(window)
files_frame.grid(row=section_rows['files'], sticky=NSEW)

label = Label(files_frame, text='Select Files', font=LARGE_FONT_BOLD)
label.grid(row=0, columnspan=3, pady=(10, 0), sticky=W)

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
    check_label = Label(files_frame, text=files_to_set[d][0])
    check_label.grid(column=0, row=i, sticky=W)

    btn = Button(files_frame, text="...", command=files_to_set[d][2])
    btn.grid(column=1, row=i, sticky=W)

    files_to_set[d][1] = Label(files_frame, 
                               text='(Select {} file)'.format(files_to_set[d][3]))
    files_to_set[d][1].grid(column=2, row=i, sticky=W)

#####################################################################
'''Directories'''

dirs_frame = Frame(window)
dirs_frame.grid(row=section_rows['dirs'], sticky=NSEW)

label = Label(dirs_frame, text='Select Directories', font=LARGE_FONT_BOLD)
label.grid(row=0, columnspan=3, pady=(10, 0), sticky=W)

def get_dir():
    return tkFileDialog.askdirectory()

def dir0_clicked():
    dirs_to_set['qaqc_dir'][1].configure(text=get_dir())
def dir1_clicked():
    dirs_to_set['las_tile_dir'][1].configure(text=get_dir())
def dir2_clicked():
    dirs_to_set['qaqc_gdb'][1].configure(text=get_dir())
def dir3_clicked():
    dirs_to_set['dz_binary_dir'][1].configure(text=get_dir())

dirs_to_set = {
    'qaqc_dir': ['QAQC Home', None, dir0_clicked],
    'las_tile_dir': ['Las Tiles', None, dir1_clicked],
    'qaqc_gdb': ['QAQC GeoDatabase', None, dir2_clicked],
    'dz_binary_dir': ['Dz Surfaces', None, dir3_clicked],
    }

for i, d in enumerate(dirs_to_set, 1):
    check_label = Label(dirs_frame, text=dirs_to_set[d][0])
    check_label.grid(column=0, row=i, sticky=W)

    btn = Button(dirs_frame, text="...", command=dirs_to_set[d][2])
    btn.grid(column=1, row=i, sticky=W)

    dirs_to_set[d][1] = Label(dirs_frame, text="(Select Directory)")
    dirs_to_set[d][1].grid(column=2, row=i, sticky=W)


#####################################################################
'''Checks'''

checks_frame = Frame(window)
checks_frame.grid(row=section_rows['checks'], sticky=NSEW)

label = Label(checks_frame, text='Select Checks', font=LARGE_FONT_BOLD)
label.grid(row=0, columnspan=3, pady=(10, 0), sticky=W)

checks_to_do = {
    'naming_convention': ['Naming Convention', None],
    'version': ['Version', None],
    'pdrf': ['Point Data Record Format (PDRF)', None],
    'gps_time_type': ['GPS Time Type', None],
    'hor_datum': ['Horizontal Datum', None],
    'ver_datum': ['Vertical Datum', None],
    'point_source_ids': ['Point Source IDs (Flight Line #)', None],
    'unexpected_classes': ['Unexpected Classes', None],
    }

for i, c in enumerate(checks_to_do, 1):
    checks_to_do[c][1] = BooleanVar()
    checks_to_do[c][1].set(True)
    chk = Checkbutton(checks_frame, text=checks_to_do[c][0], var=checks_to_do[c][1], 
                      anchor=W, justify=LEFT)
    chk.grid(column=0, row=i, sticky=W)
 
#####################################################################
'''Surfaces'''

surf_frame = Frame(window)
surf_frame.grid(row=section_rows['surfaces'], sticky=NSEW)

label = Label(surf_frame, text='Select Surfaces', font=LARGE_FONT_BOLD)
label.grid(row=0, columnspan=3, pady=(10, 0), sticky=W)

surfaces_to_make = {
    'dz': ['Dz', None],
    'hillshade': ['Hillshade', None],
    }

for i, s in enumerate(surfaces_to_make, 1):
    surfaces_to_make[s][1] = BooleanVar()
    surfaces_to_make[s][1].set(True)
    chk = Checkbutton(surf_frame, text=surfaces_to_make[s][0], 
                      var=surfaces_to_make[s], 
                      anchor=W, justify=LEFT)
    chk.grid(column=0, row=i, sticky=W)

#####################################################################

run_frame = Frame(window)
run_frame.grid(row=section_rows['run_button'], sticky=NSEW, pady=(10, 0))

def verify_input():
    pass

def save_settings():
    settings = {'checks_to_do': {}}

    for k, v in checks_to_do.iteritems():
        settings['checks_to_do'].update({k: v[1].get()})

    for k, v in dirs_to_set.iteritems():
        settings.update({k: v[1].cget('text')})

    for k, v in files_to_set.iteritems():
        settings.update({k: v[1].cget('text')})

    for k, v in metadata.iteritems():
        settings.update({k: v[1].get()})

    print(settings)
    with open('Z:\qaqc\qaqc_config.json', 'w') as f:
        json.dump(settings, f)

def run_qaqc_process():
    verify_input()
    save_settings()
    

btn = Button(run_frame, text="Run QAQC Processes", 
             command=run_qaqc_process, height=2)
btn.grid(column=0, row=0, sticky=EW, padx=(120, 0))

window.mainloop()
