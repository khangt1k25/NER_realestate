from wit import Wit
import json
import os
import pandas as pd
import matplotlib.pyplot as plt


token = os.getenv('WIT_ACCESS_TOKEN')
bot = Wit(access_token=token)

# Get clustering from Wit.ai
def clustering(message_text):
    try:
        response = bot.message(msg=message_text)
        intent = response['intents'][0]
        print(json.dumps(response, indent=4, ensure_ascii=False))
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


# Parse clustering to ES query
def parse_to_ES(result):

    
    if result['intent'] == 'query':
        conds = []
        for key, val in result.items():
            if key in ("main","Object", "Aggregator", "intent", "groupby"):
                continue
            conds.append({"match": {key: val}})
        
        body = {
                "query": {
                    "bool": {
                        "must": conds
                    }
                },
                "size": 0,
                "aggs": {
                    "avg": {
                        "avg": {
                            "field": "price"
                        }
                    },
                    "sum": {
                        "sum":{
                            "field": "price"
                        }
                    },
                    "min": {
                        "min": {
                            "field": "price"
                        }
                    },
                    "max": {
                        "max":{
                            "field": "price"
                        }
                    }
                }
            }

            
    elif result['intent'] == 'groupby':
        
        conds = []
        for key, val in result.items():
            if key in ("Object", "main","Aggregator", "intent", "groupby"):
                continue
            conds.append({"match": {key: val}})

        body = {
            "query": {
                "bool": {
                    "must": conds
                }
            },
            "size": 10000
        }
    
    return body



# For drawing chart
def convert_response_to_df(response):
    df = pd.DataFrame.from_dict(response['hits']['hits'], orient='columns')
    sources = list(df['_source'])
    return pd.DataFrame.from_dict(sources, orient='columns')


# Show the result from response
def processing(response, cluster):
    if cluster['intent'] == 'query':
        result = {}
        agg = response['aggregations']
        
        result['total'] = response['hits']['total']
        result['min'] = agg['min']['value']
        result['max'] = agg['max']['value']
        result['avg'] = agg['avg']['value']
        
        return result
    elif cluster['intent'] == 'groupby':
        
        df = convert_response_to_df(response)
        obj = cluster['Object']
        groupby = cluster['groupby']
        x = df.groupby([groupby], as_index=False).mean()
        x_a = list(x[groupby])
        y_a = list(x[obj])
        plt.figure(figsize=(25, 25))
        plt.plot(x_a, y_a)
        
        return df, obj, groupby
        
        