import sys
import six
# rozwiązuje problem z bibliteka six
if not hasattr(six._SixMetaPathImporter, '_path'):
    six._SixMetaPathImporter._path = []
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":    main()
