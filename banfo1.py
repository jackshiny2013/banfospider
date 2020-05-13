import requests
import time
import json
import csv
import random
from bs4 import BeautifulSoup
import re
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

"""
本项目首发：
B站原创视频：https://www.bilibili.com/video/BV1wK4y1t74g
哔哩哔哩：海王互联网
"""


def request_data():
    article_url_list = []
    print('正在下载，请稍等！大约需要30分钟')
    for offset in range(0, 322, 10):
        # 记得把offset后面的值改成{}
        base_url = 'http://mp.weixin.qq.com/mp/profile_ext?offset={}&count=10'

    """ 替换成你们的cookie、header、param
    """
        cookies = {
            'devicetype': 'iPhoneiOS13.0',
            'lang': 'zh_CN',
            'pass_ticket': 'oeIwS6v4F0AvHg8ZAcl1WA2rQ9GvxZiXhuH/to2325wxlKt6Qqy35d4Pf5tXS0Np',
            'version': '17000c2d',
            'wap_sid2': 'CPTSivkBElx1c21xcGF5TUZBQnY4VEpDUnJDdHBDUlF4TUtnWWRYRmxMZXBVSW5icHZTWVRlMjZBRDlTaGdtY25GZVU4dUlIVTFTX2Q1cEh0Qm51MFJVUFJaQ0tHaVFFQUFBfjCQ4Nn1BTgNQJVO',
            'wxuin': '522365300',
            'pgv_pvid': '4259106169',
            'tvfe_boss_uuid': '53d0cecfd486f85f',
        }

        headers = {
            'Host': 'mp.weixin.qq.com',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/2.3.31(0x12031f10) MacWechat Chrome/39.0.2171.95 Safari/537.36 NetType/WIFI WindowsWechat MicroMessenger/2.3.31(0x12031f10) MacWechat Chrome/39.0.2171.95 Safari/537.36 NetType/WIFI WindowsWechat MicroMessenger/2.3.31(0x12031f10) MacWechat Chrome/39.0.2171.95 Safari/537.36 NetType/WIFI WindowsWechat MicroMessenger/2.3.31(0x12031f10) MacWechat Chrome/39.0.2171.95 Safari/537.36 NetType/WIFI WindowsWechat',
            'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI5MTE2NDI2OQ==&scene=124&uin=NTIyMzY1MzAw&key=d6528087ca056ee8785d397d2af42a9dac0b03bce46caea950a257cbae1bb254209cdb7eede52797c56665642baf81dc029e2ff438d9d0ac8bc42573b5f6e328e56c907f329b4a37d4bab122d07e47b8&devicetype=iMac+MacBookPro12%2C1+OSX+OSX+10.15.4+build(19E266)&version=12031f10&lang=zh_CN&nettype=WIFI&a8scene=0&fontScale=100&pass_ticket=oeIwS6v4F0AvHg8ZAcl1WA2rQ9GvxZiXhuH%2Fto2325wxlKt6Qqy35d4Pf5tXS0Np&winzoom=1.000000',
            'Accept-Language': 'zh-cn',
            'X-Requested-With': 'XMLHttpRequest',
        }

        params = (
            ('action', 'getmsg'),
            ('__biz', 'MzI5MTE2NDI2OQ=='),
            ('f', ['json', 'json']),
            ('is_ok', '1'),
            ('scene', '124'),
            ('uin', 'NTIyMzY1MzAw'),
            ('key',
             'd6528087ca056ee8785d397d2af42a9dac0b03bce46caea950a257cbae1bb254209cdb7eede52797c56665642baf81dc029e2ff438d9d0ac8bc42573b5f6e328e56c907f329b4a37d4bab122d07e47b8'),
            ('pass_ticket', 'oeIwS6v4F0AvHg8ZAcl1WA2rQ9GvxZiXhuH/to2325wxlKt6Qqy35d4Pf5tXS0Np'),
            ('wxtoken', ''),
            ('appmsg_token', '1060_6naq8Rkh3pG3NsMEjHFvg86LapDc5NoVlgiu1g~~'),
            ('x5', '0'),
        )


        # 代理ip，失效的话请自行更换，也可以直接去掉
        proxy = {'https': '114.239.144.61:808'}

        try:
            response = requests.get(
                base_url.format(offset),
                headers=headers,
                params=params,
                cookies=cookies,
                proxies=proxy)
            if 200 == response.status_code:
                all_datas = json.loads(response.text)
                if 0 == all_datas['ret'] and all_datas['msg_count'] > 0:
                    summy_datas = all_datas['general_msg_list']
                    datas = json.loads(summy_datas)['list']
                    for data in datas:
                        try:
                            article_url = data['app_msg_ext_info']['content_url']
                            article_url_list.append(article_url)
                            print(article_url+"添加了url")
                        except Exception as e:
                            continue
        except:
            time.sleep(2)
        time.sleep(int(format(random.randint(2, 5))))
    return article_url_list


def get_urls(url):
    try:
        html = requests.get(url, timeout=30).text
    except requests.exceptions.SSLError:
        html = requests.get(url, verify=False, timeout=30).text
    except TimeoutError:
        print('请求超时')
    except Exception:
        print('获取失败')
    src = re.compile(r'data-src="(.*?)"')
    urls = re.findall(src, html)
    if urls is not None:
        url_list = []
        for url in urls:
            url_list.append(url)
            print("png url:"+url)
        return url_list


def mkdir():
    isExists = os.path.exists(r'./banfo')
    if not isExists:
        print('创建目录')
        os.makedirs(r'./banfo')  # 创建目录
        os.chdir(r'./banfo')  # 切换到创建的文件夹
        return True
    else:
        print('目录已存在，即将保存！')
        return False


def download(filename, url):
    try:
        with open(filename, 'wb+') as f:
            try:
                f.write(requests.get(url, timeout=30).content)
                print('成功下载图片：', filename)
            except requests.exceptions.SSLError:
                f.write(requests.get(url, verify=False, timeout=30).content)
                print('成功下载图片：', filename)
    except FileNotFoundError:
        print('下载失败，非表情包，直接忽略：', filename)
    except TimeoutError:
        print('下载超时：', filename)
    except Exception:
        print('下载失败：', filename)



if __name__ == '__main__':
    for url in request_data():
        url_list = get_urls(url)
        mkdir()
        for pic_url in url_list:
            filename = r'./banfo/' + pic_url.split('/')[-2] + '.' + pic_url.split('=')[-1]  # 图片的路径
            print(filename, pic_url)
            download(filename, pic_url)



