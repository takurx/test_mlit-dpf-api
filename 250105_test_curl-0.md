# API利用方法 | 国土交通DPF利用者API
https://www.mlit-data.jp/api_docs/reference/general/apiaccess.html

```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: [OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW]" \
    -d "{\"query\": \"{ search(term:\\\"橋梁\\\", first:0) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```

```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW" \
    -d "{\"query\": \"{ search(term:\\\"橋梁\\\", first:0) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```

```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW" \
    -d "{\"query\": \"{ search(term:\\\"成田空港\\\", first:5) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```




```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: OWgbj7rAlYJzyOtHSHHmhlF0oW" \
    -d "{\"query\": \"{ search(term:\\\"つくば駅\\\", first:5) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```

独自CSVの読み込み
→lattitude, longitudeを1行目に定義したら、地図のアイテムとして読み込んで、描写できた、add_xy_data
→日本語が使えるか確認したい
→読み込みはした、地図上には日本語は出てないから出せるかはまだわからない
→マウスオーバーしたときにメモを出す機能はあるか？


つくば周辺のAPIは
前回のAPIの成田空港→つくば駅に変更して
APIを試す予定


こういうのをchatgptに説明しながらやれば良いか



```
(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_geopandas_jupyter_notebook$ curl -X POST -H "Content-Type: application/json" \
>     -H "apikey: OWgbj7rAlYJzyOtHSHHmhlF0oW" \
>     -d "{\"query\": \"{ search(term:\\\"つくば駅\\\", first:5) { totalNumber } }\" }" \
>     -i https://www.mlit-data.jp/api/v1/
HTTP/2 403 
server: awselb/2.0
date: Sat, 11 Jan 2025 07:21:15 GMT
content-type: text/html
content-length: 118

<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
</body>
```


```
(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_geopandas_jupyter_notebook$ curl -X POST -H "Content-Type: application/json" \
>     -H "apikey: OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW" \
>     -d "{\"query\": \"{ search(term:\\\"成田空港\\\", first:5) { totalNumber } }\" }" \
>     -i https://www.mlit-data.jp/api/v1/
HTTP/2 200 
date: Sat, 11 Jan 2025 07:22:13 GMT
content-type: application/json; charset=utf-8
content-length: 38
server: nginx
x-powered-by: Express
etag: W/"26-3lDSzu70mV+WPACpI7XDa8wG9bo"
content-security-policy: frame-ancestors 'self';

{"data":{"search":{"totalNumber":74}}}
```


```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: OWgbj7rAlYJzyOtHSHHmhlF0oW" \
    -d "{\"query\": \"{ search(term:\\\"筑波山\\\", first:5) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```


```
(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_geopandas_jupyter_notebook$ curl -X POST -H "Content-Type: application/json" \
>     -H "apikey: OWgbj7rAlYJzyOtHSHHmhlF0oW" \
>     -d "{\"query\": \"{ search(term:\\\"筑波山\\\", first:5) { totalNumber } }\" }" \
>     -i https://www.mlit-data.jp/api/v1/
HTTP/2 403 
server: awselb/2.0
date: Sat, 11 Jan 2025 07:25:45 GMT
content-type: text/html
content-length: 118

<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
</body>
</html>
(base) 
```




```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: OWgbj7rAlYJzyOtHSHHmhlF0oW" \
    -d "{\"query\": \"{ search(term:\\\"東京駅\\\", first:5) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```



```
(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_geopandas_jupyter_notebook$ curl -X POST -H "Content-Type: application/json" \
>     -H "apikey: OWgbj7rAlYJzyOtHSHHmhlF0oW" \
>     -d "{\"query\": \"{ search(term:\\\"東京駅\\\", first:5) { totalNumber } }\" }" \
>     -i https://www.mlit-data.jp/api/v1/
HTTP/2 403 
server: awselb/2.0
date: Sat, 11 Jan 2025 07:26:51 GMT
content-type: text/html
content-length: 118

<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
</body>
</html>
(base)
```


```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: OWgbj7rAlYJzyOtHSHHmhlF0oW" \
    -d "{\"query\": \"{ search(term:\\\"万世橋\\\", first:5) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```



```
(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_geopandas_jupyter_notebook$ curl -X POST -H "Content-Type: application/json" \
>     -H "apikey: OWgbj7rAlYJzyOtHSHHmhlF0oW" \
>     -d "{\"query\": \"{ search(term:\\\"万世橋\\\", first:5) { totalNumber } }\" }" \
>     -i https://www.mlit-data.jp/api/v1/
HTTP/2 403 
server: awselb/2.0
date: Sat, 11 Jan 2025 07:27:51 GMT
content-type: text/html
content-length: 118

<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
</body>
</html>
(base) 
```



```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: OWgbj7rAlYJzyOtHSHHmhlF0oW" \
    -d "{\"query\": \"{ search(term:\\\"国土地理院\\\", first:5) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```


```
(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_geopandas_jupyter_notebook$ curl -X POST -H "Content-Type: application/json" \
>     -H "apikey: OWgbj7rAlYJzyOtHSHHmhlF0oW" \
>     -d "{\"query\": \"{ search(term:\\\"国土地理院\\\", first:5) { totalNumber } }\" }" \
>     -i https://www.mlit-data.jp/api/v1/
HTTP/2 403 
server: awselb/2.0
date: Sat, 11 Jan 2025 07:29:45 GMT
content-type: text/html
content-length: 118

<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
</body>
</html>
(base) 
```


```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: [OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW]" \
    -d "{\"query\": \"{ search(term:\\\"橋梁\\\", first:5) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```

```
(base) chino@chino-Legion-5-15IAH7H:~/LoRaWorks_230822/test_geopandas_jupyter_notebook$ curl -X POST -H "Content-Type: application/json" \
>     -H "apikey: [OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW]" \
>     -d "{\"query\": \"{ search(term:\\\"橋梁\\\", first:5) { totalNumber } }\" }" \
>     -i https://www.mlit-data.jp/api/v1/
HTTP/2 403 
server: awselb/2.0
date: Sat, 11 Jan 2025 07:33:27 GMT
content-type: text/html
content-length: 118

<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
</body>
</html>
```



```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW" \
    -d "{\"query\": \"{ search(term:\\\"成田空港\\\", first:5) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```




```
curl -X POST -H "Content-Type: application/json" \
    -H "apikey: [OWgbj7rAlYJzyOtHdMxk2~SHHmhlF0oW]" \
    -d "{\"query\": \"{ search(term:\\\"つくば\\\", first:5) { totalNumber } }\" }" \
    -i https://www.mlit-data.jp/api/v1/
```