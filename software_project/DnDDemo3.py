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



class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initialzie()

        self.tag = dict()
    def initialzie(self):
        self.entry_sv = StringVar()
        self.entry_sv.set('Drop Here !')
        self.entry_path = Entry(root, textvar=self.entry_sv,width=50, font=15)
        self.entry_path.pack(fill=X, padx=10, pady=10)
        self.entry_path.drop_target_register(DND_FILES)
        self.entry_path.dnd_bind('<<Drop>>', self.drop)

        self.entry_tag = Entry(root, width=30)
        self.entry_tag.place(width=200, height=30)
        self.entry_tag.insert(0, '#')
        self.entry_tag.pack(pady=20)

        self.btn = Button(root, text='확인', command=self.get_value)
        self.btn.pack(pady=5)

        # btn.grid(column=1, row=0)

    def drop(self, event):
        self.entry_sv.set(event.data)
        fname = self.entry_path.get().split('/')[-1]
        self.tag['fileName'] = fname
        self.tag['dir'] = self.entry_path.get()

    def get_value(self):
        value = self.entry_tag.get()
        # global tag_dict
        self.tag['tag'] = value[1:]
        # print(self.tag)
        with open('tag_list.csv', 'w') as f:
            w = csv.writer(f)
            w.writerow(self.tag.keys())
            w.writerow(self.tag.values())
        self.quit()




if __name__ == '__main__':
    root = TkinterDnD.Tk()
    root.geometry("300x150+600+300")
    root.title('Make Tag')
    App(root)


    root.mainloop()