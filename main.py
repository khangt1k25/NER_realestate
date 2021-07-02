import requests
from wit import Wit
import json


WIT_ACCESS_TOKEN = '532392274788409::TJMI4BYIZZVBCTVXXU45GPUBL2MZZAWN::CZY3B7UQJJYB2KHJK3CCGE6LRLKMQ532'
bot = Wit(access_token=WIT_ACCESS_TOKEN)




def clustering(message_text):
    try:
        response = bot.message(msg=message_text)
        print(response)
        intent = response['intents'][0]
        if intent['confidence'] > 0.1:
            cluster_name = intent['name']
            if cluster_name == 'query':
                result = response['entities']
                result = {}
                for key, value in response['entities'].items():
                    result[value[0]['name']] =  value[0]['value'] 

                return result
    except:
        return 'i dont understand, could you repeat that?'

def send_request(result):
    
    body = {
        "query": {
            "bool": {
            "must": [
                { "match": {"province": "TPHCM" } },
                { "match": {"district": "Quận Tân Bình"}},
                { "match": {"bedroom": 10}},
                { "match": {"type": "Bán Nhà Mặt Phố "}}    
            ]
            }
        },
        "size": 0,
        "aggs": {
            "aggregator": {
            "avg": {
                "field": "total_price"
            }
            }
        }
    }
    print(body)
    # response = elastic_client.search(index='real-estate', body=body, size=10000)
    # elastic_docs = response['hits']['hits']

    # aggregation_value = response['aggregations']['avg']['value']


message = input("Enter NL: ")

x = clustering(message)
# send_request(x)
print(x)