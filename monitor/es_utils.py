import requests
import json

es_host = "http://34.70.245.84:9200"
index = "sparkapps"
type = "_doc"
es_url = "%s/%s/%s" %(es_host, index, type)

def send_to_es(data):
    print (data)
    headers = {'content-type': 'application/json'}
    if data:
        response = requests.post(es_url, data=json.dumps(data[0]), headers=headers)
        print (response)
