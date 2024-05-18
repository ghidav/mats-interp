#!/bin/bash

# Upgrade pip
pip install --upgrade pip

# Install necessary packages
echo "Installing necessary packages..."
pip install -r requirements.txt
pip install -U "huggingface_hub[cli]"
pip install -U kaleido
python -m ipykernel install --user --name=myenv --display-name="mats-interp"

git clone git@github.com:ghidav/feature-circuits.git

cd PySvelte
pip install -e .
cd ..

# Set the Hugging Face token as an environment variable
CONFIG_FILE="mats-interp/keys.json"
HF_TOKEN=$(jq -r '.HF_TOKEN' "$CONFIG_FILE")
export HF_TOKEN

mkdir /workspace/huggingface
export HF_HOME=/workspace/huggingface
echo "Hugging Face token set."

# Downloading models
huggingface-cli login --token HF_TOKEN
huggingface-cli download gpt2
huggingface-cli download google/gemma-2b
huggingface-cli download jbloom/Gemma-2b-Residual-Stream-SAEs
huggingface-cli download jbloom/GPT2-Small-SAEs-Reformatted

# Prompt the user for Weights & Biases token
WANDB_TOKEN=$(jq -r '.WANDB_TOKEN' "$CONFIG_FILE")
# Initialize Weights & Biases with the provided token
wandb login $WANDB_TOKEN
echo "Weights & Biases initialized."