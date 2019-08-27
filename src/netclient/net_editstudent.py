# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'net_editstudent.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(356, 170)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.pcsbAgreementCheckBox = QtWidgets.QCheckBox(Dialog)
        self.pcsbAgreementCheckBox.setObjectName("pcsbAgreementCheckBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pcsbAgreementCheckBox)
        self.catAgreementCheckBox = QtWidgets.QCheckBox(Dialog)
        self.catAgreementCheckBox.setObjectName("catAgreementCheckBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.catAgreementCheckBox)
        self.insuranceCheckBox = QtWidgets.QCheckBox(Dialog)
        self.insuranceCheckBox.setObjectName("insuranceCheckBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.insuranceCheckBox)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label)
        self.insuranceAmountEdit = QtWidgets.QLineEdit(Dialog)
        self.insuranceAmountEdit.setObjectName("insuranceAmountEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.insuranceAmountEdit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.tabletPCSBEdit = QtWidgets.QLineEdit(Dialog)
        self.tabletPCSBEdit.setObjectName("tabletPCSBEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.tabletPCSBEdit)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit Student"))
        self.pcsbAgreementCheckBox.setText(_translate("Dialog", "PCSB Internet Agreement"))
        self.catAgreementCheckBox.setText(_translate("Dialog", "CAT Internet Agreement"))
        self.insuranceCheckBox.setText(_translate("Dialog", "Insurance Paid"))
        self.label.setText(_translate("Dialog", "Insurance Amount"))
        self.insuranceAmountEdit.setPlaceholderText(_translate("Dialog", "Example: $75"))
        self.label_2.setText(_translate("Dialog", "Assigned Tablet"))
        self.tabletPCSBEdit.setPlaceholderText(_translate("Dialog", "Scan PCSB Tag (Bar Code) here"))
