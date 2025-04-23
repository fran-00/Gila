# Gila - AI Chat Client

Gila is a Python application built with PySide6 that connects to the REST APIs of AI service providers. It allows users to interact with several large language models, store chat histories, and customize chat parameters.

## Currently supported models

- Aya Expanse 32B
- Aya Expanse 8B
- Claude 3 Opus
- Claude 3.5 Haiku
- Claude 3.5 Sonnet v2
- Claude 3.7 Sonnet
- Codestral Mamba
- Command
- Command A
- Command R
- Command R+
- Command R7B
- DeepSeek-R1
- DeepSeek-V3
- Gemini 1.5 Flash
- Gemini 1.5 Pro
- Gemini 2.0 Flash
- Gemini 2.0 Flash-Lite
- Gemini 2.5 Flash Preview 04-17
- Gemma 2 9B
- GPT-3.5 Turbo
- GPT-4
- GPT-4 Turbo
- GPT-4.1
- GPT-4.1 mini
- GPT-4.1 nano
- GPT-4.5 preview
- GPT-4o
- GPT-4o mini
- Llama 3 70B
- Llama 3 8B
- Llama 3.1 8B instant
- Llama 3.3 70B versatile
- Llama 3.3 70B (Arli AI)
- Llama 4 Maverick 17B
- Llama 4 Scout 17B
- Llama Guard 3 8B
- Mistral Nemo
- Mistral Small
- o1
- o1-mini
- o3-mini
- o4-mini
- Pixtral
- PlayAI Dialog
- Qwen 2.5 32B (Arli AI)
- Qwen/QwQ 32B

## Currently supported text-to-image models

- DALL-E 2
- DALL-E 3

## Setup and Running Instructions

To run Gila from source, you'll need **Conda** and **Git** installed in your system, along with the necessary **API keys.**. Below are the steps to set up the development environment and run the application:

1. Clone the repository:

    ```shell
    git clone https://github.com/fran-00/gila.git
    ```

2. Create a new virtual environment with *Python 3.13.2* using **Conda** and activate it:

    ```shell
    conda create --name gila python=3.13.2
    conda activate gila
    ```

3. Install the required packages via pip:

    ```shell
    pip install -r requirements.txt
    ```

4. Run Gila:

    ```shell
    python -m gila
    ```

## API Keys

When selecting an LLM and starting a new chat, if you haven't set the necessary API key, a window will prompt you to enter it. Below are links to where you can obtain API keys for the models used in Gila (an account may be required). Please note that some platforms may charge for API usage, although free plans are also available for testing purposes.

- [Anthropic](https://console.anthropic.com/settings/keys): Claude 3 Opus, Claude 3.5 Haiku, Claude 3.5 Sonnet v2, Claude 3.7 Sonnet
- [Arli AI](https://www.arliai.com/account): Llama 70B, Qwen 2.5 32B
- [Cohere](https://dashboard.cohere.com/api-keys): Aya Expanse 8B, Aya Expanse 32B, Command, Command A, Command R, Command R, Command R7B
- [DeepSeek](https://platform.deepseek.com/api_keys): DeepSeek-R1, DeepSeek-V3
- [Google](https://aistudio.google.com/app/apikey): Gemini 1.5 Flash, Gemini 1.5 Pro, Gemini 2.0 Flash, Gemini 2.0 Flash-Lite, Gemini 2.5 Flash Preview 04-17
- [Groq](https://console.groq.com/home): Gemma 2 9B, Llama 3 70B, Llama 3 8B, Llama 3.1 8B instant, Llama 3.3 70B versatile, Llama 4 Maverick 17B, Llama 4 Scout 17B, Llama Guard 3 8B, PlayAI Dialog, Qwen/QwQ 32B
- [Mistral](https://console.mistral.ai/api-keys): Codestral Mamba, Mistral Nemo, Mistral Small, Pixtral
- [OpenAI](https://platform.openai.com/settings/organization/general): DALL-E 2, DALL-E 3, GPT-3.5 Turbo, GPT-4, GPT-4 Turbo, GPT-4.1, GPT-4.1 mini, GPT-4.1 nano, GPT-4.5 preview, GPT-4o, GPT-4o mini, o1, o1-mini, o3-mini, o4-mini

If valid, the API keys will be saved in a **.env** file in the project root directory, and Gila will read them as environmental variables.

## Build the Executable

To create a standalone executable file, make sure the virtual environment is activated and PyInstaller is installed, then run the following command in the root directory:

```shell
pyinstaller build.spec
```

This will create a gila.exe file in the *dist* directory. Remember to copy the **storage** folder into the same directory as the executable before distributing it.
