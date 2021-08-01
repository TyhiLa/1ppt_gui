from requests import get
import zipfile
from os import path, rename, remove, mkdir, chdir
from tqdm import tqdm
import re
import io

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/90.0.4430.212 Safari/537.36'}
url_all = 'http://www.1ppt.com'

if not path.isdir('download'):
    mkdir('download')
chdir('download')


def req_for_web(url):
    req1 = get(url, headers=headers)
    req1.encoding = 'gbk'
    return req1.text


def get_re(req_in, pattern):
    re1 = re.compile(pattern)
    result = re1.findall(req_in)
    return result


req_site = req_for_web(url_all)
all_choose_link = get_re(req_site, 'href=\"(.*?[^article|office])\" title=\".*?\"[^>]')
all_choose_title = get_re(req_site, 'href=\".*?[^article|office]\" title=\"(.*?)\"[^>]')
all_choose_link.append('/moban')
all_choose_title.append('全部')
title = [str(all_choose_title.index(x) + 1) + '、' + x for x in all_choose_title]
for i in title:
    print(i, end=' ')
print('')
choice = int(input('请选择:'))


def get_choice_link(choose_title):
    choice_link1 = all_choose_link[choose_title - 1]
    return choice_link1


def file_download(url):
    web = req_for_web(url)
    file_first_link_list = get_re(web, 'a href=\"(.*?)\" .*</h2')
    url_list = []
    for x in [url_all + i1 for i1 in file_first_link_list]:
        second_link = get_re(req_for_web(x), 'a href=\'(.*?)\' target=')[0]
        download_url = get_re(req_for_web(url_all + second_link), 'a href=\"(.*?)\" target=')[0]
        url_list.append(download_url)
    return url_list


def format_link(web, page):
    page_link = get_re(web, 'href=\"(.*?)\">2')[0]
    return '/' + page_link[:-6] + str(page) + '.html'


def get_the_max_page(web):
    max_link = get_re(web, 'href=\'(.*?)\'>末页')[0]
    return max_link.split('_')[-1][:-5]


def auto_decode(name):
    gbk_name = str(name).encode('cp437').decode('gbk')
    x = 1
    while True:
        if path.isfile(gbk_name):
            gbk_name = str(gbk_name).split('.')[0] + f'{x}.' + str(gbk_name).split('.')[1]
            x += 1
        else:
            break
    rename(name, gbk_name)


choice_link = url_all + get_choice_link(choice)
web_for_page = req_for_web(choice_link)
for a in range(1, int(get_the_max_page(web_for_page))):
    add_page = choice_link + format_link(web_for_page, a)
    file_list = file_download(add_page)
    with tqdm(total=len(file_list)) as bar:
        bar.set_description(f'第{a}页下载中')
        for link in file_list:
            req_file = get(link, headers=headers).content
            data = io.BytesIO()
            data.write(req_file)
            zip_file = zipfile.ZipFile(data)
            for names in zip_file.namelist():
                if '.ppt' in names:
                    zip_file.extract(names)
                    auto_decode(names)
            zip_file.close()
            bar.update(1)
