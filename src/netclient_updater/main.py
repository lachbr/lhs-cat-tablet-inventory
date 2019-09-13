import hashlib

prog = open('main.exe', 'rb')
prog_hash = hashlib.md5(prog.read()).hexdigest()
prog.close()

