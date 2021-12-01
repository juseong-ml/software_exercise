import cv2
import numpy as np
from PIL import Image
import os # 파일명, 폴더명 정보를 읽어오기 위한 모듈
import shutil # 파일 이동을 위한 모듈


#파일명을 읽어와서 파일명의 분류 부분을 중복 없이 리스트화
def fileList(path_before: str) :
    file_list = os.listdir(path_before)
    category = [] # 분류 데이터 저장을 위해 빈 리스트 생성
    for file in file_list:
        temp_list = file.split('_') #파일명중 "_"로 분리하여 리스트화
        category.append(temp_list[-2]) #리스트의 -2 인덱싱 데이터를 category에 추가

    temp_set = set(category) #중복을 제거하기 위해 set 사용
    result = list(temp_set) #다시 리스트화화
    return result

# 분류 리스트를 받아와서 정해진 위치에 폴더 생성
def makeFolder(path_after:str, file_list:list):
    #폴더가 이미 생성되어 있다면 오류가 발생하므로 예외처리 진행
    for file in file_list:
        try:
            os.makedirs(path_after+"/"+file)
        except:
            pass


def moveFile(path_before, path_after):
    folderlist = os.listdir(path_after) # 이동시킬 경로에 생성된 분류별 폴더 리스트화
    filelist = os.listdir(path_before) #이동시킬 파일명들을 리스트화
    dict = {}

    #파일명에 대한 폴더명을 딕셔너리로 저장
    for file in filelist:
        temp_list = file.split("_")
        dict[file] = temp_list[-2] #{'파일명' : '분류'} 형태의 딕셔너리 생성

    #딕셔너리 정보 활용하여 파일 이동
    for key, value in dict.items():
        shutil.move(path_before+"/"+key, path_after+"/"+value)


if __name__ == '__main__':
    #분류할 파일이 있는 위치 폴더
    path_before = r'images'
        # r'분류필요한 파일 경로'
    file_list = fileList(path_before)

    #옮길 경로 폴더
    path_after = r'sorted'
        # r'옮길 폴더 경로'
    makeFolder(path_after,file_list)
    moveFile(path_before,path_after)