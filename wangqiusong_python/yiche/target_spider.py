# -*- coding: utf-8 -*-
"""
Created on 2022-10-13 15:55:16
---------
@summary:
---------
@author: 王火龙
"""

import feapder


class TargetSpider(feapder.AirSpider):
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
        yield feapder.Request("https://spidertools.cn", headers=headers, render=True)

    def parse(self, request, response):
        # 提取网站title
        print(response.xpath("//title/text()").extract_first())
        # 提取网站描述
        print(response.xpath("//meta[@name='description']/@content").extract_first())
        print("网站地址: ", response.url)


if __name__ == "__main__":
    TargetSpider().start()