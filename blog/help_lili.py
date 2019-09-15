# coding: utf-8
import requests
from random import choice
import argparse
import re
import json


# 模拟浏览器头
headers = {
    'host': "api.zhihu.com",
    'accept': "*/*",
    'x-app-za': "OS=iOS&Release=10.3.3&Model=iPhone8,2&VersionName=4.1.0&VersionCode=683&Width=1242&Height=2208&DeviceType=Phone&Brand=Apple&OperatorType=46001",
    'x-udid': "AHCAH2SzkApLBWvOUMZ7s9hG-Zh-_NhtVCM=",
    'x-app-versioncode': "683",
    'accept-language': "zh-Hans-CN;q=1, en-CN;q=0.9",
    'accept-encoding': "gzip, deflate",
    'x-api-version': "3.0.64",
    'authorization': "Bearer gt2.0AAAAAAX1feoKkLNkH4BwAAAAAAtNVQJgAgBgPzk1-59vTbuXI60W0XlSl-wNBg==",
    'x-network-type': "WiFi",
    'user-agent': "osee2unifiedRelease/4.1.0 (iPhone; iOS 10.3.3; Scale/3.00)",
    'x-app-build': "release",
    'x-app-version': "4.1.0",
    'x-suger': "SURGVj0wNDA5NjgxMS01NTI5LTRDQUQtQUEzNi1FRkI2M0VDQThDOEE7SURGQT01MDM2NDdEMy01QTlDLTRFMjItODA5NS1FRkUyM0Y5Mzg5QzM=",
    'cookie': "aliyungf_tc=AQAAAH4w9XP89AUAWgqDdYQRcynwI6xp; q_c1=97515fa2381f48a7b6ef8d46de8bc7be|1505561812000|1505561812000; z_c0=gt2.0AAAAAAX1feoKkLNkH4BwAAAAAAtNVQJgAgBgPzk1-59vTbuXI60W0XlSl-wNBg==; _xsrf=a31505e0-0f69-440b-b357-30fffc9838bd; cap_id=\"MzQ2NGE0NThiMmVjNDU3MmE5MzVhYzE0OGYyMTYzYTI=|1505561809|0c36cb283969855952e9e895b77211fd292c0df7\"; l_cap_id=\"ODE3YzMwODM5ZTE0NDdjN2IxY2UyZDdiYjQ1MGYzNDg=|1505561809|6f707b1bf6c0a0ebb6391d0c421ac06e49ceca3b\"; r_cap_id=\"ODZlYTZmNGZhYzU3NDgwOGE4YzUyOWI5OTBmMzA3NjQ=|1505561809|05c714d01ee35a0a6c96b0c330d4f10434fec8bc\"",
    'cache-control': "no-cache",
}


def get(url):
    z = requests.get(url, headers=headers, verify=False)
    return z.json()


def run(url):
    jsdata = get(url)
    info = []
    girl_info=[]
    while True:
        for i in jsdata['data']:
            if i['action_type'] =='repin' and i['member']['gender']==0:
                girl_info.append({
                    'url': i['member']['url'],
                    'name': i['member']['name'],
                }
                )
            if i['action_type'] == 'repin':
                info.append({
                    'url': i['member']['url'],
                    'name': i['member']['name'],
                })

        if not jsdata['paging']['is_end']:
            jsdata = get(jsdata['paging']['next'])
        else:
            return info,girl_info
            break


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()

    parser = argparse.ArgumentParser(description='知乎想法抽奖')
    parser.add_argument('--url', type=str, default=None)
    args = parser.parse_args()
    baseurl = 'https://api.zhihu.com/pins/{}/actions?limit=20&offset=0'
    # url = args.url
    # pin = url.split('/')[-1]
    # # 修复 当网址分享到qq的时候 有后缀的问题，如https://www.zhihu.com/pin/900498393586094080?utm_source=qq
    # pin_id = re.search('\d+',pin)[0]
    url = baseurl.format('1098266343127846912')
    print('璃狸抽奖专属页面是'+url)
    info = run(url)[0]
    girl_info = run(url)[1]
    print('拉取女性用户数据为' + str(girl_info))
    print('拉取所有用户数据为'+str(info))
    print('********本次抽奖获得者为********')
    aldnoah = choice(info)
    print('静月堂汉服,' + '知乎id为：' + aldnoah.get('name')+',个人主页为https://www.zhihu.com'+aldnoah.get('url'))
    print('让我们恭喜这位小姐姐！')
    print('三只松鼠空投箱：')
    num=1
    while num<=3:
        aldnoah = choice(info)
        print('   编号'+str(num)+','+'知乎id为：'+aldnoah.get('name')+',个人主页为https://www.zhihu.com'+aldnoah.get('url'))
        num+=1
    print('可乐樱花版一人一瓶:')
    num = 1
    while num <= 3:
        aldnoah=choice(info)
        print('   编号' + str(num) + ',' + '知乎id为：' + aldnoah.get('name')+'，个人主页为https://www.zhihu.com'+aldnoah.get('url'))
        num += 1
    print('旺仔牛奶罐装箱:')
    aldnoah = choice(info)
    print('   编号1'  + ',' + '知乎id为：' + aldnoah.get('name')+'，个人主页为https://www.zhihu.com'+aldnoah.get('url'))
    aldnoah = choice(info)
    print('摘抄狸手叠星星一罐：')
    print('   编号1' + ',' + '知乎id为：' + aldnoah.get('name')+'，个人主页为https://www.zhihu.com'+aldnoah.get('url'))
    print('********本次抽奖感谢柯基小王子提供的技术支持********')