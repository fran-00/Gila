from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QLabel,
    QWidget,
    QVBoxLayout,
)


class ImageSettingsWidget(QWidget):

    settings_changed_signal = Signal()

    def __init__(self, parent_handler):
        super().__init__()
        self.parent_handler = parent_handler
        self._build_layout()

    def _build_layout(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.Alignment.AlignTop)
        self._build_img_size_settings()

    def _build_img_size_settings(self):
        """Widget to adjust img size settings"""
        # Create inner widget and layout to contain img size settings
        self.img_size_w = QWidget()
        box_v = QVBoxLayout(self.img_size_w)
        box_v.setContentsMargins(0, 0, 0, 0)
        # Create img size lbl
        select_img_size_lbl = QLabel("Image Size")
        self.parent_handler.parent_sidebar.window.assign_css_class(
            select_img_size_lbl, "setting_name"
        )
        select_img_size_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create widget's button group with all checkboxes
        self.size_group = QButtonGroup(self)
        self.size_group.setExclusive(True)
        self.checkbox_256x256 = QCheckBox("256x256")
        self.checkbox_512x512 = QCheckBox("512x512")
        self.checkbox_1024x1024 = QCheckBox("1024x1024")
        self.checkbox_1024x1792 = QCheckBox("1024x1792")
        self.checkbox_1792x1024 = QCheckBox("1792x1024")
        self.size_group.addButton(self.checkbox_256x256)
        self.size_group.addButton(self.checkbox_512x512)
        self.size_group.addButton(self.checkbox_1024x1024)
        self.size_group.addButton(self.checkbox_1024x1792)
        self.size_group.addButton(self.checkbox_1792x1024)
        # Add lbl and checkboxes to img size inner layout
        box_v.addWidget(select_img_size_lbl)
        box_v.addWidget(self.checkbox_256x256)
        box_v.addWidget(self.checkbox_512x512)
        box_v.addWidget(self.checkbox_1024x1024)
        box_v.addWidget(self.checkbox_1024x1792)
        box_v.addWidget(self.checkbox_1792x1024)
        # Add img size inner widget to main layout
        self.layout.addWidget(self.img_size_w)
