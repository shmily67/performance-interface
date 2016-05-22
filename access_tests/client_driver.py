import multiprocessing
import socket
import threading
import select
import struct
from nose.tools import *
from another_openssl_aes import
from UserTas1_pb2 import LoginReq, LoginRsp  # , LogoutReq, LogoutRsp


class Client(object):
    def __init__(self, client_id, server_ip, server_port):
        self.conn = socket.create_connection((server_ip, server_port))
        self.send_sn = 0
        self.client_id = client_id
        self.__continue__ = True        
        self.recv_thr = threading.Thread(target=self.recv_func, args=tuple())
        self.recv_thr.start()

    def close(self):
        self.__continue__ = False
        self.recv_thr.join()
        self.conn.close()
        
    def send(self, funcode, data):
        protobuf_msg = data.SerializeToString()
        crypted_msg = self.cipher.encrypt(protobuf_msg)
        head = struct.pack('<BLLLBBl', 0xff, 19+len(crypted_msg)+5, funcode, 0, 0, 0, self.send_sn)
        crc = zlib.crc32(head, 58861227)
        msg =  head + crypted_msg + struct.pack('<l', crc) + '\x00'
        #util.hexprint(msg)
        self.sock.sendall(msg)
        self.send_sn += 1

    def recv_func(self):

        buf = ''
        while self.__continue__:
            rlist, wlist, xlist = select.select([self.conn], [], [], 0.01)
            if [] == rlist:
                continue
            s = self.conn.recv(4096)
            if '' == s:
                print 'Client(%s).recv_func(): connection closed by remote, exit.'
                break
            buf += s
            buf_len = len(buf)
            if buf_len < 5:
                continue
            msg_len = struct.unpack_from('!L', buf, 1)[0]
            if buf_len < msg_len:
                continue
            msg = buf[:msg_len]
            buf = buf[msg_len:]
            data = decode(msg)
            print 'Client(%s).recv_func(): msg received'
            print 'header =', header
            print 'data =', data
        print 'Client(%s).recv_func(): end'

def encode(funcode, sn, data):
    #tag, msg_len, funcode, sessionid, mode, version, sn = struct.unpack_from('<BLLLBBl', msg, 0)
    body = data.ToString()
    encrypted_body = body
    header = struct.pack('<BLLLBBl', tag, msg_len, funcode, sessionid, mode, version, sn)

def decode(msg):
    tag, msg_len, funcode, sessionid, mode, version, sn = struct.unpack_from('<BLLLBBl', msg, 0)
    #print 'decode(): tag, msg_len, funcode, sessionid, mode, version, sn ='
    #print tag, msg_len, funcode, sessionid, mode, version, sn
    eq_(255, tag)
    eq_(0, mode) # 0 = protobyf
    eq_(len(msg), msg_len)
    eq_('\x00', msg[-1])

    crc = zlib.crc32(msg[:19], 58861227)
    eq_(msg[-5:-1], struct.pack('<l', crc))

    if 24 < msg_len:
        protobuf_msg = crypt_msg(msg[19:-5], 'd')
        data = protobuf_dict.data_class_dict[funcode]()
        data.ParseFromString(protobuf_msg)
        return type(data), (tag, msg_len, funcode, sessionid, mode, version, sn), data
    elif 24 == msg_len:
        return None, (tag, msg_len, funcode, sessionid, mode, version, sn), None
    else:
        assert False, 'msg_len < 24: ' + binascii.b2a_hex(msg)

login_data_set = (
    ('user_1', '123456', ()),  # account_type, login_code, password
    (),
)

def login(account_type, login_code, password):

def main():
    pass


if __name__ == '__main__':
    main()
