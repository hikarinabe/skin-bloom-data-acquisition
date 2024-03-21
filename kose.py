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
return_company = {'KOSÉ': 140}

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
    
    res = [(f"https://maison.kose.co.jp{a.get('href')}",id,f"https://maison.kose.co.jp{a.img.get('src')}") for a in a_tag]
    return res


def get_product_info(url,id,img_url):

    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    
    #name
    product_name = sp.find("div",class_="p-product-detail__item__title").string
    if ("セット" in product_name and "リセット" not in product_name)or (id==3 and "ジェル" in product_name)or "キット"in product_name or "つめかえ" in product_name or "定期便" in product_name or (url=="https://maison.kose.co.jp/site/cosmedecorte/g/gJQDT/"): #ジェルをget_infoで名前のときに判定。つめかえも,定期便
        return 0

    #price
    price_str = sp.find("div",class_="p-product-detail__item__price").span.string
    price_str = price_str.replace('円','')
    price_str = price_str.replace(',','')

    #成分
    if "drphil" in url:
        detail_tag = sp.find("section",class_="c-drphil-detail__ingredients")
        if detail_tag == None:
            detail_tag = sp.find("p",class_="allingred__text")
            if detail_tag ==None:
                detail_tag = sp.find("div",class_="icu-v-performance-detail")#.find_all("dd")
                if detail_tag == None:
                    detail_tag = sp.find_all("dd",class_="ingredlist__item")
                else:
                    detail_tag = detail_tag.find_all("dd")
                detail_txt = ""
                for t in detail_tag:
                    detail_txt+=t.string
            else:
                detail_txt = detail_tag.get_text()
        else:
            detail_txt = detail_tag.find("div",class_="c-drphil-detail__text").get_text()
    else:
        detail_txt = sp.find("div",class_="p-product-detail__blend").find("div",class_="p-product-detail__text").get_text()

    
    #image_url
    img_tag = sp.find("div",class_="p-product-detail__slider__nav")#.find("img")
    if img_tag == None:
        image = img_url
    else:
        img_tag = img_tag.find("img")
        image = f"https://maison.kose.co.jp{img_tag.get('src')}"


    cd = cosmetic_data()
    cd.company = 140
    cd.company_str = "KOSÉ"
    cd.name = str(product_name)
    cd.price = int(price_str)
    cd.category = id
    cd.raw_ingredients = str(detail_txt.strip().replace('\n',''))
    cd.image_url = image

    store_db(cd)
    return 0

def main():
    
    args = sys.argv
    if len(args) != 2:
        print("python main.py <Link>")
        return
    url = args[1]

    category_url = get_category(url)    
    search_url = []
    for c_url , c_id in category_url:
        page_url = get_pager(c_url,c_id)
        for p_url, _id in page_url:
            product_url = get_product_page(p_url,_id)
            search_url+=product_url
    
    for s_url , c_id,img_url in search_url:
        get_product_info(s_url,c_id,img_url)
    print("End")


main()