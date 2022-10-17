import requests


headers = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"
}

url = "http://liuyan.people.com.cn/threads/content"
params = {
    "tid": "16257410"
}
response = requests.get(url, headers=headers, params=params, verify=False)

print(response.content.decode('utf-8'))
print(response)