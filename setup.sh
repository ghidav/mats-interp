#!/bin/bash

# Set up a Python virtual environment
echo "Creating a virtual environment..."
python3 -m venv ../myenv

# Activate the virtual environment
source ../myenv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install necessary packages
echo "Installing necessary packages..."
#pip install -r requirements.txt
pip install -U "huggingface_hub[cli]"
pip install -U kaleido
python -m ipykernel install --user --name=myenv --display-name="mats-interp"

git clone git@github.com:ghidav/feature-circuits.git

# Prompt the user for Hugging Face token
read -p "Please enter your Hugging Face token: " HF_TOKEN

# Set the Hugging Face token as an environment variable
export HF_TOKEN=$HF_TOKEN
mkdir /workspace/huggingface
export HF_HOME=/workspace/huggingface
echo "Hugging Face token set."

# Downloading models
huggingface-cli download gpt2
huggingface-cli download google/gemma-2b
huggingface-cli download jbloom/Gemma-2b-Residual-Stream-SAEs
huggingface-cli download jbloom/GPT2-Small-SAEs-Reformatted

# Prompt the user for Weights & Biases token
read -p "Please enter your Weights & Biases token: " WANDB_TOKEN

# Initialize Weights & Biases with the provided token
wandb login $WANDB_TOKEN
echo "Weights & Biases initialized."

apt update
apt-get install sudo -y
sudo apt install vim

configure_git
export EDITOR="vim"

echo "Setup completed successfully."