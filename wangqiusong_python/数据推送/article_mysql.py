# -*- coding: utf-8 -*-
"""
Created on 2022-10-25 10:03:15
---------
@summary:
---------
@author: 王火龙
"""
import traceback
import feapder
from feapder.db.mysqldb import MysqlDB
import json
import requests
import datetime
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, o)


class ArticleMysql(feapder.AirSpider):
    def start_requests(self):
        db = MysqlDB()
        arrList = db.find("select name from yq_shujukus ", 0, to_json=True, conver_col=True)
        for name in arrList:
            try:
                names = name['name']
                arr = db.find("select * from " + names + " where push_state = 0 limit 2000", 0, to_json=True,
                              conver_col=True)
                lists = []
                id = []
                for i in arr:
                    id.append(i['id'])
                    lists.append(i)
                data = {
                    "topic": "topic-wemedia",
                    "list": lists,
                }
                url = 'http://101.52.241.131:18900/api/kafka'
                res = requests.post(url, data=json.dumps(data, cls=JSONEncoder, ensure_ascii=False).encode('utf-8'), stream=True)
                if res.status_code != 200:
                    for i in id:
                        db.update("update "+names+" set push_state = 2 where id=" + str(i))
                else:
                    for i in id:
                        db.update("update "+names+" set push_state = 1 where id=" + str(i))
                        print("修改成功")
                downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('推送时间:' + downloadTime)
            except Exception as err:
                traceback.print_exc()


if __name__ == "__main__":
    while True:
        spider = ArticleMysql()
        spider.start()
        spider.join()