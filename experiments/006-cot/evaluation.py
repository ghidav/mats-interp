import string
import re
import ast
import numpy as np
import pandas as pd
from tqdm.auto import tqdm

from generation import few_shot_example
from utils import (
    sys_prompt, prompt, api_generate,
    is_a_species, is_a_subject, is_an_attribute
)

def str_to_bool(s):
    if isinstance(s, str):
        s = s.translate(str.maketrans('', '', string.punctuation))
        if 'yes' == s.lower().strip():
            return 'Yes'
        elif 'no' == s.lower().strip():
            return 'No'
    raise ValueError("Input must be a string")

def extract_answer(text):
    try:
        answer = str_to_bool(text)
    except:
        pattern = r'Answer:\s*(.*)'
        match = re.search(pattern, text)
        
        if match:
            answer = match.group(1)
        else:
            answer = "NaN"

    return answer

def extract_cot(text):
    pattern = re.compile(r'(?m)^(?:\(\d+\)|[*-]|\d+\.\s*)\s*(.+)$')
    matches = pattern.findall(text)

    return matches

def step_decompose(step):
    dec = []
    try:
        if 'is' in step:
            fst, snd = step.split('.')[0].split('is')
        elif 'are' in step:
            fst, snd = step.split('.')[0].split('are')
    except Exception as e:
        print(step.split('.'), e)

    is_sp, sp = is_a_species(fst)
    is_at, at = is_an_attribute(fst)
    is_sj, sj = is_a_subject(fst)

    if is_sp:
        dec.append(sp)
    elif is_at:
        dec.append(at)
    elif is_sj:
        dec.append(sj)

    if 'not' in step:
        dec.append('is not')
    else:
        dec.append('is')

    is_sp, sp = is_a_species(snd)
    is_at, at = is_an_attribute(snd)
    is_sj, sj = is_a_subject(snd)

    if is_sp:
        dec.append(sp)
    elif is_at:
        dec.append(at)
    elif is_sj:
        dec.append(sj)
    return dec

def check_cot(row):

    if isinstance(row['cot_gold'], str):
        gold = ast.literal_eval(row['cot_gold'])
    else:
        gold = row['cot_gold']
    if isinstance(row['cot_pred'], str):
        pred = ast.literal_eval(row['cot_pred'])
    else:
        pred = row['cot_pred']
    
    check = True
    if len(pred) > 0:
        for n, (x, y) in enumerate(zip(gold, pred)):
            for x_step, y_step in zip(step_decompose(x), step_decompose(y)):
                check = x_step == y_step
                if not check: break
            if not check: break
    else:
        check = False
        n = -1

    return check, n

def check_cot_api(row):
    if isinstance(row['cot_gold'], str):
        gold = ast.literal_eval(row['cot_gold'])
    else:
        gold = row['cot_gold']
    gold_prompt = ""
    for i, step in enumerate(gold):
        gold_prompt += f"({i}) {step}\n"

    if isinstance(row['cot_pred'], str):
        pred = ast.literal_eval(row['cot_pred'])
    else:
        pred = row['cot_pred']
    pred_prompt = ""
    for i, step in enumerate(pred):
        pred_prompt += f"({i}) {step}\n"
    
    prompt_ = prompt.format(
        gold=gold_prompt,
        pred=pred_prompt
    )
    
    eval = api_generate(prompt_, 'gpt-4o', max_tokens=8, temperature=1e-6, sys_prompt=sys_prompt)
    
    if 'CORRECT' in eval:
        return True
    elif 'WRONG' in eval:
        return False
    else:
        return np.nan
    
### EVAL FUNCTION ###
def run_eval(model_name, N, n_hops, n_shots, with_cot, p=0.5):

    prompts = [few_shot_example(n_hops=n_hops, n_shots=n_shots, p=p, with_cot=with_cot) for i in range(N)] 

    results_df = {
        'prompt': [],
        'answer': [],
        'label': [],
        'cot_gold': [],
        'pred': [],
        'cot_pred': []
    }

    err_count = 0
    for i in tqdm(range(N)):
        prompt, (c, q, label, cot) = prompts[i]
        out = api_generate(prompt, model_name, max_tokens=256, temperature=0)

        pred = extract_answer(out)
        cot_pred = extract_cot(out)
        
        if pred == "NaN":
            err_count += 1
            print(out)
        results_df['prompt'].append(prompt)
        results_df['answer'].append(out)
        results_df['label'].append(label)
        results_df['cot_gold'].append(cot)
        results_df['pred'].append(pred)
        results_df['cot_pred'].append(cot_pred)

    results_df = pd.DataFrame(results_df)

    results_df['correct_pred'] = results_df['label'] == results_df['pred'].astype('str')
    if with_cot:
        #results_df['correct_cot'] = results_df.apply(lambda x: check_cot(x)[0], axis=1)
        results_df['correct_cot'] = results_df.apply(lambda x: check_cot_api(x), axis=1)
    else:
        results_df['correct_cot'] = np.nan

    pred_acc = results_df['correct_pred'].mean()
    cot_acc = results_df['correct_cot'].mean()
    cot_pred_corr = (results_df['correct_pred'] * results_df['correct_cot']).mean() / min(results_df['correct_pred'].mean(), results_df['correct_cot'].mean())

    return results_df, pred_acc, cot_acc, cot_pred_corr