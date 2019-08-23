from src.shared.base_server_connection import BaseServerConnection
from src.shared.Consts import *

from panda3d import core

import sys
from datetime import datetime

g_server_connection = None
g_main_window = None

class ServerConnection(BaseServerConnection):
    
    def get_identity(self):
        return CLIENT_NET_ASSISTANT
        
    def handle_datagram(self, dgi, msg_type):
        if msg_type == MSG_SERVER_GET_ALL_TABLETS_RESP:
            g_main_window.handle_get_all_tablets_resp(dgi)
        elif msg_type == MSG_SERVER_GET_ALL_USERS_RESP:
            g_main_window.handle_get_all_users_resp(dgi)
        
from PyQt5 import QtWidgets, QtCore, QtGui

class ClientWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        from src.netclient.net_mainwindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.clock_timer = QtCore.QTimer()
        self.clock_timer.timeout.connect(self.__update_clock)
        self.clock_timer.setSingleShot(False)
        self.clock_timer.start(0)
        
        self.ui.userView = self.ui.tabletView_2
        self.ui.userView.cellDoubleClicked.connect(self.__handle_double_click_user_cell)
        
        self.blink_second = 0
        self.blink_state = 0
        
        self.please_wait_dialog = None
        
        self.__request_all_tablets()
        self.__request_all_users()
        
    def __request_all_tablets(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_GET_ALL_TABLETS)
        g_server_connection.send(dg)
        
    def __request_all_users(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_GET_ALL_USERS)
        g_server_connection.send(dg)
        
    def show_please_wait(self):
        self.hide_please_wait()
        
        self.please_wait_dialog = QtWidgets.QMessageBox(self)
        self.please_wait_dialog.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        self.please_wait_dialog.setText("Please wait...")
        self.please_wait_dialog.setWindowTitle("Information")
        self.please_wait_dialog.exec()
        
    def hide_please_wait(self):
        if self.please_wait_dialog:
            self.please_wait_dialog.close()
        self.please_wait_dialog = None
        
    def __handle_double_click_user_cell(self, row, column):
        print("Editing row", row)
        userView = self.ui.tabletView_2
        firstName = userView.item(row, 0).text()
        lastName = userView.item(row, 1).text()
        name = firstName + " " + lastName
        
        print("Requesting edit for", name)
        
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_EDIT_USER)
        dg.add_string(name) # We will search active directory by name
        g_server_connection.send(dg)
        
        self.show_please_wait()
        
    def update_student_row(self, i, dgi):
        userView = self.ui.tabletView_2
        
        name = dgi.get_string()
        firstLast = name.split(" ", 1)
        firstName = firstLast[0]
        lastName = firstLast[1]
        grade = dgi.get_string()
        email = dgi.get_string()
        pcsb_agreement = dgi.get_uint8()
        cat_agreement = dgi.get_uint8()
        insurance_paid = dgi.get_uint8()
        insurance_amount = dgi.get_string()
        cat_student = dgi.get_uint8()
        tablet_pcsb_tag = dgi.get_string()
        
        userView.setItem(i, 0, QtWidgets.QTableWidgetItem(firstName))
        userView.setItem(i, 1, QtWidgets.QTableWidgetItem(lastName))
        userView.setItem(i, 2, QtWidgets.QTableWidgetItem(email))
        userView.setItem(i, 3, QtWidgets.QTableWidgetItem(grade))
        userView.setItem(i, 4, QtWidgets.QTableWidgetItem(str(cat_student)))
        userView.setItem(i, 5, QtWidgets.QTableWidgetItem(tablet_pcsb_tag))
        userView.setItem(i, 6, QtWidgets.QTableWidgetItem(str(pcsb_agreement)))
        userView.setItem(i, 7, QtWidgets.QTableWidgetItem(str(cat_agreement)))
        userView.setItem(i, 8, QtWidgets.QTableWidgetItem(str(insurance_paid)))
        userView.setItem(i, 9, QtWidgets.QTableWidgetItem(insurance_amount))
        
    def handle_get_all_users_resp(self, dgi):
        userView = self.ui.tabletView_2
        
        # Clear existing rows
        userView.setRowCount(0)
        
        num_users = dgi.get_uint16()
        for i in range(num_users):
            userView.insertRow(i)
            self.update_student_row(i, dgi)
        
    def handle_get_all_tablets_resp(self, dgi):
        # Clear existing rows
        self.ui.tabletView.setRowCount(0)
        
        num_assigned_tablets = dgi.get_uint16()
        for i in range(num_assigned_tablets):
            pcsb = dgi.get_string()
            device = dgi.get_string()
            serial = dgi.get_string()
            issue = "No Issue"#dgi.get_string()
            name = dgi.get_string()
            
            self.ui.tabletView.insertRow(i)
            self.ui.tabletView.setItem(i, 0, QtWidgets.QTableWidgetItem(pcsb))
            self.ui.tabletView.setItem(i, 1, QtWidgets.QTableWidgetItem(device))
            self.ui.tabletView.setItem(i, 2, QtWidgets.QTableWidgetItem(serial))
            self.ui.tabletView.setItem(i, 3, QtWidgets.QTableWidgetItem(issue))
            self.ui.tabletView.setItem(i, 4, QtWidgets.QTableWidgetItem(name))
            
        num_unassigned_tablets = dgi.get_uint16()
        for i in range(num_unassigned_tablets):
            pcsb = dgi.get_string()
            device = dgi.get_string()
            serial = dgi.get_string()
            issue = "No Issue"
            name = "Unassigned"
            
            self.ui.tabletView.insertRow(i)
            self.ui.tabletView.setItem(i, 0, QtWidgets.QTableWidgetItem(pcsb))
            self.ui.tabletView.setItem(i, 1, QtWidgets.QTableWidgetItem(device))
            self.ui.tabletView.setItem(i, 2, QtWidgets.QTableWidgetItem(serial))
            self.ui.tabletView.setItem(i, 3, QtWidgets.QTableWidgetItem(issue))
            self.ui.tabletView.setItem(i, 4, QtWidgets.QTableWidgetItem(name))
        
    def __get_block(self, now):
        now_time = now.time()
        block_ranges = {
            "1"     : ("7:10 AM", "8:40 AM"),
            "2"     : ("8:45 AM", "10:15 AM"),
            "Lunch" : ("10:15 AM", "10:45 AM"),
            "3"     : ("10:50 AM", "12:20 PM"),
            "4"     : ("12:25 PM", "1:55 PM")
        }
        
        block = "None"
        for blockName, startEnd in block_ranges.items():
            startDt = datetime.strptime(startEnd[0], "%I:%M %p").time()
            endDt = datetime.strptime(startEnd[1], "%I:%M %p").time()
            if now_time >= startDt and now_time < endDt:
                block = blockName
                break
                
        return block
        
    def __update_clock(self):
        now = datetime.now()
        if self.blink_state:
            time_str = now.strftime("%I:%M %p")
        else:
            time_str = now.strftime("%I %M %p")
            
        self.ui.timeLabel.setText("Time: %s" % time_str)
        
        if now.second != self.blink_second:
            self.blink_state = not self.blink_state
            self.blink_second = now.second
            
        self.ui.blockLabel.setText("Block: %s" % self.__get_block(now))

class NetClientApp(QtWidgets.QApplication):
    
    def __init__(self):
        QtWidgets.QApplication.__init__(self, [])
        
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

app = NetClientApp()
sys.exit(app.exec_())
