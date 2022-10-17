import requests


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Referer": "http://liuyan.people.com.cn/threads/list?checkStatus=0&fid=741&formName=%E6%9C%9D%E9%98%B3%E5%8C%BA%E5%A7%94%E4%B9%A6%E8%AE%B0%E6%96%87%E7%8C%AE&position=0&province=4&saveLocation=4&pForumNames=%E5%8C%97%E4%BA%AC%E5%B8%82&pForumNames=%E6%9C%9D%E9%98%B3%E5%8C%BA",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"
}
cookies = {
    "wdcid": "4b7214ea9b5227c6",
    "sso_c": "0",
    "sfr": "1",
    "__jsluid_h": "40a0e62458ebfb88538253734377a0dc",
    "4de1d0bdb25d4625be2481a1b9e1350f": "WyIyMDQ3MDc5Nzk3Il0",
    "wdlast": "1665999637",
    "wdses": "52d158f4dff7e138",
    "language": "zh-CN"
}
url = "http://liuyan.people.com.cn/threads/content"
params = {
    "tid": "16257410"
}
response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False)

print(response.text)
print(response)