from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

city_id = os.environ["CITY_ID"]
ak = os.environ["AK"]

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://api.map.baidu.com/weather/v1/?district_id=%s&data_type=all&ak=%s" % (city_id, ak)
  res = requests.get(url).json()
  weather = res['result']['forecasts'][0]['text_day']
  high = res['result']['forecasts'][0]['high']
  low = res['result']['forecasts'][0]['low']
  winClass = res['result']['forecasts'][0]['wc_day']
  winDir = res['result']['forecasts'][0]['wd_day']
  date = res['result']['forecasts'][0]['date']
  return weather,high,low,winClass, winDir, date

def get_count():
  delta = datetime.now() - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, high,low,winclass,windir,date = get_weather()
data = {
  "date":{"value":date},
  "weather":{"value":wea},
  "high":{"value":high},
  "windClass":{'value':winclass},
  "windDir":{"vaule":windir},
  "anniversary":{"value":get_count()},
  "birthday":{"value":get_birthday()},
  "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
