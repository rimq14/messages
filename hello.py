#!/usr/bin/python3
#coding=utf-8
import Iciba

if __name__ == '__main__':
    # 微信配置
    wechat_config = {
        'appid': 'wx28a17aa465aad04b', #(No.1)此处填写公众号的appid
        'appsecret': 'c5fd65d3cbad7ddf6377100269ac240c', #(No.2)此处填写公众号的appsecret
        'template_id': 'iL0Lz-AxuWNtlIf6eUuDwfRFWvm7lQb2-CMwTjnhe8s' #(No.3)此处填写公众号的模板消息ID
    }
    
    # 用户列表
    openids = [
        'ooAhR6YbwCjP3H7duOV1fka0099Q', #(No.4)此处填写你的微信号（微信公众平台上的微信号）
        #'xxxxx', #如果有多个用户也可以
        #'xxxxx',
    ]

    # 执行
    icb = Iciba.iciba(wechat_config)

    '''
    run()方法可以传入openids列表，也可不传参数
    不传参数则对微信公众号的所有用户进行群发
    '''
    icb.run()
