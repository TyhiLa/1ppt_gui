from requests import get
import zipfile
import re
import io

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/90.0.4430.212 Safari/537.36'}


def req_for_web(url):
    req1 = get(url, headers=headers)
    req1.encoding = 'gbk'
    return req1
