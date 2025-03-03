from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QFontDatabase, QIcon, QPixmap
from PySide6.QtWidgets import (
    QGridLayout, 
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSplashScreen,
    QWidget,
)

from .status_bar import StatusBar
from .tool_bar import ToolBar
from .chat_log import Chat
from .sidebar.parent_sidebar import Sidebar
from .modals import (
    AboutGilaModal,
    AddAPIKeyModal,
    ManageAPIKeysModal,
    UpdateFoundModal,
    WarningModal,
)
from .utils import FileHandler as FH


class LoadingScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap("storage/assets/img/loading_screen.png"))


class View(QMainWindow):
    window_closed_signal_to_controller = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gila")
        self.setWindowIcon(QIcon("storage/assets/icons/gila_logo.svg"))
        self.resize(1024, 768)
        self.load_custom_fonts()
        self.setStyleSheet(self.load_css_file())
        self.create_layout()

    def create_layout(self):
        """Create the layout for the main window and composes the user interface.

        This method initializes the central widget and sets up various UI components 
        such as the status bar, toolbar, sidebar, chat area, and modals. It arranges 
        these components in a grid layout within the central widget of the main window.

        Notes:
            - The chat log and prompt line are initially hidden.
        """
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.status_bar = StatusBar(self)
        self.toolbar = ToolBar(self)
        self.sidebar = Sidebar(self)
        self.chat = Chat(self)
        self.add_api_key_modal = AddAPIKeyModal(self)
        self.manage_api_keys_modal = ManageAPIKeysModal(self)
        self.warning_modal = WarningModal(self)
        self.about_gila_modal = AboutGilaModal(self)
        self.update_found_modal = UpdateFoundModal(self)
        self.file_handler = FH(self)
        self.addToolBar(self.toolbar)
        self.setStatusBar(self.status_bar)
        main_layout = QGridLayout(central_widget)
        main_layout.addWidget(self.sidebar.widget_container, 0, 0)
        main_layout.addWidget(self.on_toggle_sidebar_button(), 0, 1)
        main_layout.addWidget(self.chat.widget_container, 0, 2, 1, 3)
        self.on_hide_chatlog_and_prompt_line()

    def on_toggle_sidebar_button(self):
        """Create and configure the button for toggling the sidebar.

        Initializes a QPushButton with a left arrow icon to indicate the action
        of toggling the sidebar. It sets fixed width and size policy for the
        button and connects its click event to the `toggle_sidebar` method.
        """
        self.toggle_sidebar_button = QPushButton("‹", objectName="toggle_sidebar_button")
        self.toggle_sidebar_button.setFixedWidth(10)
        self.toggle_sidebar_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toggle_sidebar_button.clicked.connect(self.toggle_sidebar)
        return self.toggle_sidebar_button

    def toggle_sidebar(self):
        """Toggle the visibility of the sidebar.

        This method checks the current visibility state of the sidebar's widget
        container and sets its visibility to the opposite state and updates
        the text of the toggle sidebar button to indicate the current action.
        """
        self.sidebar.widget_container.setVisible(not self.sidebar.widget_container.isVisible())
        if self.sidebar.widget_container.isVisible():
            self.toggle_sidebar_button.setText("‹")
        else:
            self.toggle_sidebar_button.setText("›")

    def load_css_file(self):
        """Load CSS file to apply styles to the window.

        Returns:
            str: The contents of the CSS file as a string.
        """
        return FH.load_file("storage/assets/css/styles.css", encoding="utf-8")

    def on_hide_chatlog_and_prompt_line(self):
        """Hide the chat log and prompt box.

        This method is called to hide both the chat log and the prompt layout in
        the user interface.
        """
        self.chat.on_hide_chatlog()
        self.chat.prompt_layout.on_hide_prompt_layout()

    def on_show_chatlog_and_prompt_line(self):
        """Show the chat log and prompt box.

        This method is called to display both the chat log and the prompt layout in the 
        user interface
        """
        self.chat.on_show_chatlog()
        self.chat.prompt_layout.on_show_prompt_layout()

    @Slot(str)
    def add_api_key_modal_slot(self, client_name):
        """ Slot
        Connected to one signal:
            - controller.missing_api_key_to_view

        This method is also called by the view's manage_api_keys_modal, passing
        the client name as an argument. When triggered, it sets the client name
        for the modal, updates the modal labels, and shows AddAPIKeyModal.
        """
        self.add_api_key_modal.client_name = client_name
        self.add_api_key_modal.update_modal_labels()
        self.add_api_key_modal.exec_()

    def closeEvent(self, event):
        """Handle the event when the window is closed.

        Overrides the default close event behavior. It emits a signal to the
        controller indicating that the window has been closed, allowing it to
        perform the cleanup and the state management. After emitting the signal, 
        it calls the superclass's close event method to ensure proper handling
        of the close event.

        Parameters:
            event (QCloseEvent): The close event object containing information
                                 about the event.
        """
        super().closeEvent(event)
        self.window_closed_signal_to_controller.emit()

    def assign_css_class(self, widget, class_name):
        """Assign a CSS class to a specified widget.

        Sets the given CSS class name to the specified widget's
        property, allowing for styling to be applied based on the class.

        Parameters:
            widget (QWidget): The widget to which the CSS class will be assigned.
            class_name (str): The name of the CSS class to apply to the widget.
        """
        widget.setProperty("class", class_name)

    def load_custom_fonts(self):
        """Load custom fonts into the application's font database."""
        QFontDatabase.addApplicationFont("storage/assets/fonts/BrunoAceSC-Regular.ttf")
        QFontDatabase.addApplicationFont("storage/assets/fonts/Geologica-VariableFont.ttf")
