import tkinter as tk
from TkinterDnD2 import DND_FILES, TkinterDnD

def drop_inside_list_box(event):
    listb.insert('end', event.data)


def drop_inside_image_box(event):
    pass

root = TkinterDnD.Tk()
root.geometry("600x400")

listb = tk.Listbox(root, selectmode=tk.SINGLE, background = '#ffe0d6')
listb.pack(fill=tk.X)
listb.drop_target_register(DND_FILES)
listb.dnd_bind("<<Drop>>", drop_inside_list_box())

ibox = tk.Image(root)
ibox.pack()
ibox.drop_target_register(DND_FILES)
ibox.dnd_bind("<<Drop>>", drop_inside_image_box())

image = tk.PhotoImage(file='images/junghwa_001.jpg')
label = tk.Label(root, iamge=image)
label.pack()

root.mainloop()