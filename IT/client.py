# -*- coding: utf8 -*-
import struct, socket, threading, Queue, time, zlib, select, binascii
from hashlib import md5
from Crypto.Cipher import AES
from nose.tools import *
import protobuf, util

AES_KEY = '0123456789012345'
cipher = AES.new(AES_KEY, AES.MODE_ECB)
#CRC_KEY = 58861227
#crypt_server_addr = ("127.0.0.1", 21000)

class Client(object):
    def __init__(self, ip, port, funcode_dict):
        self.data_class_dict = {}
        for funcode in funcode_dict:
            self.data_class_dict[funcode_dict[funcode]] = funcode
        self.crypt_addr = crypt_server_addr
        self.send_sn = 0
        self.sock = socket.create_connection((ip, port))
        self.recv_queue = Queue.Queue()
        self.__continue__ = True
        self.thr = threading.Thread(target=self.recv_thread_func)
        self.thr.start()

    def close(self):
        self.__continue__ = False
        self.thr.join()
        self.sock.close()

    def send(self, data):
        protobuf_msg = data.SerializeToString()
        #crypted_msg = crypt_msg(protobuf_msg, 'e') # e: encrypt    
        crypted_msg = cipher.encrypt(protobuf_msg)
        funcode = self.data_class_dict[type(data)]
        head = struct.pack('<BLLLBBl', 0xff, 19+len(crypted_msg)+5, funcode, 0, 0, 0, self.send_sn)
        crc = zlib.crc32(head, 58861227)
        msg =  head + crypted_msg + struct.pack('<l', crc) + '\x00'
        util.hexprint(msg)
        self.sock.sendall(msg)
        self.send_sn += 1

    def recv(self, timeout):
        return self.recv_queue.get(True, timeout)

    def expect(self, exp_funcode, timeout):
        funcode, data = self.recv_queue.get(True, timeout)
        eq_(exp_funcode, funcode)
        else:
            assert not data.HasField('RetCode')
        return data

    def expect2(self, exp_data, timeout):
        funcode, data = self.recv_queue.get(True, timeout)
        assert_is_instance(data, type(exp_data))
        protobuf.assert_equal(exp_data, data)

    def recv_thread_func(self):
        recv_buf = ''
        while self.__continue__:
            rlist, wlist, xlist = select.select([self.sock], [], [], 0.05)
            if [] == rlist: continue
            recv_buf += self.sock.recv(65535)
            if len(recv_buf) < 19: continue
            tag, msg_len, funcode, sessionid, mode, version, sn = struct.unpack_from('<BLLLBBl', recv_buf, 0)
            print 'recv_thread_func(): tag, msg_len, funcode, sessionid, mode, version, sn ='
            print tag, msg_len, funcode, sessionid, mode, version, sn
            eq_(255, tag)
            eq_(0, mode)
            assert_greater_equal(len(recv_buf), 24)
            if len(recv_buf) < msg_len: continue
            cry_protobuf_msg = recv_buf[19:-5]
            crc_bytes = recv_buf[-5:-1]
            eq_('\x00', recv_buf[-1])
            recv_buf = recv_buf[msg_len:]
            #protobuf_msg = crypt_msg(cry_protobuf_msg, 'd')
            protobuf_msg = aes.decrypt(cry_protobuf_msg)
            data = protobuf_dict.class_dict[funcode]()
            data.ParseFromString(protobuf_msg)
            self.recv_queue.put((funcode, data))

    def login(self, username, password):
        assert False

    def logout(self):
        assert False


def decode(msg):
    #print 'decode() msg='
    #util.hexprint(msg)
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

def _crypt_msg(msg_in, mode):
    '''
        将加密的消息发送给加密、解密服务器，获取到解密消息
    '''
    sock = socket.create_connection(crypt_server_addr)
    try:
        sock.settimeout(5.0)
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

def md5_str(password):
    buf = md5.new(password).digest()
    #util.hexprint(buf)
    return binascii.b2a_hex(buf).upper()

def EVP_ByteToKey(password, salt, key_len, iv_len):
    #Derive the key and the IV from the given password and salt.
    dtot =  md5(password + salt).digest()
    d = [ dtot ]
    while len(dtot)<(iv_len+key_len):
        d.append( md5(d[-1] + password + salt).digest() )
        dtot += d[-1]
    return dtot[:key_len], dtot[key_len:key_len+iv_len]
