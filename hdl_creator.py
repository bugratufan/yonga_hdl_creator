from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QDesktopWidget, QPushButton, \
    QFormLayout, QLabel, QComboBox, QSpinBox, QGroupBox, QVBoxLayout, QDialogButtonBox, QDialog, QMessageBox
from PyQt5.QtGui import QIcon
import json
import os
import sys
import getpass

config_user = "Bugra Tufan"
config_mail = "bugra.tufan@yongatek.com"
config_project = "ISTIF"
config_last_dir = ""
config_recent_dir = 5*[""]
print(config_recent_dir)
user_fileName = ""
user_componentName = ""
user_fileDir = ""

def updateConfig():
    data = {}
    data["user"] = config_user
    data["mail"] = config_mail
    data["project"] = config_project
    data["last_dir"] = config_last_dir
    if(config_last_dir not in config_recent_dir):
        data["recent_dir"] = [config_last_dir, config_recent_dir[0], config_recent_dir[1], config_recent_dir[2], config_recent_dir[3] ]
    else:
        data["recent_dir"] = config_recent_dir
    f = open("user_config.json", "w")
    f.write(json.dumps(data))
    f.close()

def getConfig():
    global config_user, config_mail, config_project, config_last_dir, config_recent_dir

    try:
        f = open("user_config.json", "r")
        x = f.read()
        y = json.loads(x)
        f.close()
        config_user = y["user"]
        config_mail = y["mail"]
        config_project = y["project"]
        config_last_dir = y["last_dir"]
        config_recent_dir = y["recent_dir"]

    except:
        f = open("user_config.json", "w")
        f.write('{ "user":"Bugra Tufan", "mail":"bugra.tufan@yongatek.com", "project":"ISTIF", "last_dir":"", "recent_dir":["", "", "", "", ""]}')
        f.close()


def create_vhdl_header(user, mail, project, file):
    vhdl_header = '''
-- ================================================================================
--         __   __   ___    _   _    ____      _      _____   _____   _  __
--         \ \ / /  / _ \  | \ | |  / ___|    / \    |_   _| | ____| | |/ /
--          \ V /  | | | | |  \| | | |  _    / _ \     | |   |  _|   | ' /
--           | |   | |_| | | |\  | | |_| |  / ___ \    | |   | |___  | . \\
--           |_|    \___/  |_| \_|  \____| /_/   \_\   |_|   |_____| |_|\_\\
-- ================================================================================
-- (C) COPYRIGHT 2020 YongaTek (Yonga Technology Microelectronics)
-- All rights reserved.
-- This file contains confidential and proprietary information of YongaTek and
-- is protected under international copyright and other intellectual property laws.
-- ================================================================================
-- Creator: ''' + getpass.getuser() + '''
-- Generated by Yonga HDL Creator
-- ================================================================================
-- Project           : ''' + project + '''
-- File ID           : ''' + file + '''
-- Design Unit Name  :
-- Description       :
-- Comments          :
-- Revision          : %%
-- Last Changed Date : %%
-- Last Changed By   : %%
-- Designer
--          Name     : ''' + user + '''
--          E-mail   : ''' + mail + '''
-- ================================================================================
'''
    return vhdl_header

def create_vlog_header(user, mail, project, file):
    verilog_header = '''
// ================================================================================
//         __   __   ___    _   _    ____      _      _____   _____   _  __
//         \ \ / /  / _ \  | \ | |  / ___|    / \    |_   _| | ____| | |/ /
//          \ V /  | | | | |  \| | | |  _    / _ \     | |   |  _|   | ' /
//           | |   | |_| | | |\  | | |_| |  / ___ \    | |   | |___  | . \\
//           |_|    \___/  |_| \_|  \____| /_/   \_\   |_|   |_____| |_|\_\\
// ================================================================================
// (C) COPYRIGHT 2020 YongaTek (Yonga Technology Microelectronics)
// All rights reserved.
// This file contains confidential and proprietary information of YongaTek and
// is protected under international copyright and other intellectual property laws.
// ================================================================================
// Project           : ''' + project + '''
// File ID           : ''' + file + '''
// Design Unit Name  :
// Description       :
// Comments          :
// Revision          : %%
// Last Changed Date : %%
// Last Changed By   : %%
// Designer
//          Name     : ''' + user + '''
//          E-mail   : ''' + mail + '''
// ================================================================================
'''

def enarch(projectName):
    vhdl_enarch = '''
entity '''+ projectName + ''' is
port (
);
end entity;

architecture arch of ''' + projectName +  ''' is

begin

end architecture;
'''
    return vhdl_enarch

def component_enarch(projectName):
    component='''
library IEEE;
use IEEE.Std_Logic_1164.all;
use IEEE.numeric_std.all;

package ''' + projectName + '''_comp is
    component '''+projectName+''' is
        port (
        );
    end component;
end package;
'''
    return component

def create_vhdl_files():
    f = open(user_fileDir+"/"+user_componentName+".vhd", "w", encoding="utf-8")
    f.write(create_vhdl_header(config_user,config_mail,config_project, user_componentName) + enarch(user_componentName))
    f.close()
    print(user_fileDir+"/"+user_componentName+".vhd", ": VHDL file created!")
    f = open(user_fileDir+"/"+user_componentName + "_comp.vhd", "w", encoding="utf-8")
    f.write(create_vhdl_header(config_user,config_mail,config_project, user_componentName+"_comp") + component_enarch(user_componentName))
    f.close()
    print(user_fileDir+"/"+user_componentName + "_comp.vhd", ": VHDL file created!")

class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Dialog, self).__init__()
        self.createFormGroupBox()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.resize(400, 300)
        self.setWindowTitle("Yonga HDL File Creator")

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("File Features")
        layout = QFormLayout()
        self.qt_fileName = QLineEdit(user_componentName+".vhd")
        self.qt_fileName.setReadOnly(True)
        self.qt_componentName = QLineEdit(user_componentName)
        self.qt_componentName.setReadOnly(True)
        self.qt_name = QLineEdit(config_user)
        self.qt_mail = QLineEdit(config_mail)
        self.qt_projectName = QLineEdit(config_project)
        layout.addRow(QLabel("File Name:"), self.qt_fileName)
        layout.addRow(QLabel("Component Name:"), self.qt_componentName)
        layout.addRow(QLabel("Name:"), self.qt_name)
        layout.addRow(QLabel("Mail:"), self.qt_mail)
        layout.addRow(QLabel("Project Name:"), self.qt_projectName)
        #layout.addRow(QLabel("Country:"), QComboBox())
        #layout.addRow(QLabel("Age:"), QSpinBox())
        self.formGroupBox.setLayout(layout)
    def accept(self):
        global config_user, config_project, config_mail
        print("accept")
        config_user = (self.qt_name.text())
        config_mail = (self.qt_mail.text())
        config_project = (self.qt_projectName.text())
        updateConfig()
        create_vhdl_files()
        QMessageBox.about(self, "Successful!", "File OK!")
        exit()
    def reject(self):
        print("File is not created!")
        QMessageBox.about(self, "Aborted!", "Files cannot created!")
        exit()


def getFileName(path):
    global user_fileDir
    user_fileDir, tail = os.path.split(path)
    return tail

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Yonga HDL File Creator'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        getConfig()
        self.saveFileDialog()

        # self.openFileNamesDialog()
        # self.saveFileDialog()
        self.show()


    def saveFileDialog(self):
        global config_last_dir, user_fileName, user_componentName
        getConfig()
        dialog = QFileDialog()
        options = dialog.Options()
        options |= dialog.DontUseNativeDialog
        QFileDialog.setHistory(dialog, config_recent_dir)
        fileName, oth = dialog.getSaveFileName(self, "Yonga HDL File Creator", config_last_dir, "VHDL  (*.vhd);;Verilog (*.v)", options=options)
        if fileName:
            config_last_dir = os.path.dirname(fileName)
            user_fileName, file_extension = os.path.splitext(fileName)
            updateConfig()
            if(file_extension == ""):
                if(oth == "VHDL (*.vhd)"):
                    user_componentName = getFileName(user_fileName)
                    user_fileName = user_fileName + ".vhd"

                    dlg = Dialog()
                    dlg.exec_()
                elif(oth == "Verilog (*.v)"):
                    user_componentName = getFileName(user_fileName)
                    user_fileName = user_fileName + ".v"
                    dlg = Dialog()
                    dlg.exec_()
            elif(file_extension == ".vhd" or file_extension == ".v"):
                user_componentName = getFileName(user_fileName)
                user_fileName = fileName
                dlg = Dialog()
                dlg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    #sys.exit(app.exec_())