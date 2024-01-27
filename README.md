# AI Chatbot

## How to set up development environment

To run from source, you'll need Python 3.12 and Git installed in your system. You'll also need some API Keys, but we'll cover it up later. Clone this project:

        https://github.com/fran-00/metis.git

On Windows create a new virtual environment with venv and activate it:

        py -m venv venv
        venv/Scripts/Activate.ps1

Install project's required packages via pip:

        pip install -r requirements.txt

Now you need an OpenAI API Key and a Google API Key. Once you got them, store them on a *.env* file like this:

        OPENAI_API_KEY="XXXXXXX"
        GOOGLE_API_KEY="XXXXXXX"

Put this file inside ai folder and you're ready! Run the program:

        py main.py

## Notes

APIs do have rate limits. To know more:

- [OpenAI](https://platform.openai.com/docs/guides/rate-limits/rate-limits)
- [Gemini Models](https://ai.google.dev/models/gemini)

## TODO List

- [ ] Add a Pop Up Menu on the left side of screen to adjust settings
