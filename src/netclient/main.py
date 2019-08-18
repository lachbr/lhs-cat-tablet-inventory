from src.shared.base_server_connection import BaseServerConnection
from src.shared.Consts import *

import sys

g_server_connection = None
g_main_window = None

class ServerConnection(BaseServerConnection):
    
    def get_identity(self):
        return CLIENT_NET_ASSISTANT
        
from PyQt5 import QtWidgets, QtCore

class NetClientApp(QtWidgets.QApplication):
    
    def __init__(self):
        QtWidgets.QApplication.__init__(self, [])
        
        global g_server_connection
        global g_main_window
        
        self.server_connection = ServerConnection('127.0.0.1', 7035)
        # Timer which ticks the connection to the server
        self.server_timer = QtCore.QTimer()
        self.server_timer.timeout.connect(self.server_connection.run)
        self.server_timer.setSingleShot(False)
        self.server_timer.start(0)
        
        g_server_connection = self.server_connection
        
        #self.window = ClientWindow()
        #self.window.show()
        
        #g_main_window = self.window

app = NetClientApp()
sys.exit(app.exec_())
