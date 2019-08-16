import sys

from panda3d import core

from src.shared.Consts import *

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
        
    def identify(self):
        dg = core.Datagram()
        dg.addUint16(MSG_CLIENT_IDENTIFY)
        dg.addUint8(CLIENT_STUDENT)
        self.writer.send(dg, self.connection)
        
    def __check_datagrams(self):
        if self.reader.data_available():
            dg = core.Datagram()
            if self.reader.get_data(dg):
                self.handle_datagram(dg)
                
    def handle_datagram(self, dg):
        pass
        
    def run(self):
        self.__check_datagrams()

conn = ServerConnection('127.0.0.1', 7035)
while True:
    conn.run()
