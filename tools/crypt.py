import socket
import struct
from nose.tools import *


def crypt_msg(msg_in,mode):
    sock = socket.create_connection(('192.168.31.21',21000))
    try:
        sock.settimeout(10.0)
        assert_in(mode, ('e', 'd')) # encrypt, decrypt
        msg = struct.pack('!cL', mode, len(msg_in)) + msg_in

        sock.sendall(msg)
        #print 'crypt_msg() msg sent:'
        #util.hexprint(msg_in)

        recv_buf = sock.recv(65536)
        while len(recv_buf) < 4:
            recv_buf += sock.recv(65536)
        msg_len = struct.unpack_from('!L', recv_buf, 0)[0]
        #print 'crypt_msg() head received, len = %d'%msg_len
        while len(recv_buf) < 4 + msg_len:
            recv_buf += sock.recv(65536)
        #print 'crypt_msg() msg received'
        #util.hexprint(msg_in)
        eq_(len(recv_buf), 4+msg_len)

        sock.close()
        return recv_buf[4:]
    except Exception, e:
        sock.close()
        raise e
