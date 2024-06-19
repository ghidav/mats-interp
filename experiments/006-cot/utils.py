import json
from openai import OpenAI
import replicate
import os

with open('keys.json', 'r') as f:
    keys = json.load(f)

# API Generation
anyscale_client = OpenAI(
    base_url = "https://api.endpoints.anyscale.com/v1",
    api_key=keys['anyscale'],
)

openai_client = OpenAI(
    api_key=keys['openai'],
)

os.environ['REPLICATE_API_TOKEN'] = keys['replicate']

def replicate_generate(prompt, model_name, max_tokens=128, temperature=0, sys_prompt=None, **kwargs):
    input = {
        "prompt": prompt,
        "temperature": temperature,
    }
    input.update(kwargs)

    output = replicate.run(
        model_name,
        input=input
    )
    return "".join(output)

def api_generate(prompt, model_name, max_tokens=128, temperature=0, sys_prompt=None, **kwargs):

    if 'gpt' in model_name:
        client = openai_client
    else:
        client = anyscale_client

    if sys_prompt is not None:
        messages = [{'role': 'system', 'content': sys_prompt}, {'role': 'user', 'content': prompt}]
    else:
        messages = [{'role': 'user', 'content': prompt}]

    response = client.chat.completions.create(
            model = model_name,
            messages = messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    
    return response.choices[0].message.content

all_species = ['grimpus', 'lorpus', 'wumpus', 'zumpus', 'sterpus', 'numpus', 'jompus', 'brimpus', 'yumpus', 'tumpus', 'dumpus', 'vumpus', 'rompus', 'lempus', 'gorpus', 'shumpus', 'impus']
all_attributes = ['fast', 'luminous', 'tall', 'large', 'heavy', 'blonde', 'crazy', 'hungry', 'happy']
all_subjects = ['Grom', 'Wren', 'Trux', 'Jinx', 'Rast']

def is_a_species(x):
    for s in all_species:
        if s in x.lower():
            return True, s
    return False, None

def is_an_attribute(x):
    for s in all_attributes:
        if s in x.lower():
            return True, s
    return False, None

def is_a_subject(x):
    for s in all_subjects:
        if s in x:
            return True, s
    return False, None

with open('keys.json', 'r') as f:
    keys = json.load(f)

sys_prompt = """You have to evaluate reasoning processes. You will be given a GOLD and a PREDICT processes and you have to determine whether the second is equivalent to the first and answer CORRECT or WRONG. 
Here are some examples: 

GOLD
(1) Jinx is a dumpus.
(2) Dumpuses are grimpuses.
(3) Jinx is a grimpus.
(4) Each grimpus is not hungry.
(5) Jinx is not hungry.

PRED
(1) Jinx is a sterpus.
(2) Each sterpus is a lempus. (We don't need to use this statement for now, but we'll come back to it later.)
(3) Jinx is a dumpus.
(4) Each dumpus is a grimpus.
(5) Jinx is a grimpus.
(6) Each grimpus is not hungry.
(7) Jinx is a grimpus, so Jinx is not hungry.

EVAL: CORRECT


GOLD
(1) Trux is a grimpus.
(2) Grimpuses are rompus.
(3) Trux is a rompus.
(4) Rompuses are not large.
(5) Trux is not large.

PRED
1. Trux is a grimpus.
2. Each grimpus is a rompus.
3. Trux is a rompus.
4. Rompuses are blonde. (Note: This statement is not relevant to the question, but we'll keep it in mind)
5. Each vumpus is large.
6. Vumpuses are gorpus.
7. Trux is a gorpus.
8. Vumpuses are not tall.
9. Trux is a vumpus (from step 7 and step 6).
10. Since Trux is a vumpus, it is large (from step 5).

EVAL: WRONG

Answer only with the final evaluation CORRECT or WRONG."""

prompt = "GOLD\n{gold}\n\nPRED\n{pred}"