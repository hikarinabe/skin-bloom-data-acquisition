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





def main():
    return 0

main()