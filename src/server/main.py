from panda3d import core

from src.shared.Consts import *

from pyad import *

import sqlite3

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
    
    def __init__(self):
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
        
        tablet_group = adcontainer.ADContainer.from_cn("Computers")
        #print(testgroup)
        #print(dir(testgroup))
        #members = testgroup.get_children()
        #print(members)
        #for mem in members:
        #    print(dir(mem))
        #    print(mem.guid_str)
        #print(dir(testgroup))
        
        self.db_connection = sqlite3.connect('tablet_inventory.db')
        c = self.db_connection.cursor()
        #c.execute("insert into Tablet values ('28F41AE8-AEF3-4F79-8E57-4CA88D270E1D', '234561', 'Dell Latitude 5285')")
        c.execute("select * from Tablet")
        tablet = c.fetchone()
        tablet_guid = tablet[0]
        ad_tablet = tablet_group.from_guid(tablet_guid)
        print(ad_tablet)
        print(dir(ad_tablet))
        print(ad_tablet.displayName)
        self.db_connection.commit()
        self.db_connection.close()
        
        self.clients = {}
        
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
            dg.add_uint8(1)
            dg.add_string("598253")
            dg.add_string("Dell Latitude 5295")
            dg.add_string("Brian Lach")
            dg.add_string("12")
            dg.add_string("lachb@cat.pcsb.org")
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
            
            dg.add_uint16(3) # tablet count
            for i in range(3):
                dg.add_string("044-0532")
                dg.add_string("Dell Latitude 5295")
                dg.add_string("623523")
                dg.add_string("No")
                dg.add_string("Brian Lach")
            self.writer.send(dg, connection)
    
    def run(self):
        self.__check_connections()
        self.__check_datagrams()
        self.__check_disconnections()
        
server = Server()
while True:
    server.run()
