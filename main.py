import sys

from PySide6.QtWidgets import QApplication

from core.model import Model, MainThread
from core.view import View
from core.controller import Controller
from ai.openai import OpenAIClient
from ai.google import GoogleClient
from ai.cohere import CohereClient


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()
    client = CohereClient()
    # client = GoogleClient("gemini-pro")
    # client = OpenAIClient("gpt-3.5-turbo")
    model = Model(client)
    thread = MainThread(model)
    controller = Controller(view, model, thread)
    view.show()

    sys.exit(app.exec())
