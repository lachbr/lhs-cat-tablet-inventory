from panda3d import core

from src.shared.Consts import *
from src.shared.base_tablet import BaseTablet

from pyad import *

import sqlite3

g_server_connection = None

class Student:

    @staticmethod
    def get_ad_cat_student_list():
        return pyad.from_dn("ou=+AllCATStudents,dc=cat,dc=pcsb,dc=org").get_children()
    
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
        
        return Student(
            ad_student, db_student[1], db_student[2],
            db_student[3], db_student[4], tablet_guid
        )
        
    @staticmethod
    def from_guid(guid_str):
        ad_student = pyad.from_guid(guid_str)
        return Student.from_active_directory_student(ad_student)
        
    def __init__(self, ad_student, pcsb_agreement = False, cat_agreement = False, insurance_paid = False, insurance_amount = "$0.00", tablet_guid = None):
        self.ad_student = ad_student
        self.name = ad_student.displayName
        self.grade = ad_student.description
        self.email = ad_student.userPrincipalName
        self.guid = ad_student.guid_str
        self.pcsb_agreement = pcsb_agreement
        self.cat_agreement = cat_agreement
        self.insurance_paid = insurance_paid
        self.insurance_amount = insurance_amount
        # They are a CAT student if in the +AllCATStudents container
        self.cat_student = pyad.from_dn("ou=+AllCATStudents,dc=cat,dc=pcsb,dc=org") is not None
        self.tablet_guid = tablet_guid
        
    def write_datagram(self, dg):
        dg.add_string(self.name)
        dg.add_string(self.grade)
        dg.add_string(self.email)
        dg.add_uint8(self.pcsb_agreement)
        dg.add_uint8(self.cat_agreement)
        dg.add_uint8(self.insurance_paid)
        dg.add_string(self.insurance_amount)
        dg.add_uint8(self.cat_student)
    
    def __str__(self):
        return ("GUID: %s\n\tName: %s\n\tGrade: %s\n\tPCSB Agreement: %s\n"
            "\tCAT Agreement: %s\n\tInsurance Paid: %s\n\tInsurance Amount: %s\n"
            "\tCAT Student: %s\n\tTablet GUID: %s" % (self.guid, self.name, self.grade, self.pcsb_agreement,
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
        tablet = pyad.from_guid(guid_str)
        return tablet
        
    @staticmethod
    def get_ad_tablet_from_name(name_str):
        tablet = pyad.from_cn(name_str)
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
            return Tablet(ad_tablet, pcsb_tag)
            
        # Find the student with the tablet
        student_guid = None
        c.execute("SELECT * FROM StudentTabletLink WHERE TabletGUID=?", (ad_tablet.guid_str,))
        link = c.fetchone()
        if link:
            student_guid = link[0]
        
        return Tablet(ad_tablet, pcsb_tag, tablet_info[1], tablet_info[2], student_guid)
        
    @staticmethod
    def from_pcsb_tag(pcsb_tag):
        pcsb_tag = pcsb_tag.strip('-')
        name_str = Tablet.NAME_PREFIX + pcsb_tag
        return Tablet.from_active_directory_tablet(Tablet.get_ad_tablet_from_name(name_str))
        
    def update(self):
        c = g_server_connection.db_connection.cursor()
        c.execute(
            "UPDATE Tablet SET SerialNumber = ?, SET DeviceModel = ? WHERE GUID = ?",
            (self.serial, self.device_model, self.guid)
        )
        
    def update_link(self):
        c = g_server_connection.db_connection.cursor()
        if self.student_guid is None:
            c.execute("DELETE FROM StudentTabletLink WHERE TabletGUID = ?", (self.guid))
        else:
            c.execute("UPDATE StudentTabletLink SET StudentGUID = ? WHERE TabletGUID = ?", (self.student_guid, self.guid))

class Client:
    
    def __init__(self, conn, rendezvous):
        self.connection = conn
        self.connection_id = str(conn.this)
        self.rendezvous = rendezvous
        self.client_type = CLIENT_UNIDENTIFIED
        
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
        self.socket = self.mgr.open_TCP_server_rendezvous('127.0.0.1', 7035, 10)
        self.listener.add_connection(self.socket)
        
        domain = "cat.pcsb.org"
        user = "net.assistant"
        password = "You can't handle the truth!"
        pyad.set_defaults(ldap_server = domain, username = user, password = password)
        
        self.db_connection = sqlite3.connect('tablet_inventory.db')
        #c.execute("insert into Tablet values ('28F41AE8-AEF3-4F79-8E57-4CA88D270E1D', '234561', 'Dell Latitude 5285')")
        
        #self.__build_db_from_ad()
        
        #self.__test_read_tablet_db()
        #self.__build_student_db_from_ad()
        
        self.clients = {}
        
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
            c.execute("INSERT INTO Student VALUES (?,?,?,?,?)", (ad_student.guid_str, 0, 0, 0, "$0.00"))
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
                print("No student assigned to tablet %s" % pcsb_tag)
                dg.add_uint8(0)
                self.writer.send(dg, connection)
                return
            student = Student.from_guid(tablet.student_guid)
            
            dg.add_uint8(1)
            tablet.write_datagram(dg)
            dg.add_string(student.name)
            dg.add_string(student.grade)
            dg.add_string(student.email)
            self.writer.send(dg, connection)
            
        elif msg_type == MSG_CLIENT_SUBMIT_ISSUE:
            pcsb_tag = dgi.get_string()
            incident_desc = dgi.get_string()
            incident_date = dgi.get_string()
            problem_desc = dgi.get_string()
            print("Submitting:\n\t%s\n\t%s\n\t%s\n\t%s" % (pcsb_tag, incident_desc, incident_date, problem_desc))
        
    def __handle_datagram_netassistant(self, connection, client, dgi, msg_type):
        if msg_type == MSG_CLIENT_GET_ALL_TABLETS:
        
            dg = core.Datagram()
            dg.add_uint16(MSG_SERVER_GET_ALL_TABLETS_RESP)
            
            assigned_dg = core.Datagram()
            unassigned_dg = core.Datagram()
            num_assigned_tablets = 0
            num_unassigned_tablets = 0
            
            all_tablets = Tablet.get_ad_tablet_list()
            for ad_tablet in all_tablets:
                tablet = Tablet.from_active_directory_tablet(ad_tablet)
                if not tablet:
                    continue
                    
                if tablet.student_guid:
                    tablet.write_datagram(assigned_dg)
                    student = Student.from_guid(tablet.student_guid)
                    assigned_dg.add_string(student.name)
                    num_assigned_tablets += 1
                else:
                    tablet.write_datagram(unassigned_dg)
                    num_unassigned_tablets += 1
                   
            # Write the assigned tablets, then unassigned tablets
            dg.add_uint16(num_assigned_tablets)
            dg.append_data(assigned_dg.get_message())
            dg.add_uint16(num_unassigned_tablets)
            dg.append_data(unassigned_dg.get_message())
            
            self.writer.send(dg, connection)
            
        elif msg_type == MSG_CLIENT_GET_ALL_USERS:
        
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
                
                has_tablet = False
                if student.tablet_guid:
                    tablet = Tablet.from_guid(student.tablet_guid)
                    if tablet:
                        has_tablet = True
                        student_dg.add_string(tablet.pcsb_tag)
                if not has_tablet:
                    student_dg.add_string("No Tablet Assigned")
                num_students += 1
                
            dg.add_uint16(num_students)
            dg.append_data(student_dg.get_message())
            
            self.writer.send(dg, connection)
    
    def run(self):
        self.__check_connections()
        self.__check_datagrams()
        self.__check_disconnections()
        
server = Server()
while True:
    server.run()
