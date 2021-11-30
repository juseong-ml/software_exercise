from tkinter import *
from tkinter import filedialog


def callback1(): #경로를 잡기 위한 함수
    name = filedialog.askdirectory(initaildir='.')
    depot.insert(0, str(name))

def callback2(): #경로를 잡기 위한 함수2
    name = filedialog.askdirectory(initialdir='.')
    depot2.insert(0, str(name))

def arrimg():
    imgarr.arrage_img(str(depot.get() + "/"), str(dep))

app = Tk()
app.geometry('320x240+400+300')
app.title("picAmaze")

Label(app, text="불러올 경로: ").place(x=10,y=10,width=90,height=30)
depot = Entry(app)
depot.place(x=110, y=10, width=200, height=30)
Button(app, text="읽어올 경로: ", command=callback1()).place(x=330,y=10,width=100,height=30)
Label(app, text="저장할 경로: ", command=callback2()).place(x=330,y=50,width=100,height=30)
depot2 = Entry(app)

depot2.place(x=110,y=50,width=200,height=30)

Button(app, text='저장할 경로 설정', command=callback2).place(x=330,y=50,width=100,height=30)
Button(app, text='정리 시작', command=arrimg).place(x=70,y=100,width=100,height=30)
Button(app, text='종료', command=app.quit).place(x=180,y=100,width=100,height=30)

Label(app, text = "정리 시작 버튼을 누른 후 활성화 되기 전까지는 작업을 수행 중 입니다.", fg="red",bg="black").place(x=30,y=140,width=400,height=30)

Label(app, text = "만든 사람 : KEI, http://kshyun87.tistory.com", fg="red",bg="black").place(x=30,y=180,width=400,height=30)

app.mainloop()



출처: https://kshyun87.tistory.com/35 [Coding is 취미]