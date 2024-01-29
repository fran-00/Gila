from PySide6.QtWidgets import QVBoxLayout, QPushButton, QComboBox
from PySide6.QtCore import QObject, Signal, Slot



class Sidebar(QObject):
    sidebar_signal_to_controller = Signal(tuple)

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.llms = None
        self.llms_combobox = QComboBox()

    def on_sidebar_layout(self):
        sidebar_layout = QVBoxLayout(objectName="sidebar_layout")
        # sidebar_layout.addWidget(self.on_llms_combobox())
        # sidebar_layout.addWidget(self.on_confirm_button())
        return sidebar_layout

    @Slot(tuple)
    def handle_received_signal(self, data):
        print(data)
        self.llms = data

    def on_combobox_changed(self):
        pass

    def set_client(self):
        selected_llm = self.llms_combobox.currentText()
        return self.llms.get(selected_llm)

    def on_llms_combobox(self):
        for llm in self.llms:
            self.llms_combobox.addItem(llm)
        self.llms_combobox.currentIndexChanged.connect(self.on_combobox_changed)
        return self.llms_combobox

    def on_confirm_button(self):
        confirm_button = QPushButton("Conferma", self)
        confirm_button.clicked.connect(self.set_client)
        return confirm_button
