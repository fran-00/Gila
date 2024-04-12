import sys

from PySide6.QtWidgets import QApplication

from gila_updater.download_dialog import DownloadDialog


def main():
    app = QApplication(sys.argv)
    dialog = DownloadDialog()
    dialog.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
