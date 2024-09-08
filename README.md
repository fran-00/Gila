# GILA - AI Chatbot

This is an AI chatbot client made with Python and PySide6.
Currently supported large language models:

- GPT-4o
- GPT-4o mini
- GPT-4
- GPT-4 Turbo
- Gemini 1.0 Pro
- Gemini 1.5 Pro
- Gemini 1.5 Flash
- Command
- Command R
- Command R+
- Mistral Large
- Mistral Nemo

Currently supported text-to-image models:

- DALL-E-2
- DALL-E-3

## How to set up development environment

To run from source, you'll need Python 3.12 and Git installed in your system. You'll also need some API Keys, but we'll cover it up later. Clone this project:

```shell
git clone https://github.com/fran-00/gila.git
```

On Windows create a new virtual environment with venv and activate it:

```shell
py -m venv venv
venv/Scripts/Activate.ps1
```

Install project's required packages via pip:

```shell
pip install -r requirements.txt
```

Now you need an OpenAI, Google and Cohere API Keys. Once you got them, store them on a *.env* file like this:

```python
COHERE_API_KEY='XXXXXXX'
GOOGLE_API_KEY='XXXXXXX'
OPENAI_API_KEY='XXXXXXX'
MISTRAL_API_KEY='XXXXXXX'
```

Put this file on the project root dir and you're ready! Now you can run the program as a Python package:

```shell
py -m gila
```

## How to build the .exe file

On the root directory (with the virtual environment activated and PyInstaller installed):

```shell
pyinstaller build.spec
```

The command used to create the spec file was this:

```shell
 pyinstaller cli.py --onefile --name gila --add-data="storage/saved_settings.json:." --add-data="storage/assets:."
```

You will find **gila.exe** executable file inside *dist* directory: remember to copy *storage* folder there before distributing it!

## Notes

APIs do have rate limits. To know more:

- [OpenAI](https://platform.openai.com/docs/guides/rate-limits/rate-limits)
- [Gemini Models](https://ai.google.dev/models/gemini)

## TODO List

- [x] Add a Menu on the left side of screen to adjust settings (model and temperature) and start a new chat
- [x] Sidebar must be hideable.
- [x] Add a way to load API keys and create a .json file to store them
- [x] Check Internet connection before every request to API, show a modal if client is not connected. Or/and change the color of chatlog to grey.
- [x] Ensure that model is disconnected from client on window closing.
- [x] Add a loading view on startup.
- [x] Add the ability to continue a conversation and a list of past chat to ui.
- [x] Add custom exceptions to handle as many kind of server's request errors as possible.
- [x] Prompt line must be a QTextEdit widget instead of a QLineEdit widget.
- [x] If user wants to export the current conversation, they must be able to choose file format between .txt, .docx and .pdf.
- [x] User must not be able to send another prompt if the program is waiting for API response and there must be a "waiting" symbol, like a spinning wheel.
- [x] User must be able to choose response length.
- [x] Last used settings must be saved to an external file for future use, like the current llm, temperature and maximum number of tokens.
- [x] Add the ability to change the lenght of the response.
- [x] Add a token counter, at least for OpenAI. Use [tiktoken](https://github.com/openai/tiktoken).
- [x] User must be able to rename stored chats.
- [x] Chatlog must show the number of token used.
- [x] Find a way to exit the main thread if the chat is taking too long to respond.
- [ ] Fix the gila monster image visible when opening the program not remaining aligned to the center when the window is resized.
- [ ] Add specific settings for images generation models like Dall-E 2 and 3 ([size, quality and quantity](https://platform.openai.com/docs/guides/images/generations)).
- [ ] Add logic to display model-generated images directly in the chat log.

## Future changes

- Add chat formatting.
- Add Anthropic and Meta to AI clients.
- Fix .pdf files created when chat is exported.
- Add a way for the app to search for updates from the main branch of the repo using [gitpython](https://gitpython.readthedocs.io/en/stable/)?
- Add image generation to AI Clients that supports it and internal image rendering with Pillow.
- Improve errors and exceptions management.
- Main thread must stop if API is taking too long to respond to prevent GUI freezing.
