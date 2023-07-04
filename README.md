# Easy_Backup
A Windows application to help you to backup files from your device


Easy Backup is a simple Python-based application using Tkinter for a Graphical User Interface (GUI). It allows for backing up files and directories of your choice to another location on your computer.

## Prerequisites
Before running Easy Backup, you need to have Python installed on your machine. You can download the latest version of Python from the official website.

Next, you need to install the necessary dependencies using pip, Python's package manager. The dependencies are:

-  tkinter
-  shutil
-  os
-  customtkinter
-  ttkthemes

You can install all these dependencies by using the following command in your terminal:

`pip install tk customtkinter ttkthemes`

## Usage
To use Easy Backup, first clone this repository by using the following command:

`git clone https://github.com/CorentinBzi/Easy_Backup.git`

Then change into the project directory:

`cd easy_backup`

Then, you can run the application by using the following command:

`python Easy_Backup.py`

### Features
Select folders to backup: You can select the folder or folders you want to backup by clicking the "Select" button. Alternatively, you can use the "Select by default" button to automatically select the user's "Documents" folder.

Select backup folder: You can select the folder where you want your files to be backed up to by clicking the "Select" button.

Perform backup: Once you have selected the folder to backup and the backup folder, you can click the "Perform backup" button to start the backup. The application displays a progress bar indicating the backup's progress.

Error handling: If an error occurs while copying a file, it's shown to the user, but the backup continues.

#### Support
If you encounter any issues with the application or have any questions, feel free to open an issue on GitHub.
