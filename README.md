# test_mlit-dpf-api
- 国土交通データプラットフォーム（MILT DPF）について、API gatewayのありなしでセキュリティや利便性を比較するために、国土交通データプラットフォーム（MILT DPF）と外部APIをAPI gateway (Kong gateway)を通じて使用する、またはAPI gatewayを通さず動作するサンプルアプリケーションを作成した
- 外部APIはつくば市のキョンの目撃情報を使用したAPI serverのアプリを作成した
- サンプルアプリケーションはつくばのキョンの目撃情報と国土交通データプラットフォームの建設物の情報を地図上で重ね合せて表示するGISアプリケーションを作成した

## 前提条件
- Ubuntu 22.04 にて動作を確認した
- Python, Streamlit, Dockerがインストールされていること

## 動作手順
1. キョンの目撃情報の外部APIサーバを起動する
```bash
python run_kyun_system.py
```

2. Kong Gatewayを起動する
```bash
sudo curl -Ls https://get.konghq.com/quickstart | sudo bash
```

3. Kong Gatewayの設定を行う、国土交通データプラットフォームのAPIの設定
```bash
curl -i -s -X POST http://localhost:8001/services \
    --data name=dpf_service \
    --data url='https://www.mlit-data.jp/api/v1'

curl -i -X POST http://localhost:8001/services/dpf_service/routes \
     --data 'paths[]=/dpf_mock' \
     --data name=dpf_route

curl -X GET http://localhost:8001/services/dpf_service/routes/dpf_route
```

4. Kong Gatewayの設定を行う、キョンの目撃情報のAPIの設定
```bash
curl -i -s -X POST http://localhost:8001/services \
    --data name=kyon_service \
    --data url="http://$(hostname -I | awk '{print $1}'):5000/"

curl -i -X POST http://localhost:8001/services/kyon_service/routes \
     --data 'paths[]=/kyon_mock' \
     --data name=kyon_route

curl -X GET http://localhost:8001/services/kyon_service/routes/kyon_route
```

5. つくばのキョンの目撃情報と国土交通データプラットフォームの建設物の情報を地図上で重ね合せて表示するサンプルアプリケーションを起動する
```bash
streamlit run folium_kyon_visualization.py
```

## APIアクセス状況の可視化のための追加の手順（+ Prometheus, Grafana）
6. Kong gatewayでGUIからまたはcommandでPrometheusのpluginを有効化する
7. Prometheusを起動する
```bash
sudo docker run --name prometheus -d -p 127.0.0.1:9090:9090 prom/prometheus
```
8. Grafanaを起動する
```bash
sudo docker run -d -p 3000:3000 --name=grafana grafana/grafana-enterprise
```
9. GrafanaでPrometheusのデータソースを追加する

## Kong gateway, Prometheus, Grafanaを停止するときの手順
- Kong gatewayを停止する
```bash
sudo curl -s https://get.konghq.com/quickstart | sudo bash -s -- -d -a kong-quickstart
```
- Prometheusを停止する
```bash
sudo docker ps -a
sudo docker rm prometheus
```
- Grafanaを停止する
```bash
sudo docker ps -a
sudo docker rm grafana
```

## Reference
1. [MILT Data PlatForm, 国土交通データプラットフォーム](https://www.mlit-data.jp/#/)
2. [sample, 国交 DPF 利用者 API、利用サンプルプログラム | 国土交通DPF利用者API](https://www.mlit-data.jp/api_docs/examples/introduction.html)



