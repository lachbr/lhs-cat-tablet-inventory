from PyQt5 import QtWidgets, Qt, QtCore

from panda3d import core

from src.shared import utils, issue_step
from src.shared.Consts import *

import datetime
import copy

class IssueWidgetItem(QtWidgets.QTableWidgetItem):

    def __init__(self, iid, text):
        QtWidgets.QTableWidgetItem.__init__(self, text)
        self.iid = iid

class TabletEditing:

    def __init__(self, mgr, guid, row):
        self.mgr = mgr
        self.guid = guid
        
        tablets = [tablet for tablet in self.mgr.tablets if tablet.guid == self.guid]
        if len(tablets) > 0:
            self.tablet = tablets[0]
        else:
            return
            
        self.new_steps = []
        self.mod_issues = []
        self.mod_tablet = None
        
        from src.netclient import net_edittablet
        dlg = QtWidgets.QDialog(self.mgr)
        dlgcfg = net_edittablet.Ui_EditTabletDialog()
        dlgcfg.setupUi(dlg)
        dlgcfg.deviceModelEntry.setText(self.tablet.device_model)
        dlgcfg.serialNoEntry.setText(self.tablet.serial)
        self.generate_issue_table_ui(self.get_issue_list(), dlgcfg)
        dlg.finished.connect(self.__handle_edit_tablet_finish)
        dlgcfg.issueTable.itemDoubleClicked.connect(self.__handle_double_click_issue)
        dlg.open()
        
        self.edit_dialog = (dlg, dlgcfg)
        ######################
        self.editing_issue = None
        self.edit_issue_dialog = None
        ######################
        self.new_step_dialog = None

    def generate_issue_table_ui(self, issues, dlgcfg = None):
        if not dlgcfg:
            dlgcfg = self.edit_dialog[1]
        
        dlgcfg.issueTable.clearContents()
        dlgcfg.issueTable.setRowCount(0)
        
        active_issue = False
        for i in range(len(issues)):
            dlgcfg.issueTable.insertRow(i)
            issue = issues[i]
            if not issue.resolved:
                active_issue = True
            iid = issue.issue_id
            dlgcfg.issueTable.setItem(i, 0, IssueWidgetItem(iid, issue.date_of_incident))
            dlgcfg.issueTable.setItem(i, 1, IssueWidgetItem(iid, issue.problems_desc))
            dlgcfg.issueTable.setItem(i, 2, IssueWidgetItem(iid, utils.bool_yes_no(issue.resolved)))
        if active_issue:
            dlgcfg.activeIssueLabel.setText("Active Issue: Yes")
        else:
            dlgcfg.activeIssueLabel.setText("Active Issue: No")
        
    def __handle_edit_tablet_finish(self, ret):
        if ret:
            dlgcfg = self.edit_dialog[1]
            mod_tablet = self.tablet
            mod_tablet.device_model = dlgcfg.deviceModelEntry.text()
            mod_tablet.serial = dlgcfg.serialNoEntry.text()
            self.mod_tablet = mod_tablet
        
            # send all the modifications
            dg = core.Datagram()
            dg.add_uint16(MSG_CLIENT_FINISH_EDIT_TABLET)
            dg.add_uint8(1)
            self.mod_tablet.write_datagram(dg)
            dg.add_uint16(len(self.mod_issues))
            for i in range(len(self.mod_issues)):
                issue = self.mod_issues[i]
                issue.write_datagram(dg)
            dg.add_uint16(len(self.new_steps))
            for i in range(len(self.new_steps)):
                step = self.new_steps[i]
                step.step_id = -1 # signifies new step
                step.write_datagram(dg)
            self.mgr.send_finish_edit_tablet(dg)
        else:
            dg = core.Datagram()
            dg.add_uint16(MSG_CLIENT_FINISH_EDIT_TABLET)
            dg.add_uint8(0)
            self.tablet.write_datagram(dg)
            self.mgr.send_finish_edit_tablet(dg)
        
        self.edit_dialog = None
        
    def __handle_new_step_finish(self, ret):
        if ret:
            dlgcfg = self.new_step_dialog[1]
            desc = dlgcfg.stepsEdit.toPlainText()
            hwname = dlgcfg.teamMemberCombo.currentText()
            hws = [hw for hw in self.mgr.students if hw.name == hwname]
            hwguid = hws[0].guid if len(hws) > 0 else ""
            date = utils.get_date_string()
            step = issue_step.IssueStep(len(self.new_steps), self.editing_issue.issue_id, date, desc, hwguid)
            self.new_steps.append(step)
            self.insert_step(step)
        self.new_step_dialog = None
        
    def __handle_log_new_step_pressed(self):
        print("Opening log new step...")
        from src.netclient.net_newstep import Ui_Dialog
        dlg = QtWidgets.QDialog(self.edit_issue_dialog[0])
        dlgcfg = Ui_Dialog()
        dlgcfg.setupUi(dlg)
        hwnames = []
        hws = [hw for hw in self.mgr.students if hw.net_assistant == 1]
        for i in range(len(hws)):
            hw = hws[i]
            dlgcfg.teamMemberCombo.addItem(hw.name)
            hwnames.append(hw.name)
        completer = QtWidgets.QCompleter(hwnames)
        completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        dlgcfg.teamMemberCombo.setEditable(True)
        dlgcfg.teamMemberCombo.setCompleter(completer)
        dlg.finished.connect(self.__handle_new_step_finish)
        dlg.open()
        self.new_step_dialog = (dlg, dlgcfg)
        
    def insert_step(self, step, dlgcfg = None):
        if not dlgcfg:
            dlgcfg = self.edit_issue_dialog[1]
            
        hws = [hw for hw in self.mgr.students if hw.guid == step.team_member_guid]
        hw = hws[0] if len(hws) > 0 else None
        if not hw:
            hwname = "No Team Member"
        else:
            hwname = hw.name
        
        i = dlgcfg.repairLogTable.rowCount()
        dlgcfg.repairLogTable.insertRow(i)
        dlgcfg.repairLogTable.setItem(i, 0, QtWidgets.QTableWidgetItem(step.date_of_step)) 
        dlgcfg.repairLogTable.setItem(i, 1, QtWidgets.QTableWidgetItem(hwname))
        dlgcfg.repairLogTable.setItem(i, 2, QtWidgets.QTableWidgetItem(step.step_desc))
        
    def get_issue_list(self):        
        # Modded issues should override the non-modded version
        issues = [issue for issue in self.mgr.issues if issue.tablet_guid == self.tablet.guid]
        for mod_issue in self.mod_issues:
            if mod_issue in issues:
                print("Modded issue")
                idx = issues.index(mod_issue)
                issues[idx] = mod_issue
                
        return issues
        
    def __handle_edit_issue_finish(self, ret):
        if ret:
            dlgcfg = self.edit_issue_dialog[1]
            
            mod_issue = self.editing_issue
            mod_issue.parts_ordered = dlgcfg.partsOrderedCheck.checkState() != 0
            mod_issue.parts_ordered_date = dlgcfg.partsOrderedDateEdit.text()
            mod_issue.parts_expected_date = dlgcfg.partsExpectedDateEdit.text()
            if dlgcfg.insuranceRadio.isChecked():
                mod_issue.insurance_or_warranty = 0
            elif dlgcfg.warrantyRadio.isChecked():
                mod_issue.insurance_or_warranty = 1
            else:
                mod_issue.insurance_or_warranty = 2
                
            mod_issue.resolved = dlgcfg.resolvedCheck.checkState() != 0
            mod_issue.fixed_desc = dlgcfg.fixedEdit.toPlainText()
            
            mod_issue.tablet_returned = dlgcfg.returnedToStudentCheck.checkState() != 0
            
            utils.list_add_replace(self.mod_issues, mod_issue)

            self.generate_issue_table_ui(self.get_issue_list())
            
        self.editing_issue = None
        self.edit_issue_dialog = None
        
    def __handle_double_click_issue(self, item):
        issue_id = item.iid
        issues = [issue for issue in self.mgr.issues if issue.issue_id == issue_id]
        issue = issues[0] if len(issues) > 0 else None
        if not issue:
            return
            
        if issue in self.mod_issues:
            print("Remodifying modified issue")
            # Remodifying a modified issue before submitting
            idx = self.mod_issues.index(issue)
            issue = self.mod_issues[idx]
            
        self.editing_issue = issue
        
        from src.netclient.net_editissue import Ui_Dialog
        dlg = QtWidgets.QDialog(self.edit_dialog[0])
        dlgcfg = Ui_Dialog()
        dlgcfg.setupUi(dlg)
        
        # ==================================================
        
        links = [link for link in self.mgr.student_tablet_links if link.tablet_guid == self.guid]
        if len(links) > 0:
            link = links[0]
            students = [student for student in self.mgr.students if student.guid == link.student_guid]
            if len(students) > 0:
                student = students[0]
                dlgcfg.studentNameEdit.setText(student.name)  
        team_members = [student for student in self.mgr.students if student.guid == issue.team_member_guid]
        if len(team_members) > 0:
            team_member = team_members[0]
            dlgcfg.hwTeamNameEdit.setText(team_member.name)
                
        dlgcfg.deviceModelEdit.setText(self.tablet.device_model)
        dlgcfg.serialNoEdit.setText(self.tablet.serial)
        dlgcfg.pcsbTagEdit.setText(self.tablet.pcsb_tag)
        
        dlgcfg.doiEdit.setText(issue.date_of_incident)
        dlgcfg.incidentDescEdit.setText(issue.incident_desc)
        dlgcfg.problemsEdit.setText(issue.problems_desc)
        
        dlgcfg.partsOrderedCheck.setChecked(bool(issue.parts_ordered))
        dlgcfg.partsOrderedDateEdit.setDate(utils.get_qdate(issue.parts_ordered_date))
        dlgcfg.partsExpectedDateEdit.setDate(utils.get_qdate(issue.parts_expected_date))
        if issue.insurance_or_warranty == 0:
            dlgcfg.warrantyRadio.setChecked(False)
            dlgcfg.insuranceRadio.setChecked(True)
        elif issue.insurance_or_warranty == 1:
            dlgcfg.warrantyRadio.setChecked(True)
            dlgcfg.insuranceRadio.setChecked(False)
        else:
            dlgcfg.warrantyRadio.setChecked(False)
            dlgcfg.insuranceRadio.setChecked(False)
        
        dlgcfg.resolvedCheck.setChecked(bool(issue.resolved))
        dlgcfg.fixedEdit.setText(issue.fixed_desc)
        
        dlgcfg.returnedToStudentCheck.setChecked(bool(issue.tablet_returned))
        
        # ==================================================
            
        # Setup steps log
        steps = [step for step in self.mgr.issue_steps if step.issue_id == issue_id]
        # Also do new steps
        new_steps = [step for step in self.new_steps if step.issue_id == issue_id]
        steps += new_steps
        for i in range(len(steps)):
            step = steps[i]
            self.insert_step(step, dlgcfg)
        dlgcfg.newStepButton.pressed.connect(self.__handle_log_new_step_pressed)
            
        if issue.resolved:
            # Issue has been resolved, information is for viewing only.
            dlgcfg.tab.setDisabled(True)
            dlgcfg.tab_2.setDisabled(True)
        
        dlg.finished.connect(self.__handle_edit_issue_finish)
        dlg.open()
        self.edit_issue_dialog = (dlg, dlgcfg)
        
    