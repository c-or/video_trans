#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import random
import hashlib

import execjs
import requests


translate_url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'


def get_translation_result(parameters):
    headers = {
        'User-Agent': user_agent,
        'Host': 'fanyi.youdao.com',
        'Origin': 'https://fanyi.youdao.com',
        'Referer': 'https://fanyi.youdao.com/',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'Cookie': 'OUTFOX_SEARCH_USER_ID="-1848382357@10.169.0.84"; ___rl__test__cookies=1625907853887; OUTFOX_SEARCH_USER_ID_NCOO=132978720.55854891'
    }
    response = requests.post(url=translate_url, headers=headers, data=parameters)
    try:
        result = response.json()['translateResult'][0][0]['tgt']
    except:
        print(response.text)
        result = response.json()['translateResult'][0][0]['tgt']
    return result


def get_parameters_by_python(query, translate_from, translate_to):
    # 以毫秒为单位的 13 位时间戳
    lts = str(int(time.time() * 1000))
    # 13 位时间戳+随机数字，生成 salt 值                                
    salt = lts + str(random.randint(0, 9))                   
    # 拼接字符串组成 sign         
    sign = "fanyideskweb" + query + salt + "Y2FYu%TNSbMCxc3t2u^XT"    
    # 将 sign 进行 MD5 加密，生成最终 sign 值
    sign = hashlib.md5(sign.encode()).hexdigest()   
    # 对 UA 进行 MD5 加密，生成 bv 值                  
    bv = hashlib.md5(user_agent.encode()).hexdigest()                 
    parameters = {
        'i': query,
        'from': translate_from,
        'to': translate_to,
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'lts': lts,
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    return parameters


def get_parameters_by_javascript(query, translate_from, translate_to):
    with open('youdao_encrypt.js', 'r', encoding='utf-8') as f:
        youdao_js = f.read()
    params = execjs.compile(youdao_js).call('get_params', query, user_agent)    # 通过 JavaScript 代码获取各个参数
    bv = hashlib.md5(user_agent.encode()).hexdigest()                           # 对 UA 进行 MD5 加密，生成 bv 值
    parameters = {
        'i': query,
        'from': translate_from,
        'to': translate_to,
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': params['salt'],
        'sign': params['sign'],
        'lts': params['lts'],
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    return parameters


def youdao(query,flag=0):
    # 第一次翻译成英语
    if flag == 0:
        translate_from = 'zh-CHS'
        translate_to = 'en'
    elif flag == 1:
    # 第二次翻译回汉语
        translate_from = 'en'
        translate_to = 'zh-CHS'
    # elif flag == 2:
    # # 第三次再翻译回英语
    #     translate_from = 'fr'
    #     translate_to = 'zh-CHS'
    # 通过 Python 获取加密参数或者通过 JavaScript 获取参数，二选一
    param = get_parameters_by_python(query, translate_from, translate_to)
    # param = get_parameters_by_javascript(query, translate_from, translate_to)
    result = get_translation_result(param)
    print('翻译的结果为：', result)
    return result
    
def youdao_process(query):
    # query1 = youdao(query)
    # query2 = youdao(query1,1)
    # result = youdao(query2)
    result = youdao(query)
    return result

if __name__ == '__main__':
    # query = input('请输入要翻译的文字：')
    query = '今夜我们就出发'
    youdao_process(query)



# sudo curl 
# -F "file=@/home/admini/vdnagen_script/sourcefar2/src/FIVR200K/5LFg3EsJQug.mp4.far" 
# -F "sourceFilePath=/home/admini/vdnagen_script/sourcefar2/src/FIVR200K/5LFg3EsJQug.mp4.far" 
# http://localhost:89/vg/accept/far -o ./far_test_log/$name.log

# url = 'http://localhost:89/vg/accept/far'
# headers = {
#     'file':'@/home/admini/vdnagen_script/sourcefar2/src/FIVR200K/5LFg3EsJQug.mp4.far',
#     'sourceFilePath':'/home/admini/vdnagen_script/sourcefar2/src/FIVR200K/5LFg3EsJQug.mp4.far',
# }
# res = requests.get(url,headers=headers)



#  -o ./far_test_log/$name.log



