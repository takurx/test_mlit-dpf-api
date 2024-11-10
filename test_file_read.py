# test file read 

file = open('sample_responce_test_simple_search-1.json', 'r', encoding='utf-8')

data = file.read()
print(data)

file.close()
