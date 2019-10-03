from src.shared.base_server_connection import BaseServerConnection
from src.shared.Consts import *
from src.shared.issue import Issue
from src.shared.issue_step import IssueStep
from src.shared.student import Student
from src.shared.base_tablet import BaseTablet
from src.shared.student_tablet_link import StudentTabletLink
from src.shared import utils

from panda3d import core
core.load_prc_file_data('', 'notify-level-net spam')
core.load_prc_file_data('', 'tcp-header-size 4')

import sys
import os
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
U_SEARCHMODE_LNAME          = 4

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
        elif msg_type == MSG_SERVER_GET_ALL_LINKS_RESP:
            g_main_window.handle_get_all_links_resp(dgi)
        elif msg_type == MSG_SERVER_GET_ALL_ISSUES_RESP:
            g_main_window.handle_get_all_issues_resp(dgi)
        elif msg_type == MSG_SERVER_GET_ALL_ISSUE_STEPS_RESP:
            g_main_window.handle_get_all_issue_steps_resp(dgi)
            
        elif msg_type == MSG_SERVER_UPDATE_USER:
            g_main_window.handle_update_user(dgi)
        elif msg_type == MSG_SERVER_UPDATE_TABLET:
            g_main_window.handle_update_tablet(dgi)
        elif msg_type == MSG_SERVER_UPDATE_ISSUE:
            g_main_window.handle_new_issue(dgi)
        elif msg_type == MSG_SERVER_UPDATE_ISSUE_STEP:
            g_main_window.handle_new_issue_step(dgi)
        elif msg_type == MSG_SERVER_UPDATE_LINK:
            g_main_window.handle_update_link(dgi)

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
        
        self.ui.userExportExcel.pressed.connect(self.__export_users_to_excel)
        
        self.ui.tabletView.itemDoubleClicked.connect(self.__handle_double_click_tablet_item)
        
        self.ui.radio_user_name.toggled.connect(self.__toggle_radio_user_name)
        self.ui.radio_user_email.toggled.connect(self.__toggle_radio_user_email)
        self.ui.radio_user_grade.toggled.connect(self.__toggle_radio_user_grade)
        self.ui.radio_user_tablet_pcsb.toggled.connect(self.__toggle_radio_user_tablet_pcsb)
        self.ui.radio_user_lname.toggled.connect(self.__toggle_radio_user_lname)
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
        
        self.tablet_table_generated = False
        self.user_table_generated = False
        
        self.students = []
        self.tablets = []
        self.student_tablet_links = []
        self.issues = []
        self.issue_steps = []
        
        self.__request_all_links()
        self.__request_all_issues()
        self.__request_all_issue_steps()
        self.__request_all_tablets()
        self.__request_all_users()
        
        self.show_please_wait(text = "Populating tables...")
        
    def __export_users_to_excel(self):
        filedlg = QtWidgets.QFileDialog(self, "Select export location", os.environ["USERPROFILE"] + "\\Desktop", "Excel File (*.xls)")
        filedlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        if (filedlg.exec()):
            export_path = filedlg.selectedFiles()[0]
            print("Exporting user excel sheet to", export_path)
            import xlwt
            wb = xlwt.Workbook()
            sheet = wb.add_sheet('Sheet 1')
            
            sheet.write(0, 0, 'First Name')
            sheet.write(0, 1, 'Last Name')
            sheet.write(0, 2, 'Grade')
            sheet.write(0, 3, 'Tablet PCSB Tag')
            sheet.write(0, 4, 'Tablet Serial Number')
            sheet.write(0, 5, 'Tablet Device Model')
            sheet.write(0, 6, 'PCSB Internet Agreement')
            sheet.write(0, 7, 'CAT Internet Agreement')
            sheet.write(0, 8, 'Insurance Paid')
            sheet.write(0, 9, 'Insurance Amount')
            sheet.write(0, 10, 'Insurance Date')
            
            for i in range(len(self.students)):
                student = self.students[i]
                links = [link for link in self.student_tablet_links if link.student_guid == student.guid]
                link = links[0] if len(links) > 0 else None
                tablet_pcsb = ""
                tablet_serial = ""
                tablet_device = ""
                tablet = None
                if link:
                    tablets = [t for t in self.tablets if t.guid == link.tablet_guid]
                    tablet = tablets[0] if len(tablets) > 0 else None
                if tablet:
                    tablet_pcsb = tablet.pcsb_tag
                    tablet_serial = tablet.serial
                    tablet_device = tablet.device_model
                row = i + 1
                sheet.write(row, 0, student.first_name)
                sheet.write(row, 1, student.last_name)
                sheet.write(row, 2, student.grade)
                sheet.write(row, 3, tablet_pcsb)
                sheet.write(row, 4, tablet_serial)
                sheet.write(row, 5, tablet_device)
                sheet.write(row, 6, utils.bool_yes_no(student.pcsb_agreement))
                sheet.write(row, 7, utils.bool_yes_no(student.cat_agreement))
                sheet.write(row, 8, utils.bool_yes_no(student.insurance_paid))
                sheet.write(row, 9, student.insurance_amount)
                sheet.write(row, 10, student.date_of_insurance)
            wb.save(export_path)
    
    def __handle_tablet_search_edited(self, text):
        self.filter_tablet_table()
        
    def __handle_user_search_edited(self, text):
        self.filter_user_table()
        
    ################################################################
        
    def __toggle_radio_user_name(self, flag):
        if flag:
            self.user_search_mode = U_SEARCHMODE_NAME
            self.filter_user_table()
            
    def __toggle_radio_user_lname(self, flag):
        if flag:
            self.user_search_mode = U_SEARCHMODE_LNAME
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
        elif mode == U_SEARCHMODE_LNAME:
            return 1
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
        if isinstance(string, str):
            flag = bool(int(string))
        else:
            flag = string
        if flag:
            cbox.setCheckState(QtCore.Qt.Checked)
        else:
            cbox.setCheckState(QtCore.Qt.Unchecked)
        
    def open_edit_student_dialog(self, row):
        user_view = self.ui.tabletView_2
        guid = user_view.item(row, 0).guid
        users = [user for user in self.students if user.guid == guid]
        user = users[0] if len(users) > 0 else None
        if not user:
            print("Can't find user to edit")
            return
            
        print("Opening student edit for row", row, "guid", guid)
        
        from src.netclient import net_editstudent
        dlg = QtWidgets.QDialog(self)
        dlgconfig = net_editstudent.Ui_Dialog()
        dlgconfig.setupUi(dlg)
        dlg.setWindowTitle("Edit User - %s" % user.name)
        self.__set_checkbox_state(dlgconfig.pcsbAgreementCheckBox, user.pcsb_agreement)
        self.__set_checkbox_state(dlgconfig.catAgreementCheckBox, user.cat_agreement)
        self.__set_checkbox_state(dlgconfig.insuranceCheckBox, user.insurance_paid)
        dlgconfig.insuranceAmountEdit.setText(user.insurance_amount)

        links = [link for link in self.student_tablet_links if link.student_guid == guid]
        link = links[0] if len(links) > 0 else None
        if link:
            tablets = [tablet for tablet in self.tablets if tablet.guid == link.tablet_guid]
            tablet = tablets[0] if len(tablets) > 0 else None
            if tablet:
                dlgconfig.tabletPCSBEdit.setText(tablet.pcsb_tag)
            
            
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
            has_insurance = dlgcfg.insuranceCheckBox.checkState() != 0
            students = [student for student in self.students if student.guid == self.editing_guid]
            student = students[0] if len(students) > 0 else None
            dg.add_uint8(dlgcfg.pcsbAgreementCheckBox.checkState() != 0)
            dg.add_uint8(dlgcfg.catAgreementCheckBox.checkState() != 0)
            dg.add_uint8(has_insurance)
            dg.add_string(dlgcfg.insuranceAmountEdit.text())
            dg.add_string(dlgcfg.tabletPCSBEdit.text())
            if has_insurance and (student and not student.insurance_paid):
                print("Student now has insurance")
                dg.add_string(utils.get_date_string())
            self.show_please_wait()
        g_server_connection.send(dg)
        
        self.edit_dialog = None
        
    def __request_all_links(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_GET_ALL_LINKS)
        g_server_connection.send(dg)
        
    def handle_get_all_links_resp(self, dgi):
        self.student_tablet_links = []
        num_links = dgi.get_uint32()
        for i in range(num_links):
            link = StudentTabletLink.from_datagram(dgi)
            self.student_tablet_links.append(link)
        print("Received %i links" % num_links)
        
    def __request_all_issues(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_GET_ALL_ISSUES)
        g_server_connection.send(dg)
        
    def handle_get_all_issues_resp(self, dgi):
        self.issues = []
        num_issues = dgi.get_uint32()
        for i in range(num_issues):
            issue = Issue.from_datagram(dgi)
            self.issues.append(issue)
        print("Received %i issues" % num_issues)
        
    def __request_all_issue_steps(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_GET_ALL_ISSUE_STEPS)
        g_server_connection.send(dg)
        
    def handle_get_all_issue_steps_resp(self, dgi):
        self.issue_steps = []
        num_steps = dgi.get_uint32()
        for i in range(num_steps):
            step = IssueStep.from_datagram(dgi)
            self.issue_steps.append(step)
        print("Received %i issue steps" % num_steps)
        
    def __request_all_tablets(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_GET_ALL_TABLETS)
        g_server_connection.send(dg)
        
    def __request_all_users(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_GET_ALL_USERS)
        g_server_connection.send(dg)
        
    def show_please_wait(self, title = "Information", text = "Please wait..."):
        self.hide_please_wait()
        
        self.please_wait_dialog = QtWidgets.QMessageBox(self)
        self.please_wait_dialog.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        self.please_wait_dialog.setText(text)
        self.please_wait_dialog.setWindowTitle(title)
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
        guid = self.ui.tabletView.item(row, 0).guid
        
        from src.netclient.tablet_editing import TabletEditing
        self.edit_dialog = TabletEditing(self, guid, row)
        
    def send_finish_edit_tablet(self, dg):
        #dg = core.Datagram()
        #dg.add_uint16(MSG_CLIENT_FINISH_EDIT_TABLET)
        #dg.add_string(self.editing_guid)
        g_server_connection.send(dg)
        #self.show_please_wait()
        
        #self.editing_guid = None
        
    def update_student_row_ui(self, i, student):
        userView = self.ui.tabletView_2
        
        guid = student.guid
        grade = student.grade
        email = student.email
        pcsb_agreement = student.pcsb_agreement
        cat_agreement = student.cat_agreement
        insurance_paid = student.insurance_paid
        insurance_amount = student.insurance_amount
        cat_student = student.cat_student
        pcsb_tags = [tablet.pcsb_tag for tablet in self.tablets if tablet.guid == student.tablet_guid]
        if len(pcsb_tags) > 0:
            tablet_pcsb_tag = pcsb_tags[0]
        else:
            tablet_pcsb_tag = "No Tablet Assigned"
        
        userView.setSortingEnabled(False)
        userView.setItem(i, 0, ADTableWidgetItem(guid, student.first_name))
        userView.setItem(i, 1, ADTableWidgetItem(guid, student.last_name))
        userView.setItem(i, 2, ADTableWidgetItem(guid, email))
        userView.setItem(i, 3, ADTableWidgetItem(guid, grade))
        userView.setItem(i, 4, ADTableWidgetItem(guid, utils.bool_yes_no(cat_student)))
        userView.setItem(i, 5, ADTableWidgetItem(guid, tablet_pcsb_tag))
        userView.setItem(i, 6, ADTableWidgetItem(guid, utils.bool_yes_no(pcsb_agreement)))
        userView.setItem(i, 7, ADTableWidgetItem(guid, utils.bool_yes_no(cat_agreement)))
        userView.setItem(i, 8, ADTableWidgetItem(guid, utils.bool_yes_no(insurance_paid)))
        userView.setItem(i, 9, ADTableWidgetItem(guid, insurance_amount))
        userView.setItem(i, 10, ADTableWidgetItem(guid, student.date_of_insurance))
        userView.setSortingEnabled(True)
        
    def generate_student_table_ui(self):
        userView = self.ui.tabletView_2
        
        # Clear existing rows
        userView.clearContents()
        userView.setRowCount(0)
        userView.setSortingEnabled(False)
        
        for i in range(len(self.students)):
            student = self.students[i]
            userView.setSortingEnabled(False)
            userView.insertRow(i)
            
            self.update_student_row_ui(i, student)
        
        userView.setSortingEnabled(True)
        
        self.filter_user_table()
        
        self.user_table_generated = True
        
        print("User table generated")
        
    def update_student_row(self, i, dgi, student = None):
        if not student:
            student = Student.from_datagram(dgi)

        utils.list_add_replace(self.students, student)
            
    def find_table_guid_row(self, table, guid):
        row = None
        for i in range(table.rowCount()):
            if table.item(i, 0).guid == guid:
                row = i
                break
        return row
        
    def handle_update_user(self, dgi):
        student = Student.from_datagram(dgi)
        userView = self.ui.tabletView_2
        row = self.find_table_guid_row(userView, student.guid)
        if row is None:
            print("Error: tried to update user row but couldn't find the row")
            return
            
        self.update_student_row(row, dgi, student)
        if self.user_table_generated:
            self.update_student_row_ui(row, student)
            
    def handle_new_issue(self, dgi):
        num_issues = dgi.get_uint16()
        for i in range(num_issues):
            issue = Issue.from_datagram(dgi)
            utils.list_add_replace(self.issues, issue)
            
            tablets = [tablet for tablet in self.tablets if tablet.guid == issue.tablet_guid]
            tablet = tablets[0] if len(tablets) > 0 else None
            if tablet and self.tablet_table_generated:
                self.update_tablet_row_ui(self.find_table_guid_row(self.ui.tabletView, tablet.guid), tablet)
                
    def handle_new_issue_step(self, dgi):
        num_steps = dgi.get_uint16()
        for i in range(num_steps):
            step = IssueStep.from_datagram(dgi)
            utils.list_add_replace(self.issue_steps, step)
                
    def handle_update_link(self, dgi):
        num_links = dgi.get_uint16()
        for i in range(num_links):
            link = StudentTabletLink.from_datagram(dgi)
            utils.list_add_replace(self.student_tablet_links, link)
            
            tablets = [tablet for tablet in self.tablets if tablet.guid == link.tablet_guid]
            tablet = tablets[0] if len(tablets) > 0 else None
            users = [user for user in self.students if user.guid == link.student_guid]
            user = users[0] if len(users) > 0 else None
            if tablet and self.tablet_table_generated:
                self.update_tablet_row_ui(self.find_table_guid_row(self.ui.tabletView, tablet.guid), tablet)
            if user and self.user_table_generated:
                self.update_student_row_ui(self.find_table_guid_row(self.ui.tabletView_2, user.guid), user)
                
    def handle_update_tablet(self, dgi):
        tablet = BaseTablet.from_datagram(dgi)
        utils.list_add_replace(self.tablets, tablet)
            
        if self.tablet_table_generated:
            row = self.find_table_guid_row(self.ui.tabletView, tablet.guid)
            if row is not None:
                self.update_tablet_row_ui(row, tablet)
        
    def handle_get_all_users_resp(self, dgi):
        self.students = []

        num_users = dgi.get_uint16()
        for i in range(num_users):
            self.update_student_row(i, dgi)
            
        print("Received %i users" % num_users)
            
        if not self.user_table_generated:
            self.generate_student_table_ui()
        if not self.tablet_table_generated:
            self.generate_tablet_table_ui()
            
        self.hide_please_wait()
            
    def update_tablet_row_ui(self, i, tablet):
        guid = tablet.guid
        pcsb = tablet.pcsb_tag
        device = tablet.device_model
        serial = tablet.serial
        
        link = None
        student = None
        
        links = [link for link in self.student_tablet_links if link.tablet_guid == tablet.guid]
        if len(links) > 0:
            link = links[0]
        if link:
            students = [student for student in self.students if student.guid == link.student_guid]
            if len(students) > 0:
                student = students[0]
        if student:
            name = student.first_name + " " + student.last_name
        else:
            name = "Unassigned"
        issues = [issue for issue in self.issues if issue.tablet_guid == tablet.guid]
        active_issue = False
        issue_problems = ""
        for issue in issues:
            if not issue.resolved:
                active_issue = True
                issue_problems = issue.problems_desc
                break
        if active_issue:
            issue = "Active Issue"
        else:
            issue = "No Active Issue"
        
        self.ui.tabletView.setSortingEnabled(False)
        self.ui.tabletView.setItem(i, 0, ADTableWidgetItem(guid, pcsb))
        self.ui.tabletView.setItem(i, 1, ADTableWidgetItem(guid, device))
        self.ui.tabletView.setItem(i, 2, ADTableWidgetItem(guid, serial))
        self.ui.tabletView.setItem(i, 3, ADTableWidgetItem(guid, issue))
        self.ui.tabletView.setItem(i, 4, ADTableWidgetItem(guid, issue_problems))
        self.ui.tabletView.setItem(i, 5, ADTableWidgetItem(guid, name))
        self.ui.tabletView.setSortingEnabled(True)
            
    def generate_tablet_table_ui(self):
        # Clear existing rows
        self.ui.tabletView.clearContents()
        self.ui.tabletView.setRowCount(0)
        self.ui.tabletView.setSortingEnabled(False)
        
        for i in range(len(self.tablets)):
            tablet = self.tablets[i]
            self.ui.tabletView.setSortingEnabled(False)
            self.ui.tabletView.insertRow(i)
            self.update_tablet_row_ui(i, tablet)
            
        self.ui.tabletView.setSortingEnabled(True)
        
        self.filter_tablet_table()
        
        self.tablet_table_generated = True
        
        print("Tablet table generated")
        
    def handle_get_all_tablets_resp(self, dgi):
        self.tablets = []      
        
        num_tablets = dgi.get_uint16()
        for i in range(num_tablets):
            tablet = BaseTablet.from_datagram(dgi)
            self.tablets.append(tablet)
            
        print("Received %i tablets" % num_tablets)
        
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

app = NetClientApp()
sys.exit(app.exec_())
