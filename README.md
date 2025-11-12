# Desktop Cleaner

## Project Title and Description
**Desktop Cleaner** is a desktop application built using PySide6 that provides tools to manage files on a computer. The application allows users to delete or move files based on their extensions, helping keep the desktop and file system organized.

## Features
- **Move Files by Extension:** Allows users to select a source and destination folder to move files of a specific type.
- **Delete Files by Extension:** Provides the ability to delete all files of a selected type across the system or in a specific directory.
- **File Type Details:** Displays information about the selected file type, including a brief description.
- **Queue-Based Operating Model:** Performs file operations in the background without freezing the UI, leveraging PyQt's QThread for smooth operation.

## Installation and Setup
To run the Desktop Cleaner, ensure you have Python (version 3.6 or higher) and Pip installed. Then, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/desktop-cleaner.git
   ```
2. Navigate to the project directory:
   ```bash
   cd desktop-cleaner
   ```
3. Install the required modules:
   ```bash
   pip install PySide6
   ```

## Basic Usage
To start using the application, simply run the main script:
```bash
python main.py
```
This will open the Desktop Cleaner GUI, where you can choose file operations.

## Configuration
There are no specific configuration files or environment variables required for this application. However, ensure the operating system has permissions to delete or move files.

## Contributing Guidelines
Contributions to the Desktop Cleaner project are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes and push the branch to your fork.
4. Open a pull request detailing your changes.

Please ensure your code is well-documented and adheres to the existing code style.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



