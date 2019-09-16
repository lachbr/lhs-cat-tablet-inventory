import hashlib
import ftplib
import os

class UpdaterLauncher:
    
    def __init__(self, server_hash_file, server_exe_file, local_exe_file):
        self.server_hash_file = server_hash_file
        self.server_exe_file = server_exe_file
        self.local_exe_file = local_exe_file
        
    def make_ftp(self):
        ftp = ftplib.FTP('c2031snas2')
        ftp.login('tablet_inventory', 'The Force is Strong')
        return ftp
        
    def __handle_get_server_hash(self, server_hash):
        # Get local hash
        print("Server hash is", server_hash)
        prog = open(self.local_exe_file, 'rb')
        prog_hash = hashlib.md5(prog.read()).hexdigest()
        prog.close()
        print("Local hash is", prog_hash)
        
        if prog_hash != server_hash:
            print("Local exe is out of date, downloading")
            local = open(self.local_exe_file, 'wb')
            ftp = self.make_ftp()
            ftp.retrbinary('RETR ' + self.server_exe_file, local.write)
            local.flush()
            local.close()
            
        print("Up to date!")
        self.__launch()
        
    def __launch(self):
        os.system(self.local_exe_file)
        
    def do_update_and_launch(self):
        ftp = self.make_ftp()
        ftp.retrlines('RETR ' + self.server_hash_file, self.__handle_get_server_hash)
        
def do_update_and_launch(server_hash_file, server_exe_file, local_exe_file):
    ul = UpdaterLauncher(server_hash_file, server_exe_file, local_exe_file)
    ul.do_update_and_launch()
