curl -X POST -H "Content-Type: application/json" \
    -H "apikey: OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW" \
    -d "{\"query\": \"{ search(term:\\\"つくば\\\", first:5) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/

# -d "{\"query\": \"{ search(term:\\\"成田空港\\\", first:5) { totalNumber } }\" }" \

<< COMMENTOUT
#    -d "{\"query\": \"{ search(term:\\\"つくば\\\", first:5) { totalNumber } }\" }" \

(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_mlit-dpf-api$ ./test_api_shell-0.sh
HTTP/2 200 
date: Sat, 11 Jan 2025 07:44:39 GMT
content-type: application/json; charset=utf-8
content-length: 40
server: nginx
x-powered-by: Express
etag: W/"28-Erq33OoloDDSr8x9N7Cra3CHyU4"
content-security-policy: frame-ancestors 'self';

{"data":{"search":{"totalNumber":6318}}}(base)
COMMENTOUT