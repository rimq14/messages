#!/usr/bin/python3
#coding=utf-8
import sys
import json
import requests
from datetime import date, datetime
import math
import os
import random


class iciba:
    # 初始化
    def __init__(self, wechat_config):
        self.appid = wechat_config['appid'].strip()
        self.appsecret = wechat_config['appsecret'].strip()
        self.template_id = wechat_config['template_id'].strip()
        
        self.birthday = wechat_config['birthday'].strip()
        self.anniversary = wechat_config['anniversary'].strip()
        
        self.access_token = ''

    # 错误代码
    def get_error_info(self, errcode):
        return {
            40013: '不合法的 AppID ，请开发者检查 AppID 的正确性，避免异常字符，注意大小写',
            40125: '无效的appsecret',
            41001: '缺少 access_token 参数',
            40003: '不合法的 OpenID ，请开发者确认 OpenID （该用户）是否已关注公众号，或是否是其他公众号的 OpenID',
            40037: '无效的模板ID',
        }.get(errcode,'unknown error')
    

    # 打印日志
    def print_log(self, data, openid=''):
        errcode = data['errcode']
        errmsg = data['errmsg']
        if errcode == 0:
            print(' [INFO] send to %s is success' % openid)
        else:
            print(' [ERROR] (%s) %s - %s' % (errcode, errmsg, self.get_error_info(errcode)))
            if openid != '':
                print(' [ERROR] send to %s is error' % openid)
            sys.exit(1)

    # 获取access_token
    def get_access_token(self, appid, appsecret):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, appsecret)
        r = requests.get(url)
        data = json.loads(r.text)
        if 'errcode' in data:
            self.print_log(data)
        else:
            self.access_token = data['access_token']

    # 获取用户列表
    def get_user_list(self):
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=' % self.access_token
        r = requests.get(url)
        data = json.loads(r.text)
        if 'errcode' in data:
            self.print_log(data)
        else:
            openids = data['data']['openid']
            return openids
       
    
#     # 纪念日计算     
#     def get_count(self, anniversary):
#       delta = date - datetime.strptime(anniversary, "%Y-%m-%d")
#       return delta.days
    
#     # 生日计算
#     def get_birthday(self, birthday):
#       next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#       if next < datetime.now():
#         next = next.replace(year=next.year + 1)
#       return (next - today).days

#     # 颜色随机
#     def get_random_color(self):
#       return "#%06x" % random.randint(0, 0xFFFFFF)

    
    # 发送消息
    def send_msg(self, openid, template_id, iciba_everyday):
        url = "https://api.map.baidu.com/weather/v1/?district_id=360102&data_type=all&ak=t7SXk9QH7NnT6Agqi1NKyrHnzqMTknjZ"
        res = requests.get(url).json()
        wea = res['result']['forecasts'][0]['text_day']
        high = res['result']['forecasts'][0]['high']
        low = res['result']['forecasts'][0]['low']
        winClass = res['result']['forecasts'][0]['wc_day']
        winDir = res['result']['forecasts'][0]['wd_day']
        date = res['result']['forecasts'][0]['date']
        msg = {
            'touser': openid,
            'template_id': template_id,
            'url': iciba_everyday['fenxiang_img'],
            'data': {
                "date": {"value":date},
                "weather":{"value":wea},
                "high":{"value":high},
                "low":{'value':low},
#                 "annivarsary":{"value":get_count(),'color':get_random_color()},
#                 "birthday":{"value":get_birthday()},
                'content': {
                    'value': iciba_everyday['content'],
                    'color': '#0000CD'
                    },
                'note': {
                    'value': iciba_everyday['note'],
                },
                'translation': {
                    'value': iciba_everyday['translation'],
                }
            }
        }
        json_data = json.dumps(msg)
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % self.access_token
        r = requests.post(url, json_data)
        return json.loads(r.text)

    # 获取爱词霸每日一句
    def get_iciba_everyday(self):
        url = 'http://open.iciba.com/dsapi/'
        r = requests.get(url)
        return json.loads(r.text)

    # 为设置的用户列表发送消息
    def send_everyday_words(self, openids):
        everyday_words = self.get_iciba_everyday()
        for openid in openids:
            openid = openid.strip()
            result = self.send_msg(openid, self.template_id, everyday_words)
            self.print_log(result, openid)

    # 执行
    def run(self, openids=[]):
        if openids == []:
            # 如果openids为空，则遍历用户列表
            openids = self.get_user_list()
        # 根据openids对用户进行群发
        self.send_everyday_words(openids)
