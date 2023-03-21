from bs4 import BeautifulSoup
from urllib import request
from io import BytesIO
import gzip
import urllib
import re
import ssl
import xlwt


class Spider:
    def __init__(self, baseUrl, itemInfs):
        self.dataList = []
        self.baseUrl = baseUrl
        self.itemInfs = itemInfs

    def gethtml(self, url):  # Murl获取html数据

        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        req = request.Request(url, headers=head)
        context = ssl._create_unverified_context()
        html = ""

        try:
            response = request.urlopen(req, context=context)
            html = response.read()#.decode("utf-8")
            buff = BytesIO(html)
            f = gzip.GzipFile(fileobj=buff)
            html = f.read().decode('utf-8')
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)

        return html

    def parseData(self, item):  # 从单元数据中解析详细数据
        data = []
        res = re.findall(eval(self.itemInfs["title"]), item)[0]
        data.append(res)
        res = re.findall(eval(self.itemInfs["rating"]), item)[0]
        data.append(res)
        res = re.findall(eval(self.itemInfs["judgenum"]), item)[0]
        data.append(res)
        try:
            res = re.findall(eval(self.itemInfs["inq"]), item)[0]
        except:
            res = ''
        finally:
            data.append(res)
        res = re.findall(eval(self.itemInfs["link"]), item)[0]
        data.append(res)
        return data

    def getData(self):  # Murl获取html数据,从html数据中找到单元数据,并完成数据解析
        for i in range(0, 10):
            url = self.baseUrl + str(i * 25)
            html = self.gethtml(url)
            bs = BeautifulSoup(html, "html.parser")
            for item in bs.find_all('div', class_="item"):
                data = self.parseData(str(item))
                self.dataList.append(data)

    def saveXls(self, fname):  # 存储数据到xls文件
        workbook = xlwt.Workbook(encoding="utf-8")  # 创建工作簿
        worksheet = workbook.add_sheet('sheet1')  # 创建工作表#写入数据‘python’，第1行，第1列
        keys = self.itemInfs.keys()
        for i, key in enumerate(keys):  # 标题行
            worksheet.write(0, i, key)
        for i, film in enumerate(self.dataList):  # 影片数据
            for j, item in enumerate(film):
                worksheet.write(i + 1, j, item)
        workbook.save(fname)
        print('保存xls文件完成！')
