# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.toolButton_2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout.addWidget(self.toolButton_2)
        self.checkBox_drive_letter = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_drive_letter.setChecked(False)
        self.checkBox_drive_letter.setObjectName("checkBox_drive_letter")
        self.horizontalLayout.addWidget(self.checkBox_drive_letter)
        self.checkBox_folder_path = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_folder_path.setChecked(True)
        self.checkBox_folder_path.setObjectName("checkBox_folder_path")
        self.horizontalLayout.addWidget(self.checkBox_folder_path)
        self.checkBox_file_name = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_file_name.setChecked(True)
        self.checkBox_file_name.setObjectName("checkBox_file_name")
        self.horizontalLayout.addWidget(self.checkBox_file_name)
        self.checkBox_suffix = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_suffix.setChecked(True)
        self.checkBox_suffix.setObjectName("checkBox_suffix")
        self.horizontalLayout.addWidget(self.checkBox_suffix)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(False)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setDefaultSectionSize(300)
        self.tableView.horizontalHeader().setMinimumSectionSize(80)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.checkBox_drive_letter.clicked.connect(MainWindow.check_box_changed)
        self.checkBox_suffix.clicked.connect(MainWindow.check_box_changed)
        self.checkBox_folder_path.clicked.connect(MainWindow.check_box_changed)
        self.checkBox_file_name.clicked.connect(MainWindow.check_box_changed)
        self.toolButton.clicked.connect(MainWindow.save)
        self.toolButton_2.clicked.connect(MainWindow.clear_list)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setText(_translate("MainWindow", "Save"))
        self.toolButton_2.setText(_translate("MainWindow", "List clear"))
        self.checkBox_drive_letter.setText(_translate("MainWindow", "Drive letter"))
        self.checkBox_folder_path.setText(_translate("MainWindow", "Folder path"))
        self.checkBox_file_name.setText(_translate("MainWindow", "File name"))
        self.checkBox_suffix.setText(_translate("MainWindow", "Suffix"))
