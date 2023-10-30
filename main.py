# beautifulsoupでスクレイピングする

import requests
from bs4 import BeautifulSoup
import re


def fetch_ingredients(url_list):
    ingredient_dict = {}
    for url in url_list:
        print(url)
        # スクレイピング対象のURL
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        serving_num = soup.find(class_="servings").string
        # 食材一覧を取得する
        ingredients = [ingredient.get_text() for ingredient in soup.find_all(class_="ingredient-list-item")]
        for ingredient in ingredients:
            name = re.search(r'\s*([^\n]+)', ingredient)
            amount = re.search(r'(\S*\d*)$', ingredient)
            if name.group(1) in ingredient_dict:
                ingredient_dict[name.group(1)] = calc_weight(ingredient_dict[name.group(1)], amount.group(1))
            else: 
                ingredient_dict[name.group(1).replace("(A)", '')] = amount.group(1)
    print(ingredient_dict)

def calc_weight(weight_1, weight_2):
    weight_1 = int(re.search(r'\d+', weight_1).group())
    weight_2 = int(re.search(r'\d+', weight_2).group())
    return str(weight_1 + weight_2) + "g"

if __name__ == '__main__':
    url_list = ["https://www.kurashiru.com/recipes/b083f7b3-635f-405a-a5e2-4db352efda03", "https://www.kurashiru.com/recipes/b0dcfbc4-c8b3-4be3-985b-40df45275191"]
    fetch_ingredients(url_list)