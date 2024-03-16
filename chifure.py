import re
import sys

import bs4
import fireo
import requests
from bs4 import BeautifulSoup
from fireo import models as mdl


class cosmetic_data(mdl.Model):
    # name ... 商品名
    name = mdl.TextField()
    # price ... 価格
    price = mdl.NumberField()
    # company ... 120: "ちふれ"
    company = mdl.NumberField() 
    # category ... 以下から選択
    category = mdl.NumberField()
    # raw_ingredients ... とりあえず取得した成分データをそのまま突っ込む
    raw_ingredients = mdl.TextField()
    # image_url ... とりあえずurlで入れておいて必要な時にstorageに入れる
    image_url = mdl.TextField()


def store_db(cd: cosmetic_data):
    # Use a service account
    fireo.connection(from_file="./key.json")
    cd.save()
    

def extract_price(text: str):
    extract_list = []
    for t in text:
        if t == '円':
            return int("".join(extract_list))
        try:
            int(t)
            extract_list.append(t)
        except:
            continue
    return int("".join(extract_list))
# text = '価格：880円（税込）詰替用 770円（税込）'
# print(extract_price(text))

def extract_table(lst: list[bs4.element.Tag]):
    table = []
    for l in lst:
        raw_text = l.text
        # 変なマークを除外
        if raw_text.find('〃') >= 0:
            continue
        # 分量も今のところ除外
        if raw_text.find('%') >= 0:
            continue
        if raw_text.find('％') >= 0:
            continue
        if raw_text.find('適量') >= 0:
            continue
        table.append(raw_text)
    return ",".join(table)
# test_list = ['<td>ＢＧ</td>', '<td>5.00%</td>', '<td>〃</td>', '<td>グリセリン</td>', '<td>4.00%</td>']
# print(extract_table(test_list))

return_category = {'skinfreshener': 1, 'skinlotion': 1, 'milkylotion': 2,'milky_lotion': 2 ,'essence': 3, 'facewash': 4, 'cleansing': 5, 'moisturecream': 6, 'allinone': 7, 'specialcare': 8}
return_company = {'ちふれ': 120}

def parse_url(text: str):
    link_list = text.split('/')
    return {
        'category': link_list[4],
        'id': link_list[5]
    }
# parse_url("https://www.chifure.co.jp/products/cleansing/2139")

def main():
    args = sys.argv
    if len(args) != 2:
        print("python main.py <Link>")
        return
    url = args[1]
    info = parse_url(url)
    print('category:', info['category'])
    print('id:', info['id'])

    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')

    cd = cosmetic_data()

    # 商品名
    row0 = sp.select('h1')
    cd.name = row0[0].text
    print("商品名:", cd.name)

    # 価格
    price = sp.find('p', class_="item__price")
    cd.price = extract_price(price.text[price.text.find('価格'):])
    print("値段", cd.price)

     # company ... 120: "ちふれ"
    cd.company = return_company['ちふれ']
    print("会社:", cd.company)

    # category ... 以下から選択
    cd.category = return_category[info['category']]
    print("カテゴリー:", cd.category)

    # 成分
    table = sp.find('div', class_="component__content").select('table')
    table = table[0].select('td')
    table.pop(0) # 最初の成分表を除外
    cd.raw_ingredients = extract_table(table)
    print("テーブル", cd.raw_ingredients)

    # image URL
    image_comp = sp.find('figure', class_="item__thumb").select('img')
    cd.image_url = image_comp[0].get("data-src")
    print(cd.image_url)

    answer = input('Do you want proceed?: [y/N] ')
    if answer == 'y':
        store_db(cd)

main()

"""
$ python chifure.py <URL>
"""
