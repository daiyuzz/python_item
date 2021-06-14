import time
import hashlib

import requests

url = "http://drug.dev.jyclinical.com/medicine-knowledge/tcm/admin/category/list?parentId=1200"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "appId": "JYAPPID016",
    "Connection": "keep-alive",
    "Cookie": "JSESSIONID=AE14BAF6E6EA08BF9B0ABC7DAE89140E",
    "Host": "drug.dev.jyclinical.com",
    "Referer": "http://drug.dev.jyclinical.com/tcm/category-manage",
    "a": {},
    "s": {},
    "sign": {},
    "t": {},
    "tid": "8062a64047f0eed43222dd4ea26be29c",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
}

t = str(round(time.time() * 1000))
ak = "SA0E496-8240-950F-EF8A-0EB28E4508BE"
uas = "S0792DF-8B97-A052-8A2D-F9995EFB26E1"
ua = headers['User-Agent']
a = ak + t[11:12]
s = uas + t[9:10]
sign = hashlib.md5(
    ((hashlib.md5((a + s).encode(encoding="UTF-8")).hexdigest() + t + ua).encode(encoding="UTF-8"))).hexdigest()

result_a = hashlib.md5(a.encode(encoding="UTF-8")).hexdigest()
result_s = hashlib.md5(s.encode(encoding="UTF-8")).hexdigest()



headers["a"] = result_a
headers["s"] = result_s
headers["sign"] = sign
headers["t"] = t

def get_html(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


if __name__ == '__main__':
    response = get_html(url)
    print(response)
