import os
import shutil
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QRadioButton,QCheckBox,QLineEdit,QButtonGroup,QComboBox,QMessageBox,QFileDialog
from PySide6.QtGui import QFont,QIcon
from PySide6.QtCore import Qt,QThread,Signal
import random
import glob

class FileDeleter(QThread):
    deletion_done = Signal(int)  
    error_occurred = Signal(str) 

    def __init__(self, extension):
        super().__init__()
        self.extension = extension

    def run(self):
        try:
            files_to_delete = glob.glob(f"C:\\**\\*{self.extension}", recursive=True) if os.name == "nt" else glob.glob(f"/**/*{self.extension}", recursive=True)

            if not files_to_delete:
                self.error_occurred.emit(f"No {self.extension} files found on the system.")
                return

            deleted_count = 0
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

            self.deletion_done.emit(deleted_count)

        except Exception as e:
            self.error_occurred.emit(str(e))


class FileMover(QThread):
    move_done = Signal(int)  
    error_occurred = Signal(str) 

    def __init__(self, extension, destination_path, search_directory=None):
        super().__init__()
        self.extension = extension
        self.destination_path = destination_path
        self.search_directory = search_directory or (os.path.expanduser("~") if os.name != "nt" else "C:\\")

    def run(self):
        try:
            search_pattern = os.path.join(self.search_directory, f"**/*{self.extension}")
            files_to_move = glob.glob(search_pattern, recursive=True)

            if not files_to_move:
                self.error_occurred.emit(f"No {self.extension} files found in {self.search_directory}.")
                return

            move_count = 0
            for file_path in files_to_move:
                try:
                    if os.path.abspath(file_path) == os.path.abspath(self.destination_path):
                        continue  # Avoid moving files into the same folder

                    shutil.move(file_path, self.destination_path)
                    move_count += 1
                except Exception as e:
                    self.error_occurred.emit(f"Failed to move {file_path}: {str(e)}")

            self.move_done.emit(move_count)

        except Exception as e:
            self.error_occurred.emit(str(e))





class Desktop_Cleaner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Tools")

        layout1 = QVBoxLayout()
        

        title_label = QLabel("Desktop Tools")

        title_label.setAlignment(Qt.AlignHCenter)
        font1 = QFont("Monteserrat",20)

        font1.setUnderline(True)
        layout1.addWidget(title_label)
        layout1.addStretch(1)

        title_label.setFont(font1)
        label1 = QLabel("Select your Extension:")

        

        font2 = QFont("Pacifico",10)
        label1.setFont(font2)
        layout1.addWidget(label1)

        layout1.addStretch(1)
        self.extension_combo = QComboBox(self)
        self.extension_combo.addItems([".py",".java",".sql",".jpeg",".png",".jpg",".mp4",".mp3",".pdf",".docx",".pptx",".xlsx",".txt",".html",".css",".js",".cpp",".c",".java",".jar",".xml",".json",".csv",".blend"])
        layout1.addWidget(self.extension_combo)
        Move_Button = QPushButton("Move files by type")
        Delete_all_Button = QPushButton("Delete Files by type")
        What_Button = QPushButton("File type details")
        Move_Button.clicked.connect(self.move_files)
        Delete_all_Button.clicked.connect(self.delete_all_files)
        What_Button.clicked.connect(self.what_files)
       
        layout1.addStretch(1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(Move_Button)
        button_layout.addWidget(Delete_all_Button)
        button_layout.addWidget(What_Button)
        layout1.addLayout(button_layout)
        layout1.addStretch(1)
        Move_all = QPushButton("Move all files")
        Delete_directory = QPushButton("Delete Selected files")
        Move_all.clicked.connect(self.move_all_files)
        Delete_directory.clicked.connect(self.delete_files)
        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(Move_all)
        button_layout2.addWidget(Delete_directory)  
        layout1.addLayout(button_layout2) 

        layout1.addStretch(15)


        self.setLayout(layout1)
        self.setMinimumSize(800,700)


    
    def move_files(self):
        try:
            source_path = QFileDialog.getExistingDirectory(self,"Choose source folder")
            destination_path = QFileDialog.getExistingDirectory(self,"Choose destination folder")
            if not source_path and not destination_path:
                QMessageBox.critical(self,"Error","Select source and destination path")
            
            elif not source_path:
                QMessageBox.critical(self,"Error","Select source path")
            
            elif not destination_path:
                QMessageBox.critical(self,"Error","Select destination path")

            elif destination_path == source_path:
                QMessageBox.critical(self,"Error","Source and destination path cannot be the same")

            else:
                reply = QMessageBox.question(self, 'Move Files', 'Do you want to proceed with moving the files?',
                                 QMessageBox.Ok | QMessageBox.Cancel)
                
                if reply == QMessageBox.Ok:
                    extension = self.extension_combo.currentText()
                    files_moved = 0 
                    for file in os.listdir(source_path):
                        if file.endswith(extension):
                            destination_file = os.path.join(destination_path, file)
                            if os.path.exists(destination_file):
                                base, ext = os.path.splitext(file)
                                new_file = f"{base}_{str(random.randint(1, 100))}{ext}"
                                destination_file = os.path.join(destination_path, new_file)
                            shutil.move(os.path.join(source_path, file), destination_file)
                            files_moved += 1

                    if files_moved > 0:
                        QMessageBox.information(self, "Success", f"{files_moved} files moved successfully")
                    else:
                        QMessageBox.information(self, "Information", "No files with the selected extension were found to move.")
               
                else:
                    QMessageBox.information(self, "Information", "Operation Cancelled")


        except Exception as e:
            QMessageBox.critical(self,"Error",f"An error occured: {e}")




    def delete_all_files(self):
        try:
            extension = self.extension_combo.currentText()
            reply = QMessageBox.question(
                self, "Confirm Deletion",
                f"Are you sure you want to delete all {extension} files across the system?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.No:
                QMessageBox.information(self, "Cancelled", "Operation cancelled.")
                return

            self.deleter = FileDeleter(extension)

            self.deleter.deletion_done.connect(self.on_deletion_complete)
            self.deleter.error_occurred.connect(self.show_error)
            self.deleter.start()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def on_deletion_complete(self, count):
        QMessageBox.information(self, "Success", f"Deleted {count} files successfully!")

    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)



    def what_files(self):

        extension = self.extension_combo.currentText()
        descriptions = {
        ".py": "Python script file",
        ".java": "Java source code file",
        ".sql": "SQL database script",
        ".jpeg": "JPEG image file",
        ".png": "Portable Network Graphics image file",
        ".jpg": "JPEG image file",
        ".mp4": "MPEG-4 video file",
        ".mp3": "MP3 audio file",
        ".pdf": "Portable Document Format file",
        ".docx": "Microsoft Word document",
        ".pptx": "Microsoft PowerPoint presentation",
        ".xlsx": "Microsoft Excel spreadsheet",
        ".txt": "Plain text file",
        ".html": "HTML web page file",
        ".css": "Cascading Style Sheets file",
        ".js": "JavaScript file",
        ".cpp": "C++ source code file",
        ".c": "C source code file",
        ".jar": "Java ARchive file",
        ".xml": "XML data file",
        ".json": "JSON data file",
        ".csv": "Comma-separated values file",
        ".blend": "Blender 3D data file"
    }

        description = descriptions.get(extension, "Unknown file extension")
        QMessageBox.information(None, "File Extension Description", f"{extension}: {description}")


    def move_all_files(self):
        try:
            extension = self.extension_combo.currentText()
            destination = QFileDialog.getExistingDirectory(self, "Choose destination folder")
            reply = QMessageBox.question(
                self, "Confirm Move",
                f"Are you sure you want to move all {extension} files across the system?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.No:
                QMessageBox.information(self, "Cancelled", "Operation cancelled.")
                return

            self.move1 = FileMover(extension,destination)

            self.move1.move_done.connect(self.on_move_complete1)
            self.move1.error_occurred.connect(self.show_error1)
    
            self.move1.start()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def on_move_complete1(self, count):
        QMessageBox.information(self, "Success", f"Moved {count} files successfully!")
    
    def show_error1(self, message):
        QMessageBox.warning(self, "Error", message)

    def delete_files(self):
        extension = self.extension_combo.currentText()
        directory = QFileDialog.getExistingDirectory(self, "Choose directory to delete files")
        if not directory:
            QMessageBox.critical(self, "Error", "No directory selected.")
            return

        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete all files with extension '{extension}' in {directory}?",
            QMessageBox.Yes | QMessageBox.No
            )

        if reply == QMessageBox.No:
            QMessageBox.information(self, "Cancelled", "Operation cancelled.")
            return

    
        files = os.listdir(directory)
        files_to_delete = [file for file in files if file.endswith(f"{extension}")]

        if not files_to_delete:
            QMessageBox.information(self, "No Files Found", f"No files found with the extension '{extension}'.")
            return

        try:
            for file in files_to_delete:
                os.remove(os.path.join(directory, file))
                QMessageBox.information(self, "Success", "Files deleted successfully.")
        
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while deleting files: {str(e)}")