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


def get_choice_link(choose_title, all_choose_link):
    choice_link1 = all_choose_link[choose_title - 1]
    return choice_link1


def file_download(url):
    web = req_for_web(url)
    file_first_link_list = xpath(web, '/html/body/div[5]/dl/dd/ul//li/h2/a/@href')
    url_list = []
    for x in [url_all + i1 for i1 in file_first_link_list]:
        second_link = xpath(req_for_web(x), '/html/body/div[4]/div[1]/dl/dd/ul[1]/li/a/@href')[0]
        download_url = xpath(req_for_web(url_all + second_link), '/html/body/dl/dd/ul[2]/li[1]/a/@href')[0]
        url_list.append(download_url)
    return url_list


def format_link(web, page):
    page_link = xpath(web, '/html/body/div[5]/dl/dd/div[2]/ul/li[3]/a/@href')[0]
    return '/' + page_link[:-6] + str(page) + '.html'


def get_the_max_page(web):
    max_link = xpath(web, '/html/body/div[5]/dl/dd/div[2]/ul/li[16]/a/@href')[0]
    return max_link.split('_')[-1][:-5]


def auto_decode(name):
    gbkname = str(name).encode('cp437').decode('gbk')
    x = 1
    while True:
        if path.isfile(gbkname):
            gbkname = str(gbkname).split('.')[0] + f'{x}.' + str(gbkname).split('.')[1]
            x += 1
        else:
            break
    rename(name, gbkname)

# Get $choice from ListBox which binded <Double click>
def extract(choice, all_choose_link):
    choice_link = url_all + get_choice_link(choice, all_choose_link)
    web_for_page = req_for_web(choice_link)
    for a in range(1, int(get_the_max_page(web_for_page))):
        add_page = choice_link + format_link(web_for_page, a)
        file_list = file_download(add_page)
        with tqdm(total=len(file_list)) as bar:
            bar.set_description(f'第{a}页下载中')
            for link in file_list:
                req_file = get(link, headers=headers).content
                with open('log' + '.zip', 'wb') as f:
                    f.write(req_file)
                zip_file = zipfile.ZipFile('log' + '.zip')
                for names in zip_file.namelist():
                    if '.ppt' in names:
                        zip_file.extract(names)
                        auto_decode(names)
                zip_file.close()
                remove('log' + '.zip')
                bar.update(1)

# return essential value for display
# TODO:Need every artical titles and links
def getTitleLink(url, index):
    html = xpath(req_for_web(url), '/html/body/div[5]/dl/dd/ul/li')
    # print(html)
    # TODO: iter for too many times, need Improving
    # title = [re.findall('target="_blank">(.*?)</a></h2>', x)[0] for x in html]
    # img = [re.findall('<img src="(.*?)"', x)[0] for x in html]
    temp = [re.findall('<img src="(.*?)" alt="(.*?)">', x)[0] for x in html]
    title = [x[1] for x in temp]
    img_url = [x[0] for x in temp]
    print(img_url)
    return title, img_url[index]


def valueImport():
    req_site = req_for_web(url_all)
    all_choose_link = [url_all + x for x in xpath(req_site, '/html/body/div[5]/div//ul/li[2]/a/@href')]
    all_choose_title = xpath(req_site, '/html/body/div[5]/div//ul/li[2]/a/@title')
    return all_choose_link, all_choose_title


if __name__ == '__main__':
    # print(valueImport())
    getTitleLink('http://www.1ppt.com/moban/tags/121', 1)