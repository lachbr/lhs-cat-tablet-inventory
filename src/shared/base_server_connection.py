from panda3d import core

import sys

from src.shared.Consts import *

class BaseServerConnection:

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
        
    def get_identity(self):
        return CLIENT_UNIDENTIFIED
        
    def send(self, dg):
        self.writer.send(dg, self.connection)
        
    def identify(self):
        dg = core.Datagram()
        dg.add_uint16(MSG_CLIENT_IDENTIFY)
        dg.add_uint8(self.get_identity())
        self.writer.send(dg, self.connection)
        
    def handle_datagram(self, dgi, msg_type):
        pass
        
    def __handle_datagram(self, dg):
        dgi = core.DatagramIterator(dg)
        
        msg_type = dgi.get_uint16()
        
        self.handle_datagram(dgi, msg_type)
        
    def __check_datagrams(self):
        if self.reader.data_available():
            dg = core.Datagram()
            if self.reader.get_data(dg):
                self.__handle_datagram(dg)
                
    def run(self):
        self.__check_datagrams()
