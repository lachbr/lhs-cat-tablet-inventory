# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'net_newstep.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 179)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.buttonBox)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.stepsEdit = QtWidgets.QTextEdit(Dialog)
        self.stepsEdit.setObjectName("stepsEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.stepsEdit)
        self.teamMemberCombo = QtWidgets.QComboBox(Dialog)
        self.teamMemberCombo.setObjectName("teamMemberCombo")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.teamMemberCombo)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New Step"))
        self.label.setText(_translate("Dialog", "Steps Taken to Fix the Tablet"))
        self.label_2.setText(_translate("Dialog", "Team Member"))
