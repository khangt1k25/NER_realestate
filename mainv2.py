import requests
import json
WIT_ACCESS_TOKEN = 'TJMI4BYIZZVBCTVXXU45GPUBL2MZZAWN'
# import urllib.request

header  = {
    "Authorization": "Bearer %s" % WIT_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

base_url = 'https://api.wit.ai/message?v=20210701&q='
message = "tell me the avg price in HaNoi city"
message = message.replace(" ", "%20")


print(base_url+message)
rsp = requests.get(headers=header, url=base_url+message)

print(rsp.json())
# def clustering(message_text):
#     try:
#         # response = bot.message(msg=message_text)
#         response = requests.get()
#         intent = response['intents'][0]
#         if intent['confidence'] > 0.1:
#             cluster_name = intent['name']
#             if cluster_name == 'query':
#                 result = response['entities']
#                 result = {}
#                 for key, value in response['entities'].items():
#                     result[value[0]['name']] =  value[0]['value'] 

#                 return result
#     except:
#         return 'i dont understand, could you repeat that?'



# message = input("Enter NL: ")

# x = clustering(message)
# # send_request(x)
# print(x)