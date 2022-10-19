# -*- coding: utf-8 -*-
'''
---------
@summary:
---------
@author:
'''
import datetime
import json
import re
import ssl
import time
import uuid
from pprint import pformat
import hashlib
from retry import retry
import pymysql
from utils.mylog import log
import requests

# 全局取消ssl证书验证
ssl._create_default_https_context = ssl._create_unverified_context

_regexs = {}


def date_to_timestamp(date, time_format="%Y-%m-%d %H:%M:%S"):
    """
    @summary:
    ---------
    @param date:将"2011-09-28 10:00:00"时间格式转化为时间戳
    @param format:时间格式
    ---------
    @result: 返回时间戳
    """

    timestamp = time.mktime(time.strptime(date, time_format))
    return int(timestamp)


def md5(str):
    # 加密指定段
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


# @log_function_time
def get_info(html, regexs, allow_repeat=True, fetch_one=False, split=None):
    regexs = isinstance(regexs, str) and [regexs] or regexs

    infos = []
    for regex in regexs:
        if regex == '':
            continue

        if regex not in _regexs.keys():
            _regexs[regex] = re.compile(regex, re.S)

        if fetch_one:
            infos = _regexs[regex].search(html)
            if infos:
                infos = infos.groups()
            else:
                continue
        else:
            infos = _regexs[regex].findall(str(html))

        if len(infos) > 0:
            # print(regex)
            break

    if fetch_one:
        infos = infos if infos else ('',)
        return infos if len(infos) > 1 else infos[0]
    else:
        infos = allow_repeat and infos or sorted(set(infos), key=infos.index)
        infos = split.join(infos) if split else infos
        return infos


def get_param(url, key):
    params = url.split('?')[-1].split('&')
    for param in params:
        key_value = param.split('=', 1)
        if key == key_value[0]:
            return key_value[1]
    return None


def url_to_dict(url):
    '''
    @summary: 将url转化为字典
    :param url:
    :return: dict
    '''
    url_dict = {}
    url_list = url.split('&')
    for i in url_list:
        key = i.split('=')[0]
        value = i.split('=')[1]
        url_dict[key] = value
    return url_dict


def get_current_timestamp():
    return int(time.time())


def get_current_date(date_format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(date_format)
    # return time.strftime(date_format, time.localtime(time.time()))


def timestamp_to_date(timestamp, time_format='%Y-%m-%d %H:%M:%S'):
    '''
    @summary:
    ---------
    @param timestamp: 将时间戳转化为日期
    @param format: 日期格式
    ---------
    @result: 返回日期
    '''

    date = time.localtime(timestamp)
    return time.strftime(time_format, date)


def get_json(json_str):
    '''
    @summary: 取json对象
    ---------
    @param json_str: json格式的字符串
    ---------
    @result: 返回json对象
    '''

    try:
        return json.loads(json_str) if json_str else {}
    except Exception as e1:
        try:
            json_str = json_str.strip()
            json_str = json_str.replace("'", '"')
            keys = get_info(json_str, "(\w+):")
            for key in keys:
                json_str = json_str.replace(key, '"%s"' % key)

            return json.loads(json_str) if json_str else {}

        except Exception as e2:
            log.error(
                '''
                e1: %s
                format json_str: %s
                e2: %s
                ''' % (e1, json_str, e2)
            )

        return {}


def dumps_json(json_, indent=4):
    '''
    @summary: 格式化json 用于打印
    ---------
    @param json_: json格式的字符串或json对象
    ---------
    @result: 格式化后的字符串
    '''
    try:
        if isinstance(json_, str):
            json_ = get_json(json_)

        json_ = json.dumps(json_, ensure_ascii=False, indent=indent, skipkeys=True)

    except Exception as e:
        log.error(e)
        json_ = pformat(json_)

    return json_


############
def format_sql_value(value):
    if isinstance(value, str):
        value = pymysql.escape_string(value)

    elif isinstance(value, list) or isinstance(value, dict):
        value = dumps_json(value, indent=None)

    elif isinstance(value, bool):
        value = int(value)

    return value


def list2str(datas):
    '''
    列表转字符串
    :param datas: [1, 2]
    :return: (1, 2)
    '''
    data_str = str(tuple(datas))
    data_str = re.sub(",\)$", ')', data_str)
    return data_str


def make_insert_sql(table, data, auto_update=False, update_columns=(), insert_ignore=False):
    '''
    @summary: 适用于mysql， oracle数据库时间需要to_date 处理（TODO）
    ---------
    @param table:
    @param data: 表数据 json格式
    @param auto_update: 使用的是replace into， 为完全覆盖已存在的数据
    @param update_columns: 需要更新的列 默认全部，当指定值时，auto_update设置无效，当duplicate key冲突时更新指定的列
    @param insert_ignore: 数据存在忽略
    ---------
    @result:
    '''

    keys = ['`{}`'.format(key) for key in data.keys()]
    keys = list2str(keys).replace("'", '')

    values = [format_sql_value(value) for value in data.values()]
    values = list2str(values)

    if update_columns:
        if not isinstance(update_columns, (tuple, list)):
            update_columns = [update_columns]
        update_columns_ = ', '.join(["{key}=values({key})".format(key=key) for key in update_columns])
        sql = 'insert%s into {table} {keys} values {values} on duplicate key update %s' % (' ignore' if insert_ignore else '', update_columns_)

    elif auto_update:
        sql = 'replace into {table} {keys} values {values}'
    else:
        sql = 'insert%s into {table} {keys} values {values}' % (' ignore' if insert_ignore else '')

    sql = sql.format(table=table, keys=keys, values=values).replace('None', 'null')
    return sql


def make_update_sql(table, data, condition):
    '''
    @summary: 适用于mysql， oracle数据库时间需要to_date 处理（TODO）
    ---------
    @param table:
    @param data: 表数据 json格式
    @param condition: where 条件
    ---------
    @result:
    '''
    key_values = []

    for key, value in data.items():
        value = format_sql_value(value)
        if isinstance(value, str):
            key_values.append("`{}`='{}'".format(key, value))
        elif value is None:
            key_values.append("`{}`={}".format(key, 'null'))
        else:
            key_values.append("`{}`={}".format(key, value))

    key_values = ', '.join(key_values)

    sql = 'update {table} set {key_values} where {condition}'
    sql = sql.format(table=table, key_values=key_values, condition=condition)
    return sql


def make_batch_sql(table, datas, auto_update=False, update_columns=()):
    '''
    @summary: 生产批量的sql
    ---------
    @param table:
    @param datas: 表数据 [{...}]
    @param auto_update: 使用的是replace into， 为完全覆盖已存在的数据
    @param update_columns: 需要更新的列 默认全部，当指定值时，auto_update设置无效，当duplicate key冲突时更新指定的列
    ---------
    @result:
    '''
    if not datas:
        return

    keys = list(datas[0].keys())
    values_placeholder = ['%s'] * len(keys)

    values = []
    for data in datas:
        value = []
        for key in keys:
            current_data = data.get(key)
            current_data = format_sql_value(current_data)

            value.append(current_data)

        values.append(value)

    keys = ['`{}`'.format(key) for key in keys]
    keys = str(keys).replace('[', '(').replace(']', ')').replace("'", '')
    values_placeholder = str(values_placeholder).replace('[', '(').replace(']', ')').replace("'", '')

    if update_columns:
        if not isinstance(update_columns, (tuple, list)):
            update_columns = [update_columns]
        update_columns_ = ', '.join(["`{key}`=values(`{key}`)".format(key=key) for key in update_columns])
        sql = 'insert into {table} {keys} values {values_placeholder} on duplicate key update {update_columns}'.format(table=table, keys=keys, values_placeholder=values_placeholder,
                                                                                                                       update_columns=update_columns_)
    elif auto_update:
        sql = 'replace into {table} {keys} values {values_placeholder}'.format(table=table, keys=keys, values_placeholder=values_placeholder)
    else:
        sql = 'insert ignore into {table} {keys} values {values_placeholder}'.format(table=table, keys=keys, values_placeholder=values_placeholder)

    return sql, values


##########

def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def get_md5(*args):
    '''
    @summary: 获取唯一的32位md5
    ---------
    @param *args: 参与联合去重的值
    ---------
    @result: 7c8684bcbdfcea6697650aa53d7b1405
    '''

    m = hashlib.md5()
    for arg in args:
        m.update(str(arg).encode())

    return m.hexdigest()


def numftime(timestamp):
    """
    :param timestamp:
    :return: 时间戳➡格式化时间
    """
    time_local = time.localtime(int(timestamp))
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


@retry(tries=10, delay=3)
def dingding_send(text):
    # send info to dingding
    text = f'{time.strftime("%m月%d日 %H:%M.", time.localtime())}\n{text}'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    post_data = {
        "msgtype": "text",
        "text": {"content": text}
    }
    dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=1c738f72f1a733eab02902af25d26ade6d793d503f4d4ed52036894ebd6f0886"
    requests.post(dingding_url, headers=headers, data=json.dumps(post_data))


def sort_dict(params: dict):
    keys = sorted(params.keys())[::-1]
    new_dict = {}
    for k in keys:
        new_dict[k] = params[k]
    return new_dict


def is_in_crawl_time_rang(timestamp, day=7):
    """
    '2021-03-04 09:45:17'
    '1614822317'
    给定一个时间或者时间戳 判断是否是七天内的时间
    :param timestamp:
    :return:
    """
    try:
        timestamp = int(timestamp)
    except:
        d = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timestamp = int(time.mktime(t))

    history_timestamp = time.time() - (86400 * day)

    if int(timestamp) >= history_timestamp:
        return True
    else:
        return False


def get_next_page(req_url):
    """
    获取下一页页面js
    :param response:
    :return:
    """
    params = url_to_dict(req_url)
    __biz = params.get("__biz")
    pass_ticket = params.get("pass_ticket")
    appmsg_token = params.get("appmsg_token")
    offset = params.get("offset", "0")

    next_page_url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={__biz}&f=json&offset={offset}&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket={pass_ticket}&wxtoken=&appmsg_token={appmsg_token}&x5=0&f=json".format(
        __biz=__biz,
        offset=offset,
        pass_ticket=pass_ticket,
        appmsg_token=appmsg_token,
    )
    tip = "抓取列表页"
    sleep_time = 10
    next_page = "{tip} 休眠 {sleep_time}s 下次刷新时间 {begin_spider_time} <script>setTimeout(function(){{window.location.href='{url}';}},{sleep_time_msec});</script>".format(
        tip=tip and tip + ' ', sleep_time=sleep_time, begin_spider_time=timestamp_to_date(get_current_timestamp() + sleep_time), url=next_page_url, sleep_time_msec=sleep_time * 1000
    )
    return next_page

# if __name__ == '__main__':
#     print( is_in_crawl_time_rang('2021-06-3 11:19:19', day=1))
