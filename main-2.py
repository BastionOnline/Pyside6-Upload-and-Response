import sys # exit app cleanly
from PySide6.QtWidgets import QApplication, QFileDialog # QApplication → runs the GUI event loop
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

        # Generate "thank you" text
        thank_you_text = "Thank you for uploading your file!"

        # Send it back to JS
        # Using `runJavaScript` to call the JS download function
        # view.page().runJavaScript(f'triggerDownload("thank_you.txt", {repr(thank_you_text)})')
        # view.page().runJavaScript(f'setThankYouFile({repr(thank_you_text)})')
        view.page().profile().downloadRequested.connect(handle_download)



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


# # Optional: intercept downloads to allow user to choose location
# def handle_download(download: QWebEngineDownloadItem):
#     filename, _ = QFileDialog.getSaveFileName(
#         None, "Save Thank You File", download.path(), "Text Files (*.txt)"
#     )
#     if filename:
#         download.setPath(filename)
#         download.accept()
#     else:
#         download.cancel()

def resource_path(relative_path):
    # checks if the script is running from a PyInstaller executable.
    if getattr(sys, 'frozen', False):
        # PyInstaller puts files in a temporary folder when frozen
        # sys._MEIPASS → the temporary folder where PyInstaller extracts HTML, CSS, JS, etc.
        base_path = sys._MEIPASS
    else:
        # Running normally in Python
        # used when running normally, so it still works outside of an exe.
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