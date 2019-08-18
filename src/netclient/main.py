from src.shared.base_server_connection import BaseServerConnection
from src.shared.Consts import *

import sys
from datetime import datetime

g_server_connection = None
g_main_window = None

class ServerConnection(BaseServerConnection):
    
    def get_identity(self):
        return CLIENT_NET_ASSISTANT
        
from PyQt5 import QtWidgets, QtCore

class ClientWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        from src.netclient.net_mainwindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.clock_timer = QtCore.QTimer()
        self.clock_timer.timeout.connect(self.__update_clock)
        self.clock_timer.setSingleShot(False)
        self.clock_timer.start(0)
        
        self.blink_second = 0
        self.blink_state = 0
        
    def __get_block(self, now):
        block_ranges = {
            "1"     : ("7:10 AM", "8:40 AM"),
            "2"     : ("8:45 AM", "10:15 AM"),
            "Lunch" : ("10:15 AM", "10:45 AM"),
            "3"     : ("10:50 AM", "12:20 PM"),
            "4"     : ("12:25 PM", "1:55 PM")
        }
        
        block = "None"
        for blockName, startEnd in block_ranges.items():
            startDt = datetime.strptime(startEnd[0], "%I:%M %p")
            endDt = datetime.strptime(startEnd[1], "%I:%M %p")
            if now >= startDt and now < endDt:
                block = blockName
                break
                
        return block
        
    def __update_clock(self):
        now = datetime.now()
        if self.blink_state:
            time_str = now.strftime("%I:%M %p")
        else:
            time_str = now.strftime("%I %M %p")
            
        self.ui.timeLabel.setText("Time: %s" % time_str)
        
        if now.second != self.blink_second:
            self.blink_state = not self.blink_state
            self.blink_second = now.second
            
        self.ui.blockLabel.setText("Block: %s" % self.__get_block(now))

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
        
        self.window = ClientWindow()
        self.window.show()
        
        g_main_window = self.window

app = NetClientApp()
sys.exit(app.exec_())
