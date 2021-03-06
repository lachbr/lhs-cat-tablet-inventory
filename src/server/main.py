from panda3d import core
core.load_prc_file_data('', 'tcp-header-size 4')

from src.shared.Consts import *
from src.shared.issue import Issue
from src.shared.issue_step import IssueStep
from src.shared.student import Student
from src.shared.base_tablet import BaseTablet
from src.shared.student_tablet_link import StudentTabletLink

from pyad import *

import sqlite3

g_server_connection = None

EXCEL_IMPORT = False
SYNC_ACTIVE_DIRECTORY = True
WIPE_DB = False

class Student:

    CAT_GROUP = "ou=+AllCATStudents"
    NET_GROUP = "ou=+NetworkAssistants"

    @staticmethod
    def get_ad_cat_student_list():
        cat_students = pyad.from_dn("ou=+AllCATStudents,dc=cat,dc=pcsb,dc=org").get_children()
        net_assistants = pyad.from_dn("ou=+NetworkAssistants,dc=cat,dc=pcsb,dc=org").get_children()
        pcsb_students = pyad.from_dn("ou=+LHSO365Students,dc=cat,dc=pcsb,dc=org").get_children()
        cat_faculty = pyad.from_dn("ou=+AllFaculty,dc=cat,dc=pcsb,dc=org").get_children()
        return cat_students + net_assistants + pcsb_students + cat_faculty
        
    @staticmethod
    def get_ad_net_assistants():
        net_assistants = pyad.from_dn("ou=+NetworkAssistants,dc=cat,dc=pcsb,dc=org").get_children()
        return net_assistants
    
    @staticmethod
    def from_active_directory_student(ad_student):
        if not ad_student:
            return None
            
        c = g_server_connection.db_connection.cursor()
        c.execute("SELECT * FROM Student WHERE GUID = ?", (ad_student.guid_str,))
        db_student = c.fetchone()
        if not db_student:
            # Student in active directory but not inventory system
            return Student(ad_student)
            
        tablet_guid = None
        
        # Search for the tablet assigned to this student
        c.execute("SELECT * FROM StudentTabletLink WHERE StudentGUID = ?", (ad_student.guid_str,))
        link = c.fetchone()
        if link:
            tablet_guid = link[1]
            
        equipment_receipt = db_student[6] if len(db_student) >= 7 else None
        
        return Student(
            ad_student, db_student[1], db_student[2],
            db_student[3], db_student[4], db_student[5], equipment_receipt, tablet_guid
        )
        
    @staticmethod
    def from_guid(guid_str):
        try:
            ad_student = pyad.from_guid(guid_str)
        except:
            ad_student = None
        return Student.from_active_directory_student(ad_student)
        
    @staticmethod
    def from_name(name_str):
        try:
            ad_student = pyad.from_cn(name_str)
        except:
            ad_student = None
        return Student.from_active_directory_student(ad_student)
        
    def __init__(self, ad_student, pcsb_agreement = False, cat_agreement = False, insurance_paid = False, insurance_amount = "$0.00", insurance_date = "", equipment_receipt = False, tablet_guid = None):
        self.ad_student = ad_student
        self.first_name = ad_student.givenName
        if not self.first_name:
            self.first_name = ""
        self.last_name = ad_student.sn
        if not self.last_name:
            self.last_name = ""
        self.name = self.first_name + " " + self.last_name
        self.grade = ad_student.description
        self.email = ad_student.userPrincipalName
        self.guid = ad_student.guid_str
        self.pcsb_agreement = pcsb_agreement
        self.cat_agreement = cat_agreement
        self.insurance_paid = insurance_paid
        self.insurance_amount = insurance_amount
        self.date_of_insurance = insurance_date
        self.equipment_receipt = equipment_receipt
        if self.equipment_receipt is None:
            self.equipment_receipt = 0
        
        group_name = ad_student.parent_container.prefixed_cn
        self.cat_student = group_name in [Student.NET_GROUP, Student.CAT_GROUP]
        self.net_assistant = group_name == Student.NET_GROUP

        self.tablet_guid = tablet_guid
        self.orig_tablet_guid = tablet_guid
        
    def write_datagram(self, dg):
        dg.add_string(self.guid)
        dg.add_string(self.first_name)
        dg.add_string(self.last_name)
        dg.add_string(str(self.grade))
        dg.add_string(self.email)
        dg.add_uint8(self.pcsb_agreement)
        dg.add_uint8(self.cat_agreement)
        dg.add_uint8(self.insurance_paid)
        dg.add_string(self.insurance_amount)
        dg.add_string(self.date_of_insurance)
        dg.add_uint8(self.cat_student)
        if self.tablet_guid:
            dg.add_string(self.tablet_guid)
        else:
            dg.add_string("")
        dg.add_uint8(self.net_assistant)
        dg.add_uint8(self.equipment_receipt)
        
    def update(self):
        c = g_server_connection.db_connection.cursor()
        c.execute("UPDATE Student SET InternetAgreementPCSB = ?, InternetAgreementCAT = ?, InsurancePaid = ?, InsuranceAmount = ?, InsuranceDate = ?, EquipmentReceipt = ? WHERE GUID = ?",
                 (int(self.pcsb_agreement), int(self.cat_agreement), int(self.insurance_paid), self.insurance_amount, self.date_of_insurance, self.equipment_receipt, self.guid))
        g_server_connection.db_connection.commit()
                 
    def update_link(self):
        c = g_server_connection.db_connection.cursor()
        if not self.orig_tablet_guid and self.tablet_guid:
            c.execute("INSERT INTO StudentTabletLink VALUES (?, ?)", (self.guid, self.tablet_guid))
        elif self.tablet_guid and self.orig_tablet_guid:
            c.execute("UPDATE StudentTabletLink SET TabletGUID = ? WHERE StudentGUID = ?", (self.tablet_guid, self.guid))
        elif not self.tablet_guid and self.orig_tablet_guid:
            c.execute("DELETE FROM StudentTabletLink WHERE StudentGUID = ?", (self.guid,))
        g_server_connection.db_connection.commit()
            
        self.orig_tablet_guid = self.tablet_guid
    
    def __str__(self):
        return ("GUID: %s\n\tName: %s\n\tGrade: %s\n\tPCSB Agreement: %s\n"
            "\tCAT Agreement: %s\n\tInsurance Paid: %s\n\tInsurance Amount: %s\n"
            "\tCAT Student: %s\n\tTablet GUID: %s" % (self.guid, self.first_name + " " + self.last_name, self.grade, self.pcsb_agreement,
                self.cat_agreement, self.insurance_paid, self.insurance_amount, self.cat_student, self.tablet_guid))

class Tablet(BaseTablet):
    
    NAME_PREFIX = "C2031T"
    
    @staticmethod
    def get_ad_tablet_list():
        tablet_container = pyad.from_dn("ou=+AllTablets,dc=cat,dc=pcsb,dc=org")
        all_tablets = tablet_container.get_children()
        return all_tablets
    
    @staticmethod
    def get_ad_tablet_from_guid(guid_str):
        try:
            tablet = pyad.from_guid(guid_str)
        except:
            tablet = None
        return tablet
        
    @staticmethod
    def get_ad_tablet_from_name(name_str):
        try:
            tablet = pyad.from_cn(name_str)
        except:
            tablet = None
        return tablet
        
    @staticmethod
    def get_pcsb_tag_from_name(name):
        return name[len(Tablet.NAME_PREFIX):]
    
    @staticmethod
    def get_pcsb_tag_from_guid(guid_str):
        tablet = Tablet.get_ad_tablet_from_guid(guid_str)
        if tablet:
            # The PCSB tag is after the C2031T
            return Tablet.get_pcsb_tag_from_name(tablet.cn)
        return None
    
    @staticmethod
    def from_guid(guid_str):
        # First get the tablet's active directory info
        ad_tablet = Tablet.get_ad_tablet_from_guid(guid_str)            
        return Tablet.from_active_directory_tablet(ad_tablet)
            
    @staticmethod
    def from_active_directory_tablet(ad_tablet):
        if not ad_tablet:
            return None
            
        pcsb_tag = Tablet.get_pcsb_tag_from_name(ad_tablet.cn)
            
        # Get tablet from database
        c = g_server_connection.db_connection.cursor()
        c.execute("SELECT * FROM Tablet WHERE GUID=?", (ad_tablet.guid_str,))
        tablet_info = c.fetchone()
        if not tablet_info:
            # In active directory but not inventory
            return Tablet(ad_tablet.guid_str, pcsb_tag, ad_tablet = ad_tablet)
            
        # Find the student with the tablet
        student_guid = None
        c.execute("SELECT * FROM StudentTabletLink WHERE TabletGUID=?", (ad_tablet.guid_str,))
        link = c.fetchone()
        if link:
            student_guid = link[0]
        
        return Tablet(ad_tablet.guid_str, pcsb_tag, tablet_info[1], tablet_info[2], student_guid, ad_tablet)
        
    @staticmethod
    def from_pcsb_tag(pcsb_tag):
        pcsb_tag = pcsb_tag.replace('-', '')
        name_str = Tablet.NAME_PREFIX + pcsb_tag
        return Tablet.from_active_directory_tablet(Tablet.get_ad_tablet_from_name(name_str))
        
    def update(self):
        c = g_server_connection.db_connection.cursor()
        c.execute(
            "UPDATE Tablet SET SerialNumber = ?, DeviceModel = ? WHERE GUID = ?",
            (self.serial, self.device_model, self.guid)
        )
        g_server_connection.db_connection.commit()
        
    def update_link(self):
        c = g_server_connection.db_connection.cursor()
        if self.student_guid is None:
            c.execute("DELETE FROM StudentTabletLink WHERE TabletGUID = ?", (self.guid,))
        else:
            c.execute("UPDATE StudentTabletLink SET StudentGUID = ? WHERE TabletGUID = ?", (self.student_guid, self.guid))
        g_server_connection.db_connection.commit()

class Client:
    
    def __init__(self, conn, rendezvous):
        self.connection = conn
        self.connection_id = str(conn.this)
        self.rendezvous = rendezvous
        self.client_type = CLIENT_UNIDENTIFIED
        self.tablet_editing = None
        self.user_editing = None
        
    def is_identified(self):
        return self.client_type != CLIENT_UNIDENTIFIED
        
    def identify(self, ident):
        self.client_type = ident

class Server:

    TABLET_GROUP = "AllTablets"
    
    def __init__(self):
        global g_server_connection
        g_server_connection = self
        self.mgr = core.QueuedConnectionManager()
        self.listener = core.QueuedConnectionListener(self.mgr, 1)
        self.reader = core.QueuedConnectionReader(self.mgr, 1)
        self.writer = core.ConnectionWriter(self.mgr, 1)
        self.socket = self.mgr.open_TCP_server_rendezvous(7035, 10)
        self.listener.add_connection(self.socket)
        
        domain = "cat.pcsb.org"
        user = "net.assistant"
        password = "The Force is Strong"
        pyad.set_defaults(ldap_server = domain, username = user, password = password)
        
        self.db_connection = sqlite3.connect('tablet_inventory.db')
        #c.execute("insert into Tablet values ('28F41AE8-AEF3-4F79-8E57-4CA88D270E1D', '234561', 'Dell Latitude 5285')")
        
        #self.__build_db_from_ad()
        
        #self.__test_read_tablet_db()
        #self.__build_student_db_from_ad()
        
        self.clients = {}
        
        self.tablets_being_edited = []
        self.users_being_edited = []
        
        if WIPE_DB:
            self.__wipe_db()
        
        if SYNC_ACTIVE_DIRECTORY:
            self.__sync_tablet_db()
            self.__sync_user_db()
            
        if EXCEL_IMPORT:
            self.__import_excel()
            
        self.__check_link_singularities()
        
        print("Server is now running.")
        
    def __import_excel(self):
        not_found = []
        tablets_not_found = []
        
        import xlrd
        wb = xlrd.open_workbook('excel_db.xls')
        sheet = wb.sheets()[0]
        for row in range(sheet.nrows):
            if row == 0:
                continue
            
            first_name = sheet.cell(row, 0).value
            last_name = sheet.cell(row, 1).value
            tablet_pcsb = sheet.cell(row, 3).value.replace("-", "")
            tablet_serial = sheet.cell(row, 4).value
            tablet_device = "%i" % sheet.cell(row, 5).value
            
            student = Student.from_name(first_name + " " + last_name)
            if len(first_name) > 0 and not student:
                # Name couldn't be found
                print("Student", first_name + " " + last_name, "not found in Active Directory!")
                not_found.append(first_name + " " + last_name)
            
            tablet = Tablet.from_pcsb_tag(tablet_pcsb)
            if tablet:
                print("Tablet from excel sheet:", tablet_device, tablet_serial)
                tablet.device_model = tablet_device
                tablet.serial = tablet_serial
                tablet.update()
                
                if student:
                    print("\tStudent on tablet:", student.first_name + " " + student.last_name)
                    student.tablet_guid = tablet.guid
                    student.update_link()
                else:
                    print("\tNo student on tablet")
            elif len(tablet_pcsb) > 0:
                print("Can't find tablet", tablet_pcsb)
                tablets_not_found.append(tablet_pcsb)
                    
            if student:
                student.update()
                
        self.db_connection.commit()
        
        import_errors_out = open('excel_import_errors.txt', 'w')
        import_errors_out.write("Students not found in active directory:\n")
        for name in not_found:
            import_errors_out.write("\t" + name + "\n")
        import_errors_out.write("Tablets not found in active directory:\n")
        for t in tablets_not_found:
            import_errors_out.write("\t" + t + "\n")
        import_errors_out.flush()
        import_errors_out.close()
        
    def __wipe_db(self):
        c = self.db_connection.cursor()
        c.execute("DELETE FROM Tablet")
        c.execute("DELETE FROM Student")
        c.execute("DELETE FROM StudentTabletLink")
        c.execute("DELETE FROM TabletIssue")
        c.execute("DELETE FROM TabletIssueStep")
        self.db_connection.commit()
        print("Local database wiped")
        
    def __check_link_singularities(self):
        """
        Make sure that all student/tablet links reference valid students and tablets.
        If a link references a nonexistent student or tablet, the link will be removed.
        """
        c = self.db_connection.cursor()
        c.execute("SELECT * FROM StudentTabletLink")
        links = c.fetchall()
        for link in links:
            student_guid = link[0]
            tablet_guid = link[1]
            # Ensure both the student and tablet exist
            student = Student.from_guid(student_guid)
            tablet = Tablet.from_guid(tablet_guid)
            if (not student) or (not tablet):
                c.execute("DELETE FROM StudentTabletLink WHERE StudentGUID = ? AND TabletGUID = ?", (student_guid, tablet_guid))
                print("Deleting student/tablet link that references nonexistent student or tablet.")
                
        self.db_connection.commit()
        
    def __sync_user_db(self):
        """Makes sure our local database contains all of the Active Directory users."""
        print("Syncing local user database with Active Directory...")
        c = self.db_connection.cursor()
        all_students = Student.get_ad_cat_student_list()
        for ad_student in all_students:
            # Check for an entry
            c.execute("SELECT * FROM Student WHERE GUID = ?", (ad_student.guid_str,))
            student = c.fetchone()
            if not student:
                # Doesn't exist, make a default entry.
                c.execute("INSERT INTO Student VALUES (?,?,?,?,?,?,?)", (ad_student.guid_str, 0, 0, 0, "$0.00", "", 0))
                print("Added new student", ad_student.cn)
                
        # Now search for students in our local database that no longer exist in Active Directory.
        c.execute("SELECT * FROM Student")
        db_users = c.fetchall()
        for db_user in db_users:
            guid = db_user[0]
            student = Student.from_guid(guid)
            if not student:
                # Removed student
                c.execute("DELETE FROM Student WHERE GUID = ?", (guid,))
                print("Removed deleted student", guid)
                
                # Remove their tablet link
                c.execute("SELECT FROM StudentTabletLink WHERE StudentGUID = ?", (guid,))
                link = c.fetchone()
                if link:
                    c.execute("DELETE FROM StudentTabletLink WHERE StudentGUID = ?", (guid,))
                    print("\tRemoved student/tablet link for removed student")
                
        self.db_connection.commit()
        
        print("Done")
        
    def __sync_tablet_db(self):
        """Makes sure our local database contains all of the Active Directory tablets."""
        print("Syncing local tablet database with Active Directory...")
        
        c = self.db_connection.cursor()
        
        notspecified = 0
        
        all_tablets = Tablet.get_ad_tablet_list()
        
        for ad_tablet in all_tablets:
            # Check for an entry in our local database
            c.execute("SELECT * FROM Tablet WHERE GUID = ?", (ad_tablet.guid_str,))
            tablet = c.fetchone()
            if not tablet:
                # Doesn't exist, make a default entry.
                c.execute("INSERT INTO Tablet VALUES (?,'Not Specified','Not Specified')", (ad_tablet.guid_str,))
                print("Inserted new tablet")
                notspecified += 1
                
        # Now search for tablets in our local database that no longer exist in Active Directory.
        c.execute("SELECT * FROM Tablet")
        db_tablets = c.fetchall()
        for db_tablet in db_tablets:
            guid = db_tablet[0]
            tablet = Tablet.from_guid(guid)
            if not tablet:
                # Dead tablet
                c.execute("DELETE FROM Tablet WHERE GUID = ?", (guid,))
                print("Removed deleted tablet")
                
                # Remove their tablet link
                c.execute("SELECT FROM StudentTabletLink WHERE TabletGUID = ?", (guid,))
                link = c.fetchone()
                if link:
                    c.execute("DELETE FROM StudentTabletLink WHERE TabletGUID = ?", (guid,))
                    print("\tRemoved student/tablet link for removed tablet")
                
        self.db_connection.commit()
        
        print("Done")
        
    def __test_read_tablet_db(self):
        all_tablets = Tablet.get_ad_tablet_list()
        for ad_tablet in all_tablets:
            tablet = Tablet.from_active_directory_tablet(ad_tablet)
            print(str(tablet))
            
    def __build_student_db_from_ad(self):
        """Builds a database of students from entries in Active Directory."""
        c = self.db_connection.cursor()
        c.execute("DELETE FROM Student")
        
        all_students = Student.get_ad_cat_student_list()
        for ad_student in all_students:
            print (ad_student)
            c.execute("INSERT INTO Student VALUES (?,?,?,?,?,?)", (ad_student.guid_str, 0, 0, 0, "$0.00", ""))
        self.db_connection.commit()
        
    def __build_tablet_db_from_ad(self):
        """Builds a database of tablets from tablet entries in Active Directory."""
        
        c = self.db_connection.cursor()
        # Remove all current rows
        c.execute("DELETE FROM Tablet")
        
        all_tablets = Tablet.get_ad_tablet_list()
        
        notspecified = 0
        
        for tablet in all_tablets:
            c.execute("INSERT INTO Tablet VALUES (?,?,'Not Specified')", (tablet.guid_str, "Not Specified %s" % notspecified))
            print("Inserted tablet", tablet.guid_str)
            notspecified += 1
        self.db_connection.commit()
        
    def __check_connections(self):
        if self.listener.new_connection_available():
            print("-----------------------------------")
            print("New connection available...")
            rendezvous = core.PointerToConnection()
            net_addr = core.NetAddress()
            new_conn = core.PointerToConnection()
            if self.listener.get_new_connection(rendezvous, net_addr, new_conn):
                new_conn = new_conn.p()
                self.clients[str(new_conn.this)] = Client(new_conn, rendezvous)
                self.reader.add_connection(new_conn)
                print("IP Address: %s" % new_conn.get_address())
                print("Connection ID: %s" % new_conn.this)
                
    def __check_datagrams(self):
        if self.reader.data_available():
            datagram = core.NetDatagram()
            if self.reader.get_data(datagram):
                self.handle_datagram(datagram)
                
    def __check_disconnections(self):
        if self.mgr.reset_connection_available():
            pconn = core.PointerToConnection()
            self.mgr.get_reset_connection(pconn)
            lost_conn = pconn.p()
            print("-----------------------------------")
            print("Farewell connection...")
            print("ConnectionID: %s" % lost_conn.this)
            client = self.clients[str(lost_conn.this)]
            
            # Free up any users/tablets that were being edited by this client.
            if client.user_editing is not None and client.user_editing in self.users_being_edited:
                print("Client was editing user", client.user_editing)
                self.users_being_edited.remove(client.user_editing)
            if client.tablet_editing is not None and client.tablet_editing in self.tablets_being_edited:
                print("Client was editing tablet", client.tablet_editing)
                self.tablets_being_edited.remove(client.tablet_editing)
                
            del self.clients[str(lost_conn.this)]
            self.mgr.close_connection(lost_conn)
                
    def handle_datagram(self, dg):
        connection = dg.get_connection()
        client = self.clients.get(str(connection.this), None)
        if not client:
            print("Received datagram from unknown client")
            return
        
        dgi = core.DatagramIterator(dg)
        
        msg_type = dgi.get_uint16()
        
        if client.client_type == CLIENT_UNIDENTIFIED:
            self.__handle_datagram_unidentified(connection, client, dgi, msg_type)
        elif client.client_type == CLIENT_STUDENT:
            self.__handle_datagram_student(connection, client, dgi, msg_type)
        elif client.client_type == CLIENT_NET_ASSISTANT:
            self.__handle_datagram_netassistant(connection, client, dgi, msg_type)
        else:
            print("Received datagram from unknown client type")
            
    def __handle_datagram_unidentified(self, connection, client, dgi, msg_type):
        if msg_type == MSG_CLIENT_IDENTIFY:
            client_type = dgi.get_uint8()
            print("Client %s identified as %i" % (client.connection_id, client_type))
            client.identify(client_type)
            
    def __handle_datagram_student(self, connection, client, dgi, msg_type):
        if msg_type == MSG_CLIENT_LOOKUP_TABLET:
            pcsb_tag = dgi.get_string()
            
            dg = core.Datagram()
            dg.add_uint16(MSG_SERVER_LOOKUP_TABLET_RESP)
            
            tablet = Tablet.from_pcsb_tag(pcsb_tag)
            if not tablet:
                print("Can't find tablet with PCSB Tag %s" % pcsb_tag)
                dg.add_uint8(0)
                self.writer.send(dg, connection)
                return
                
            if not tablet.student_guid:
                student_name = ""
                student_email = ""
                student_grade = ""
            else:
                student = Student.from_guid(tablet.student_guid)
                student_name = student.first_name + " " + student.last_name
                student_grade = student.grade
                student_email = student.email
                
            if not student_grade:
                student_grade = ""
            if not student_email:
                student_email = ""
            
            dg.add_uint8(1)
            tablet.write_datagram(dg)
            dg.add_string(student_name)
            dg.add_string(student_grade)
            dg.add_string(student_email)
            self.writer.send(dg, connection)
            
        elif msg_type == MSG_CLIENT_SUBMIT_ISSUE:
            pcsb_tag = dgi.get_string()
            tablet = Tablet.from_pcsb_tag(pcsb_tag)
            if not tablet:
                print("Can't submit issue, pcsb tag %s not found" % pcsb_tag)
                return
            incident_desc = dgi.get_string()
            incident_date = dgi.get_string()
            problem_desc = dgi.get_string()
            hwguid = dgi.get_string()
            c = self.db_connection.cursor()
            issue = Issue(-1, tablet.guid, incident_desc, problem_desc, incident_date, 0, "", "", 2, "", 0, hwguid, "", 0)
            issue.write_database(c)
            self.db_connection.commit()
            print("Submitting:\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s" % (pcsb_tag, incident_desc, incident_date, problem_desc, hwguid))
            
            dg = core.Datagram()
            dg.add_uint16(MSG_SERVER_UPDATE_ISSUE)
            dg.add_uint16(1)
            issue.write_datagram(dg)
            self.send(dg, self.get_all_client_connections(CLIENT_NET_ASSISTANT))
            
        elif msg_type == MSG_CLIENT_REQ_NET_ASSISTANTS:
            hws = Student.get_ad_net_assistants()
            
            # Borg doesn't want this selectable in the issue dropdown.
            for hw in hws:
                if hw.name == "CAT network assistant":
                    hws.remove(hw)
                    break
                    
            dg = core.Datagram()
            dg.add_uint16(MSG_SERVER_NET_ASSISTANTS_RESP)
            num_hws = len(hws)
            dg.add_uint32(num_hws)
            for i in range(num_hws):
                hw = Student.from_active_directory_student(hws[i])
                hw.write_datagram(dg)
            self.writer.send(dg, connection)
            
    def get_all_client_connections(self, client_type):
        clients = []
        for client in self.clients.values():
            if client.client_type == client_type:
                clients.append(client.connection)
        return clients
        
    def __write_user_tablet(self, student, dg):
        has_tablet = False
        if student.tablet_guid:
            tablet = Tablet.from_guid(student.tablet_guid)
            if tablet:
                has_tablet = True
                dg.add_string(tablet.pcsb_tag)
        if not has_tablet:
            dg.add_string("No Tablet Assigned")
            
    def send(self, dg, connections):
        if isinstance(connections, list):
            for conn in connections:
                self.writer.send(dg, conn)
        else:
            self.writer.send(dg, connections)
        
    def __send_user(self, guid, connections):
        dg = core.Datagram()
        dg.add_uint16(MSG_SERVER_UPDATE_USER)
        
        student = Student.from_guid(guid)
        if not student:
            return
            
        student.write_datagram(dg)
        
        self.send(dg, connections)
            
    def __send_all_users(self, connections):
        dg = core.Datagram()
        dg.add_uint16(MSG_SERVER_GET_ALL_USERS_RESP)
        
        student_dg = core.Datagram()
        
        all_students = Student.get_ad_cat_student_list()
        
        num_students = 0
        
        for ad_student in all_students:
            student = Student.from_active_directory_student(ad_student)
            if not student:
                continue
            student.write_datagram(student_dg)
            num_students += 1
            
        dg.add_uint16(num_students)
        dg.append_data(student_dg.get_message())
        
        self.send(dg, connections)
        
    def __handle_datagram_netassistant(self, connection, client, dgi, msg_type):
        if msg_type == MSG_CLIENT_GET_ALL_TABLETS:
        
            dg = core.Datagram()
            dg.add_uint16(MSG_SERVER_GET_ALL_TABLETS_RESP)
            
            tablet_dg = core.Datagram()
            num_tablets = 0
            
            all_tablets = Tablet.get_ad_tablet_list()
            for ad_tablet in all_tablets:
                tablet = Tablet.from_active_directory_tablet(ad_tablet)
                if not tablet:
                    continue
                    
                tablet.write_datagram(tablet_dg)
                num_tablets += 1
                
            dg.add_uint16(num_tablets)
            dg.append_data(tablet_dg.get_message())
            
            self.writer.send(dg, connection)
            
        elif msg_type == MSG_CLIENT_GET_ALL_USERS:
            self.__send_all_users(connection)
            
        elif msg_type == MSG_CLIENT_EDIT_USER:
            guid = dgi.get_string()
            print("Received edit user request for guid:", guid)
            dg = core.Datagram()
            dg.add_uint16(MSG_SERVER_EDIT_USER_RESP)
            if not guid in self.users_being_edited and client.user_editing is None:
                dg.add_uint8(1)
                dg.add_string(guid)
                client.user_editing = guid
                self.users_being_edited.append(guid)
            else:
                # User is already being edited by another client
                dg.add_uint8(0)
            self.writer.send(dg, connection)
            
        elif msg_type == MSG_CLIENT_EDIT_TABLET:
            guid = dgi.get_string()
            dg = core.Datagram()
            dg.add_uint16(MSG_SERVER_EDIT_TABLET_RESP)
            if not guid in self.tablets_being_edited and client.tablet_editing is None:
                dg.add_uint8(1)
                dg.add_string(guid)
                client.tablet_editing = guid
                self.tablets_being_edited.append(guid)
            else:
                # Tablet is already being edited by another client
                dg.add_uint8(0)
            self.writer.send(dg, connection)
            
        elif msg_type == MSG_CLIENT_FINISH_EDIT_TABLET:
            ret = dgi.get_uint8()
            
            mod_tablet = BaseTablet.from_datagram(dgi)
            
            guid = mod_tablet.guid
            if guid in self.tablets_being_edited and client.tablet_editing == guid:
                if ret:
                    mod_tablet.__class__ = Tablet # hack
                    mod_tablet.update()
                    
                    c = self.db_connection.cursor()
                    
                    issues_dg = core.Datagram()
                    issues_dg.add_uint16(MSG_SERVER_UPDATE_ISSUE)
                    num_issues = dgi.get_uint16()
                    issues_dg.add_uint16(num_issues)
                    for i in range(num_issues):
                        issue = Issue.from_datagram(dgi)
                        issue.write_database(c)
                        issue.write_datagram(issues_dg)
                    
                    steps_dg = core.Datagram()
                    steps_dg.add_uint16(MSG_SERVER_UPDATE_ISSUE_STEP)
                    num_steps = dgi.get_uint16()
                    steps_dg.add_uint16(num_steps)
                    for i in range(num_steps):
                        step = IssueStep.from_datagram(dgi)
                        step.write_database(c)
                        step.write_datagram(steps_dg)
                    
                    tablet_dg = core.Datagram()
                    tablet_dg.add_uint16(MSG_SERVER_UPDATE_TABLET)
                    mod_tablet.write_datagram(tablet_dg)
                    
                    # Send the updated data to all net clients.
                    netconns = self.get_all_client_connections(CLIENT_NET_ASSISTANT)
                    self.send(issues_dg, netconns)
                    self.send(steps_dg, netconns)
                    self.send(tablet_dg, netconns)
                        
                    self.db_connection.commit()
                    
                print("Done editing tablet", guid)
                client.tablet_editing = None
                self.tablets_being_edited.remove(guid)
            else:
                print("Suspicious: finished editing a tablet that wasn't being edited")
                
        elif msg_type == MSG_CLIENT_GET_ALL_ISSUES:
            c = self.db_connection.cursor()
            c.execute("SELECT * FROM TabletIssue")
            issues = c.fetchall()
            num_issues = len(issues)
            dg = core.Datagram()
            dg.add_uint16(MSG_SERVER_GET_ALL_ISSUES_RESP)
            dg.add_uint32(num_issues)
            for i in range(num_issues):
                data = issues[i]
                issue = Issue(*data)
                issue.write_datagram(dg)
            self.writer.send(dg, connection)
            
        elif msg_type == MSG_CLIENT_GET_ALL_ISSUE_STEPS:
            c = self.db_connection.cursor()
            c.execute("SELECT * FROM TabletIssueStep")
            steps = c.fetchall()
            num_steps = len(steps)
            dg = core.Datagram()
            dg.add_uint16(MSG_SERVER_GET_ALL_ISSUE_STEPS_RESP)
            dg.add_uint32(num_steps)
            for i in range(num_steps):
                data = steps[i]
                step = IssueStep(*data)
                step.write_datagram(dg)
            self.writer.send(dg, connection)
            
        elif msg_type == MSG_CLIENT_GET_ALL_LINKS:
            c = self.db_connection.cursor()
            c.execute("SELECT * FROM StudentTabletLink")
            links = c.fetchall()
            num_links = len(links)
            dg = core.Datagram()
            dg.add_uint16(MSG_SERVER_GET_ALL_LINKS_RESP)
            dg.add_uint32(num_links)
            for i in range(num_links):
                data = links[i]
                link = StudentTabletLink(*data)
                link.write_datagram(dg)
            self.writer.send(dg, connection)
                
        elif msg_type == MSG_CLIENT_FINISH_EDIT_USER:
            guid = dgi.get_string()
            if guid in self.users_being_edited and client.user_editing == guid:
                print("Done editing user", guid)
                client.user_editing = None
                self.users_being_edited.remove(guid)
                
                ret = dgi.get_uint8()
                if ret:
                    pcsb_agreement = dgi.get_uint8()
                    cat_agreement = dgi.get_uint8()
                    insurance = dgi.get_uint8()
                    insurance_amt = dgi.get_string()
                    tablet_pcsb = dgi.get_string()
                    equipment_receipt = dgi.get_uint8()
                    
                    error = 0
                    
                    student = Student.from_guid(guid)
                    
                    has_new_insurance = False
                    if insurance and not student.insurance_paid:
                        has_new_insurance = True
                        insurance_date = dgi.get_string()
                        print("New insurance date", insurance_date)
                    
                    student.pcsb_agreement = pcsb_agreement
                    student.cat_agreement = cat_agreement
                    student.equipment_receipt = equipment_receipt
                    student.insurance_paid = insurance
                    student.insurance_amount = insurance_amt
                    if not insurance:
                        student.date_of_insurance = ""
                    elif has_new_insurance:
                        student.date_of_insurance = insurance_date
                    if len(tablet_pcsb) > 0:
                        tablet = Tablet.from_pcsb_tag(tablet_pcsb)
                        if not tablet:
                            error = 1
                        else:
                            student.tablet_guid = Tablet.from_pcsb_tag(tablet_pcsb).guid
                    else:
                        student.tablet_guid = None
                    student.update()
                    
                    dg = core.Datagram()
                    dg.add_uint16(MSG_SERVER_FINISH_EDIT_USER_RESP)

                    if error == 0:
                        try:
                            student.update_link()
                            dg.add_uint8(1)
                        except Exception as e:
                            error = 2
                            
                    if error == 1:
                        dg.add_uint8(0)
                        dg.add_string("There was an error assigning the tablet: bad PCSB Tag")
                    elif error == 2:
                        dg.add_uint8(0)
                        dg.add_string("There was an error assigning the tablet: already assigned")
                        
                    self.writer.send(dg, connection)
                    
                    self.__send_user(guid, self.get_all_client_connections(CLIENT_NET_ASSISTANT))

                    # Send the updated link, if there is one
                    c = self.db_connection.cursor()
                    c.execute("SELECT * FROM StudentTabletLink WHERE StudentGUID = ?", (student.guid,))
                    link = c.fetchone()
                    if link:
                        dg = core.Datagram()
                        dg.add_uint16(MSG_SERVER_UPDATE_LINK)
                        dg.add_uint16(1)
                        slink = StudentTabletLink(*link)
                        slink.write_datagram(dg)
                        self.send(dg, self.get_all_client_connections(CLIENT_NET_ASSISTANT))
                    
            else:
                print("Suspicious: finished editing a user that wasn't being edited")
    
    def run(self):
        self.__check_connections()
        self.__check_datagrams()
        self.__check_disconnections()
        
server = Server()
while True:
    server.run()
