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

return_category = {'skinfreshener': 1, 'skinlotion': 1, 'milkylotion': 2,'milky_lotion': 2 ,'essence': 3, 'facewash': 4, 'cleansing': 5, 'moisturecream': 6, 'allinone': 7, 'specialcare': 8}
return_company = {'資生堂': 110}

def store_db(cd: cosmetic_data):
    # Use a service account
    fireo.connection(from_file="./key.json")
    cd.save()


def main():
    args = sys.argv
    if len(args) != 2:
        print("python main.py <Link>")
        return
    url = args[1]

    rs = requests.get(url)
    sp = BeautifulSoup(rs.text.encode(rs.encoding),'html.parser')
    div_tag = sp.find('div', class_="product_detailbox01").select('img')
    
    cd = cosmetic_data()
    cd.image_url = args[1] + div_tag[0].get("src")
    print(cd.image_url)
    # image = sp.find_all('img')
    cd.company = 130
    cd.company_str = "ロート製薬"
    

    answer = input('Do you want proceed?: [y/N] ')
    if answer == 'y':
        store_db(cd)

main()

"""
$ python chifure.py <URL>
"""
