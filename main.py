import requests
from wit import Wit
import json
import os

token = os.getenv('WIT_ACCESS_TOKEN')


bot = Wit(access_token=token)




def clustering(message_text):
    try:
        response = bot.message(msg=message_text)
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
    
    conds = []
    for key, val in result.items():
        if key in ("Object", "Aggregator"):
            continue
        conds.append({"match": {key: val}});

    body = {
        "query": {
            "bool": {
            "must": conds
            }
        },
        "size": 0,
        "aggs": {
            "aggregator": {
            str(result['Aggregator']): {
                "field": "total_price"
            }
            }
        }
    }
    return body



message = input("Enter NL: ")

x = clustering(message)
print(x)
y = send_request(x)
print(y)
