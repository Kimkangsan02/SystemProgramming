#!/usr/bin/env python
# coding: utf-8

# In[8]:


import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests

words = ['재킷', '맨투맨', '민소매', '반팔', '후드티', '겨울니트', '긴팔', '긴팔셔츠', '미니스커트', '숏팬츠', '슬랙스', '청바지', '롱스커트', '면바지']
for word in words:
    chrome_options = Options()
    driver = webdriver.Chrome('./chromedriver')

    URL = 'https://www.musinsa.com/app/'
    driver.get(URL)

    engine = driver.find_element('xpath', '//*[@id="search_query"]')
    engine.click()  # 검색창 선택
    engine.send_keys(word)  # 검색어 입력
    engine.send_keys(Keys.ENTER)  # 검색 수행
    driver.find_element('xpath', '/html/body/div[2]/div[3]/section/nav/a[2]').click()

    while True:
        bh = driver.execute_script("return document.body.scrollHeight")  # 초기 로딩된 페이지 높이, before height
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # scrolling
        time.sleep(2)
        ah = driver.execute_script("return document.body.scrollHeight")  # 스크롤 후 높이, after height
        if ah == bh:
            break
        bh = ah

    infos = driver.find_elements(By.CSS_SELECTOR, ".article_info")

    names = []  # 상품명
    prices = []  # 가격
    review_cnts = []  # 리뷰 수
    links = []
    imgs = []

    # 각 상품의 상품명, 가격, 링크를 추출합니다.
    for info in infos:
        try:
            name = info.find_element(By.CSS_SELECTOR, ".list_info").text
            names.append(name)
        except:
            names.append(None)  # 값이 없는 경우 None 추가

        try:
            price = info.find_element(By.CSS_SELECTOR, ".price").text.split()[0]
            prices.append(price)
        except:
            prices.append(None)  # 값이 없는 경우 None 추가

        try:
            review_cnt = info.find_element(By.CSS_SELECTOR, ".count").text
            review_cnts.append(review_cnt)
        except:
            review_cnts.append(None)  # 값이 없는 경우 None 추가

        try:
            link = info.find_element(By.CSS_SELECTOR, "p.list_info a").get_attribute("href")
            links.append(link)
        except:
            links.append(None)  # 값이 없는 경우 None 추가
            
    # 결과 출력
    df = pd.DataFrame({
        '상품명': names,
        '가격': prices,
        '링크': links,
        '리뷰 수': review_cnts,
    })

    
    for link in links:
        try:
            driver.get(link)
            img = driver.find_element(By.XPATH, '//*[@id="bigimg"]').get_attribute('src')
            print(img)
            imgs.append(img)
        except:
            imgs.append(None)
    df['이미지']=imgs

    df=df.dropna(axis=0)
    
    print(df)
    
    df.to_csv('./{}무신사2.csv'.format(word), sep = ",", encoding= "utf-8-sig")
driver.close()


# In[ ]:




