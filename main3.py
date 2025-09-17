import tempfile
import pathlib
from PySide6.QtCore import QUrl
import sys # exit app cleanly
from PySide6.QtWidgets import QApplication, QFileDialog, QPushButton, QVBoxLayout, QWidget # QApplication → runs the GUI event loop
from PySide6.QtWebEngineWidgets import QWebEngineView # QWebEngineView → displays your HTML page

# QObject, Slot → backend Python class that JS can call  
# QUrl → load local HTML into the app
from PySide6.QtCore import QObject, Slot, QUrl 
from PySide6.QtWebChannel import QWebChannel # QWebChannel → bridge between JS ↔ Python
import os # os → safely find files on disk

class Backend(QObject):
    @Slot(str, str)
    def receiveFile(self, filename, content):
        print(f"Received file: {filename}")
        print("Content:", content)

        thank_you_text = "Thank you for uploading your file!"

        # Write to a temporary file
        temp_file = pathlib.Path(tempfile.gettempdir()) / "thank_you.txt"
        temp_file.write_text(thank_you_text, encoding="utf-8")

        # Trigger download in QWebEngineView
        view.page().download(QUrl.fromLocalFile(str(temp_file)))
    @Slot()
    def downloadThankYouFile(self):
        thank_you_text = "Thank you for uploading your file!"
        temp_file = pathlib.Path(tempfile.gettempdir()) / "thank_you.txt"
        temp_file.write_text(thank_you_text, encoding="utf-8")
        view.page().download(QUrl.fromLocalFile(str(temp_file)))

# No need to import QWebEngineDownloadItem
def handle_download(download):
    # download is already a QWebEngineDownloadItem instance
    filename, _ = QFileDialog.getSaveFileName(
        None, "Save Thank You File", download.path(), "Text Files (*.txt)"
    )
    if filename:
        download.setPath(filename)
        download.accept()
    else:
        download.cancel()



# Utility to locate HTML
def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)



app = QApplication(sys.argv)

view = QWebEngineView()

# Set up the channel
channel = QWebChannel()
backend = Backend()
channel.registerObject("backend", backend)
view.page().setWebChannel(channel)

# Load HTML
html_file = resource_path('index.html')
view.load(QUrl.fromLocalFile(html_file))
view.show()

sys.exit(app.exec())