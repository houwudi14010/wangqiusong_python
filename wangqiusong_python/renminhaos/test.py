import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
}
cookies = {
    "simulation_id": "pc6350e6bbd085b49",
}
url = "https://rmh.pdnews.cn/Pc/ArticleApi/rightList"
params = {
    "type": "list",
    "label_id": "20"
}
response = requests.get(url, cookies=cookies, params=params)

print(response.text)
print(response)