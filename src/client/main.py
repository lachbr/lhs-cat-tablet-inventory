import sys

from panda3d import core
core.load_prc_file_data('', 'tcp-header-size 4')

from src.shared.Consts import *
from src.shared.base_server_connection import BaseServerConnection
from src.shared.base_tablet import BaseTablet
from src.shared.student import Student
from src.shared import utils

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore, QtWidgets

g_server_connection = None
g_main_window = None

class ServerConnection(BaseServerConnection):
    
    def get_identity(self):
        return CLIENT_STUDENT
                
    def handle_datagram(self, dgi, msg_type):
        if msg_type == MSG_SERVER_LOOKUP_TABLET_RESP:
            g_main_window.handle_lookup_tablet_response(dgi)
        elif msg_type == MSG_SERVER_NET_ASSISTANTS_RESP:
            g_main_window.handle_net_assistants_resp(dgi)
        
class ClientWindow(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        
        from src.client.client_issuereport import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.submitBtn.pressed.connect(self.__handle_press_submit)
        self.ui.pcsbTagTextBox.returnPressed.connect(self.__handle_pcsbtag_submit)
        self.ui.resetButton.pressed.connect(self.__reset)
        
        self.please_wait_dialog = QtWidgets.QMessageBox(self)
        self.please_wait_dialog.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        self.please_wait_dialog.setText("Please wait...")
        self.please_wait_dialog.setWindowTitle("Information")
        self.please_wait_dialog.open()
        
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_REQ_NET_ASSISTANTS)
        g_server_connection.send(dg)
        
        self.hws = []
        
    def handle_net_assistants_resp(self, dgi):
        num_hws = dgi.get_uint32()
        for i in range(num_hws):
            hw = Student.from_datagram(dgi)
            self.hws.append(hw)
            
        hwnames = []
        for hw in self.hws:
            self.ui.hwCombo.addItem(hw.name)
            hwnames.append(hw.name)
        completer = QtWidgets.QCompleter(hwnames)
        completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.ui.hwCombo.setEditable(True)
        self.ui.hwCombo.setCompleter(completer)
            
        self.please_wait_dialog.done(0)
        self.please_wait_dialog = None
        self.__reset()
        
    def __handle_pcsbtag_submit(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_LOOKUP_TABLET)
        dg.add_string(self.ui.pcsbTagTextBox.text())
        g_server_connection.send(dg)
        
        self.ui.pcsbTagTextBox.setReadOnly(True)
        
    def handle_lookup_tablet_response(self, dgi):
        valid = dgi.get_uint8()
        if valid:
            tablet = BaseTablet.from_datagram(dgi)
            student_name = dgi.get_string()
            student_grade = dgi.get_string()
            student_email = dgi.get_string()
            
            self.ui.serialNoTextBox.setText(tablet.serial)
            self.ui.deviceModelTextBox.setText(tablet.device_model)
            self.ui.nameTextBox.setText(student_name)
            self.ui.gradeTextBox.setText(student_grade)
            self.ui.emailTextBox.setText(student_email)
            
            self.ui.pcsbTagTextBox.setReadOnly(True)
            self.ui.serialNoLabel.setEnabled(True)
            self.ui.serialNoTextBox.setEnabled(True)
            self.ui.deviceModelLabel.setEnabled(True)
            self.ui.deviceModelTextBox.setEnabled(True)
            
            self.ui.studentInfoGroup.setEnabled(True)
            self.ui.issueReportGroup.setEnabled(True)
        else:
            QMessageBox.critical(self, "Tablet Not Found", "That PCSB Tag (bar code) was not found in our database.")
            self.__reset()
        
    def __handle_press_submit(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_SUBMIT_ISSUE)
        dg.add_string(self.ui.pcsbTagTextBox.text())
        dg.add_string(self.ui.descTextEntry.toPlainText())
        dg.add_string(self.ui.dateEntry.text())
        dg.add_string(self.ui.problemsTextEntry.toPlainText())
        
        hws = [hw for hw in self.hws if hw.name == self.ui.hwCombo.currentText()]
        hw = hws[0] if len(hws) > 0 else None
        if hw:
            print("HW who submitted:", hw.guid)
            dg.add_string(hw.guid)
        else:
            dg.add_string("")
            
        g_server_connection.send(dg)
        
        QMessageBox.information(self, "Submitted",
            "Thank you for submitting your issue. The Net Assistants will get your tablet back to you as soon as possible.")
            
        self.__reset()
        
    def __reset(self):
        self.ui.tabletInfoGroup.setEnabled(True)
        self.ui.pcsbTagTextBox.setText("")
        self.ui.pcsbTagTextBox.setEnabled(True)
        self.ui.pcsbTagTextBox.setReadOnly(False)
        self.ui.pcsbTagTextBox.setFocus()
        self.ui.serialNoTextBox.setEnabled(False)
        self.ui.serialNoTextBox.setText("")
        self.ui.serialNoLabel.setEnabled(False)
        self.ui.deviceModelTextBox.setEnabled(False)
        self.ui.deviceModelTextBox.setText("")
        self.ui.deviceModelLabel.setEnabled(False)
        
        self.ui.studentInfoGroup.setEnabled(False)
        self.ui.nameTextBox.setText("")
        self.ui.gradeTextBox.setText("")     
        self.ui.emailTextBox.setText("")
        
        self.ui.dateEntry.setDate(utils.get_qdate(utils.get_date_string()))
        
        self.ui.issueReportGroup.setEnabled(False)
        self.ui.descTextEntry.setText("")
        self.ui.problemsTextEntry.setText("")
        
    def __handle_submit_dialog_ack(self, r):
        print("Ack")
        
class ClientApp(QApplication):

    def __init__(self):
        QApplication.__init__(self, [])
        
        global g_server_connection
        global g_main_window
        
        host = 'c2031svcat2'
        self.server_connection = ServerConnection(host, 7035)
        # Timer which ticks the connection to the server
        self.server_timer = QtCore.QTimer()
        self.server_timer.timeout.connect(self.server_connection.run)
        self.server_timer.setSingleShot(False)
        self.server_timer.start(0)
        
        g_server_connection = self.server_connection
        
        self.window = ClientWindow()
        self.window.show()
        
        g_main_window = self.window

app = ClientApp()
sys.exit(app.exec_())
