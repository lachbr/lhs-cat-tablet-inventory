# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_issuereport.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(908, 718)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.studentInfoGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.studentInfoGroup.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.studentInfoGroup.setFont(font)
        self.studentInfoGroup.setObjectName("studentInfoGroup")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.studentInfoGroup)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.nameLabel = QtWidgets.QLabel(self.studentInfoGroup)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.verticalLayout_3.addWidget(self.nameLabel)
        self.nameTextBox = QtWidgets.QLineEdit(self.studentInfoGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameTextBox.sizePolicy().hasHeightForWidth())
        self.nameTextBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameTextBox.setFont(font)
        self.nameTextBox.setReadOnly(True)
        self.nameTextBox.setObjectName("nameTextBox")
        self.verticalLayout_3.addWidget(self.nameTextBox)
        self.gradeLabel = QtWidgets.QLabel(self.studentInfoGroup)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.gradeLabel.setFont(font)
        self.gradeLabel.setObjectName("gradeLabel")
        self.verticalLayout_3.addWidget(self.gradeLabel)
        self.gradeTextBox = QtWidgets.QLineEdit(self.studentInfoGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gradeTextBox.sizePolicy().hasHeightForWidth())
        self.gradeTextBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.gradeTextBox.setFont(font)
        self.gradeTextBox.setReadOnly(True)
        self.gradeTextBox.setObjectName("gradeTextBox")
        self.verticalLayout_3.addWidget(self.gradeTextBox)
        self.emailLabel = QtWidgets.QLabel(self.studentInfoGroup)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.emailLabel.setFont(font)
        self.emailLabel.setObjectName("emailLabel")
        self.verticalLayout_3.addWidget(self.emailLabel)
        self.emailTextBox = QtWidgets.QLineEdit(self.studentInfoGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emailTextBox.sizePolicy().hasHeightForWidth())
        self.emailTextBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.emailTextBox.setFont(font)
        self.emailTextBox.setReadOnly(True)
        self.emailTextBox.setObjectName("emailTextBox")
        self.verticalLayout_3.addWidget(self.emailTextBox)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.gridLayout_5.addWidget(self.studentInfoGroup, 0, 1, 1, 1)
        self.tabletInfoGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.tabletInfoGroup.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tabletInfoGroup.setFont(font)
        self.tabletInfoGroup.setObjectName("tabletInfoGroup")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabletInfoGroup)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pcsbTagLabel = QtWidgets.QLabel(self.tabletInfoGroup)
        self.pcsbTagLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pcsbTagLabel.setFont(font)
        self.pcsbTagLabel.setScaledContents(False)
        self.pcsbTagLabel.setIndent(-1)
        self.pcsbTagLabel.setObjectName("pcsbTagLabel")
        self.verticalLayout_2.addWidget(self.pcsbTagLabel)
        self.pcsbTagTextBox = QtWidgets.QLineEdit(self.tabletInfoGroup)
        self.pcsbTagTextBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pcsbTagTextBox.sizePolicy().hasHeightForWidth())
        self.pcsbTagTextBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pcsbTagTextBox.setFont(font)
        self.pcsbTagTextBox.setObjectName("pcsbTagTextBox")
        self.verticalLayout_2.addWidget(self.pcsbTagTextBox)
        self.serialNoLabel = QtWidgets.QLabel(self.tabletInfoGroup)
        self.serialNoLabel.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.serialNoLabel.setFont(font)
        self.serialNoLabel.setScaledContents(False)
        self.serialNoLabel.setIndent(-1)
        self.serialNoLabel.setObjectName("serialNoLabel")
        self.verticalLayout_2.addWidget(self.serialNoLabel)
        self.serialNoTextBox = QtWidgets.QLineEdit(self.tabletInfoGroup)
        self.serialNoTextBox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serialNoTextBox.sizePolicy().hasHeightForWidth())
        self.serialNoTextBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.serialNoTextBox.setFont(font)
        self.serialNoTextBox.setReadOnly(True)
        self.serialNoTextBox.setObjectName("serialNoTextBox")
        self.verticalLayout_2.addWidget(self.serialNoTextBox)
        self.deviceModelLabel = QtWidgets.QLabel(self.tabletInfoGroup)
        self.deviceModelLabel.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.deviceModelLabel.setFont(font)
        self.deviceModelLabel.setScaledContents(False)
        self.deviceModelLabel.setIndent(-1)
        self.deviceModelLabel.setObjectName("deviceModelLabel")
        self.verticalLayout_2.addWidget(self.deviceModelLabel)
        self.deviceModelTextBox = QtWidgets.QLineEdit(self.tabletInfoGroup)
        self.deviceModelTextBox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceModelTextBox.sizePolicy().hasHeightForWidth())
        self.deviceModelTextBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.deviceModelTextBox.setFont(font)
        self.deviceModelTextBox.setReadOnly(True)
        self.deviceModelTextBox.setObjectName("deviceModelTextBox")
        self.verticalLayout_2.addWidget(self.deviceModelTextBox)
        self.gridLayout_4.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.tabletInfoGroup, 0, 0, 1, 1)
        self.issueReportGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.issueReportGroup.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.issueReportGroup.setFont(font)
        self.issueReportGroup.setObjectName("issueReportGroup")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.issueReportGroup)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.dateEntry = QtWidgets.QDateEdit(self.issueReportGroup)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateEntry.setFont(font)
        self.dateEntry.setCalendarPopup(True)
        self.dateEntry.setObjectName("dateEntry")
        self.gridLayout_6.addWidget(self.dateEntry, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.issueReportGroup)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_6.addWidget(self.label_8, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.issueReportGroup)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_6.addWidget(self.label_7, 5, 0, 1, 1)
        self.descTextEntry = QtWidgets.QTextEdit(self.issueReportGroup)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.descTextEntry.setFont(font)
        self.descTextEntry.setObjectName("descTextEntry")
        self.gridLayout_6.addWidget(self.descTextEntry, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.issueReportGroup)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)
        self.problemsTextEntry = QtWidgets.QTextEdit(self.issueReportGroup)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.problemsTextEntry.setFont(font)
        self.problemsTextEntry.setObjectName("problemsTextEntry")
        self.gridLayout_6.addWidget(self.problemsTextEntry, 6, 0, 1, 1)
        self.submitBtn = QtWidgets.QPushButton(self.issueReportGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submitBtn.sizePolicy().hasHeightForWidth())
        self.submitBtn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.submitBtn.setFont(font)
        self.submitBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.submitBtn.setAutoExclusive(False)
        self.submitBtn.setObjectName("submitBtn")
        self.gridLayout_6.addWidget(self.submitBtn, 7, 0, 1, 1, QtCore.Qt.AlignRight)
        self.gridLayout_5.addWidget(self.issueReportGroup, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout_5)
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetButton.sizePolicy().hasHeightForWidth())
        self.resetButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.resetButton.setFont(font)
        self.resetButton.setObjectName("resetButton")
        self.verticalLayout.addWidget(self.resetButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.studentInfoGroup.setTitle(_translate("MainWindow", "Student Info"))
        self.nameLabel.setText(_translate("MainWindow", "Name"))
        self.gradeLabel.setText(_translate("MainWindow", "Grade"))
        self.emailLabel.setText(_translate("MainWindow", "E-Mail Address"))
        self.tabletInfoGroup.setTitle(_translate("MainWindow", "Tablet Info"))
        self.pcsbTagLabel.setText(_translate("MainWindow", "PCSB Tag (Bar Code)"))
        self.serialNoLabel.setText(_translate("MainWindow", "Serial No."))
        self.deviceModelLabel.setText(_translate("MainWindow", "Device Model"))
        self.issueReportGroup.setTitle(_translate("MainWindow", "Issue Report"))
        self.label_8.setText(_translate("MainWindow", "Date of Incident"))
        self.label_7.setText(_translate("MainWindow", "Problems?"))
        self.label_6.setText(_translate("MainWindow", "Description of Incident"))
        self.submitBtn.setText(_translate("MainWindow", "Submit"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))