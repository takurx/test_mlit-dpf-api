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

    return result


# 検索の関数を呼び出して、結果を出力する。
#sampleresult = get_data("橋梁", 35.69394069179055, 139.75364318486396, 0.01)
#sampleresult = get_data("橋梁", 35.69394069179055, 139.75364318486396, 1.00)
#sampleresult = get_data("橋梁", 35.69394069179055, 139.75364318486396, 1.00)
#sampleresult = get_data("空港", 35.69394069179055, 139.75364318486396, 1.00)
#sampleresult = get_data("成田空港", 35.69394069179055, 139.75364318486396, 1.00)
# つくば市役所、36.08352908243843, 140.0763501705197
sampleresult = get_data("つくば", 36.08352908243843, 140.0763501705197, 1.00)

print(sampleresult)

#(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_mlit-dpf-api$ python ./test_simple_search-1.py 
#{'data': {'search': {'totalNumber': 6289, 'searchResults': [{'title': 'つくば2'}, {'title': 'つくばウェルネスパーク'}, {'title': 'つくばカピオ'}, {'title': 'つくばウェルネスパーク'}, {'title': 'つくばウェルネスパーク'}, {'title': 'つくばウェルネスパーク'}, {'title': 'つくばエクスプレス橋'}, {'title': 'つくばエクスプレス橋'}, {'title': 'つくば牛久31'}, {'title': 'つくば牛久30'}]}}}
#['つくば2', 'つくばウェルネスパーク', 'つくばカピオ', 'つくばウェルネスパーク', 'つくばウェルネスパーク', 'つくばウェルネスパーク', 'つくばエクスプレス橋', 'つくばエクスプレス橋', 'つくば牛久31', 'つくば牛久30']