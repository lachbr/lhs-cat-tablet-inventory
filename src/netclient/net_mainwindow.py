# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'net_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1078, 798)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout_3.addWidget(self.radioButton, 0, 0, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout_3.addWidget(self.radioButton_2, 1, 0, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout_3.addWidget(self.radioButton_3, 0, 1, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout_3.addWidget(self.radioButton_4, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.searchEntry = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchEntry.sizePolicy().hasHeightForWidth())
        self.searchEntry.setSizePolicy(sizePolicy)
        self.searchEntry.setBaseSize(QtCore.QSize(0, 0))
        self.searchEntry.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.searchEntry.setObjectName("searchEntry")
        self.verticalLayout_2.addWidget(self.searchEntry)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabletView = QtWidgets.QTableWidget(self.groupBox_2)
        self.tabletView.setRowCount(0)
        self.tabletView.setColumnCount(5)
        self.tabletView.setObjectName("tabletView")
        item = QtWidgets.QTableWidgetItem()
        self.tabletView.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView.setHorizontalHeaderItem(4, item)
        self.verticalLayout_3.addWidget(self.tabletView)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_6)
        self.radioButton_5.setChecked(True)
        self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout_4.addWidget(self.radioButton_5, 0, 0, 1, 1)
        self.radioButton_6 = QtWidgets.QRadioButton(self.groupBox_6)
        self.radioButton_6.setObjectName("radioButton_6")
        self.gridLayout_4.addWidget(self.radioButton_6, 1, 0, 1, 1)
        self.radioButton_7 = QtWidgets.QRadioButton(self.groupBox_6)
        self.radioButton_7.setObjectName("radioButton_7")
        self.gridLayout_4.addWidget(self.radioButton_7, 0, 1, 1, 1)
        self.radioButton_8 = QtWidgets.QRadioButton(self.groupBox_6)
        self.radioButton_8.setObjectName("radioButton_8")
        self.gridLayout_4.addWidget(self.radioButton_8, 1, 1, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox_6)
        self.facultySearchEntry = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.facultySearchEntry.sizePolicy().hasHeightForWidth())
        self.facultySearchEntry.setSizePolicy(sizePolicy)
        self.facultySearchEntry.setBaseSize(QtCore.QSize(0, 0))
        self.facultySearchEntry.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.facultySearchEntry.setObjectName("facultySearchEntry")
        self.verticalLayout_5.addWidget(self.facultySearchEntry)
        self.verticalLayout_6.addWidget(self.groupBox_5)
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabletView_2 = QtWidgets.QTableWidget(self.groupBox_4)
        self.tabletView_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabletView_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tabletView_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabletView_2.setRowCount(0)
        self.tabletView_2.setColumnCount(10)
        self.tabletView_2.setObjectName("tabletView_2")
        item = QtWidgets.QTableWidgetItem()
        self.tabletView_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView_2.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView_2.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView_2.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView_2.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabletView_2.setHorizontalHeaderItem(9, item)
        self.verticalLayout_4.addWidget(self.tabletView_2)
        self.verticalLayout_6.addWidget(self.groupBox_4)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 9, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.timeLabel = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.timeLabel.setFont(font)
        self.timeLabel.setObjectName("timeLabel")
        self.horizontalLayout.addWidget(self.timeLabel)
        self.blockLabel = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.blockLabel.setFont(font)
        self.blockLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.blockLabel.setObjectName("blockLabel")
        self.horizontalLayout.addWidget(self.blockLabel)
        self.gridLayout.addWidget(self.frame, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tablet Inventory - Net Assistants"))
        self.groupBox.setTitle(_translate("MainWindow", "Search"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Search By"))
        self.radioButton.setText(_translate("MainWindow", "PCSB Tag"))
        self.radioButton_2.setText(_translate("MainWindow", "Student/Faculty Name"))
        self.radioButton_3.setText(_translate("MainWindow", "Device Model"))
        self.radioButton_4.setText(_translate("MainWindow", "Serial Number"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Tablets"))
        item = self.tabletView.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "PCSB Tag"))
        item = self.tabletView.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Device Model"))
        item = self.tabletView.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Serial No."))
        item = self.tabletView.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Active Issue"))
        item = self.tabletView.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Assignee"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tablet Inventory"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Search"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Search By"))
        self.radioButton_5.setText(_translate("MainWindow", "Name"))
        self.radioButton_6.setText(_translate("MainWindow", "Tablet PCSB Tag"))
        self.radioButton_7.setText(_translate("MainWindow", "E-Mail Address"))
        self.radioButton_8.setText(_translate("MainWindow", "Grade"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Students/Faculty"))
        self.tabletView_2.setSortingEnabled(True)
        item = self.tabletView_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "First Name"))
        item = self.tabletView_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Last Name"))
        item = self.tabletView_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "E-Mail Address"))
        item = self.tabletView_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Grade"))
        item = self.tabletView_2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "In CAT"))
        item = self.tabletView_2.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Tablet PCSB Tag"))
        item = self.tabletView_2.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Internet Agreement"))
        item = self.tabletView_2.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "CAT Internet Agreement"))
        item = self.tabletView_2.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Insurance Paid"))
        item = self.tabletView_2.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Insurance Amount"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Students/Faculty"))
        self.timeLabel.setText(_translate("MainWindow", "Time: 8:46 AM"))
        self.blockLabel.setText(_translate("MainWindow", "Block: 1"))
