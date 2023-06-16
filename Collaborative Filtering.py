import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import re
import time
import os
from sklearn.metrics.pairwise import cosine_similarity

options = webdriver.ChromeOptions()
options.add_argument('--headless')        # Head-less 설정
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

def make_rating_csv(read_obj):
  from time import sleep

  reviews = []
  #read_obj='면바지'
  read_file = pd.read_csv(f'./{read_obj}무신사2.csv')

  for _ in range(10):#len(read_file)
    name = read_file.loc[ _, '상품명' ]
    address = read_file.loc[ _, '링크' ]
    count = int(read_file.loc[ _, '리뷰 수' ].replace(",", ""))
    price = int(read_file.loc[ _, '가격' ].replace(",", "").replace("원", ""))

    driver.get(address)

    pagnition = driver.find_element(by=By.XPATH,value='//*[@id="estimate_style"]')#네트워크가 불안정할 때 크롤링에 필요한 time.sleep을 충분히 주지 않을 경우 에러발생
    pagnition = int(re.sub(r'[^0-9]', '', pagnition.text))
    time.sleep(1)#타임 슬립을 늘리면 안정성이 증가하나 실행시간이 오래걸림

    k=1
    for i in range(int(pagnition/10)):

      if i>10:#리뷰 최대 10 * 10개만
        break

      if i>0:
        if i%5==1:
          k=1
        else:
          k+=1
        try:
          driver.find_element(by=By.XPATH,value=f'//*[@id="reviewListFragment"]/div[last()]/div[2]/div/a[{k+3}]').send_keys('\n')
        except:
          print(f'error: {name}')
          break
        time.sleep(1)

      paglist = driver.find_element(by=By.XPATH,value='//*[@id="reviewListFragment"]')
      time.sleep(1)

      for j in range(10):

        reviewer = paglist.find_element(by=By.XPATH,value=f'//*[@id="reviewListFragment"]/div[{j+1}]/div[1]/div/div[1]/p')
        time.sleep(0.1)
        reviewer = reviewer.text[5:]
        stars = paglist.find_element(by=By.XPATH,value=f'//*[@id="reviewListFragment"]/div[{j+1}]/div[3]/span/span/span')
        time.sleep(0.1)
        stars = int(re.sub(r'[^0-9]', '', stars.get_dom_attribute('style')))/20

        reviews.append([name, stars, reviewer, address, count, price])

  df = pd.DataFrame(columns=['name', 'star', 'reviewer', 'address', 'count', 'price'], data=reviews)
  df.to_csv(f'{read_obj}rating.csv')

  return df

def get_item_based_collabor(title):
  return item_based_collabor[title].sort_values(ascending=False)[:3]  # 추천되는 항목의 수 조절

def predict_rating(ratings_arr, item_sim_arr):
    sum_sr = ratings_arr @ item_sim_arr
    sum_s_abs = np.array([np.abs(item_sim_arr).sum(axis=1)])
    ratings_pred = sum_sr / sum_s_abs
    return ratings_pred

def get_ratings_pred_matrix(name):
  return ratings_pred_matrix.loc[name].sort_values(ascending=False)[:3]  # 추천되는 항목의 수 조절

try:
  keyword=pd.read_csv('./keyword.csv')
except:
  keyword=['가디건','면바지','긴팔']
try:
  user_name=pd.read_csv(f'./사용자.csv')
except:
  user_name='익명'
output_df = pd.DataFrame()

for _ in keyword:
  try:
    df = pd.read_csv(f'./무신사rating/{_}rating.csv')  # 미리 사전 크롤링된 데이터베이스를 사용할 경우 실행시간이 빠름
  except:
    print("데이터베이스 제작중")
    df = make_rating_csv(_)  # 항목당 약 1분의 시간이 소요(20개 크롤링 시 20분) -> 크롤링 에러로 멈추면 다시 실행해야함

  user_rating = df.pivot_table('star', index='name', columns='reviewer')
  user_rating.fillna(0, inplace=True)

  item_based_collabor = pd.DataFrame(data=cosine_similarity(user_rating), index=user_rating.index,
                                     columns=user_rating.index)
  shortdf = df.drop_duplicates(['name'])

  try:  # 평가 기록이 있을 경우 사용자 기반 추천
    ratings_pred = predict_rating(user_rating.T.values, item_based_collabor.values)
    ratings_pred_matrix = pd.DataFrame(data=ratings_pred, index=user_rating.columns, columns=user_rating.index)
    set_list = get_ratings_pred_matrix(user_name)
  except:  # 없을경우 리뷰 많은 것과 관련된 물품 추천
    selection = df.drop_duplicates(['name'])['count'].sort_values(ascending=False)
    set_list = get_item_based_collabor(shortdf.loc[selection.index[0], 'name'])

  empty_df = pd.DataFrame()

  for i in set_list.index.to_list():  # 리뷰 많은 것과 관련된 물품 추천
    idx = shortdf.index[shortdf['name'] == i]
    empty_df = pd.concat([empty_df, shortdf.loc[idx, ['name', 'address']]])
  empty_df['categori'] = _

  output_df = pd.concat([output_df, empty_df])

df.to_csv('output_df.csv')
print(output_df)