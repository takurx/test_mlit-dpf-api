# test json file read 
import json

#Windowsで標準出力をUTF8にする
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file = open('sample_responce_test_simple_search-1.json', 'r', encoding='utf-8')

data = file.read()
#print(data)

file.close()

jsondata = json.dumps(data)
#sprint(jsondata)
#print(jsondata, encoding='utf-8')
print(str(jsondata["data"]["search"]))

