import core

CLIENT_UNIDENTIFIED     = 0
CLIENT_NET_ASSISTANT    = 1
CLIENT_STUDENT          = 2

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
                print("ConnectionID: %s" % new_conn.this)
                
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
        pass
    
    def run(self):
        self.__check_connections()
        self.__check_datagrams()
        self.__check_disconnections()
        
server = Server()
while True:
    server.run()
