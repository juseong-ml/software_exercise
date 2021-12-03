from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from PIL import Image
import os
import shutil
from software_project import insta
from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class App(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.initializer()

    def initializer(self):
        self.label = Label(self.root, text='ID를 입력하세요')
        self.label.pack()
        self.entry = Entry(self.root)
        self.entry.pack(padx=10, pady=6, fill='x')
        # self.entry.set('ID를 입력하세요')
        self.btn = Button(self.root, text='확인', command=self.crawling)
        self.btn.pack(pady=6)
        self.value = self.entry.get()

    # def get_value(self):
    #     self.value = self.entry.get()
    #     print(self.value)

    def crawling(self):

        baseUrl = 'https://www.instagram.com/'
        plusUrl = self.value
        # plusUrl = input('검색할 아이디를 입력하세요 : ')
        url = baseUrl + plusUrl

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)

        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        insta = soup.select('.v1Nh3.kIKUG._bz0w')

        n = 1
        for i in insta:
            # print('http://instagram.com/' + i.a['href'])
            imgUrl = i.select_one('.KL4Bh').img['src']
            with urlopen(imgUrl) as f:
                with open('./test_folder/' + plusUrl + '_' + str(n).zfill(3) + '.jpg', 'wb') as h:
                    img = f.read()
                    h.write(img)
            n += 1

        driver.close()
        self.root.quit()

def main():
    root = Tk()
    root.title('crawling')
    root.geometry('250x90+400+300')
    App(root)
    root.mainloop()

if __name__ == '__main__':

    main()