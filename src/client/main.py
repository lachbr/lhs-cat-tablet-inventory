import sys

from panda3d import core

from src.shared.Consts import *

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore

g_server_connection = None
g_main_window = None

class ServerConnection:
    
    def __init__(self, address, port):
        self.mgr = core.QueuedConnectionManager()
        self.reader = core.QueuedConnectionReader(self.mgr, 1)
        self.writer = core.ConnectionWriter(self.mgr, 1)
        self.address = address
        self.port = port
        
        self.connection = self.mgr.open_TCP_client_connection(self.address, self.port, 0)
        if not self.connection:
            print("ERROR: Can't connect")
            sys.exit(1)
        self.reader.add_connection(self.connection)
        self.identify()
        
    def send(self, dg):
        self.writer.send(dg, self.connection)
        
    def identify(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_IDENTIFY)
        dg.add_uint8(CLIENT_STUDENT)
        self.writer.send(dg, self.connection)
        
    def __check_datagrams(self):
        if self.reader.data_available():
            dg = core.Datagram()
            if self.reader.get_data(dg):
                self.handle_datagram(dg)
                
    def handle_datagram(self, dg):
        dgi = core.DatagramIterator(dg)
        
        msg_type = dgi.get_uint16()
        
        if msg_type == MSG_SERVER_LOOKUP_TABLET_RESP:
            g_main_window.handle_lookup_tablet_response(dgi)
        
    def run(self):
        self.__check_datagrams()
        
class ClientWindow(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        
        from src.client.client_issuereport import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.submitBtn.pressed.connect(self.__handle_press_submit)
        self.ui.pcsbTagTextBox.returnPressed.connect(self.__handle_pcsbtag_submit)
        
    def __handle_pcsbtag_submit(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_LOOKUP_TABLET)
        dg.add_string(self.ui.pcsbTagTextBox.text())
        g_server_connection.send(dg)
        
        self.ui.pcsbTagTextBox.setEnabled(False)
        
    def handle_lookup_tablet_response(self, dgi):
        valid = dgi.getUint8()
        if valid:
            serialNo = dgi.get_string()
            deviceModel = dgi.get_string()
            studentName = dgi.get_string()
            grade = dgi.get_string()
            
            self.ui.serialNoTextBox.setText(serialNo)
            self.ui.deviceModelTextBox.setText(deviceModel)
            self.ui.nameTextBox.setText(studentName)
            self.ui.gradeTextBox.setText(grade)
        else:
            QMessageBox.critical(self, "Tablet Not Found", "That PCSB Tag (bar code) was not found in our database.")
            self.__reset()
        
    def __handle_press_submit(self):
        QMessageBox.information(self, "Submitted",
            "Thank you for submitting your issue. The Net Assistants will get your tablet back to you as soon as possible.")
            
        self.__reset()
        
    def __reset(self):
        self.ui.descTextEntry.setText("")
        self.ui.descTextEntry.setEnabled(False)
        
        self.ui.problemsTextEntry.setText("")
        self.ui.problemsTextEntry.setEnabled(False)
        
        self.ui.dateEntry.setEnabled(False)
        
        self.ui.nameTextBox.setText("")
        self.ui.nameTextBox.setEnabled(False)
        
        self.ui.gradeTextBox.setText("")
        self.ui.gradeTextBox.setEnabled(False)        
        
        self.ui.serialNoTextBox.setText("")
        self.ui.serialNoTextBox.setEnabled(False)
        
        self.ui.deviceModelTextBox.setText("")
        self.ui.deviceModelTextBox.setEnabled(False)
        
        self.ui.pcsbTagTextBox.setText("")
        self.ui.pcsbTagTextBox.setEnabled(True)
        self.ui.pcsbTagTextBox.setFocus()
        
    def __handle_submit_dialog_ack(self, r):
        print("Ack")
        
class ClientApp(QApplication):

    def __init__(self):
        QApplication.__init__(self, [])
        
        global g_server_connection
        global g_main_window
        
        self.server_connection = ServerConnection('127.0.0.1', 7035)
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
