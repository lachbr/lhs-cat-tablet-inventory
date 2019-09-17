import hashlib

fname = input("File to hash: ")
fout = input("Hash output file: ")

prog = open(fname, 'rb')
prog_hash = hashlib.md5(prog.read()).hexdigest()
print(prog_hash)

out = open(fout, 'w')
out.write(prog_hash)
out.flush()
out.close()

