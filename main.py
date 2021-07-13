import requests
from wit import Wit
import json
import os
import argparse

parser = argparse.ArgumentParser()

opt = parser.parse_args()


# parser.add_argument("--nl", nargs = '+', type=str, default="Tell me the avg price Apartment 2 rooms in Đống Đa district, Hà Nội city, 2021", help="nl to query")
# parser.add_argument("--nl", nargs='+')
# parser.add_argument('string', help='Input String', type=str, nargs='+')

token = os.getenv('WIT_ACCESS_TOKEN')
bot = Wit(access_token=token)


def clustering(message_text):
    try:
        response = bot.message(msg=message_text)
        intent = response['intents'][0]
        #print(json.dumps(response, indent=4, ensure_ascii=False))

        if intent['confidence'] > 0.1:
            cluster_name = intent['name']
            if cluster_name in ['query', 'groupby']:
                result = response['entities']
                result = {}
                result['intent'] = cluster_name
                for key, value in response['entities'].items():
                    # name = key.split(':')[-1]
                    result[value[0]['role']] = value[0]['value']

                
                return result
            
    except:
        return 'i dont understand, could you repeat that?'


def send_request(result):

    
    if result['intent'] == 'query':
        conds = []
        for key, val in result.items():
            if key in ("Object", "Aggregator", "intent"):
                continue
            conds.append({"match": {key: val}})

        if result['Aggregator'] == 'count':
            body = {
                "query": {
                    "bool": {
                        "must": conds
                    }
                },
                "size": 5
            }
        else:
            body = {
                "query": {
                    "bool": {
                        "must": conds
                    }
                },
                "size": 5,
                "aggs": {
                    "aggregator": {
                        str(result['Aggregator']): {
                            "field": "total_price"  # still fix only query price
                        }
                    }
                }
            }
    elif result['intent'] == 'groupby':
        
        conds = []
        for key, val in result.items():
            if key in ("Object", "Aggregator", "intent", "groupby"):
                continue
            conds.append({"match": {key: val}})

        body = {
            "query": {
                "bool": {
                    "must": conds
                }
            },
            "size": 5
        }
    print(body)
    return body



# still fail because of authe
def send_to_ES(body):
    headers = {
        'Content-Type': 'application/json'
    }
    proxies = {
        'https':'http://192.168.1.124:443'
    }
    re = requests.get(
        # url='http://localhost:9200/real_estate/_search',
        url='https://kibana.data.cohost.biz/_plugin/kibana/real_estate/_search',
        # url='https://192.168.1.124:9200/real_estate/_search',
        headers=headers,
        data=body,
        proxies=proxies

    )
    print(re)
    return re

if __name__ == '__main__':
    # print(opt['string'])
    # nl = opt['string']
    nl = 'draw me a chart of Apartment price in SaiGon city, in 2021 groupby by district'
    x = clustering(nl)
    # print(x)
    print(x)
    y = send_request(x)

    # print(y)

    # with open("./res.json", "w") as f:
    #     f.write(json.dumps(y, indent=4, ensure_ascii=False))
    #print(json.dumps(y, indent=4, ensure_ascii=False))

    #z = send_to_ES(y)