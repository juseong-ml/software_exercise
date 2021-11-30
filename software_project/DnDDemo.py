import sys
from TkinterDnD2 import DND_FILES, TkinterDnD

if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
from TkinterDnD2 import *


def drop(event):
    entry_sv.set(event.data)


root = TkinterDnD.Tk()
entry_sv = StringVar()
entry_sv.set('Drop Here !')
entry = Entry(root, textvar=entry_sv, height=30, width=60)
entry.pack(fill=X, padx=10, pady=10)
entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', drop)
root.mainloop()