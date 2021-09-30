import pandas
from bs4 import BeautifulSoup
import requests


def str2dict(s, s1=';', s2='='):
    '''
    将字符串转换为字典

    s：待转换字符串，s1：键值对之间的分隔符，s2：键和值的连接符
    '''
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res


if __name__ == '__main__':
    url = "https://movie.douban.com/top250?start="
    header_str = '''
Please replace this string with your own headers.
'''
    headers = str2dict(header_str, '\n', ': ')

    movie_list = []
    for i in range(10):
        r = requests.get(url+str(i*25), headers=headers,
                         timeout=10)
        print(r.text)
        soup = BeautifulSoup(r.text, 'lxml')
        div_list = soup.find_all('div', class_='info')
        for each in div_list:
            title = each.find('div', class_='hd').a.span.text.strip()
            print(title)
            year = each.find('div', class_='bd').p.text.split('\n')[
                2].strip().split('/')[0]
            country = each.find('div', class_='bd').p.text.split('\n')[
                2].strip().split('/')[-2]
            label = each.find('div', class_='bd').p.text.split('\n')[
                2].strip().split('/')[-1]
            rating = each.find('span', class_='rating_num').text.strip()
            movie_list.append([title, year, country, label, rating])

    df = pandas.DataFrame(movie_list, columns=[
                          '电影名称', '年份', '国家', '标签', '评分'], index=None)
    df.to_csv("douban250.csv")
