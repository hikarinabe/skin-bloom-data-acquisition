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
    # company ... 110: "資生堂"
    company = mdl.NumberField() 
    company_str = mdl.TextField()
    # category ... 以下から選択
    category = mdl.NumberField()
    # raw_ingredients ... とりあえず取得した成分データをそのまま突っ込む
    raw_ingredients = mdl.TextField()
    # image_url ... とりあえずurlで入れておいて必要な時にstorageに入れる
    image_url = mdl.TextField()

return_category = {'クレンジング': 5, '洗顔料':4, '化粧水':1, '乳液':2,  'クリーム':6, 'ジェル・美容液':3, 'パック・マスク':8}
return_company = {'資生堂': 110}

def store_db(cd: cosmetic_data):
    # Use a service account
    fireo.connection(from_file="./key.json")
    cd.save()

def get_category(url):
    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    category_tag = sp.find("p",class_="p-product__left__list-title is-choice").next_sibling.next_sibling.find_all("li",class_="list-category__item")
    res = []
    for li in category_tag:
        category = li.get_text()
        if category in return_category.keys():
            a = li.find("a").get('href')
            res.append([f"https://maison.kose.co.jp{a}",return_category[category]])

    return res

def get_pager(url,id):
    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    a_tag = sp.find_all("a",class_="c-pager__button")
    res = [(f"https://maison.kose.co.jp{a.get('href')}",id) for a in a_tag[1:]]
    return res
def get_product_page(url,id):
    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    a_tag = sp.find_all("a",class_="c-product__thumb__img")
    res = [(f"https://maison.kose.co.jp{a.get('href')}",id) for a in a_tag]
    return res

#ジェルをget_infoで名前のときに判定。つめかえも,定期便

def main():
    
    args = sys.argv
    if len(args) != 2:
        print("python main.py <Link>")
        return
    url = args[1]
    # test = get_category(url)
    # test = get_product_page(url,0)
    # test = get_pager(url)
    # print(test)
    return 0

    category_url = get_category(url)    
    search_url = []
    for c_url , c_id in category_url[:1]:
        page_url = get_pager(c_url,c_id)
        for p_url, _id in page_url[:2]:
            product_url = get_product_page(p_url,_id)
            search_url+=product_url
    print(search_url[0])

main()