"""爬取阳光高考的院校库，保存学校名，双一流信息，保存为csv"""
import requests
from bs4 import BeautifulSoup
import csv

lis = []
ul = None


def deal_tr(_tr):  # 输入<td>list 返回<td>的内容
    return {'school': _tr[0].a.string.strip() if _tr[0].a is not None else _tr[0].string.strip(),
            'u1': 1 if _tr[5].string is None else 0,
            'm1': 1 if _tr[6].string is None else 0}


def paa(_url):  # 输入单页url 获取<tr>list 并赋值下一页url
    global ul
    r = requests.get(_url)
    soup = BeautifulSoup(r.text, 'lxml')
    al = soup.find_all(class_='yxk-table')[0]
    print(al)
    ul = soup.find_all(class_='ch-page clearfix')[0].find_all('li')[-2].a
    for tr in al.table.find_all('tr')[1:]:
        lis.append(deal_tr(tr.find_all('td')))


paa('https://gaokao.chsi.com.cn/sch/')  # 先跑一次
print(ul)
while ul is not None and not ul.attrs['href'] == "###":  # 循环获取下一页内容并向lis插入内容
    print(ul)
    paa('https://gaokao.chsi.com.cn' + ul.attrs['href'])

print(lis)
with open('C:\\Users\\I\\Desktop\\cc.csv', 'w', newline="")as f:  # 存为csv
    fc = csv.DictWriter(f, ["school", "u1", "m1"])
    fc.writeheader()
    fc.writerows(lis)
