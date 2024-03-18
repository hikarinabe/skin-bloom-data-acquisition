from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('./key.json')
initialize_app(cred)

'''DBから画像を持ってくる'''
# python3 store_storage.py > out.txt
def get_image_data():
    db = firestore.client()
    data = db.collection(u'cosmetic_data').get()

    result = []
    for d in data:
        result.append({"doc_id": d.id, "dict": d.to_dict()['image_url']})
    print(result)


'''imageをリサイズする'''
from PIL import Image

PATH =  'original/'

def resize_image(filename):

    img = Image.open(filename)
    img = img.convert('RGB')

    img_resize = img.resize((512, 512))
    filename = filename[11:]
    filename = filename.rstrip('.jpg')
    filename = filename.rstrip('.jpeg')
    print(filename)
    img_resize.save(f'./dist/{filename}.jpg')

# filename =  './original/udCALlOaUmyzoreaRwU1.jpg'
# resize_image(filename)


'''URLから画像をダウンロードする'''
import urllib.request


def get_original_image():
    out = [{'doc_id': '3tBBk1XvFmf7wtAswDXO', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/b42000a9390bc61c203c86892371dc24.jpg'}, {'doc_id': '475aLMUgaF0DdwH8gT83', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/06/4e1fe7dc5df1eba0791ee1fa2452b39c.jpg'}, {'doc_id': '5ZrMbxNzfwOZMtMvnlwe', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/01/e05220e6a9a9ed318c81b6b0b1384875.jpg'}, {'doc_id': '7MLO8LrBYv5prBblQEMR', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/07/ba7d71f3eb94643070c03d83f62a94a9.jpg'}, {'doc_id': 'B19lNbPdSUwfNzwqZipd', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/227c93b0c4061761d979f7d61653b165.png'}, {'doc_id': 'Bqxtijc0Cm3O2RtUWqk5', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2022/07/065d782369fe68920138d86aebfcf317.png'}, {'doc_id': 'FUlSuZci78XEMUkrzylS', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2022/07/55b2c89d2d7050b7e3a349b68ef87f5b.png'}, {'doc_id': 'FvqSiA54bzdDVyzcEdoN', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2024/01/bc763117d86e4f6b7021502a646ef756.jpg'}, {'doc_id': 'Fyl5oRERCsxRV4irXefk', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2022/07/11673403e4d2bd1cfb40a6171cf12629.png'}, {'doc_id': 'GTRE11zFBBUiokMQXuRy', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/cec2d6bd3db19ac36a74918ee8147f16.jpg'}, {'doc_id': 'HQH2U8CwOrl7lQlGvzvv', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/1734649de07d3290d8bcc067b19030e3.jpg'}, {'doc_id': 'HzLJwLofcGNzPqKazMw3', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2022/07/91756b0ccabcb7410114f78a2bba1201.png'}, {'doc_id': 'MHdD2jbVLBu2Inu3IvkK', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/af623ba58c6f2776bc704cfd118488e0.jpg'}, {'doc_id': 'MacMYSm7bDJtSfERtGrq', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/0b3cf0478944cbb259b5338ededc3a47.jpg'}, {'doc_id': 'NwCyFwB7IOkRh3cCjS8T', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/07/a02a1a34cf9d6a6b594f28dfaa5dafa7.jpg'}, {'doc_id': 'OFNDc4eX7LJ3lCVGEudN', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/07/79aa34b555eb9071cde63af234174214.jpg'}, {'doc_id': 'PRlv62IXLLyWSwapJZn4', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/93b756e6fca0f420ad5ec1ee00b5a833.jpg'}, {'doc_id': 'R6sKXDiilTE3eUhZnJki', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/602da8d405a530f92f0c9e6ea996cd5b.jpg'}, {'doc_id': 'RdrCGTZfCQTwyxmy8uKv', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/06/70bb474fd347b7e0ffb905e63e601595.jpg'}, {'doc_id': 'YaU1NWWBRTpvEYs8qtof', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2022/07/d9c88f221a8685e9cdb252049b994722.png'}, {'doc_id': 'Yy1rAMNsh2qR6TvDevJ1', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/f91cb367149caee8b7ff60e897ef407d.png'}, {'doc_id': 'ZFV6vVuHxKehB8T7LD4p', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/5f39f0ad0e20f068dfb1c4678837ebe2.jpg'}, {'doc_id': 'a7GtB6nZGwT91cyaZY62', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/6fe8cf3b1701486b6e2fe9b3fcc57cc5-2.jpg'}, {'doc_id': 'b2uUWvgXIekI9oAor9HJ', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/12/f33f9720d774fa59e38cb3415a3fbcb8.jpg'}, {'doc_id': 'd2WWoaSAyGZpXh1uR8tO', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/75c175d7578ec046b1daa82b02943935.jpg'}, {'doc_id': 'e6doftiHpjOLsjkfls9T', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/0203/01/000d88e6b23be1af57483923f031753f.jpg'}, {'doc_id': 'f4wzzfmtMpeLFoVt3BJ7', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/10eacde3af8805e70e9bb15161161ca0.jpg'}, {'doc_id': 'hGXOdAEnREKrJg6nzw6J', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/ca91599de7a573bf25f30fcdf7ade340.jpg'}, {'doc_id': 'jr4VWVP0GtHgFUp8FCUw', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/15d9ee3feb96e1c8729fbebc1a572c9c.jpg'}, {'doc_id': 'lTbPTlmMto4wu5NaaUS6', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/5350ace4f6c26f49f129872676dd1c8f.png'}, {'doc_id': 'mxE1wyRoCSceLQRY8N3O', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/92021884d738433636476a3226410020.jpg'}, {'doc_id': 'nZrEBHn7ovzA2y4rccN9', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/92021884d738433636476a3226410020.jpg'}, {'doc_id': 'p11IvKl3z8KPOuayxFvX', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/5e5fa222219dc1ebee23ef5343ceb685-1.jpg'}, {'doc_id': 'qbwq61c7v9WPHR0Jz1I7', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/07/4b636cd9be650facfb59b67f5586dca5.jpg'}, {'doc_id': 'tKWDgFGhIE7bCZU6FNn7', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/197df83a0d455cae072c8ec8301a0f0e-1.jpg'}, {'doc_id': 'udCALlOaUmyzoreaRwU1', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/d92a4abbcd3c9beffc4a7d9a06c2a223.png'}, {'doc_id': 'vqnewEowZ6wG78j4wxUo', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/e5ccb0f694d34d313fca7b73d10683db.png'}, {'doc_id': 'xuk9Jhgval5LXOjlCsU3', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/64ecbad8e7841f6f1e225dc10ab01c58.png'}, {'doc_id': 'yj5bKj0Eo4OrjVZSznFD', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2023/05/6f76420f5bfdc86ab069c73cc76c4ce7-2.jpg'}, {'doc_id': 'ysgQrYQQuRtsZaOVCPJT', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/d8dade8805235ec6f7a224f451cfbfec.png'}, {'doc_id': 'yxrKEWjuZGBRUAv3hRd1', 'dict': 'https://www.chifure.co.jp/wp/wp-content/uploads/2018/09/0e94aed08695be4c2bfc33566078fa26.png'}]
    
    for one_item in out:
        urllib.request.urlretrieve(one_item['dict'], PATH+one_item['doc_id']+'.jpg')

# get_original_image()
        
import glob

'''ダウンロードした画像をリサイズする'''
def resize_images():
    img_list = glob.glob("./original/*")
    # print(img_list)
    for path in img_list:
        resize_image(path)

resize_images()

