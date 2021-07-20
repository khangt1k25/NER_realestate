import openai
from openai.api_resources import engine
import json
import os

def set_openai_key():
    OPENAI_API_KEY = os.getenv("OPEN_AI_ACCESS_TOKEN")
    openai.api_key = OPENAI_API_KEY


class Pair():
    """Stores an text, sql pair"""

    def __init__(self, text, sql):
        self.text = text
        self.sql = sql

    def format(self):
        """Formats the text, sql pair."""
        return f"text: {self.text}\nsql: {self.sql}\n"

class Text2SQL():
    def __init__(self, engine='davinci',
                 temperature=0.5,
                 max_tokens=100):
        self.examples = []
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.default_prompt = "Create a SQL request to {text}\n\n SELECT"

    def add_example(self, ex):

        assert isinstance(ex, Pair), "Please create an Pair object."
        self.examples.append(ex.format())

    def add_examples_from_json(self, path):
        with open(path, 'rb') as f:
            examples = json.load(f)
        for ex in examples:
            ex_formated = Pair(ex['text'], ex['sql']);
            self.examples.append(ex_formated.format())

    def get_all_examples(self):
    
        return '\n'.join(self.examples) + '\n'

    def format_query(self, prompt):

        return self.get_all_examples() + "text: " + prompt + "\n"
  

    def call_request(self, query):
        
        if len(self.examples) != 0:
            response = openai.Completion.create(
                engine=self.engine,
                prompt=self.format_query(query),
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=1,
                n=1,
                stream=False,
                stop="\ntext:"
            )
        else:
            response = openai.Completion.create(
                engine=self.engine,
                prompt=f"text: {query} \nSELECT ",
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=1,
                n=1,
                stream=False,
                stop="\ntext:"
            )

        return response.choices[0].text


        