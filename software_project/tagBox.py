import tkinter as tk
# from tkinter import ttk
root = tk.Tk()
root.geometry("250x90+600+300")
root.title("Make Tag")


e = tk.Entry(root, width=30)
e.place(width=200, height=20)
e.insert(0, '#')
e.pack(pady=10)

def get_value():
    value= e.get()
    print(value[1:])


btn = tk.Button(root, text='확인', command=get_value)
btn.pack(pady=10)

root.mainloop()

