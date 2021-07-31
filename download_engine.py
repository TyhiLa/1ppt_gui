from requests import get
import zipfile
import re
from io import BytesIO
from os import path, rename


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


url_all = 'http://www.1ppt.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/90.0.4430.212 Safari/537.36'}
pattern_2 = 'a href=\'(.*?)\' target='
pattern_d = 'a href=\"(.*?)\" target='


def re_for_web(url, pattern):
    req1 = get(url, headers=headers)
    req1.encoding = 'gbk'
    re1 = re.compile(pattern)
    result = re1.findall(req1.text)
    return result


def get_download_link(url):
    second_link = re_for_web(url, pattern_2)
    download_link = re_for_web(url_all + second_link[0], pattern_d)
    return download_link[0]


def launch(first_url):
    download_link = get_download_link(first_url)
    data = BytesIO()
    data.write(get(download_link, headers=headers).content)
    zip_file = zipfile.ZipFile(data)
    for names in zip_file.namelist():
        if '.ppt' in names:
            zip_file.extract(names)
            auto_decode(names)
    zip_file.close()

if __name__ == "__main__":
    launch('http://www.1ppt.com/article/79809.html')
