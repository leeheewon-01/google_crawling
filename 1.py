from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request
from multiprocessing import Pool
import pandas as pd

key=pd.read_csv('./keyword.txt',encoding='cp949',names=['keyword'])
keyword=[]
[keyword.append(key['keyword'][x]) for x in range(len(key))]

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def image_download(keyword):
    createFolder('./' + keyword + '_low resolution')

    chromedriver = 'C://chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    driver.implicitly_wait(3)

    print(keyword, '검색')
    driver.get('https://www.google.co.kr/imghp?hl=ko')
    time.sleep(1)
    Keyword = driver.find_element_by_xpath("""/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input""")
    Keyword.send_keys(keyword)

    driver.find_element_by_xpath('//*[@id="sbtc"]/button').click()

    print(keyword + ' 스크롤 중 .............')
    elem = driver.find_element_by_tag_name("body")
    for i in range(60):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)

    try:
        driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[4]/div[2]/input').click()
        for i in range(60):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
    except:
        pass

    links = []
    images = driver.find_elements_by_css_selector("img.rg_i.Q4LuWd")
    for image in images:
        if image.get_attribute('src') != None:
            links.append(image.get_attribute('src'))

    print(keyword + ' 찾은 이미지 개수:', len(links))
    time.sleep(2)

    for k, i in enumerate(links):
        url = i
        start = time.time()
        urllib.request.urlretrieve(url, "./" + keyword + "_low resolution/" + keyword + "_" + str(k) + ".jpg")
        print(str(k + 1) + '/' + str(len(links)) + ' ' + keyword + ' 다운로드 중....... Download time : ' + str(
            time.time() - start)[:5] + ' 초')
    print(keyword + ' ---다운로드 완료---')

    driver.close()

if __name__=='__main__':
    pool = Pool(processes=4)
    pool.map(image_download, keyword)