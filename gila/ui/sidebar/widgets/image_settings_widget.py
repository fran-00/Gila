from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QSlider,
    QWidget,
    QVBoxLayout,
)


class ImageSettingsWidget(QWidget):

    def __init__(self, parent_handler):
        super().__init__()
        self.parent_handler = parent_handler
        self._build_layout()

    def _build_layout(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.Alignment.AlignTop)
        self._build_img_size_settings()
        self.parent_handler.add_line_separator(self.layout)
        self._build_img_quality_settings()
        self._build_img_num_settings()

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

    def _build_img_quality_settings(self):
        """ Widget to adjust img quality settings """
        # Create inner widget and layout to contain img quality settings
        self.img_quality_w = QWidget()
        box_v = QVBoxLayout(self.img_quality_w)
        box_v.setContentsMargins(0, 0, 0, 0)
        # Create img quality lbl
        select_img_quality_lbl = QLabel("Image Quality")
        self.parent_handler.parent_sidebar.window.assign_css_class(
            select_img_quality_lbl, "setting_name"
        )
        select_img_quality_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create widget's button group with checkboxes
        self.quality_group = QButtonGroup(self)
        self.quality_group.setExclusive(True)
        self.checkbox_standard = QCheckBox("Standard")
        self.checkbox_hd = QCheckBox("HD")
        self.quality_group.addButton(self.checkbox_standard)
        self.quality_group.addButton(self.checkbox_hd)
        # Add lbl and checkboxes to img quality inner layout
        box_v.addWidget(select_img_quality_lbl)
        box_v.addWidget(self.checkbox_standard)
        box_v.addWidget(self.checkbox_hd)
        # Add img quality inner widget to main layout
        self.layout.addWidget(self.img_quality_w)

    def _build_img_num_settings(self):
        """ Widget to adjust img quantity settings """
        # Create inner widget and layout to contain max tokens settings
        self.img_num_w = QWidget()
        box_v = QVBoxLayout(self.img_num_w)
        box_v.setContentsMargins(0, 0, 0, 0)
        # Create max_tokens lbl
        select_img_num_lbl = QLabel("Number of images")
        self.parent_handler.parent_sidebar.window.assign_css_class(
            select_img_num_lbl, "setting_name"
        )
        select_img_num_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create widgets and slider's sub-layout
        img_num_slider_sub_h = QHBoxLayout()
        min_img_num_lbl = QLabel("1")
        max_img_num_lbl = QLabel("10")
        self.img_num_slider = QSlider(Qt.Horizontal)
        self.max_img_num_current_value_lbl = QLabel("1")
        self.parent_handler.parent_sidebar.window.assign_css_class(
            self.max_img_num_current_value_lbl, "current_value_lbl"
        )
        # Adjust lbls settings and width
        self.max_img_num_current_value_lbl.setAlignment(Qt.Alignment.AlignCenter)
        min_img_num_lbl.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_img_num_lbl.setFixedWidth(30)
        max_img_num_lbl.setFixedWidth(30)
        img_num_slider_sub_h.setStretchFactor(min_img_num_lbl, 0)
        img_num_slider_sub_h.setStretchFactor(self.img_num_slider, 1)
        img_num_slider_sub_h.setStretchFactor(max_img_num_lbl, 0)
        self.parent_handler.parent_sidebar.window.assign_css_class(
            min_img_num_lbl, "slider_value_lbl"
        )
        self.parent_handler.parent_sidebar.window.assign_css_class(
            max_img_num_lbl, "slider_value_lbl"
        )
        # Adjust slider's settings
        self.img_num_slider.setMinimum(1)
        self.img_num_slider.setMaximum(10)
        self.img_num_slider.setTickInterval(1)
        self.img_num_slider.setSingleStep(1)
        self.img_num_slider.valueChanged.connect(self._on_img_num_settings_changed)
        # Add widgets and slider to img quantity slider sub layout
        img_num_slider_sub_h.addWidget(min_img_num_lbl)
        img_num_slider_sub_h.addWidget(self.img_num_slider)
        img_num_slider_sub_h.addWidget(max_img_num_lbl)
        # Add lbl, slider sub layout and current value to max tokens inner layout
        box_v.addWidget(select_img_num_lbl)
        box_v.addLayout(img_num_slider_sub_h)
        box_v.addWidget(self.max_img_num_current_value_lbl)
        # Add temperture inner widget to main layout
        self.layout.addWidget(self.img_num_w)

    def _on_img_num_settings_changed(self):
        self.max_img_num_current_value_lbl.setText(str(self.img_num_slider.value()))

    def update_settings_when_model_changes(self):
        selected_size_button = self.size_group.checkedButton()
        if self.parent_handler.selected_llm in ["DALL-E 2"]:
            self.img_num_w.show()
            self.checkbox_256x256.show()
            self.checkbox_512x512.show()
            self.checkbox_1024x1792.hide()
            self.checkbox_1792x1024.hide()
            self.img_quality_w.hide()
            if selected_size_button in [self.checkbox_1024x1792, self.checkbox_1792x1024]:
                self.checkbox_1024x1024.setChecked(True)

        elif self.parent_handler.selected_llm in ["DALL-E 3"]:
            self.img_num_w.hide()
            self.checkbox_256x256.hide()
            self.checkbox_512x512.hide()
            self.checkbox_1024x1792.show()
            self.checkbox_1792x1024.show()
            self.img_quality_w.show()
            if selected_size_button in [self.checkbox_256x256, self.checkbox_512x512]:
                self.checkbox_1024x1024.setChecked(True)
