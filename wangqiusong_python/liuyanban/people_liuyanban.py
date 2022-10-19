# -*- coding: utf-8 -*-
"""
Created on 2022-10-13 16:40:50
---------
@summary:
---------
@author: 王火龙
"""
import click as click
import feapder
from feapder.db.mysqldb import MysqlDB
import setting as cfg
import hashlib
import datetime
import json
import time
import requests
import re
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from liuyanban import yq_liuyanban_item


class people_liuyanban(feapder.Spider):
    a = 0
    db = MysqlDB()
    headerss = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://liuyan.people.com.cn",
        "Referer": "http://liuyan.people.com.cn/threads/content?tid=14592777",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        "token": ""
    }
    datass = {
        "appCode": "PC42ce3bfa4980a9",
        "token": "",
        "signature": "18d497371f56c631390ca2f9a196b130",
        "param": "{\"tid\":\"16152844\",\"fromTrash\":0}"

    }

    def start_requests(self, ):
        while True:
            # for fids in range(539, 4476):
            arr = [1, 2, 5]
            fidArr = ['5050', '5051', '5052', '5054', '5055', '5056', '5057', '5058', '5059', '5060', '5061', '5062',
                      '5063',
                      '5064',
                      '5065', '5066', '5067', '5068', '5069', '5070', '5071', '5072', '5073',
                      '5074', '5075', '5076', '5077', '5078', '5079', '5080', '5081', '5082', '5083', '5084', '5085',
                      '5086',
                      '5087',
                      '5088', '5089', '5090', '5091', '5092', '5093', '5094', '5095', '5096',
                      '5097', '5098', '5099', '5100', '539', '540', '733', '734', '735', '736', '741', '742', '743', '744',
                      '745',
                      '746', '747', '748', '749', '750', '751', '752', '753', '754', '755', '756',
                      '757', '758', '759', '760', '761', '762', '765', '766', '767', '768', '763', '764', '5118', '5119',
                      '541',
                      '542', '769', '770', '771', '772', '773', '774', '775', '776', '777', '778',
                      '779', '780', '781', '782', '787', '788', '789', '790', '791', '792', '793', '794', '795', '796',
                      '797',
                      '798',
                      '799', '800', '801', '802', '803', '804', '543', '544', '805', '806', '807',
                      '808', '809', '810', '811', '812', '813', '814', '815', '816', '817', '818', '819', '820', '821',
                      '822',
                      '823',
                      '824', '825', '826', '4732', '4733', '1682', '4744', '1600', '4749', '545',
                      '546', '827', '828', '829', '830', '831', '832', '833', '834', '835', '836', '837', '838', '839',
                      '840',
                      '841',
                      '842', '843', '844', '845', '846', '847', '848', '547', '548', '849', '850',
                      '851', '852', '853', '854', '855', '856', '857', '858', '859', '860', '861', '862', '863', '864',
                      '865',
                      '866',
                      '867', '868', '871', '872', '869', '870', '549', '550', '873', '874', '875',
                      '876', '877', '878', '879', '880', '881', '882', '883', '884', '885', '886', '887', '888', '889',
                      '890',
                      '891',
                      '892', '893', '894', '895', '896', '897', '898', '899', '900', '551', '552',
                      '901', '902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914',
                      '915',
                      '916',
                      '1545', '1546', '553', '554', '917', '918', '919', '920', '921', '922',
                      '923', '924', '927', '928', '929', '930', '931', '932', '933', '934', '935', '936', '937', '938',
                      '939',
                      '940',
                      '925', '926', '941', '942', '555', '556', '943', '944', '947', '948', '949',
                      '950', '951', '952', '953', '954', '957', '958', '959', '960', '961', '962', '963', '964', '965',
                      '966',
                      '967',
                      '968', '969', '970', '971', '972', '973', '974', '977', '978', '979', '980',
                      '557', '558', '981', '982', '1001', '1002', '987', '988', '983', '984', '989', '990', '999', '1000',
                      '991',
                      '992', '995', '996', '985', '986', '997', '998', '1003', '1004', '1005', '1006',
                      '993', '994', '559', '560', '1007', '1008', '1009', '1010', '1011', '1012', '1013', '1014', '1015',
                      '1016',
                      '1017', '1018', '1019', '1020', '1021', '1022', '1023', '1024', '1025', '1026',
                      '1027', '1028', '561', '562', '1029', '1030', '1031', '1032', '1033', '1034', '1035', '1036', '1037',
                      '1038',
                      '1039', '1040', '1041', '1042', '1043', '1044', '1045', '1046', '1047',
                      '1048', '1049', '1050', '1051', '1052', '1055', '1056', '1572', '1573', '1057', '1058', '1059',
                      '1060',
                      '563',
                      '564', '1061', '1062', '1065', '1066', '1067', '1068', '1069', '1070',
                      '1071', '1072', '1063', '1064', '1073', '1074', '1075', '1076', '1077', '1078', '4641', '4642', '565',
                      '566',
                      '1079', '1080', '1081', '1082', '1083', '1084', '1085', '1086', '1087',
                      '1088', '1089', '1090', '1091', '1092', '1093', '1094', '1095', '1096', '1097', '1098', '1099',
                      '1100',
                      '567',
                      '568', '1101', '1102', '1103', '1104', '1105', '1106', '1107', '1108',
                      '1109', '1110', '1111', '1112', '1113', '1114', '1117', '1118', '1119', '1120', '1115', '1116',
                      '1121',
                      '1122',
                      '1125', '1126', '1127', '1128', '1129', '1130', '1131', '1132', '1133',
                      '1134', '569', '570', '1135', '1136', '1137', '1138', '1139', '1140', '1141', '1142', '1149', '1150',
                      '1145',
                      '1146', '1147', '1148', '1143', '1144', '1151', '1152', '1153', '1154',
                      '1155', '1156', '1157', '1158', '1159', '1160', '1161', '1162', '1163', '1164', '1165', '1166',
                      '1167',
                      '1168',
                      '4475', '4474', '2370', '4666', '2383', '4667', '2405', '4668', '2444',
                      '4669', '2435', '4670', '2471', '4671', '2484', '4672', '2497', '4673', '2507', '4674', '2519',
                      '4675',
                      '571',
                      '572', '1169', '1170', '1171', '1172', '1175', '1176', '1179', '1180',
                      '1173', '1174', '1183', '1184', '1181', '1182', '1185', '1186', '1177', '1178', '1187', '1188',
                      '1189',
                      '1190',
                      '1191', '1192', '1547', '1548', '4483', '4484', '4485', '4486', '4487',
                      '4488', '4489', '4490', '573', '574', '1193', '1194', '1562', '1563', '1195', '1196', '1197', '1198',
                      '1199',
                      '1200', '1201', '1202', '1203', '1204', '1205', '1206', '1207', '1208',
                      '1209', '1210', '1211', '1212', '1213', '1214', '1215', '1216', '1564', '1565', '575', '576', '1217',
                      '1218',
                      '1225', '1226', '1219', '1220', '1221', '1222', '1223', '1224', '1227',
                      '1228', '1229', '1230', '1231', '1232', '1233', '1234', '1235', '1236', '1237', '1238', '1239',
                      '1240',
                      '1241',
                      '1242', '1243', '1244', '1245', '1246', '1247', '1248', '1249', '1250',
                      '1251', '1252', '1253', '1254', '1255', '1256', '1257', '1258', '577', '578', '1259', '1260', '1261',
                      '1262',
                      '1263', '1264', '1559', '1560', '1267', '1268', '1269', '1270', '1271',
                      '1272', '1273', '1274', '1275', '1276', '1277', '1278', '1279', '1280', '1281', '1282', '1283',
                      '1284',
                      '1590',
                      '1591', '579', '580', '1285', '1286', '1287', '1288', '4501', '4502',
                      '4429', '4712', '581', '582', '1595', '1596', '1465', '1466', '1467', '1468', '1469', '1470', '1471',
                      '1472',
                      '1473', '1474', '1475', '1476', '1477', '1478', '1479', '1480', '1481',
                      '1482', '1483', '1484', '1485', '1486', '1487', '1488', '1489', '1490', '1491', '1492', '1493',
                      '1494',
                      '1495',
                      '1496', '1497', '1498', '1499', '1500', '1501', '1502', '1503', '1504',
                      '1505', '1506', '1507', '1508', '1509', '1510', '1511', '1512', '1513', '1514', '1515', '1516',
                      '1517',
                      '1518',
                      '1519', '1520', '1521', '1522', '1523', '1524', '1525', '1526', '1527',
                      '1528', '1529', '1530', '1531', '1532', '1533', '1534', '1535', '1536', '1537', '1538', '1539',
                      '1540',
                      '1541',
                      '1542', '1543', '1544', '5113', '5114', '583', '584', '1289', '1290',
                      '1291', '1292', '1293', '1294', '1295', '1296', '1297', '1298', '1299', '1300', '1301', '1302',
                      '1303',
                      '1304',
                      '1305', '1306', '1307', '1308', '1309', '1310', '1317', '1318', '1311',
                      '1312', '1313', '1314', '1315', '1316', '1319', '1320', '1321', '1322', '1323', '1324', '1549',
                      '1550',
                      '1551',
                      '1552', '1553', '1554', '585', '586', '1325', '1326', '1327', '1328',
                      '1329', '1330', '1331', '1332', '1333', '1334', '1566', '1567', '1335', '1336', '1568', '1569',
                      '1570',
                      '1571',
                      '4680', '4681', '587', '588', '1337', '1338', '1339', '1340', '1341',
                      '1342', '1343', '1344', '1345', '1346', '1347', '1348', '1349', '1350', '1351', '1352', '1574',
                      '1575',
                      '1576',
                      '1577', '1578', '1579', '1580', '1581', '1582', '1583', '1584', '1585',
                      '1586', '1587', '1588', '1589', '589', '590', '1353', '1354', '1355', '1356', '1357', '1358', '1359',
                      '1360',
                      '1361', '1362', '1363', '1364', '1365', '1366', '591', '592', '1367', '1368',
                      '1369', '1370', '1371', '1372', '1373', '1374', '1375', '1376', '1377', '1378', '1379', '1380',
                      '1381',
                      '1382',
                      '1383', '1384', '1385', '1386', '4454', '5173', '5174', '593', '594',
                      '1387', '1388', '1391', '1392', '1389', '1390', '1393', '1394', '1395', '1396', '1397', '1398',
                      '1399',
                      '1400',
                      '1401', '1402', '1403', '1404', '1405', '1406', '1407', '1408', '1409',
                      '1410', '1555', '1556', '1557', '1558', '595', '596', '1411', '1412', '1413', '1414', '1415', '1416',
                      '1417',
                      '1418', '1419', '1420', '1421', '1422', '1423', '1424', '1425', '1426', '597',
                      '598', '1427', '1428', '1429', '1430', '1431', '1432', '1435', '1436', '1433', '1434', '599', '1592',
                      '1437',
                      '1438', '1439', '1440', '1441', '1442', '1443', '1444', '1455', '1456',
                      '1457', '1458', '1453', '1454', '1447', '1448', '1451', '1452', '1449', '1450', '1445', '1446',
                      '1459',
                      '1460',
                      '1461', '1462', '1463', '1464', '600', '601']
            # fidArr = [539]
            for fids in fidArr:
                for nums in arr:
                    type = 2
                    signatures = self.signature(fids, type, nums)
                    dataa = json.dumps(signatures)
                    url = "http://liuyan.people.com.cn/v1/threads/list/df"
                    yield feapder.Request(url, timeout=30, data=dataa, allow_redirects=False, download_midware=self.download_midware,)

    def signature(self, tids, type, nums):
        if type == 1:
            self.datass['param'] = "{\"tid\":\"" + str(tids) + "\",\"fromTrash\":0}"
            pwds = "/v1/threads/content{\"tid\":\"" + str(tids) + "\",\"fromTrash\":0}"
        else:
            self.datass['param'] = "{\"fid\":\"" + str(tids) + "\",\"showUnAnswer\":1,\"typeId\":" + str(
                nums) + ",\"lastItem\":\"\",\"position\":\"0\",\"rows\":10,\"orderType\":2}"
            pwds = "/v1/threads/list/df{\"fid\":\"" + str(tids) + "\",\"showUnAnswer\":1,\"typeId\":" + str(
                nums) + ",\"lastItem\":\"\",\"position\":\"0\",\"rows\":10,\"orderType\":2}"
        pwd = self.datass['appCode']
        pwd = hashlib.md5(bytes(pwd, encoding='utf-8'))
        pwdss = pwds + pwd.hexdigest()[0:16]
        self.datass['signature'] = hashlib.md5(bytes(pwdss, encoding='utf-8')).hexdigest()
        return self.datass

    def parse(self, request, response):
            # if response.status_code != 200:
            #     raise Exception("非法页面")
            tid = re.compile('"tid":(.*?),').findall(response.text)
            for tids in tid:
                time.sleep(1)
                urls = "http://liuyan.people.com.cn/v1/threads/content"
                type = 1
                num = 2
                signatures = self.signature(tids, type, num)
                dataa = json.dumps(signatures)
                res = requests.post(urls, headers=self.headerss, data=dataa, timeout=30, verify=False)
                title = re.compile('"subject":"(.*?)",').findall(res.content.decode('utf-8'))
                content = re.compile('"content":"([\s\S]*?)",').findall(res.content.decode('utf-8'))
                pubtime = re.compile('"createDateline":([\s\S]*?),').findall(res.content.decode('utf-8'))
                time_tuple_1 = time.localtime(int(pubtime[0]))
                bj_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple_1)
                downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                pubTimes = datetime.datetime.strptime(bj_time, "%Y-%m-%d %H:%M:%S")
                downloadTimes = datetime.datetime.strptime(downloadTime, "%Y-%m-%d %H:%M:%S")
                site = "领导留言板"
                siteId = 1047953
                articleStatue = 0
                item = yq_liuyanban_item.YqLiuyanbanItem()  # 声明一个item
                item.url = "https://liuyan.people.com.cn/threads/content?tid=" + tids  # 给item属性赋值
                item.title = title[0]  # 给item属性赋值
                item.pub_time = pubTimes  # 给item属性赋值
                item.content = content[0]  # 给item属性赋值
                item.download_time = downloadTimes  # 给item属性赋值
                item.site = site  # 给item属性赋值
                item.site_id = siteId  # 给item属性赋值
                item.aid = tids  # 给item属性赋值
                item.push_state = articleStatue  # 给item属性赋值
                yield item

    def download_midware(self, request):
        """
            下载中间件处理参数
            :param request:
            :return:
            """
        request.headers  = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Referer": "http://liuyan.people.com.cn/threads/list?fid=5050&position=1",
        }
        try:
            ip = requests.get(f"http://192.168.1.26:16666/get/", timeout=3).json().get("proxy")
            request.proxies = {"http": ip, "https": ip}
        except:
            pass
        return request


@click.command(name='mian')
# @click.option('--t', default=cfg.THREAD_NUM, help="num 线程数")
@click.option('--p', default=1, help="是否开启代理")
def mian(p):
    cfg.ISPROXY = p
    spider = people_liuyanban(redis_key='wqs', )
    spider.start()


if __name__ == "__main__":
    mian()
