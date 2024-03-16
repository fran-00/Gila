from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton

from .parent_modal import Modal


class ChangeSettingsModal(Modal):
    selected_client_to_controller = Signal(str)

    def __init__(self, window, current_settings):
        super().__init__(window)
        self.setWindowTitle("Modifica Impostazioni")
        self.current_settings = current_settings
        self.on_modal_layout()

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.modal_text = QLabel("Modifica le impostazioni, saranno applicate all'avvio di una nuova chat.")
        self.modal_text.setWordWrap(True)
        self.modal_layout.addWidget(self.modal_text)
        self.modal_layout.addWidget(self.on_llms_combobox())
        self.modal_layout.addWidget(self.on_confirm_button())

    def on_llms_combobox(self):
        """ Creates ComboBox with llms list """
        self.llms_combobox = QComboBox()
        for llm in self.current_settings.llms:
            self.llms_combobox.addItem(llm)
        self.llms_combobox.currentIndexChanged.connect(
            self.on_combobox_changed)
        return self.llms_combobox

    def on_combobox_changed(self):
        pass

    def on_confirm_button(self):
        """ Creates button to confirm llm selection """
        confirm_button = QPushButton("Conferma")
        confirm_button.clicked.connect(self.send_selected_client_to_controller)
        confirm_button.clicked.connect(self.accept)
        return confirm_button

    def send_selected_client_to_controller(self):
        """ Sends selected llm to controller: signal is triggered when Confirm
            Button is pressed
        """
        selected_llm = self.llms_combobox.currentText()
        self.selected_client_to_controller.emit(selected_llm)
