import socket, md5, struct
from nose.tools import *

class CryptServerClient(object):
    def __init__(self, ip, port):
        self.sock = socket.create_connection((ip, port))
        self.sock.settimeout(1.0)
        self.recv_buf = ''

    def close(self):
        self.sock.close()
        
    def crypt_msg(self, msg_in, mode):
        print 'Enter crypt_msg()'
        assert_in(mode, ('e', 'd')) # encrypt, decrypt
        msg = struct.pack('!cL', mode, len(msg_in)) + msg_in

        self.sock.sendall(msg)
        print 'crypt_msg() msg sent:'
        hexprint(msg_in)
    
        self.recv_buf += self.sock.recv(65536)
        while len(self.recv_buf) < 4:
            self.recv_buf += self.sock.recv(65536)
        msg_len = struct.unpack_from('!L', self.recv_buf, 0)[0]
        print 'crypt_msg() head received, len = %d'%msg_len
        while len(self.recv_buf) < 4+msg_len:
            self.recv_buf += self.sock.recv(65536)
        print 'crypt_msg() msg received'

        resp_msg = self.recv_buf[4:4+msg_len]
        self.recv_buf = self.recv_buf[4+msg_len:]
        return resp_msg        

def hexprint(msg):
    s, i = '', 0    
    for c in msg:
        v = ord(c)
        if v < 16:
            s += '0' + hex(v)[2:]
        else:
            s += hex(v)[2:]
        if 1 == i%2: s += ' '
        if 31 == i%32: s += '\n'
        i += 1
    print s

def iphex(ip_str): # "127.0.0.1" -> "\xff\x00\x00\x01"
    d=map(lambda s:int(s), ip_str.split('.'))
    return struct.pack('!BBBB', *d)

def ipstr(buf):
    eq_(4, len(buf))    
    return '.'.join(map(lambda c:str(ord(c)), buf))


