
from PySide6.QtWidgets import QApplication
import sys
from tools import Desktop_Cleaner



app = QApplication(sys.argv)
window = Desktop_Cleaner()

window.show()
app.exec()








