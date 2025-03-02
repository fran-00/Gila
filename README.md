# GILA - AI Chatbot

Gila is AI chatbot client made with Python and PySide6.
Currently supported large language models:

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
- Command
- Command R
- Command R+
- Claude 3 Haiku
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3.5 Sonnet

Currently supported text-to-image models:

- DALL-E 2
- DALL-E 3

We will use [PyInstaller](https://pyinstaller.org/en/stable/operating-mode.html) to create an executable file that will allow us to start the client without having to deal with the source code. The executable file that **PyInstaller** will create depends on the operating system: this guide refers specifically to **Windows** but the steps for Linux and MacOs are practically the same. For the same reason I chose [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) as the virtual environment manager to run **Gila**: it allows you to specify a Python version and is easy to use on Windows, Linux and MacOs, but you can use any manager of your choice depending on the operating system you are on.

## How to set up development environment

To run from source, you'll need **Conda** and **Git** installed in your system. You'll also need some API Keys, but we'll cover it up later. Clone this project:

```shell
git clone https://github.com/fran-00/gila.git
```

Create a new virtual environment with *Python 3.13.2* using **conda** and activate it:

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

When you select an LLM from the settings and start a new chat, if you have not set the API Key required to use that LLM, a window will appear asking you to enter it. Depending on the LLM you have chosen, you will need to obtain an API key from a specific platform. Below are links to the pages where you can create API keys for the models used in Gila: to access these pages you must have an account first. Please note that in some cases there are costs associated with using API keys, although some platforms offer free plans to try out their services.

- [OpenAI](https://platform.openai.com/settings/organization/general): GPT-4o mini, GPT-4o, GPT-4, GPT-4 Turbo, DALL-E 2, DALL-E 3
- [Google](https://aistudio.google.com/app/apikey): Gemini 2.0 Flash, Gemini 1.5 Flash, Gemini 1.5 Pro
- [DeepSeek](https://platform.deepseek.com/api_keys): DeepSeek-V3, DeepSeek-R1
- [Mistral](https://console.mistral.ai/api-keys): Mistral Small, Mistral Nemo, Pixtral, Codestral Mamba
- [Arli AI](https://www.arliai.com/account): Llama70B, Qwen2.5-32B
- [Cohere](https://dashboard.cohere.com/api-keys): Command, Command R, Command R+
- [Anthropic](https://console.anthropic.com/settings/keys): Claude 3 Haiku, Claude 3 Opus, Claude 3 Sonnet, Claude 3.5 Sonnet

If valid, the entered API keys will be saved in a **.env** file in the root of the project and will be read by Gila as environmental variables.

## How to build the .exe file

On the root directory (with the virtual environment activated and PyInstaller installed):

```shell
pyinstaller build.spec
```

You will find **gila.exe** executable file inside *dist* directory: remember to copy *storage* folder there before distributing it!
