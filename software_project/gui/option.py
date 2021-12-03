from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from PIL import Image
import os
import shutil



root = Tk()

root.title('sorting')
root.geometry('400x530+500+400')



root.resizable(False, False)


#파일 추가
def add_file():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요", \
                                        filetypes=(("모든 파일", "*.*"),('PNG 파일', "*.png")),\
                                    initialdir="C:/Users/Jessie인영/Desktop/\
                                    software_exercise/software_project/insta_images")
    for file in files:
        list_file.insert(END, file)


#선택 삭제
def del_file():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)


#저장 경로 (폴더)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected is None: #사용자가 취소를 누를때
        return
    txt_dest_path.delete(0,END)
    txt_dest_path.insert(0,folder_selected)

#시작
def start():
    #각 옵션들 값을 확인
    if list_file.size() == 0:
        msgbox.showwarning("경고", "이미지 파일을 추가하세요")
        return
    # 저장 경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 선택하세요")
        return
    sort_img()

def sort_img(): #모든 파일 목록을 가져오기
    #정렬 방법
    sort_method = cmb_sort.get()
    if sort_method == '날짜별':
        sort_method = 1
    else: # 이름별
        sort_method = 2

    space_method = cmb_space.get()
    if space_method == '복사':
        space_method = 1
    else: # 이동
        space_method = 2

    image_list = [list_file.get(0,END)] #선택한 파일들

    for idx, img in enumerate(image_list):
        progress = (idx +1) / len(image_list) * 100
        p_var.set(progress)
        progress_bar.update()

    path_before = os.path.dirname(list_file.get(0))
    #path_before :  #C:/Users/Jessie인영/Desktop/software_exercise/software_project/insta
    category = [] # 분류 데이터 저장을 위해 빈 리스트 생성

    if sort_method == 1: #날짜별
        image_list = list(image_list[0])
        for file in image_list:

            temp_list = file.split('/')
            category.append(temp_list[-1].split('_')[1])
        temp_set = set(category)
        file_list = list(temp_set) # 날짜들 리스트
        path_after = txt_dest_path.get()
        filelist = os.listdir(path_before)
        dict = {}
        for file in filelist:
            folder_list = file.split('_')
            dict[file] = folder_list[1]

    if sort_method == 2: #이름별
        for file in list(image_list[0]):
            # print(file)
            temp_list = file.split('/') #파일명중 "_"로 분리하여 리스트화
            category.append(temp_list[-1].split('_')[0]) #리스트의 -2 인덱싱 데이터를 category에 추가
        # print(category)
        temp_set = set(category) #중복을 제거하기 위해 set 사용
        file_list = list(temp_set) #다시 리스트화화

        path_after = txt_dest_path.get()
        # 이동시킬 경로에 생성된 분류별 폴더 리스트화
        filelist = os.listdir(path_before)  # 이동시킬 파일명들을 리스트화
        dict = {}

        # 파일명에 대한 폴더명을 딕셔너리로 저장
        for file in filelist:
            temp_list = file.split("_")
            dict[file] = temp_list[-2]  # {'파일명' : '분류'} 형태의 딕셔너리 생성


    for file in file_list:
        try:
            os.makedirs(path_after+'/'+file)
        except:
            pass

    # 딕셔너리 정보 활용하여 파일 이동
    for key, value in dict.items():
        if space_method == 1: #복사
        # shutil.copy(path_after + '/' + value)
            shutil.copy(path_before + "/" + key, path_after+ "/" + value)
        else: #이동
            shutil.move(path_before + "/" + key, path_after+ "/" + value)

        # print(path_before + '/' + key, path_after + '/' + value)
    msgbox.showinfo("알림", "작업이 완료되었습니다.")



#파일 프레임 (파일 추가, 선택 삭제)
file_frame= Frame(root)
file_frame.pack(fill='x',padx=5,pady=5)

btn_add_file = Button(file_frame, padx=5, pady=5, width=10, text='파일추가', command=add_file)
btn_add_file.pack(side='left')

btn_del_file = Button(file_frame,padx=5, pady=5, width=10,  text='선택삭제', command=del_file)
btn_del_file.pack(side='right')

#리스트 프레임
list_frame = Frame(root)
list_frame.pack(fill='both')

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side='right', fill='y')

list_file = Listbox(list_frame, selectmode='extended', height=15,yscrollcommand=scrollbar.set)
list_file.pack(side='left', fill='both', expand=True)
scrollbar.config(command=list_file.yview)

#저장 경로 프레임
path_frame = LabelFrame(root, text='저장경로')
path_frame.pack(fill='x')
txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side='left', fill='x', expand=True,padx=5,pady=5, ipady=4) #높이 변경

btn_dest_path = Button(path_frame, text='찾아보기', width=10, command=browse_dest_path)
btn_dest_path.pack(side='right',padx=5,pady=5, ipady=5)


frame_optiom = LabelFrame(root, text='옵션')
frame_optiom.pack(padx=5,pady=5)

#가로 넓이 옵션
#가로 넓이 레이블
lbl_sort = Label(frame_optiom, text='정렬 방법', width=8)
lbl_sort.pack(side='left',padx=5,pady=5)
#가로 넓이 콤보
opt_sort = ['날짜별', '이름별']
cmb_sort = ttk.Combobox(frame_optiom, state='readonly', values=opt_sort, width=10)
cmb_sort.current(0)
cmb_sort.pack(side='left',padx=5,pady=5)

# 간격 옵션
# 간격 옵션 레이블
lbl_space = Label(frame_optiom, text='정렬 형태', width=8)
lbl_space.pack(side='left')
# 간격 옵션 콤보
opt_space = ['이동', '복사']
cmb_space = ttk.Combobox(frame_optiom, state='readonly', values=opt_space, width=10)
cmb_space.current(0)
cmb_space.pack(side='left',padx=5,pady=5)

#진행 상황 progress bar
frame_progress = LabelFrame(root, text='진행상황')
frame_progress.pack(fill='x',padx=5,pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable= p_var)
progress_bar.pack(fill='x',padx=5,pady=5)

#실행 프레임
frame_run = Frame(root)
frame_run.pack(fill='x',padx=5,pady=5)


btn_close = Button(frame_run, padx=5, pady=5, text='닫기', width=10, command=root.quit)
btn_close.pack(side='right',padx=5,pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text='시작', width=10, command=start)
btn_start.pack(side='right',padx=5,pady=5)





#파일 포맷 옵션




root.mainloop()