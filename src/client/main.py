import sys

class ServerConnection:
    
    def __init__(self, address, port):
        self.mgr = core.QueuedConnectionManager()
        self.reader = core.QueuedConnectionReader(self.mgr, 1)
        self.writer = core.QueuedConnectionWriter(self.mgr, 1)
        self.address = address
        self.port = port
        
        self.connection = self.mgr.open_TCP_client_connection(self.address, self.port, 0)
        if not self.connection:
            print "ERROR: Can't connect"
            sys.exit(1)
        self.reader.add_connection(self.connection)
