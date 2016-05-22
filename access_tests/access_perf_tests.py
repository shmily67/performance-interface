import time
import socket
import pickle
import struct
import sys
import threading
import Queue
import traceback
from nose.tools import *
from transaction_pressure import TestManager, transaction  #, Proxy

target_host, target_port = '192.168.31.61', 7878


class ClientActor(object):
    def __init__(self, host, port, test_code, req_msg):
        self.addr = (host, port)
        self.req_msg = req_msg
        self.test_code = test_code

    def act(self):
        conn = socket.create_connection(self.addr)
        conn.settimeout(60.0)
        # print 'connected'
        try:
            with transaction('Login'):
                conn.sendall(self.req_msg)
                # print 'msg sent'
                rsp_msg = conn.recv(4096)
                assert_greater(len(rsp_msg), 24)
                # print 'msg recved'
                eq_('\xff', rsp_msg[0])
                msg_len, funcode, session_id, test_code_r, sn = struct.unpack_from('<LLLHl', rsp_msg, 1)
                eq_(self.test_code, test_code_r)
            # print 'msg_len=%d, funcode=%d, session_id=%d, mode=%d, version=%d, sn=%d' %\
            #    (msg_len, funcode, session_id, mode, version, sn)
            """body = crypt.crypt_msg(rsp_msg[19:-5], 'd')
            rsp = LoginRsp()
            rsp.ParseFromString(body)
            eq_(0, rsp.RetCode)
            eq_('sucess', rsp.RetDesc)
            eq_(exp_rsp.AccountType, rsp.AccountType)
            eq_(exp_rsp.Token, rsp.Token)"""
        finally:
            # time.sleep(10.0)
            conn.close()


def parallel_tests():
    with open('test_data.bin', 'rb') as f:
        test_data_dict = pickle.load(f)
    manager = TestManager(False)
    n = int(sys.argv[1])
    for test_code in range(n):
        req_msg = test_data_dict[test_code][2]
        actor = ClientActor('192.168.31.61', 7878, test_code, req_msg)
        manager.add_actor(actor)
    manager.start()


if __name__ == '__main__':
    parallel_tests()
