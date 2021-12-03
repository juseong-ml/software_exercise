from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# https://www.instagram.com/jusep.v/


def main():
    baseUrl = 'https://www.instagram.com/'
    plusUrl = input('검색할 아이디를 입력하세요 : ')
    url = baseUrl + plusUrl

    # print(url)
    driver = webdriver.Chrome()
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
            with open('./insta/' + plusUrl + '_' + str(n).zfill(3) + '.jpg', 'wb') as h:
                img = f.read()
                h.write(img)
        n += 1
        # print(imgUrl)
        # print()



    driver.close()


if __name__ == '__main__':
    main()