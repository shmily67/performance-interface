import struct
import socket
import time
import random
import zlib
import pickle
from nose.tools import *
from UserTas1_pb2 import LoginReq, LoginRsp
import crypt


def setup():
    global test_data_dict, conn
    with open('test_data.bin', 'rb') as f:
        test_data_dict = pickle.load(f)
    conn = socket.create_connection(('192.168.31.160', 7878))
    conn.settimeout(5.0)
    print 'setup(): connected'


def teardown():
    conn.close()


def test_client_login():
    req = LoginReq(
        AccountType=random.randint(1, 10),
        LoginCode=str(10000),
        LoginPWD=str(random.randint(10000, 50000)),
        MemberCode=str(random.randint(10000, 50000)),
        LoginType=random.randint(1, 10),
        ClientType=random.randint(1, 10),
        Version=str(random.randint(10000, 50000)),
        MobilePhone=str(random.randint(10000, 50000)),
        GUID=str(random.randint(10000, 50000)),
        )
    body = crypt.crypt_msg(req.SerializeToString(), 'e')
    print 'msg encrtpted'
    head = struct.pack('<BLLLBBl', 0xff, 19+len(body)+5, 131293, 0, 0, 0, 1)
    crc = zlib.crc32(head, 58861227)
    msg = head + body + struct.pack('<l', crc) + '\x00'

    conn.sendall(msg)
    print 'req sent'
    rsp_msg = conn.recv(4096)
    print 'rsp received'
    assert_greater(len(rsp_msg), 24)
    eq_('\xff', rsp_msg[0])
    msg_len, funcode, session_id, mode, version, sn = struct.unpack_from('<LLLBBl', rsp_msg, 1)
    print 'msg_len=%d, funcode=%d, session_id=%d, mode=%d, version=%d, sn=%d' %\
          (msg_len, funcode, session_id, mode, version, sn)
    rsp = LoginRsp()
    body = crypt.crypt_msg(rsp_msg[19:-5], 'd')
    rsp.ParseFromString(body)
    print 'rsp ='
    print rsp


def test_loop():
    i = 0
    for test_code in test_data_dict:
        if i == 2:
            break
        i += 1
        req, rsp, req_msg, rsp_msg = test_data_dict[test_code]
        yield step_a, req_msg, rsp


def step_a(req_msg, exp_rsp):
    conn.sendall(req_msg)
    print 'req sent'
    rsp_msg = conn.recv(4096)
    print 'rsp received'
    assert_greater(len(rsp_msg), 24)
    eq_('\xff', rsp_msg[0])
    msg_len, funcode, session_id, mode, version, sn = struct.unpack_from('<LLLBBl', rsp_msg, 1)
    print 'msg_len=%d, funcode=%d, session_id=%d, mode=%d, version=%d, sn=%d' %\
          (msg_len, funcode, session_id, mode, version, sn)
    rsp = LoginRsp()
    body = crypt.crypt_msg(rsp_msg[19:-5], 'd')
    rsp.ParseFromString(body)
    print 'rsp ='
    print rsp
    eq_(0, rsp.RetCode)
    eq_('sucess', rsp.RetDesc)
    eq_(exp_rsp.AccountType, rsp.AccountType)
    eq_(exp_rsp.Token, rsp.Token)



