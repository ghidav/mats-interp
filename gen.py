from openai import OpenAI
import os
from tqdm import tqdm

openai = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

with open('pages.txt', 'r') as f:
    pages = f.read().splitlines()

with open('titles.txt', 'r') as f:
    titles = f.read().splitlines()

def generate(content):
    response = openai.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages = [{
            'role': 'assistant',
            'content': content
        }],
            temperature=1,
            max_tokens=512,
            top_p=1
        )

    return response.choices[0].message.content

pages_content = "Using only HTML, generate a page for the following purpose: {prompt}\nReturn only the code and nothing else."
text_content = "Generate a one page story with the following title: {prompt}\nReturn only the text of the story and nothing else."

code = []
text = []
for page, title in tqdm(zip(pages, titles)):
    code.append(generate(pages_content.format(prompt=page)))
    text.append(generate(text_content.format(prompt=title)))

with open('gen_pages.txt', 'w') as f:
    f.write('\n---\n'.join(code))

with open('gen_text.txt', 'w') as f:
    f.write('\n---\n'.join(text))