# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


def get_detail_url_list(url):
    """
    获取每页的详细url列表
    """
    r = requests.get(url)
    content = BeautifulSoup(r.content)
    list_body = content.find(attrs={"class": "browseListBody"})
    detail_soup_list = list_body.find_all(attrs={"compid": "uniprof"})
    assert len(detail_soup_list) == 15
    return [i.find(attrs={"itemprop": "name"}).get("href") for i in detail_soup_list]


def get_detail_info(detail_url):
    """
    获取每条详细信息
    """
    r = requests.get(detail_url)
    content = BeautifulSoup(r.content)
    phone_info = content.find(attrs={"compid" :"Profile_Phone"}).find_all("a")
    phone = phone_info[0].get("phone")
    website = phone_info[1].get("href")
    detail_info = content.find(attrs={"class": "profile-about-right"}).find_all(attrs={"class": "info-list-label"})
    detail_data = [i.find(attrs={"class": "info-list-text"}).text.replace("\n", "") for i in detail_info]
    return [phone, website] + detail_data

def write_to_file(file_name, *args):
    """
    数据写入到记事本
    """
    with open(file_name, "a") as f:
        f.write(','.join(args))
        f.write("\r\n")


def main():
    base_url = 'https://www.houzz.com/professionals/kitchen-and-bath-remodelers/c/United-States/sortReviews/p/{0}'
    for page in range(0, 62816/15+1):
    # for page in range(0, 2):
        """
        0为起始页，总页码为62816/15
        """
        url_list = get_detail_url_list(base_url.format(page*15))
        file_name = 'houzz_data.txt'
        for url in url_list:
            data = get_detail_info(url)
            write_to_file(file_name, *data)
    
if __name__ == '__main__':
    main()
