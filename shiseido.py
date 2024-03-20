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
    
return_category = {'洗顔料': 4,  'メイク落とし': 5, '化粧水':1, '乳液':2, '美容液':3, 'エッセンス':3, 'クリーム':6, 'アイクリーム':6, 'オールインワン':7, 'マスク':8}
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
    






def main():
    args = sys.argv
    if len(args) != 2:
        print("python main.py <Link>")
        return
    
    url = args[1]
    category_url = get_product_category(url)
    res = get_puroduct_page(category_url[0][0],category_url[0][1])
    
    print(res[0])
    # return True

main()