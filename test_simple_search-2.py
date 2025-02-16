import requests

# エンドポイントとAPIキーを定義しておく
END_POINT = "https://www.mlit-data.jp/api/v1/"
# API_KEY = "please use your own key"
API_KEY = "OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW"

# 指定したキーワードと緯度経度の付近で最初にヒットした5件のデータ名（タイトル）の検索を行う。
# keyword = 検索キーワード
# lat = 十進数での緯度
# lon = 十進数での経度
# range = 度単位で検索する範囲を指定する。


def get_data(keyword, lat, lon, range):
    # GraphQLクエリー内容を作成
    top = lat + range
    bottom = lat - range
    left = lon - range
    right = lon + range
    graph_ql_query = """
    query {
      search(
        term: "%s",
        first: 0,
        size: 10,
        locationFilter: {
          rectangle: {
            topLeft: {
              lat: %f,
              lon: %f
            },
            bottomRight: {
              lat: %f,
              lon: %f
            }
          }
        }
      ) {
        totalNumber
        searchResults {
          title
          lat
          lon
        }
      }
    }
    """ % (keyword, top, left, bottom, right)

    # APIを呼び出して結果を準備する。
    result = []
    response_data = requests.post(
        END_POINT,
        headers={
            "Content-type": "application/json",
            "apikey": API_KEY,
        },
        json={"query": graph_ql_query}).json()
    print(response_data)

    for data in response_data["data"]["search"]["searchResults"]:
        result.append(data["title"])
        result.append(data["lat"])
        result.append(data["lon"])
    
    return result


# 検索の関数を呼び出して、結果を出力する。
#sampleresult = get_data("橋梁", 35.69394069179055, 139.75364318486396, 0.01)
#sampleresult = get_data("橋梁", 35.69394069179055, 139.75364318486396, 1.00)
#sampleresult = get_data("橋梁", 35.69394069179055, 139.75364318486396, 1.00)
#sampleresult = get_data("空港", 35.69394069179055, 139.75364318486396, 1.00)
#sampleresult = get_data("成田空港", 35.69394069179055, 139.75364318486396, 1.00)
# つくば市役所、36.08352908243843, 140.0763501705197
sampleresult = get_data("つくば", 36.08352908243843, 140.0763501705197, 1.00)

#print(sampleresult)

"""
(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_mlit-dpf-api$ python ./test_simple_search-2.py 
{'data': {'search': {'totalNumber': 6289, 'searchResults': [{'title': 'つくば2', 'lat': 36.05738, 'lon': 140.08835}, {'title': 'つくばウェルネスパーク', 'lat': 36.16161971668303, 'lon': 140.0710818576131}, {'title': 'つくばカピオ', 'lat': 36.079049084390206, 'lon': 140.11588147518532}, {'title': 'つくばウェルネスパーク', 'lat': 36.160575, 'lon': 140.07108}, {'title': 'つくばウェルネスパーク', 'lat': 36.161621, 'lon': 140.071074}, {'title': 'つくばウェルネスパーク', 'lat': 36.161226, 'lon': 140.068517}, {'title': 'つくばエクスプレス橋', 'lat': 35.82097, 'lon': 139.8734}, {'title': 'つくばエクスプレス橋', 'lat': 35.82094, 'lon': 139.87329}, {'title': 'つくば牛久31', 'lat': 35.99167, 'lon': 140.18077}, {'title': 'つくば牛久30', 'lat': 35.99194, 'lon': 140.18083}]}}}
['つくば2', 36.05738, 140.08835, 'つくばウェルネスパーク', 36.16161971668303, 140.0710818576131, 'つくばカピオ', 36.079049084390206, 140.11588147518532, 'つくばウェルネスパーク', 36.160575, 140.07108, 'つくばウェルネスパーク', 36.161621, 140.071074, 'つくばウェルネスパーク', 36.161226, 140.068517, 'つくばエクスプレス橋', 35.82097, 139.8734, 'つくばエクスプレス橋', 35.82094, 139.87329, 'つくば牛久31', 35.99167, 140.18077, 'つくば牛久30', 35.99194, 140.18083]
"""
