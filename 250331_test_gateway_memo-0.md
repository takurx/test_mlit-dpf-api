###

```
cd ~/LoRaWorks_230822/test_mlit-dpf-api
python run_kyon_system.py
```

```
sudo curl -Ls https://get.konghq.com/quickstart | sudo bash
```

```
curl -i -s -X POST http://localhost:8001/services \
   --data name=dpf_service \
   --data url='https://www.mlit-data.jp/api/v1'
curl -i -X POST http://localhost:8001/services/dpf_service/routes \
    --data 'paths[]=/dpf_mock' \
    --data name=dpf_route
```

```
curl -i -s -X POST http://localhost:8001/services \
   --data name=kyon_service \
   --data url='http://localhost:5000/api/kyon/sightings'
curl -i -X POST http://localhost:8001/services/kyon_service/routes \
    --data 'paths[]=/kyon_mock' \
    --data name=kyon_route
```

```
streamlit run folium_kyon_visualization.py
```



