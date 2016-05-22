import socket, struct, time, binascii, sys, random
from nose.tools import *

ip, port = '', 21000

def crypt(mode, msg_in):
    assert_in(mode, ('e', 'd'))
    c = socket.create_connection((ip, port))
    try:
        msg = struct.pack('!cL', mode, len(msg_in)) + msg_in
        c.sendall(msg)

        buf, endtime = '', time.time()+1.0
        while time.time() < endtime:
            s = c.recv(8192)
            ok_(s)
            buf += s
            if len(buf) < 4:
                continue
            msg_len = struct.unpack_from('!L', buf, 0)[0]
            if len(buf) < 4 + msg_len:
                continue
            assert len(buf) == 4 + msg_len, 'msg_len=%d, len(buf)=%d'%(msg_len, len(buf))
            c.close()
            return buf[4:]
        assert False, 'Receive timeout'
    finally:
        c.close()

def loop_test():
    msg_list = []
    for i in range(1000):
        msg = ''
        for j in range(random.randint(1, 2000)):
            msg += chr(random.randint(0, 255))
        msg_list.append(msg)

    for msg in msg_list:
        try:
            encrypted = crypt('e', msg)
            decrypted = crypt('d', encrypted)
            eq_(msg, decrypted)
            sys.stdout.write('.')
            sys.stdout.flush()
        except Exception as e:            
            print e
            print 'msg =', binascii.b2a_hex(msg)
            print ''
        
if __name__ == '__main__':
    loop_test()

    
"""
c = socket.create_connection((ip, port))

pt1 = 'abcd\1\2\3\4'
print 'pt1 =', binascii.b2a_hex(pt1)
msg = struct.pack('!cL', 'e', len(pt1)) + pt1
c.sendall(msg)

time.sleep(1.0)
buf = c.recv(4096)
msg_len = struct.unpack_from('!L', buf, 0)[0]
assert len(buf) == 4 + msg_len, 'msg_len=%d, len(buf)=%d'%(msg_len, len(buf))
en_msg = buf[4:4+msg_len]
print 'ct =', binascii.b2a_hex(en_msg)


c2 = socket.create_connection(('', 21000))

msg2 = struct.pack('!cL', 'd', len(en_msg)) + en_msg
c2.sendall(msg2)

time.sleep(1.0)
buf2 = c2.recv(4096)
msg_len = struct.unpack_from('!L', buf2, 0)[0]
assert len(buf2) == 4 + msg_len, 'msg_len=%d, len(buf)=%d'%(msg_len, len(buf2))
pt2 = buf2[4:]
print 'pt2 =', binascii.b2a_hex(pt2)

assert pt1 == pt2
"""
