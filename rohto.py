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
return_company = {'資生堂': 110}

def store_db(cd: cosmetic_data):
    # Use a service account
    fireo.connection(from_file="./key.json")
    cd.save()

    
def get_product_category(url,num):
    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    nav_tag = sp.find(id=f"lnav-lv3-item{num}")
    return f"https://jp.rohto.com{nav_tag.a.get('href')}"
        
def get_product_page(url):
    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    a_tag = sp.find_all('a',class_="prodcard-wrap")
    res = []
    for href in a_tag:
        category = href.find('p',class_="prodcard-categ").string
        if category in return_category.keys():
            category_id = return_category[category]
            res.append([f"https://jp.rohto.com{href.get('href')}",category_id])
    return res
 
def get_ingredients(url):
    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    p_tag = sp.find("p",class_="textLeft01")
    res = p_tag.get_text()
        
    return res
       
def get_product_info(url,id):
    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    
    #image_url
    div_tag= sp.find('div', class_="product_detailbox01").select('img')
    
    #name
    h1_tag = sp.find('h1').string
    
    #price
    td_tag = sp.find('td', class_="tbl_s_pric").string
    
    #raw_ingredients
    a_tag = str(sp.find('a', class_="txtLinks01 btn_seibun"))
    tmp = a_tag.split(" ")
    key = re.search(r'\d+',tmp[4]).group()
    ingredients = get_ingredients(f"https://jp.rohto.com/seib/seib/?kw={key}")
    
    #classに追加
    cd = cosmetic_data()
    cd.company = 130
    cd.company_str = "ロート製薬"
    cd.name = str(h1_tag)
    cd.price = None
    cd.category = id
    cd.raw_ingredients = ingredients
    cd.image_url = f"https://jp.rohto.com{div_tag[0].get('src')}"
    
    
    store_db(cd)
    # return True
       
def main():
    args = sys.argv
    if len(args) != 2:
        print("python main.py <Link>")
        return
    url = args[1]
    cnt=1
    for num in range(17,24):
        category_url = get_product_category(url,num)
        producut_url = get_product_page(category_url)
        for p_url,id in producut_url:
            get_product_info(p_url,id)
            cnt+=1
            if cnt%10==0:
                print(cnt,end=" ")
            
    print()
    print("Done")
    
    # answer = input('Do you want proceed?: [y/N] ')
    # if answer == 'y':
    #     store_db(cd) #データベースに追加

main()

"""
$ python chifure.py <URL>
"""
