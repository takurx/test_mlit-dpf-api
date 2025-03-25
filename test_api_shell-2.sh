curl -X POST -H "Content-Type: application/json" \
    -H "apikey: OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW" \
    -d "{\"query\": \"{ search(term:\\\"つくば\\\", attributeFilter:[{attributeName:\\\"全国道路施設点検データベース\\\"}], first:5) { totalNumber } }\" }" \
    -i http://localhost:8000/dpf_mock/

<< COMMENTOUT
    http://localhost:8001/services/dpf_service/

    -i https://www.mlit-data.jp/api/v1/

    -d "{\"query\": \"{ search(term:\\\"つくば\\\", attributeFilter:\\\"全国道路施設点検データベース\\\", first:5) { totalNumber } }\" }" \

{"data":{"search":{"totalNumber":10000}}}(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_mlit-dpf-api$ ./test_api_shell-1.sh
HTTP/2 400 
date: Sun, 26 Jan 2025 21:53:28 GMT
content-type: application/json; charset=utf-8
content-length: 170
server: nginx
x-powered-by: Express
etag: W/"aa-aKEVg3a0HA+//TiQGCP1o6RAo9U"

{"errors":[{"message":"Expected value of type \"AttributeFilterInputType\", found \"全国道路施設点検データベース\".","locations":[{"line":1,"column":



(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_mlit-dpf-api$ ./test_api_shell-1.sh
HTTP/2 400 
date: Sun, 26 Jan 2025 21:54:58 GMT
content-type: application/json; charset=utf-8
content-length: 128
server: nginx
x-powered-by: Express
etag: W/"80-CgtIaIF+wTBfQPQnQU+TaFt44EM"

{"errors":[{"message":"Expected value of type \"AttributeFilterInputType\", found rsdb.","locations":[{"line":1,"column":38}]}]}



(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_mlit-dpf-api$ ./test_api_shell-1.sh
HTTP/2 400 
date: Sun, 26 Jan 2025 21:58:51 GMT
content-type: application/json; charset=utf-8
content-length: 189
server: nginx
x-powered-by: Express
etag: W/"bd-bRubVd4TTTLveKngSLh1xZtmd+c"

{"errors":[{"message":"Expected value of type \"AttributeFilterInputType\", found [{attributeName: \"全国道路施設点検データベース\"}].","locations":[{"line":1,"column":38}]}]}

COMMENTOUT