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
    
return_category = {'メイク落とし ・ クレンジング': 5, '洗顔 ・ 石鹸':4, '化粧水 ・ ローション':1, '保湿液':3, '乳液':2,  'クリーム ・ アイクリーム':6, '美容液':3, 'パック ・ マスク':8, '収れん化粧水':1, 'オールインワン':7}
return_company = {'資生堂': 110}

def store_db(cd: cosmetic_data):
    # Use a service account
    fireo.connection(from_file="./key.json")
    cd.save()
    

def get_product_category(url):
    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    a_tag = sp.find("ul",class_="child-category-list search-category-list").find_all("a")
    
    res = []
    for a in a_tag:
        if a.string in return_category.keys():
            res.append([f"https://www.shiseido.co.jp/{a.get('href')}",return_category[a.string]])
    return res

def get_puroduct_page(url,c_id):
    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    a_tag = sp.find_all('a',class_="link-to-detail-page")
    res = [[f"https://www.shiseido.co.jp/{a.get('href')}",c_id] for a in a_tag]
        
    return res
    


def get_product_info(url,c_id):
    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    
  
    #name
    h1_tag = str(sp.find('h1').string)
    if "詰め替え" in h1_tag or "つめかえ" in h1_tag or "レフィル" in h1_tag:
        return True
    
    
    #image_url
    image_url = sp.find('li', class_='item-list__item').find('img').get('src')
   
    #price
    price = sp.find('div',class_="product-price").span.get('content')
    
    #成分
    dt_tag = sp.find('div',class_="product-detail tabContent notShowMe").find_all("dt")
    for i in range(len(dt_tag)-1,-1,-1):
        if dt_tag[i].string=="成分":
            index = i
            break

    dd_tag = dt_tag[index].next_sibling.next_sibling
    dd_tag.div.decompose()
    table = str(dd_tag.get_text())
    table = table.strip()
  
    #classに追加
    cd = cosmetic_data()
    cd.company = 110
    cd.company_str = "資生堂"
    cd.name = h1_tag
    cd.price = int(price)
    cd.category = c_id
    cd.raw_ingredients = table
    cd.image_url = image_url

    store_db(cd)
    


def main():
    args = sys.argv
    if len(args) != 2:
        print("python main.py <Link>")
        return
    
    url = args[1]
    
    category_url = get_product_category(url)
    cnt = 0
    for c_url, c_id in category_url:
        product_url = get_puroduct_page(c_url,c_id)
        for p_url, id in product_url:
            get_product_info(p_url,id)
            cnt += 1
            if cnt%10==0:
                print(cnt,end=" ")
    

main()