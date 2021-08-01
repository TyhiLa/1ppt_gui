from os import path, rename, remove, mkdir, chdir
import re
from parsel import Selector
from requests import get
import zipfile
from tqdm import tqdm

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/90.0.4430.212 Safari/537.36'}
url_all = 'http://www.1ppt.com'

if not path.isdir('download'):
    mkdir('download')
chdir('download')


def req_for_web(url):
    req1 = get(url, headers=headers)
    req1.encoding = 'gbk'
    return req1


def xpath(req_in, xpath_road):
    req_xpath = Selector(req_in.text)
    selector_re = req_xpath.xpath(xpath_road).extract()
    return selector_re



def getTitleLink(url, index):
    html = xpath(req_for_web(url), '/html/body/div[5]/dl/dd/ul/li')
    # print(html)
    # TODO: iter for too many times, need Improving
    # title = [re.findall('target="_blank">(.*?)</a></h2>', x)[0] for x in html]
    # img = [re.findall('<img src="(.*?)"', x)[0] for x in html]
    temp = [re.findall('<img src="(.*?)" alt="(.*?)">', x)[0] for x in html]
    dow_url = [url_all + re.findall('<a href="(.*?)"', x)[0] for x in html]
    title = [x[1] for x in temp]
    img_url = [x[0] for x in temp]
    return title, img_url[index], dow_url


def valueImport():
    req_site = req_for_web(url_all)
    all_choose_link = [url_all + x for x in xpath(req_site, '/html/body/div[5]/div//ul/li[2]/a/@href')]
    all_choose_title = xpath(req_site, '/html/body/div[5]/div//ul/li[2]/a/@title')
    return all_choose_link, all_choose_title


if __name__ == '__main__':
    # print(valueImport())
    getTitleLink('http://www.1ppt.com/moban/jianjie/', 1)