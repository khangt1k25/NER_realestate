import json
from openaiclient import Text2SQL, Pair, set_openai_key



set_openai_key()
engine = Text2SQL()
engine.add_examples_from_json(path="./prompts.json")

# x = engine.get_all_examples()
# print(x)
res = engine.call_request("how many house in ba dinh district, ha noi city")
print(res)