#

API利用方法 | 国土交通DPF利用者API
https://www.mlit-data.jp/api_docs/reference/general/apiaccess.html

```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: [your api key]" \
    -d "{\"query\": \"{ search(term:\\\"橋梁\\\", first:0) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```

