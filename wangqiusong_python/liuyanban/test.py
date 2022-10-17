# # -*- coding: utf-8 -*-
# """
# Created on 2022-10-13 16:40:50
# ---------
# @summary:
# ---------
# @author: 王火龙
# """
# import click as click
# import feapder
# from feapder.db.mysqldb import MysqlDB
# import setting as cfg
# import hashlib
# import datetime
# import json
# import time
# import requests
# import re
#
# from liuyanban import yq_liuyanban_item
#
#
# class Liuyanban1(feapder.Spider):
#     db = MysqlDB()
#     headerss = {
#         "Accept": "application/json, text/plain, */*",
#         "Accept-Language": "zh-CN",
#         "Connection": "keep-alive",
#         "Content-Type": "application/json;charset=UTF-8",
#         "Origin": "http://liuyan.people.com.cn",
#         "Referer": "http://liuyan.people.com.cn/threads/content?tid=14592777",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
#         "token": ""
#     }
#     datass = {
#         "appCode": "PC42ce3bfa4980a9",
#         "token": "",
#         "signature": "18d497371f56c631390ca2f9a196b130",
#         "param": "{\"tid\":\"16152844\",\"fromTrash\":0}"
#
#     }
#
#     def start_requests(self):
#         # for fids in range(539, 4476):
#         for fids in range(539, 540):
#             data = {
#                 "fid": "4476",
#                 "lastItem": "0",
#                 "typeId": "2"
#             }
#             datas = dict(data)
#             datas['fid'] = str(fids)
#             url = "http://liuyan.people.com.cn/threads/queryThreadsList"
#             yield feapder.Request(url, timeout=30, data=datas, allow_redirects=False)
#
#     def signature(self, tids, type):
#         if type == 1:
#             self.datass['param'] = "{\"tid\":\"" + tids + "\",\"fromTrash\":0}"
#             pwds = "/v1/threads/content{\"tid\":\"" + tids + "\",\"fromTrash\":0}"
#         else:
#             self.datass['param'] = "{\"fid\":\"" + tids + "\",\"showUnAnswer\":1,\"typeId\":2,\"lastItem\":\"\",\"position\":\"0\",\"rows\":10,\"orderType\":2}"
#             pwds = "/v1/threads/list/df{\"tid\":\"" + tids + "\",\"fromTrash\":0}"
#         pwd = self.datass['appCode']
#         pwd = hashlib.md5(bytes(pwd, encoding='utf-8'))
#         pwds = pwds+ pwd.hexdigest()[0:16]
#         self.datass['signature'] = hashlib.md5(bytes(pwds, encoding='utf-8')).hexdigest()
#         return self.datass
#
#     def parse(self, request, response):
#         if response.status_code != 200:
#             raise Exception("非法页面")
#         tid = re.compile('"tid":(.*?),').findall(response.text)
#         for tids in tid:
#             time.sleep(1)
#             urls = "http://liuyan.people.com.cn/v1/threads/content"
#             type = 1
#             dataa = self.signature(tids, type)
#             dataa = json.dumps(self.datass)
#             res = requests.post(urls, headers=self.headerss, data=dataa, timeout=30, verify=False)
#             title = re.compile('"subject":"(.*?)",').findall(res.content.decode('utf-8'))
#             content = re.compile('"content":"([\s\S]*?)",').findall(res.content.decode('utf-8'))
#             pubtime = re.compile('"createDateline":([\s\S]*?),').findall(res.content.decode('utf-8'))
#             time_tuple_1 = time.localtime(int(pubtime[0]))
#             bj_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple_1)
#             downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             pubTimes = datetime.datetime.strptime(bj_time, "%Y-%m-%d %H:%M:%S")
#             downloadTimes = datetime.datetime.strptime(downloadTime, "%Y-%m-%d %H:%M:%S")
#             site = "领导留言板"
#             siteId = 1047953
#             articleStatue = 0
#             item = yq_liuyanban_item.YqLiuyanbanItem()  # 声明一个item
#             item.url = "https://liuyan.people.com.cn/threads/content?tid=" + tids  # 给item属性赋值
#             item.title = title[0]  # 给item属性赋值
#             item.pub_time = pubTimes  # 给item属性赋值
#             item.content = content[0]  # 给item属性赋值
#             item.download_time = downloadTimes  # 给item属性赋值
#             item.site = site  # 给item属性赋值
#             item.site_id = siteId  # 给item属性赋值
#             item.aid = tids  # 给item属性赋值
#             item.push_state = articleStatue  # 给item属性赋值
#             yield item
#
#     def download_midware(self, request):
#         """
#             下载中间件处理参数
#             :param request:
#             :return:
#             """
#         request.headers = headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
#             "Referer": "http://liuyan.people.com.cn/threads/list?fid=5050&position=1",
#         }
#         try:
#             ip = requests.get(f"http://192.168.1.26:16666/get/", timeout=3).json().get("proxy")
#             request.proxies = {"http": ip, "https": ip}
#         except:
#             pass
#         return request
#
#
# @click.command(name='mian')
# @click.option('--t', default=cfg.THREAD_NUM, help="num 线程数")
# @click.option('--p', default=1, help="是否开启代理")
# def mian(t, p, ):
#     cfg.ISPROXY = p
#     # for i in range(t):
#     spider = Liuyanban1(redis_key='test')
#     spider.start()
#
#
# if __name__ == "__main__":
#     mian()
