# Gila - AI Chat Client

Gila is a Python application built with PySide6 that connects to the REST APIs of AI service providers. It allows users to interact with several large language models, store chat histories, and customize chat parameters.

## Currently supported models

- GPT-4o mini
- GPT-4o
- GPT-4
- GPT-4 Turbo
- GPT-4.5 preview
- Gemini 2.0 Flash
- Gemini 1.5 Flash
- Gemini 1.5 Pro
- DeepSeek-V3
- DeepSeek-R1
- Mistral Small
- Mistral Nemo
- Pixtral
- Codestral Mamba
- Llama70B
- Qwen2.5-32B
- Command R7B
- Command R+
- Command R
- Command
- Aya Expanse 8B
- Aya Expanse 32B
- Claude 3.7 Sonnet
- Claude 3.5 Sonnet v2
- Claude 3.5 Haiku
- Claude 3 Opus

## Currently supported text-to-image models

- DALL-E 2
- DALL-E 3

## Setup and Running Instructions

To run Gila from source, you'll need **Conda** and **Git** installed in your system, along with the necessary API keys. Below are the steps to set up the development environment and run the application:

```shell
git clone https://github.com/fran-00/gila.git
```

Create a new virtual environment with *Python 3.13.2* using **Conda** and activate it:

```shell
conda create --name gila python=3.13.2
conda activate gila
```

Install project's required packages via pip:

```shell
pip install -r requirements.txt
```

Now you can run Gila:

```shell
python -m gila
```

## API Keys

When selecting an LLM and starting a new chat, if you haven't set the necessary API key, a window will prompt you to enter it. Below are links to where you can obtain API keys for the models used in Gila (an account may be required). Please note that some platforms may charge for API usage, although free plans are also available for testing purposes.

- [OpenAI](https://platform.openai.com/settings/organization/general): GPT-4o mini, GPT-4o, GPT-4, GPT-4 Turbo, DALL-E 2, DALL-E 3
- [Google](https://aistudio.google.com/app/apikey): Gemini 2.0 Flash, Gemini 1.5 Flash, Gemini 1.5 Pro
- [DeepSeek](https://platform.deepseek.com/api_keys): DeepSeek-V3, DeepSeek-R1
- [Mistral](https://console.mistral.ai/api-keys): Mistral Small, Mistral Nemo, Pixtral, Codestral Mamba
- [Arli AI](https://www.arliai.com/account): Llama70B, Qwen2.5-32B
- [Cohere](https://dashboard.cohere.com/api-keys): Command R7B, Command R+, Command R, Command, Aya Expanse 8B, Aya Expanse 32B
- [Anthropic](https://console.anthropic.com/settings/keys): Claude 3.7 Sonnet, Claude 3.5 Sonnet v2, Claude 3.5 Haiku, Claude 3 Opus

If valid, the API keys will be saved in a **.env** file in the project root directory, and Gila will read them as environmental variables

## Build the Executable

To create a standalone executable file, make sure the virtual environment is activated and PyInstaller is installed, then run the following command in the root directory:

```shell
pyinstaller build.spec
```

This will create a gila.exe file in the *dist* directory. Remember to copy the **storage** folder into the same directory as the executable before distributing it.
