# -*- coding: utf-8 -*-
"""
Created on 2022-10-20 14:18:18
---------
@summary:
---------
@author: 王火龙
"""

import feapder
import sys
import os
import re
import datetime
from renminhaos import yq_renminhao_item

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Renminhao(feapder.Spider):
    cookies = {
        "simulation_id": "pc6350e6bbd085b49",
    }
    params = {
        "type": "list",
        "label_id": "20"
    }

    # 循环请求频道地址
    def start_requests(self):
        for labelId in range(1, 20):
            self.params['label_id'] = str(labelId)
            self.params['label_id'] = str(2)
            yield feapder.Request("https://rmh.pdnews.cn/Pc/ArticleApi/rightList", method="POST", cookies=self.cookies,
                                  params=self.params, allow_redirects=False, )

    # 处理频道地址 请求文章地址
    def parse(self, request, response):
        jsons = response.json['data']
        for arr in jsons:
            data = []
            arUrl = arr['id']
            title = arr['title']
            source = arr['gov_name']
            cover = arr['cover_img']
            if arr['video_url'] != "":
                video = '<video src="' + arr['video_url'] + '" controls=""></video><br>'
                arUrl = "https://rmh.pdnews.cn/Pc/ArtInfoApi/video?id=" + arr['id']
                data.append(arUrl)
                data.append(video)
            else:
                arUrl = "https://rmh.pdnews.cn/Pc/ArtInfoApi/article?id=" + arr['id']
                video = ""
                data.append(arUrl)
                data.append(video)
            data.append(title)
            data.append(source)
            data.append(cover)
            yield feapder.Request(arUrl, callback=self.parser_detail, method="POST", metas=data, cookies=self.cookies,
                                  allow_redirects=False)

    # 处理正文内容
    def parser_detail(self, request, response):
        try:
            pubTime = re.compile('<meta name="og:time" content="(.*?)">').findall(response.text)
            content = re.compile('<div class="content">([\s\S]*?)<!-- 声明  -->').findall(response.text)
            if not content :
                content = re.compile('<div class="short-content">([\s\S]*?)<!-- 声明  -->').findall(response.text)
                if not content:
                    contents = request.metas[1] + "<br>"
                else:
                    contents = request.metas[1]+"<br>" +content[0]
            # pubTimes = datetime.datetime.strptime(pubTime[0], '%Y年%m月%d日').strftime('%Y-%m-%d %H:%M:%S')
            downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            site = "人民号"
            siteId = 1037104
            articleStatue = 0
            item = yq_renminhao_item.YqRenminhaoItem()  # 声明一个item
            item.url = request.metas[0]  # 给item属性赋值
            item.title = request.metas[2]  # 给item属性赋值
            item.pub_time = pubTime[0]  # 给item属性赋值
            item.content = contents  # 给item属性赋值
            item.download_time = downloadTime  # 给item属性赋值
            item.site = site  # 给item属性赋值
            item.site_id = siteId  # 给item属性赋值
            item.aid = request.metas[0]  # 给item属性赋值
            item.push_state = articleStatue  # 给item属性赋值
            item.cover = request.metas[4]  # 给item属性赋值
            yield item
        except Exception as err:
            import traceback
            traceback.print_exc()
            pass


if __name__ == "__main__":
    while True:
        spider = Renminhao(redis_key="wqs_renminhao")
        spider.start()
        spider.join()
