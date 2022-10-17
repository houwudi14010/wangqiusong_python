# -*- coding: utf-8 -*-
"""
Created on 2022-10-13 14:58:12
---------
@summary:
---------
@author: 王火龙
"""

import feapder
from feapder.db.mysqldb import MysqlDB

from wangyi.article_list_tieba_article_item import ArticleListTiebaArticleItem


class WangyiNew(feapder.AirSpider):
    def start_requests(self):
        yield feapder.Request("https://spidertools.cn").json

    def parse(self, request, response):
        # 提取网站title
        print(response.xpath("//title/text()").extract_first())
        # 提取网站描述
        print(response.xpath("//meta[@name='description']/@content").extract_first())
        print("网站地址: ", response.url)
        self.query(response)


if __name__ == "__main__":
    WangyiNew(thread_count=5).start()
