import json
import execjs
import requests
import os

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://www.xiaohongshu.com",
    "pragma": "no-cache",
    "referer": "https://www.xiaohongshu.com/",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}


def extract_cookie_value(cookie, key):
    # 将 cookie 字符串转换为字典
    cookies_dict = dict(item.split('=', 1) for item in cookie.split(';'))
    # 返回指定 key 的值
    return cookies_dict.get(key.strip())


def sentPostRequest(host, api, data, cookie):
    if cookie == "":
        print("need cookie")
        return

    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, "xhs.js")
    xs_xt = execjs.compile(open(file_path, 'r', encoding='utf-8').read()).call('getXs', api, data,
                                                                               extract_cookie_value(cookie, 'a1'))
    headers['cookie'] = cookie
    headers['X-s'] = xs_xt['X-s']
    headers['X-t'] = str(xs_xt['X-t'])

    response = requests.post(url=host + api,
                             data=json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
                             headers=headers)
    return response.json()


if __name__ == '__main__':
    cookie = "a1=;web_session="  # put your cookie here
    api = '/api/sns/web/v1/search/notes'
    host = 'https://edith.xiaohongshu.com'
    page = 1
    data = {
        "keyword": '洪崖洞',
        "page": page,
        "page_size": 20,
        "search_id": '2e0gronyjdkna5fll09bj',
        "sort": 'general',
        "note_type": 0,
        "ext_flags": [],
        "image_formats": [
            'jpg',
            'webp',
            'avif'
        ]
    }
    try:
        response = sentPostRequest(host, api, data, cookie)
        data = response['data']
        print(len(data))
        has_more = data['has_more']
        for i in data['items']:
            print(i)
    except Exception:
        pass
