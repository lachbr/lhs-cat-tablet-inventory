# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'net_editissue.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 703)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.studentNameEdit = QtWidgets.QLineEdit(self.tab)
        self.studentNameEdit.setEnabled(False)
        self.studentNameEdit.setReadOnly(True)
        self.studentNameEdit.setObjectName("studentNameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.studentNameEdit)
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.hwTeamNameEdit = QtWidgets.QLineEdit(self.tab)
        self.hwTeamNameEdit.setEnabled(False)
        self.hwTeamNameEdit.setReadOnly(True)
        self.hwTeamNameEdit.setObjectName("hwTeamNameEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.hwTeamNameEdit)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.deviceModelEdit = QtWidgets.QLineEdit(self.tab)
        self.deviceModelEdit.setEnabled(False)
        self.deviceModelEdit.setReadOnly(True)
        self.deviceModelEdit.setObjectName("deviceModelEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.deviceModelEdit)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.serialNoEdit = QtWidgets.QLineEdit(self.tab)
        self.serialNoEdit.setEnabled(False)
        self.serialNoEdit.setReadOnly(True)
        self.serialNoEdit.setObjectName("serialNoEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.serialNoEdit)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.pcsbTagEdit = QtWidgets.QLineEdit(self.tab)
        self.pcsbTagEdit.setEnabled(False)
        self.pcsbTagEdit.setReadOnly(True)
        self.pcsbTagEdit.setObjectName("pcsbTagEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.pcsbTagEdit)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.doiEdit = QtWidgets.QLineEdit(self.tab)
        self.doiEdit.setEnabled(False)
        self.doiEdit.setReadOnly(True)
        self.doiEdit.setObjectName("doiEdit")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.doiEdit)
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.incidentDescEdit = QtWidgets.QTextEdit(self.tab)
        self.incidentDescEdit.setEnabled(False)
        self.incidentDescEdit.setReadOnly(True)
        self.incidentDescEdit.setObjectName("incidentDescEdit")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.incidentDescEdit)
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.problemsEdit = QtWidgets.QTextEdit(self.tab)
        self.problemsEdit.setEnabled(False)
        self.problemsEdit.setReadOnly(True)
        self.problemsEdit.setObjectName("problemsEdit")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.problemsEdit)
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.partsOrderedCheck = QtWidgets.QCheckBox(self.tab)
        self.partsOrderedCheck.setText("")
        self.partsOrderedCheck.setObjectName("partsOrderedCheck")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.partsOrderedCheck)
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.partsOrderedDateEdit = QtWidgets.QDateEdit(self.tab)
        self.partsOrderedDateEdit.setCalendarPopup(True)
        self.partsOrderedDateEdit.setObjectName("partsOrderedDateEdit")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.partsOrderedDateEdit)
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.partsExpectedDateEdit = QtWidgets.QDateEdit(self.tab)
        self.partsExpectedDateEdit.setCalendarPopup(True)
        self.partsExpectedDateEdit.setObjectName("partsExpectedDateEdit")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.partsExpectedDateEdit)
        self.insuranceRadio = QtWidgets.QRadioButton(self.tab)
        self.insuranceRadio.setObjectName("insuranceRadio")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.LabelRole, self.insuranceRadio)
        self.warrantyRadio = QtWidgets.QRadioButton(self.tab)
        self.warrantyRadio.setObjectName("warrantyRadio")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.warrantyRadio)
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(17, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.fixedEdit = QtWidgets.QTextEdit(self.tab)
        self.fixedEdit.setObjectName("fixedEdit")
        self.formLayout.setWidget(17, QtWidgets.QFormLayout.FieldRole, self.fixedEdit)
        self.returnedToStudentCheck = QtWidgets.QCheckBox(self.tab)
        self.returnedToStudentCheck.setText("")
        self.returnedToStudentCheck.setObjectName("returnedToStudentCheck")
        self.formLayout.setWidget(19, QtWidgets.QFormLayout.FieldRole, self.returnedToStudentCheck)
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(19, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(16, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.resolvedCheck = QtWidgets.QCheckBox(self.tab)
        self.resolvedCheck.setText("")
        self.resolvedCheck.setObjectName("resolvedCheck")
        self.formLayout.setWidget(16, QtWidgets.QFormLayout.FieldRole, self.resolvedCheck)
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.line)
        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.SpanningRole, self.line_2)
        self.line_3 = QtWidgets.QFrame(self.tab)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.formLayout.setWidget(18, QtWidgets.QFormLayout.SpanningRole, self.line_3)
        self.line_4 = QtWidgets.QFrame(self.tab)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.line_4)
        self.line_5 = QtWidgets.QFrame(self.tab)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.line_5)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.repairLogTable = QtWidgets.QTableWidget(self.tab_2)
        self.repairLogTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.repairLogTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.repairLogTable.setObjectName("repairLogTable")
        self.repairLogTable.setColumnCount(3)
        self.repairLogTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.repairLogTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.repairLogTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.repairLogTable.setHorizontalHeaderItem(2, item)
        self.repairLogTable.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_3.addWidget(self.repairLogTable, 0, 0, 1, 1)
        self.newStepButton = QtWidgets.QPushButton(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newStepButton.sizePolicy().hasHeightForWidth())
        self.newStepButton.setSizePolicy(sizePolicy)
        self.newStepButton.setObjectName("newStepButton")
        self.gridLayout_3.addWidget(self.newStepButton, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Issue"))
        self.label.setText(_translate("Dialog", "Student/Teacher Name"))
        self.label_13.setText(_translate("Dialog", "Hardware Team Member"))
        self.label_2.setText(_translate("Dialog", "Device Model"))
        self.label_3.setText(_translate("Dialog", "Serial No"))
        self.label_4.setText(_translate("Dialog", "PCSB Tag"))
        self.label_5.setText(_translate("Dialog", "Date of Incident"))
        self.label_6.setText(_translate("Dialog", "Description of Incident"))
        self.label_7.setText(_translate("Dialog", "Problems?"))
        self.label_8.setText(_translate("Dialog", "Parts Ordered?"))
        self.label_9.setText(_translate("Dialog", "Date Ordered"))
        self.label_10.setText(_translate("Dialog", "Date Expected"))
        self.insuranceRadio.setText(_translate("Dialog", "Insurance"))
        self.warrantyRadio.setText(_translate("Dialog", "Warranty"))
        self.label_11.setText(_translate("Dialog", "How was the tablet fixed?"))
        self.label_12.setText(_translate("Dialog", "Tablet returned to student?"))
        self.label_14.setText(_translate("Dialog", "Tablet is fixed?"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Broken Tablet Form"))
        self.repairLogTable.setSortingEnabled(False)
        item = self.repairLogTable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Date"))
        item = self.repairLogTable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Team Member"))
        item = self.repairLogTable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Steps Taken to Fix the Tablet"))
        self.newStepButton.setText(_translate("Dialog", "Log New Step"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Repair Log"))
