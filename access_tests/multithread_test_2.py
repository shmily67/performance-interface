import socket
import zlib
import pickle
import struct
import time
import sys
import threading
import itertools
import Queue
from select import select
from nose.tools import *
from UserTas1_pb2 import LoginRsp
import crypt

target_host, target_port = '192.168.31.160', 7878


def setup():
    global test_data_dict
    with open('test_data.bin', 'rb') as f:
        test_data_dict = pickle.load(f)


def parallee_tests():
    queue, thr_list = Queue.Queue(), []
    thr_num = int(sys.argv[1])
    print 'Begin to start threads'
    for test_code in range(thr_num):
        thr = threading.Thread(target=client_thread_func, args=(target_host, target_port, test_code, queue))
        thr.start()
        thr_list.append(thr)
        # time.sleep(0.01)

    print 'Waiting for end of all threads'
    for thr in thr_list:
        thr.join()

    print 'All threads terminated, read the queue'
    pass_num, timeout_num, error_num, sum_dt = 0, 0, 0, 0.0
    while True:
        try:
            ret, dt = queue.get(True, 0.5)
            print 'result:', ret, '  ', dt
        except Queue.Empty:
            break
        #sys.stdout.write('.')
        #sys.stdout.flush()
        if 0 == ret:
            pass_num += 1
            sum_dt += dt
        elif 1 == ret:
            timeout_num += 1
        elif 2 == ret:
            error_num += 1
        else:
            assert False, ret
    if pass_num:
        avg_dt = sum_dt/pass_num
    else:
        avg_dt = 0.0
    print 'thr_num=%d, pass_num=%d, timeout_num=%d, error_num=%d, arv_dt=%f' %\
          (thr_num, pass_num, timeout_num, error_num, avg_dt)


def client_thread_func(host, port, test_code, queue):
    conn = socket.create_connection((host, port))
    conn.settimeout(60.0)
    print 'connected'
    try:
            _, exp_rsp, req_msg, _ = test_data_dict[test_code]
            conn.sendall(req_msg)
            t0 = time.time()
            print 'msg sent'
            rsp_msg = conn.recv(4096)
            assert_greater(len(rsp_msg), 24)
            dt = time.time() - t0
            print 'msg recved'
            eq_('\xff', rsp_msg[0])
            msg_len, funcode, session_id, mode, version, sn = struct.unpack_from('<LLLBBl', rsp_msg, 1)
            # print 'msg_len=%d, funcode=%d, session_id=%d, mode=%d, version=%d, sn=%d' %\
            #    (msg_len, funcode, session_id, mode, version, sn)
            rsp = LoginRsp()
            body = crypt.crypt_msg(rsp_msg[19:-5], 'd')
            rsp.ParseFromString(body)
            eq_(0, rsp.RetCode)
            eq_('sucess', rsp.RetDesc)
            eq_(exp_rsp.AccountType, rsp.AccountType)
            eq_(exp_rsp.Token, rsp.Token)
            queue.put((0, dt))  # pass
    except socket.timeout:
        queue.put((1, 0.0))  # timeout
    except Exception as e:
        print e
        queue.put((2, 0.0))  # error
    finally:
        conn.close()


if __name__ == '__main__':
    setup()
    parallee_tests()