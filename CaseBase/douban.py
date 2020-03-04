import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import csv
import time


def logs(func):
    def wrapper(*args):
        print(f'{func.__name__}执行开始：{time.time()}')
        func(url)
        print(f'{func.__name__}执行结束：{time.time()}')

    return wrapper


@logs
def get_url_name(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    headers = {'user-agent': user_agent}
    response = requests.get(url, headers=headers)
    bs_info = bs(response.text, 'html.parser')

    with open('../Data/douban.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for tags in bs_info.find_all('div', attrs={'class': 'pl2'}):
            for tag in tags.find_all('a'):
                row = [tag.get('title')]
                bookInfo = requests.get(url=tag.get('href'), headers=headers)
                bs_info_bk = bs(bookInfo.text, 'html.parser')
                row.append(bs_info_bk.find('strong').text)
                for rating_pers in bs_info_bk.find_all('span', attrs={'class': 'rating_per'}):
                    row.append(rating_pers.text)
                for shorts in bs_info_bk.find_all('p', attrs={'class': 'comment-content'}):
                    for short in shorts.find_all('span', attrs={'class', 'short'}):
                        print(short)
                        row.append(str(short.text).replace(',', '，'))
                # 写入数据
                writer.writerow(row)


if __name__ == '__main__':
    urls = tuple(f'https://book.douban.com/top250?start={page * 25}&filter=' for page in range(10))
    # 写入文件头部
    with open('../Data/douban.csv', 'w', newline='', encoding='utf-8') as f:
        title = ['title', 'rating_num', 'stars5', 'stars4', 'stars3', 'stars2', 'stars1', 'short1', 'short2'
            , 'short3', 'short4', 'short5', 'short6', 'short7', 'short8', 'short9', 'short10']
        writer = csv.writer(f)
        writer.writerow(title)
    # 获取数据
    for url in urls:
        get_url_name(url)
        sleep(5)
