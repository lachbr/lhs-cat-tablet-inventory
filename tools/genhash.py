import hashlib

prog = open('built_client\\main.exe', 'rb')
prog_hash = hashlib.md5(prog.read()).hexdigest()
print(prog_hash)