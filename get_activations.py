from transformer_lens import HookedTransformer, utils
from datasets import load_dataset
from tqdm import tqdm
import torch
import os

# Load model
model_name = 'gpt2'
model = HookedTransformer.from_pretrained(model_name, device='cuda')
model.eval()
nl = len(model.blocks)

# Load and prepare the dataset
data_name = 'c4-code-20k'
dataset = load_dataset('NeelNanda/c4-code-20k')['train']
tokens = utils.tokenize_and_concatenate(dataset, model.tokenizer, max_length=512)['tokens'] # [n_batches 512]

activations_path = f'activations/{model_name}_{data_name}'
if not os.path.exists(activations_path):
    os.makedirs(activations_path)

component = 'hook_resid_pre'
n_files = 10
batch_size = 32
tokens = tokens.reshape(n_files, -1, 512)

for i in range(n_files):

    activations = {f'blocks.{l}.{component}': [] for l in range(nl)}

    for b in tqdm(range(0, tokens.shape[1], batch_size)):
        with torch.no_grad():
            _, cache = model.run_with_cache(tokens[i, b:b+batch_size])

        for l in range(nl):
            activations[f'blocks.{l}.{component}'].append(cache[f'blocks.{l}.{component}'].cpu())
        
        del cache

    activations = {k: torch.cat(v) for k, v in activations.items()}

    for l in range(nl):
        component_path = os.path.join(activations_path, f"blocks.{l}.{component}")
        if not os.path.exists(component_path):
            os.makedirs(component_path)
        
        torch.save(activations[f"blocks.{l}.{component}"], os.path.join(component_path, f"{i}.pt"))