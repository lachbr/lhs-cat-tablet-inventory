from src.shared.base_server_connection import BaseServerConnection
from src.shared.Consts import *

from panda3d import core

import sys
from datetime import datetime

from PyQt5 import QtWidgets, QtCore, QtGui

g_server_connection = None
g_main_window = None

T_SEARCHMODE_PCSB           = 0
T_SEARCHMODE_SERIAL         = 1
T_SEARCHMODE_DEVICE_MODEL   = 2
T_SEARCHMODE_NAME           = 3

U_SEARCHMODE_NAME           = 0
U_SEARCHMODE_TABLET_PCSB    = 1
U_SEARCHMODE_EMAIL          = 2
U_SEARCHMODE_GRADE          = 3

class ADTableWidgetItem(QtWidgets.QTableWidgetItem):

    def __init__(self, guid, text):
        QtWidgets.QTableWidgetItem.__init__(self, text)
        self.guid = guid

class ServerConnection(BaseServerConnection):
    
    def get_identity(self):
        return CLIENT_NET_ASSISTANT
        
    def handle_datagram(self, dgi, msg_type):
        if msg_type == MSG_SERVER_GET_ALL_TABLETS_RESP:
            g_main_window.handle_get_all_tablets_resp(dgi)
        elif msg_type == MSG_SERVER_GET_ALL_USERS_RESP:
            g_main_window.handle_get_all_users_resp(dgi)
        elif msg_type == MSG_SERVER_EDIT_USER_RESP:
            g_main_window.handle_edit_user_resp(dgi)
        elif msg_type == MSG_SERVER_EDIT_TABLET_RESP:
            g_main_window.handle_edit_tablet_resp(dgi)
        elif msg_type == MSG_SERVER_FINISH_EDIT_USER_RESP:
            g_main_window.handle_finish_edit_user_resp(dgi)
        elif msg_type == MSG_SERVER_UPDATE_USER:
            g_main_window.handle_update_user(dgi)

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
        self.ui.userView.itemDoubleClicked.connect(self.__handle_double_click_user_item)
        
        self.ui.tabletView.itemDoubleClicked.connect(self.__handle_double_click_tablet_item)
        
        self.ui.radio_user_name.toggled.connect(self.__toggle_radio_user_name)
        self.ui.radio_user_email.toggled.connect(self.__toggle_radio_user_email)
        self.ui.radio_user_grade.toggled.connect(self.__toggle_radio_user_grade)
        self.ui.radio_user_tablet_pcsb.toggled.connect(self.__toggle_radio_user_tablet_pcsb)
        self.ui.facultySearchEntry.textChanged.connect(self.__handle_user_search_edited)
        
        self.ui.radio_tablet_pcsb.toggled.connect(self.__toggle_radio_tablet_pcsb)
        self.ui.radio_tablet_serial.toggled.connect(self.__toggle_radio_tablet_serial)
        self.ui.radio_tablet_username.toggled.connect(self.__toggle_radio_tablet_username)
        self.ui.radio_tablet_devicemodel.toggled.connect(self.__toggle_radio_tablet_username)
        self.ui.searchEntry.textChanged.connect(self.__handle_tablet_search_edited)
        
        self.user_search_mode = U_SEARCHMODE_NAME
        self.tablet_search_mode = T_SEARCHMODE_PCSB
        
        self.blink_second = 0
        self.blink_state = 0
        
        self.edit_req_item = None
        self.editing_guid = None
        
        self.please_wait_dialog = None
        self.edit_dialog = None
        
        self.user_guid_names = {}
        
        self.__request_all_tablets()
        self.__request_all_users()
    
    def __handle_tablet_search_edited(self, text):
        self.filter_tablet_table()
        
    def __handle_user_search_edited(self, text):
        self.filter_user_table()
        
    ################################################################
        
    def __toggle_radio_user_name(self, flag):
        if flag:
            self.user_search_mode = U_SEARCHMODE_NAME
            self.filter_user_table()
    
    def __toggle_radio_user_email(self, flag):
        if flag:
            self.user_search_mode = U_SEARCHMODE_EMAIL
            self.filter_user_table()
            
    def __toggle_radio_user_grade(self, flag):
        if flag:
            self.user_search_mode = U_SEARCHMODE_GRADE
            self.filter_user_table()
    
    def __toggle_radio_user_tablet_pcsb(self, flag):
        if flag:
            self.user_search_mode = U_SEARCHMODE_TABLET_PCSB
            self.filter_user_table()
            
    ################################################################
            
    def __toggle_radio_tablet_pcsb(self, flag):
        if flag:
            self.tablet_search_mode = T_SEARCHMODE_PCSB
            self.filter_tablet_table()
            
    def __toggle_radio_tablet_serial(self, flag):
        if flag:
            self.tablet_search_mode = T_SEARCHMODE_SERIAL
            self.filter_tablet_table()
            
    def __toggle_radio_tablet_username(self, flag):
        if flag:
            self.tablet_search_mode = T_SEARCHMODE_NAME
            self.filter_tablet_table()
            
    def __toggle_radio_tablet_devicemodel(self, flag):
        if flag:
            self.tablet_search_mode = T_SEARCHMODE_DEVICE_MODEL
            self.filter_tablet_table()
            
    ################################################################
    
    def get_column_for_tablet_search_mode(self):
        mode = self.tablet_search_mode
        if mode == T_SEARCHMODE_PCSB:
            return 0
        elif mode == T_SEARCHMODE_DEVICE_MODEL:
            return 1
        elif mode == T_SEARCHMODE_SERIAL:
            return 2
        elif mode == T_SEARCHMODE_NAME:
            return 4
            
    def get_column_for_user_search_mode(self):
        mode = self.user_search_mode
        if mode == U_SEARCHMODE_NAME:
            return 0
        elif mode == U_SEARCHMODE_EMAIL:
            return 2
        elif mode == U_SEARCHMODE_GRADE:
            return 3
        elif mode == U_SEARCHMODE_TABLET_PCSB:
            return 5
            
    def filter_user_table(self):
        print("Filtering user table")
        self.filter_table(self.ui.userView,
            self.get_column_for_user_search_mode(), self.ui.facultySearchEntry.text())
            
    def filter_tablet_table(self):
        print("Filtering tablet table")
        self.filter_table(self.ui.tabletView,
            self.get_column_for_tablet_search_mode(), self.ui.searchEntry.text())
    
    def filter_table(self, table, column, filter_str):        
        if len(filter_str) == 0:
            for i in range(table.rowCount()):
                table.showRow(i)
            return
            
        for i in range(table.rowCount()):
            table.hideRow(i)
            
        items = table.findItems(filter_str, QtCore.Qt.MatchContains)
        for item in items:
            if item.column() == column:
                table.showRow(item.row())
        
    def __set_checkbox_state(self, cbox, string):
        flag = bool(int(string))
        if flag:
            cbox.setCheckState(QtCore.Qt.Checked)
        else:
            cbox.setCheckState(QtCore.Qt.Unchecked)
        
    def open_edit_student_dialog(self, row):
        user_view = self.ui.tabletView_2
        print("Opening student edit for row", row)
        from src.netclient import net_editstudent
        dlg = QtWidgets.QDialog(self)
        dlgconfig = net_editstudent.Ui_Dialog()
        dlgconfig.setupUi(dlg)
        self.__set_checkbox_state(dlgconfig.pcsbAgreementCheckBox, user_view.item(row, 6).text())
        self.__set_checkbox_state(dlgconfig.catAgreementCheckBox, user_view.item(row, 7).text())
        self.__set_checkbox_state(dlgconfig.insuranceCheckBox, user_view.item(row, 8).text())
        dlgconfig.insuranceAmountEdit.setText(user_view.item(row, 9).text())
        
        tablet_data = user_view.item(row, 5).text()
        if tablet_data != "No Tablet Assigned": # yuck
            dlgconfig.tabletPCSBEdit.setText(user_view.item(row, 5).text())
            
        dlg.open()
        dlg.finished.connect(self.__handle_edit_student_finish)
        self.edit_dialog = (dlg, dlgconfig)
        
    def handle_finish_edit_user_resp(self, dgi):
        self.hide_please_wait()
        ret = dgi.get_uint8()
        if not ret:
            error_msg = dgi.get_string()
            QtWidgets.QMessageBox.information(self, "Message From Server", error_msg)
        
    def __handle_edit_student_finish(self, ret):
        print("Done editing")
        
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_FINISH_EDIT_USER)
        dg.add_string(self.editing_guid)
        dg.add_uint8(ret)
        if ret:
            dlgcfg = self.edit_dialog[1]
            dg.add_uint8(dlgcfg.pcsbAgreementCheckBox.checkState() != 0)
            dg.add_uint8(dlgcfg.catAgreementCheckBox.checkState() != 0)
            dg.add_uint8(dlgcfg.insuranceCheckBox.checkState() != 0)
            dg.add_string(dlgcfg.insuranceAmountEdit.text())
            dg.add_string(dlgcfg.tabletPCSBEdit.text())
            self.show_please_wait()
        g_server_connection.send(dg)
        
        self.edit_dialog = None
        
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
        self.please_wait_dialog.open()
        
    def hide_please_wait(self):
        if self.please_wait_dialog:
            self.please_wait_dialog.done(0)
        self.please_wait_dialog = None
        
    def handle_edit_user_resp(self, dgi):
        self.hide_please_wait()
        flag = dgi.get_uint8()
        if not flag:
            QtWidgets.QMessageBox.information(self, "Error", "This user is currently being edited by someone else.")
        else:
            print("Edit it!")
            guid = dgi.get_string()
            self.editing_guid = guid
            self.open_edit_student_dialog(self.ui.tabletView_2.row(self.edit_req_item))
        
    def __handle_double_click_user_item(self, item):
        self.edit_req_item = item
        guid = item.guid
        print("Requesting edit for", guid)
        
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_EDIT_USER)
        dg.add_string(guid) # We will search active directory by guid
        g_server_connection.send(dg)
        
        self.show_please_wait()
        
    def __handle_double_click_tablet_item(self, item):
        self.edit_req_item = item
        guid = item.guid
        print("Requesting edit for tablet", guid)
        
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_EDIT_TABLET)
        dg.add_string(guid)
        g_server_connection.send(dg)
        
        self.show_please_wait()
        
    def handle_edit_tablet_resp(self, dgi):
        self.hide_please_wait()
        flag = dgi.get_uint8()
        if not flag:
            QtWidgets.QMessageBox.information(self, "Error", "This tablet is currently being edited by someone else.")
        else:
            print("Now editing tablet")
            guid = dgi.get_string()
            self.editing_guid = guid
            self.open_edit_tablet_dialog(self.ui.tabletView.row(self.edit_req_item))
            
    def open_edit_tablet_dialog(self, row):
        print("Opening tablet edit dialog for row", row)
        from src.netclient import net_edittablet
        dlg = QtWidgets.QDialog(self)
        dlgcfg = net_edittablet.Ui_EditTabletDialog()
        dlgcfg.setupUi(dlg)
        dlgcfg.deviceModelEntry.setText(self.ui.tabletView.item(row, 1).text())
        dlgcfg.serialNoEntry.setText(self.ui.tabletView.item(row, 2).text())
        dlg.open()
        self.edit_dialog = (dlg, dlgcfg)
        
    def update_student_row(self, i, dgi, guid = None):
        userView = self.ui.tabletView_2
        
        if not guid:
            guid = dgi.get_string()
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
        
        self.user_guid_names[guid] = name
        
        userView.setItem(i, 0, ADTableWidgetItem(guid, firstName))
        userView.setItem(i, 1, ADTableWidgetItem(guid, lastName))
        userView.setItem(i, 2, ADTableWidgetItem(guid, email))
        userView.setItem(i, 3, ADTableWidgetItem(guid, grade))
        userView.setItem(i, 4, ADTableWidgetItem(guid, str(cat_student)))
        userView.setItem(i, 5, ADTableWidgetItem(guid, tablet_pcsb_tag))
        userView.setItem(i, 6, ADTableWidgetItem(guid, str(pcsb_agreement)))
        userView.setItem(i, 7, ADTableWidgetItem(guid, str(cat_agreement)))
        userView.setItem(i, 8, ADTableWidgetItem(guid, str(insurance_paid)))
        userView.setItem(i, 9, ADTableWidgetItem(guid, insurance_amount))
        
    def handle_update_user(self, dgi):
        guid = dgi.get_string()
        userView = self.ui.tabletView_2
        row = None
        # Find the row containing this user GUID
        for i in range(userView.rowCount()):
            if userView.item(i, 0).guid == guid:
                row = i
                break
        if row is None:
            print("Error: tried to update user row but couldn't find the row")
            return
           
        self.update_student_row(row, dgi, guid)
        
    def handle_get_all_users_resp(self, dgi):
        userView = self.ui.tabletView_2
        
        self.user_guid_names = {}
        
        # Clear existing rows
        userView.clearContents()
        userView.setRowCount(0)
        userView.setSortingEnabled(False)
        
        num_users = dgi.get_uint16()
        for i in range(num_users):
            userView.insertRow(i)
            self.update_student_row(i, dgi)
            
        userView.setSortingEnabled(True)
        
        self.filter_user_table()
        
    def handle_get_all_tablets_resp(self, dgi):
        # Clear existing rows
        self.ui.tabletView.clearContents()
        self.ui.tabletView.setRowCount(0)
        self.ui.tabletView.setSortingEnabled(False)
        
        num_assigned_tablets = dgi.get_uint16()
        for i in range(num_assigned_tablets):
            guid = dgi.get_string()
            pcsb = dgi.get_string()
            device = dgi.get_string()
            serial = dgi.get_string()
            issue = "No Issue"#dgi.get_string()
            name = dgi.get_string()
            
            self.ui.tabletView.insertRow(i)
            self.ui.tabletView.setItem(i, 0, ADTableWidgetItem(guid, pcsb))
            self.ui.tabletView.setItem(i, 1, ADTableWidgetItem(guid, device))
            self.ui.tabletView.setItem(i, 2, ADTableWidgetItem(guid, serial))
            self.ui.tabletView.setItem(i, 3, ADTableWidgetItem(guid, issue))
            self.ui.tabletView.setItem(i, 4, ADTableWidgetItem(guid, name))
            
        num_unassigned_tablets = dgi.get_uint16()
        for i in range(num_unassigned_tablets):
            guid = dgi.get_string()
            pcsb = dgi.get_string()
            device = dgi.get_string()
            serial = dgi.get_string()
            issue = "No Issue"
            name = "Unassigned"
            
            self.ui.tabletView.insertRow(i)
            self.ui.tabletView.setItem(i, 0, ADTableWidgetItem(guid, pcsb))
            self.ui.tabletView.setItem(i, 1, ADTableWidgetItem(guid, device))
            self.ui.tabletView.setItem(i, 2, ADTableWidgetItem(guid, serial))
            self.ui.tabletView.setItem(i, 3, ADTableWidgetItem(guid, issue))
            self.ui.tabletView.setItem(i, 4, ADTableWidgetItem(guid, name))
            
        self.ui.tabletView.setSortingEnabled(True)
        
        self.filter_tablet_table()
        
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
