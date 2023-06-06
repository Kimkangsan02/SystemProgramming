# 필요한 모듈 import
import sys
import requests
from bs4 import BeautifulSoup

# 저장할 txt file 생성
f = open("weather.txt", "w")

# 네이버 날씨 url 가져오기
html = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%ED%98%84%ED%92%8D%EC%9D%8D+%EB%82%A0%EC%94%A8')
soup = BeautifulSoup(html.text, 'html.parser')

# 오늘 날씨 정보 가져오기
weekly_weather_data = soup.find('div', {'class' : 'list_box _weekly_weather'})
today_data = weekly_weather_data.find('li', {'class':'week_item today'})

# 오늘 날씨 최저, 최고 기온
today_temperature = today_data.find('div', {'class':'cell_temperature'})
b = today_temperature.find('span', {'class':'temperature_inner'})
lowest_temperature = b.find('span', {'class': 'lowest'}).text.strip()[4:6]
print(lowest_temperature, file=f)
highest_temperature = b.find('span', {'class': 'highest'}).text.strip()[4:6]
print(highest_temperature, file=f)

# 현재 날씨 
weather_info = soup.find('div', {'class':'weather_info'})
weatherStatus = weather_info.find('span', {'class':'weather before_slash'}).text

# 강수 확률
ra = today_data.find('div', {'class':'cell_weather'})
r = list(ra.find_all('span', {'class':'weather_inner'}))
morn_rainfall = int(r[0].find('span', {'class':'rainfall'}).text.replace('%', ''))
after_rainfall = int(r[1].find('span', {'class':'rainfall'}).text.replace('%', ''))

c = str(0)
if weatherStatus == "맑음":
    c = str(0)
elif weatherStatus == "흐림" or "구름많음":
    c = str(1)
elif weatherStatus == "비":
    c = str(2)
elif weatherStatus == "눈":
    c = str(3)
elif morn_rainfall >= 50 or after_rainfall >= 50:
    c = str(2)
print(c, file=f)
    