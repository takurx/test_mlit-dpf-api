# Pythonでdict型（辞書型）のデータをインデント付きの見やすいJSONに変換してprintする #Python3 - Qiita
# https://qiita.com/yutami/items/ceb0ee84a2ab0d196569

import json

# JSONに変換して出力したいdictをここに定義
target_dict = {'food': {'fruits': {'red_fruits': ['apple', 'strawberry', 'cherry'], 'yellow_fruits': ['banana', 'pineapple', 'lemon'], 'green_fruits': ['kiwi', 'grape', 'green apple']}, 'vegetables': {'leafy_greens': ['spinach', 'lettuce', 'kale'], 'root_vegetables': ['potato', 'carrot', 'radish'], 'nightshades': ['tomato', 'cucumber', 'bell pepper']}}, 'animals': {'mammals': {'carnivores': ['lion', 'tiger', 'bear'], 'rodents': ['squirrel', 'guinea pig', 'beaver'], 'ungulates': ['horse', 'cow', 'deer']}, 'birds': {'birds_of_prey': ['eagle', 'hawk', 'vulture'], 'waterfowl': ['duck', 'pelican', 'seagull'], 'songbirds': ['nightingale', 'mockingbird', 'canary']}, 'reptiles': {'snakes': ['anaconda', 'boa constrictor', 'cobra'], 'turtles': ['red-eared slider', 'box turtle', 'sea turtle'], 'lizards': ['iguana', 'gecko', 'chameleon']}}, 'space': {'constellations': {'northern_hemisphere': ['Ursa Major', 'Cassiopeia', 'Perseus'], 'southern_hemisphere': ['Centaurus', 'Phoenix', 'Southern Cross']}, 'planets': {'inner_planets': ['Mercury', 'Venus', 'Earth', 'Mars'], 'gas_giants': ['Jupiter', 'Saturn'], 'ice_giants': ['Uranus', 'Neptune'], 'dwarf_planets': ['Pluto', 'Eris']}, 'astronauts': {'NASA': ['Neil Armstrong', 'Buzz Aldrin', 'Sally Ride'], 'Roscosmos': ['Yuri Gagarin', 'Valentina Tereshkova'], 'ESA': ['Thomas Pesquet', 'Samantha Cristoforetti']}}}

# インデント4のJSONデータに変換
json_data = json.dumps(target_dict, indent=4)
#print(json_data)

# print(json_data['food']['fruits']['red_fruits'][0])
# TypeError: string indices must be integers, not 'str'

json_dict = json.loads(json_data)

"""
for key in json_dict.keys():
    print(key)
    #print(json_data[key])
    print('---------------------')
"""

"""
food
---------------------
animals
---------------------
space
---------------------
"""

# AttributeError: 'list' object has no attribute 'keys'
# AttributeError: 'list' object has no attribute 'values'
# AttributeError: 'list' object has no attribute 'items'
print(type(json_dict))　# <class 'dict'>
for key, value in json_dict["food"]["fruits"].items():
    print(key, value)
    #print(json_data[key])
    print('---------------------')

"""
red_fruits ['apple', 'strawberry', 'cherry']
---------------------
yellow_fruits ['banana', 'pineapple', 'lemon']
---------------------
green_fruits ['kiwi', 'grape', 'green apple']
---------------------
"""

# 【Python 入門】辞書 (dictionary) を for 文でループ処理する方法をわかりやすく解説！ | キカガクブログ
#https://www.kikagaku.co.jp/kikagaku-blog/python-for-dictionary/

staff = {'太郎': '24歳', '花子': '28歳', '次郎': '18歳'}
for value in staff.values():
    print(value)



