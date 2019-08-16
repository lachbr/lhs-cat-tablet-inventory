import pickle

def serialize(obj):
    return pickle.dumps(obj, -1)
    
def unserialize(obj):
    return pickle.loads(obj)
    
NEW_MESSAGE = bytes(NEW_MESSAGE, 'ascii')
    
def send(conn, pszdata):
    pszdata = NEW_MESSAGE + pszdata
    conn.send(pszdata)
    
SERVER_ADDRESS  = '127.0.0.1'
SERVER_PORT     = 7035
    
#############################################

import threading
    

    
class Client:
    
    def __init__(self, conn, address):
        print("New client:", conn, address)
        self.connection = conn
        self.address = address
        self.client_type = CLIENT_UNIDENTIFIED
        
        self.reader_thread = threading.Thread(target = self.__reader_thread_func)
        self.reader_thread.start()
        
    def __lost_connection(self):
        print("Client at {0} lost connection".format(self.address))
        self.cleanup()
        
    def cleanup(self):
        self.reader_thread = None
        self.connection = None
        self.address = None
        self.client_type = None
        
    def __do_read_message(self):
        length = None
        buff = ""
        
        while True:
            try:
                pszdata = self.connection.recv(4096)
            except:
                pszdata = None
            if not pszdata:
                self.__lost_connection()
                break
                
            if NEW_MESSAGE in pszdata:
                
            
                data = unserialize(pszdata)
                print("Received from client:", data)
        
    def __reader_thread_func(self):
        while True:
            self.__do_read_message()
        
    def is_identified(self):
        return self.client_type != CLIENT_UNIDENTIFIED
        
    def identify(self, ident):
        self.client_type = ident
