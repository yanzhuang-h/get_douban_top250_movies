import re
from spider import Spider
from bs4 import BeautifulSoup

douban250 = {
    "title": '''re.compile(r'<span class="title">(.*)</span>')''',  # 电影名称
    "rating": '''re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')''',
    "judgenum": '''re.compile(r'<span>(\d*)人评价</span>')''',  # 点评人数
    "inq": '''re.compile(r'<span class="inq">(.*)</span>')''',  # 一句话评论
    "link": '''re.compile(r'<a href="(.*)">')'''  # 影片链接
}
baseurl = 'https://movie.douban.com/top250?start='
savexlsname = 'douban.xls'
mySpider = Spider(baseurl, douban250)

# # count = 0
# for i in range(0, 10):
#     url = mySpider.baseUrl + str(i * 25)
#     html = mySpider.gethtml(url)
#     bs = BeautifulSoup(html, "html.parser")
#     for item in bs.find_all('div', class_="item"):
#         data = mySpider.parseData(str(item))
#         print(data)
#         # count += 1
#         # print(count)

mySpider.getData()
mySpider.saveXls(savexlsname)

