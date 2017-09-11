#encoding:utf-8
from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
from randomIp import get_ip_list
from randomIp import get_random_ip
from concurrent.futures import ThreadPoolExecutor
#读取本页小说地址列表
num = 0
def gettheallnovel(url):
    novels = []
    html = requests.get(url)
    html.encoding = 'gb2312'
    bsobj = BeautifulSoup(html.text, "html.parser")
    divs = bsobj.findAll("div", {"class": "n"})
    for i in divs:
        index = "https://www.diyibanzhu.in"+i.find("a").attrs["href"]
        novels.append(index)
    return novels
#获取所有小说页地址
def alllist():
    lists = []
    for i in range(1,113):
        strs = "https://www.diyibanzhu.in/qitaleibie/shuku_0_"+str(i)+".html"
        lists.append(strs)
    return lists

#https://www.diyibanzhu.in/modules/article/txtarticle.php?id=2608
#下载函数
def downnovel(href,name):
    src = "https://www.diyibanzhu.in"+href
    urlretrieve(src, "E:\code\\downnovels\\novels\%s.txt" % name)
    print("下载"+name+"完成")
#随机ip下载一本小说
def getdowntxt(url,ip,sleep_time=5):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
    while True:
        try:
            html = requests.get(url, proxies=ip)
            html.encoding = 'gb2312'
            bsobj = BeautifulSoup(html.text, "html.parser")
            href = bsobj.find("div", {"class": "down"}).find("a").attrs["href"]
            name = bsobj.find("img", {"class": "lazy"}).attrs["alt"]
            print("尝试下载"+name+ip)
            downnovel(href=href, name=name)
            break
        except:
            sleep_time += 5
            print("sleep_time={}".format(sleep_time))
#获取随机ip
url = 'http://www.xicidaili.com/wt/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
ip_list = get_ip_list(url, headers=headers)
proxies = get_random_ip(ip_list)
#建立线程池
executer = ThreadPoolExecutor(100)
lists = alllist()
for list in lists:
    urls= gettheallnovel(list)
    for url in urls:
        proxies = get_random_ip(ip_list)
        executer.submit(getdowntxt, url, proxies)