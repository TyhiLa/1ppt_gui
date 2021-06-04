from parsel import Selector
from requests import get
import zipfile
from os import path, rename, remove, mkdir, chdir
from tqdm import tqdm

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
url_all = 'http://www.1ppt.com'

if not path.isdir('download'):
    mkdir('download')
chdir('download')


def req_for_xpath(url, xpath_road):
    req1 = get(url, headers=HEADERS)
    req1.encoding = 'gbk'
    req_xpath = Selector(req1.text)
    selector_re = req_xpath.xpath(xpath_road).extract()
    return selector_re


all_choose_link = req_for_xpath(url_all, '/html/body/div[5]/div//ul/li[2]/a/@href')
all_choose_title = req_for_xpath(url_all, '/html/body/div[5]/div//ul/li[2]/a/@title')
title = []


def get_choice_link(choose_title):
    choice_link1 = all_choose_link[choose_title - 1]
    return choice_link1


def file_download(url):
    file_first_link_list = req_for_xpath(url, '/html/body/div[5]/dl/dd/ul//li/h2/a/@href')
    url_list = []
    for x in [url_all + i for i in file_first_link_list]:
        second_link = req_for_xpath(x, '/html/body/div[4]/div[1]/dl/dd/ul[1]/li/a/@href')[0]
        download_url = req_for_xpath(url_all + second_link, '/html/body/dl/dd/ul[2]/li[1]/a/@href')[0]
        url_list.append(download_url)
    name = req_for_xpath(url, '/html/body/div[5]/dl/dd/ul//li/a/img/@alt')
    file_dict = dict(zip(name, url_list))
    return file_dict


def get_the_format(url, page):
    page_link = req_for_xpath(url, '/html/body/div[5]/dl/dd/div[2]/ul/li[3]/a/@href')[0]
    return '/' + page_link[:-6] + str(page) + '.html'


def get_the_max_page(url):
    max_link = req_for_xpath(url, '/html/body/div[5]/dl/dd/div[2]/ul/li[16]/a/@href')[0]
    return max_link.split('_')[-1][:-5]


def main():
    choice = int(input())
    choice_link = url_all + get_choice_link(choice)
    for a in range(1, int(get_the_max_page(choice_link))):
        add_page = choice_link + get_the_format(choice_link, a)
        file_dict1 = file_download(add_page)
        with tqdm(total=len(file_dict1)) as bar:
            bar.set_description(f'第{a}页下载中')
            for (key, value) in file_dict1.items():
                req_file = get(value, headers=HEADERS).content
                with open(key + '.zip', 'wb') as f:
                    f.write(req_file)
                zip_file = zipfile.ZipFile(key + '.zip')
                for names in zip_file.namelist():
                    gbk_names = str(names).encode('cp437').decode('GBK')
                    if '.ppt' in names:
                        zip_file.extract(names)
                        rename(str(names), gbk_names)
                    else:
                        pass
                zip_file.close()
                remove(key + '.zip')
                bar.update(1)


if __name__ == '__main__':
    main()
