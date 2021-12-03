from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import shutil

baseUrl = 'https://www.instagram.com/'
plusUrl = input('검색할 아이디를 입력하세요 : ')
url = baseUrl + plusUrl

# print(url)
driver = webdriver.Chrome()
driver.get(url)

time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

imgList = []

for i in range(0,5):
    insta = soup.select('.v1Nh3.kIKUG._bz0w')

    for i in insta:
        imgUrl = i.select_one('.KL4Bh').img['src']
        imgList.append(imgUrl)
        # imgList = list(set(imgList))
        html = driver.page_source
        soup = BeautifulSoup(html, features='lxml')
        insta = soup.select('.v1Nh3.kIKUG._bz0w')

    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)

n=1
for i in range(0,50):

    image_url = imgList[n]
    resp = requests.get(image_url, stream=True)
    local_file = open('./insta/' + plusUrl + '_'+ str(n).zfill(3) + '.jpg', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    n += 1
    del resp
driver.close()