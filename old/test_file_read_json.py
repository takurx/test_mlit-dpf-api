# test json file read 
import json

#Windowsで標準出力をUTF8にする
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file = open('sample_responce_test_simple_search-3.json', 'r', encoding='utf-8')

#data = file.read()
data = json.load(file)
print(data)
# {'data': {'search': {'totalNumber': 77, 'searchResults': [{'title': '成田市古込１−１成田国際空港第２旅客ターミナルビル地下１階 日本医科大学成田国際空港クリニック', 'lat': 35.77365489125021, 'lon': 140.38844830973645}, {'title': '成田国際空港警察署', 'lat': 35.78104658, 'lon': 140.362453}, {'title': '成田国際空港', 'lat': 35.761558, 'lon': 140.387063}, {'title': '成田2', 'lat': 35.78361, 'lon': 140.35889}, {'title': '駒井野橋', 'lat': 35.78529, 'lon': 140.3714}]}}}

print(type(data))
# <class 'dict'>

#data = json.dump(json_data, file)

file.close()

print(type(data))
# <class 'dict'>

#json_data = json.dumps(data, indent=4)
json_data = json.dumps(data, indent=4, ensure_ascii=False)
#print(json_data)
#print(json_data, encoding='utf-8')
print(type(json_data))
# <class 'str'>

json_dict = json.loads(json_data)
#json_dict = json.loads(json_data, encoding="utf-8")
#json_dict = json.dump(json_data, )
#print(json_dict)

#print(str(json_data["data"]["search"]))
#print(json_data["data"]["search"])
#print(json_dict[0]) #{
#print(json_dict.get("data"))
#test = json_dict.get('data')
#test = json_data.get('data')
#test = json_dict.get('data', 'not found')
#print(test)

print(type(json_dict)) # <class 'str'>
# <class 'dict'>

for key in json_dict.keys():
    #print(key)
    # data
    #print(json_dict[key])
    # {'search': {'totalNumber': 77, 'searchResults': [{'title': '成田市古込１−１成田国際空港第２旅客ターミナルビル地下１階 日本医科大学成田国際空港クリニック', 'lat': 35.77365489125021, 'lon': 140.38844830973645}, {'title': '成田国際空港警察署', 'lat': 35.78104658, 'lon': 140.362453}, {'title': '成田国際空港', 'lat': 35.761558, 'lon': 140.387063}, {'title': '成田2', 'lat': 35.78361, 'lon': 140.35889}, {'title': '駒井野橋', 'lat': 35.78529, 'lon': 140.3714}]}}
    #print(json_dict[key]["search"])
    # {'totalNumber': 77, 'searchResults': [{'title': '成田市古込１−１成田国際空港第２旅客ターミナルビル地下１階 日本医科大学成田国際空港クリニック', 'lat': 35.77365489125021, 'lon': 140.38844830973645}, {'title': '成田国際空港警察署', 'lat': 35.78104658, 'lon': 140.362453}, {'title': '成田国際空港', 'lat': 35.761558, 'lon': 140.387063}, {'title': '成田2', 'lat': 35.78361, 'lon': 140.35889}, {'title': '駒井野橋', 'lat': 35.78529, 'lon': 140.3714}]}
    print(json_dict[key]["search"]["searchResults"])
    # [{'title': '成田市古込１−１成田国際空港第２旅客ターミナルビル地下１階 日本医科大学成田国際空港クリニック', 'lat': 35.77365489125021, 'lon': 140.38844830973645}, {'title': '成田国際空港警察署', 'lat': 35.78104658, 'lon': 140.362453}, {'title': '成田国際空港', 'lat': 35.761558, 'lon': 140.387063}, {'title': '成田2', 'lat': 35.78361, 'lon': 140.35889}, {'title': '駒井野橋', 'lat': 35.78529, 'lon': 140.3714}]
    #print(json_dict[key]["search"]["searchResults"]["title"])
    # TypeError: list indices must be integers or slices, not str

    #print(key, values)
    #print(json_dict[key])
    #print(type(json_dict[key]))
    #print('---------------------')
    #print(json_dict[key]["search"])
    #print(json_dict[key]["search"]["edges"])
    #print(json_dict[key]["search"]["edges"][0])
    #print(json_dict[key]["search"]["edges"][0]["node"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"])
    #print(json_dict[key]["search"]["edges"][0]["node"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"]["name"])
    #print(json
    # AttributeError: 'str' object has no attribute 'keys'

print(json_dict["data"]["search"]["searchResults"][0])
# {'title': '成田市古込１−１成田国際空港第２旅客ターミナルビル地下１階 日本医科大学成田国際空港クリニック', 'lat': 35.77365489125021, 'lon': 140.38844830973645}
print(json_dict["data"]["search"]["searchResults"][0]["title"])
# 成田市古込１−１成田国際空港第２旅客ターミナルビル地下１階 日本医科大学成田国際空港クリニック
print(json_dict["data"]["search"]["searchResults"][0]["lat"])
# 35.77365489125021
print(json_dict["data"]["search"]["searchResults"][0]["lon"])
# 140.38844830973645

print("a" + ", " + "b")
# a, b

print(json_dict["data"]["search"]["searchResults"][0]["title"] + ", " 
    + str(json_dict["data"]["search"]["searchResults"][0]["lat"]) + ", " 
    + str(json_dict["data"]["search"]["searchResults"][0]["lon"]))
# 成田市古込１−１成田国際空港第２旅客ターミナルビル地下１階 日本医科大学成田国際空港クリニック, 35.77365489125021, 140.38844830973645

# for key in json_dict["data"]["search"]["searchResults"].get("title", "not found"):
    # print(key)
    # AttributeError: 'list' object has no attribute 'get'

