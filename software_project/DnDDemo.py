import sys
from tkinter import filedialog
from TkinterDnD2 import DND_FILES, TkinterDnD
import pandas as pd
import csv

if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
from TkinterDnD2 import *

def drop(event):
    entry_sv.set(event.data)
    fname = entry_path.get().split('/')[-1]
    # print(entry_path.get().split('/'))
    print(fname)
    print(type)
    # global tag_dict
    # tag_dict['directory'] = entry_path.get()
    # tag_dict['fileName'] = fname

def get_value():
    value= entry_tag.get()
    # global tag_dict
    # tag_dict['tag'] = value[1:]
    root.quit()


root = TkinterDnD.Tk()
root.geometry("300x150+600+300")
root.title('Make Tag')

tmp = StringVar()

entry_sv = StringVar()
entry_sv.set('Drop Here !')

entry_path = Entry(root, textvar=entry_sv,width=50, font=15)
entry_path.pack(fill=X, padx=10, pady=10)
entry_path.drop_target_register(DND_FILES)
entry_path.dnd_bind('<<Drop>>', drop)



entry_tag = Entry(root, width=30)
entry_tag.place(width=200, height=30)
entry_tag.insert(0, '#')
entry_tag.pack(pady=20)

btn = Button(root, text='확인', command=get_value)
btn.pack(pady=5)

#
root.mainloop()