# --*-- coding: utf-8 --*--
# @Author  : sheldon
# @Software: PyCharm
import csv
import requests,json, pymysql, pymongo
from fake_useragent import UserAgent
from lxml import etree


ua = UserAgent()  # 构造随机UA
url = "https://book.douban.com/tag/%E8%AF%97%E6%AD%8C" # start_url
headers = {'User-Agent': ua.random}
response = requests.get(url, headers=headers).content.decode()  # 获取响应
# print(response)
html_data = etree.HTML(response) # 声明文本，进行初始化
ret = html_data.xpath('//*[@id="subject_list"]/ul/li')  # xpath提取首页中标签对象
print(ret)


"""1、保存为.json文件"""
# ret_list = []
# for tr in ret:
#     ret_dict = {}
#     ret_dict["title"] = tr.xpath('./div[@class="info"]/h2/a/@title')[0]
#     ret_dict["rat"] = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
#     ret_dict["pub"] = tr.xpath('./div[@class="info"]/div[@class="pub"]/text()')[0].replace("\u2022","").replace('\n', '')
#     ret_dict["appraise"] = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="pl"]/text()')[0].replace('\n', '')
#     ret_list.append(ret_dict)
# print(ret_list)
# str_list = str(ret_list)
# data = json.dumps(str_list)
# print(data)
# with open('data.json', 'w') as f:
#     f.write(json.dumps(str_list, indent=2, ensure_ascii=False))


"""2、保存为.txt文件"""
# for tr in ret:
#     title = tr.xpath('./div[@class="info"]/h2/a/@title')[0]
#     rat = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
#     pub = tr.xpath('./div[@class="info"]/div[@class="pub"]/text()')[0]
#     appraise = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="pl"]')[0]
#     file = open('explore.txt', 'a', encoding='utf-8')
#     file.write('\n'.join([title, rat, pub, appraise]))
#     file.write('\n' + '=' * 50 + '\n')
#     file.close()

"""3、保存为.csv文件"""
# fp = open('data.csv', 'w', newline="", encoding="utf-8")
# writer = csv.writer(fp)
# writer.writerow(('书名', '评分', '出版', '评论'))
# for tr in ret:
#     books = []
#     title = tr.xpath('./div[@class="info"]/h2/a/@title')[0]
#     rat = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
#     pub = tr.xpath('./div[@class="info"]/div[@class="pub"]/text()')[0].replace("\u2022","").replace('\n', '')
#     appraise = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="pl"]/text()')[0].replace('\n', '')
#     books.append([title, rat, pub, appraise])
#
#     for rows in books:
#         writer.writerow(rows)
# fp.close()


"""4、保存至MySQL数据库"""
# db = pymysql.connect(host='localhost', user='root', password='mysql', port=3306, db='douban')
# cursor = db.cursor()
# sql = 'create table if not exists books(title varchar(225) not null, rat varchar(225) not null, pub varchar(225) not null,appraise varchar(225) not null)'
# cursor.execute(sql)
#
# for tr in ret:
#     ret_dict = {}
#     ret_dict["title"] = tr.xpath('./div[@class="info"]/h2/a/@title')[0]
#     ret_dict["rat"] = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
#     ret_dict["pub"] = tr.xpath('./div[@class="info"]/div[@class="pub"]/text()')[0].replace("\u2022","").replace('\n', '')
#     ret_dict["appraise"] = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="pl"]/text()')[0].replace('\n', '')
#
#     sql_insert = 'insert into books(title, rat, pub, appraise) values(%s, %s, %s, %s)'
#
#     cursor.execute(sql_insert, (ret_dict["title"], ret_dict["rat"],ret_dict["pub"], ret_dict["appraise"]))
#     db.commit()
# db.close()







"""5、保存至MongoDB数据库"""
client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.douban

#  方法一
# ret_list = []
# for tr in ret:
#     ret_dict = {}
#     ret_dict["title"] = tr.xpath('./div[@class="info"]/h2/a/@title')[0]
#     ret_dict["rat"] = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
#     ret_dict["pub"] = tr.xpath('./div[@class="info"]/div[@class="pub"]/text()')[0].replace("\u2022","").replace('\n', '')
#     ret_dict["appraise"] = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="pl"]/text()')[0].replace('\n', '')
#     ret_list.append(ret_dict)
# print(ret_list)
# for i in ret_list:
#     collection.insert_one({'书名': i["title"], '评分': i["rat"], '出版': i["pub"], '评价数': i["appraise"]})

#  方法二
books_list = []
for tr in ret:
    title = tr.xpath('./div[@class="info"]/h2/a/@title')[0]
    rat = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
    pub = tr.xpath('./div[@class="info"]/div[@class="pub"]/text()')[0].replace("\u2022","").replace('\n', '')
    appraise = tr.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="pl"]/text()')[0].replace('\n', '')
    books_list.append([title, rat, pub, appraise])
print(books_list)
lenth =len(books_list)
print(lenth)
for i in range(0,lenth):
    books = {}
    books['title'] = books_list[i][0]
    books['rat'] = books_list[i][1]
    books['pub'] = books_list[i][2]
    books['appraise'] = books_list[i][3]
    collection.insert_one(books)
    print('第{}条数据插入成功'.format(i+1))











