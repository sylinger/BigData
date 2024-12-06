import requests
import time
import os
import json
import random
from retry import retry
from fake_useragent import UserAgent

@retry(tries=5, delay=5)
def getWeek_json(url, json_path):
    print('正在爬取数据，url为：{}'.format(url))
    # headers信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.5.9101 SLBChan/25 SLBVPV/64-bit",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com/",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": "DedeUserID=253765121; DedeUserID__ckMd5=8b204e33e8749e9f; rpdid=|(J|YkuJ~mYl0J'uY)l))|k|); LIVE_BUVID=AUTO2216863966706138; buvid_fp_plain=undefined; enable_web_push=DISABLE; CURRENT_FNVAL=4048; home_feed_column=5; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; PVID=1; buvid3=728C5EC6-5E1A-0716-F5E1-E908372396AC82000infoc; b_nut=1717491682; _uuid=96EC5CDB-7311-D6CA-36AC-745478634EAD83478infoc; header_theme_version=CLOSE; buvid4=310C4DC4-04D6-7F17-9640-8CB5C34DB30F75093-024110307-nNMmHe4Tv0n7wnXnmwBcgA%3D%3D; fingerprint=c9717eea2899312e53a904b9fa78e511; buvid_fp=c9717eea2899312e53a904b9fa78e511; bp_t_offset_253765121=1003208342056730624; match_float_version=ENABLE; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzMzODYyMTgsImlhdCI6MTczMzEyNjk1OCwicGx0IjotMX0.2Ej8ERf0r5lOowDgICaAwPAIjZoTQvpBkh21impgr9w; bili_ticket_expires=1733386158; CURRENT_QUALITY=16; browser_resolution=1488-720; SESSDATA=e1daf441%2C1748836071%2C3dfa9%2Ac1CjBaHAY7ANkSx6gh-Lgfo9j_awxqTFnyx82H9BCSEVl6pU6XCa_XeRDmt2PIId1EqooSVnRzanZaUXJ0U2xWRjdjaExBTVN5ZnNELXRGdWlIOEhkeTF5MnVUcXU5Q1d3QjJJWThGSnc2dmdwamxoUjR1em9vX09ORlR3bW43N2h3QXlVWmRvZzVnIIEC; bili_jct=53c18dc5192ddb5318c6180ef74c9748; sid=dlppcwpv; b_lsid=99543F410_19390480EB7",
    }
    try:
        # 获取响应，转为json格式并保存
        response = requests.get(url=url, headers=headers, timeout=10)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get("code") != 0:
            print(f"请求失败，code: {response_data.get('code')}, message: {response_data.get('message')}")
            return
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False)
        print('数据爬取成功，保存到：{}'.format(json_path))
    except requests.exceptions.RequestException as e:
        print('请求失败：{}'.format(e))
        raise
    # 在请求结束后，增加随机的休眠时间，确保不会被反爬
    sleep_time = random.uniform(3, 7)  # 3 到 7 秒之间随机
    time.sleep(sleep_time)

if __name__ == '__main__':
    # 官方api
    url = 'https://api.bilibili.com/x/web-interface/popular/series/one?number={}'
    # 爬虫数据存储路径
    data_folder = './data'
    os.makedirs(data_folder, exist_ok=True)
    # 开始爬虫
    for i in range(1, 298):
        print('开始爬取第{}期数据'.format(str(i)))
        URL = url.format(str(i))
        # 每周数据存储路径
        json_fpath = os.path.join(data_folder, 'week_{}.json'.format(str(i)))
        getWeek_json(URL, json_fpath)
