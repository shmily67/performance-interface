import socket, threading, time, subprocess, sys, zlib, binascii, multiprocessing, Queue, pickle
from select import select
from struct import unpack_from, pack
from nose.tools import *

port = 10777

def start_proxy_mock():
    global test_data_dict
    with open('../test_data.bin', 'rb') as f:
        test_data_dict = pickle.load(f)

    proxy_listen_sock = socket.socket()
    proxy_listen_sock.bind(('', port))
    proxy_listen_sock.listen(1)
    try:
        while True:
            print 'Begin to accept at', port
            conn, addr = proxy_listen_sock.accept()
            try:
                print 'Connection accepted'
                mock_run_r(conn)
            finally:
                conn.close()
    finally:
        proxy_listen_sock.close()


def mock_run_r(conn):  # use recv
    buf = ''
    t0 = time.time()
    while True:
        try:
            s = conn.recv(4096)
        except socket.timeout:
            continue
        rt = time.time()
        if '' == s:
            print 'connection was closed by remote, break'
            break
        # print '%5.3f  bytes received: ' % (time.time()-t0) + binascii.b2a_hex(s)
        buf += s
        while len(buf) >= 24:
            msg_len, funcode, session_id, test_code, sn = unpack_from('<LLLHl', buf, 1)
            if len(buf) < msg_len:
                break
            eq_('\xff', buf[0])
            eq_('\x00', buf[msg_len-1])
            # crc = zlib.crc32(buf[:19], 58861227)
            # eq_(msg[-5:-1], pack('<l', crc))
            #print '\n%5.3f  msg received: ' % (time.time()-t0) + binascii.b2a_hex(buf[:msg_len])
            buf = buf[msg_len:]
            if 131293 == funcode:
                if test_code in test_data_dict:
                    rsp_body = test_data_dict[test_code][3]
                    rsp_msg = pack('<BLLLHl', 0xff, 19+len(rsp_body), 131294, session_id, test_code, sn) + rsp_body
                    conn.sendall(rsp_msg)
                    #print '%5.3f  msg sent, dt=%f, msg=' % (time.time()-t0, time.time()-rt), binascii.b2a_hex(rsp_msg)
                else:
                    print 'Invalid test_code: %d'%test_code
            elif 0 == funcode:
                print '.'
            else:
                assert False, 'Invalid funcode: %d'%funcode


def mock_run_s(conn):  # use select
    buf, t0 = '', time.time()
    while True:
        rlist, wlist, xlist = select([conn], [], [], 0.01)
        if not rlist:
            continue
        rt = time.time()
        s = conn.recv(4096)
        t0 = time.time()
        if '' == s:
            print 'connection was closed by remote, break'
            break
        #print 'bytes received: ' + binascii.b2a_hex(s)
        buf += s
        buf_len = len(buf)
        if buf_len < 24:
            continue
        msg_len, funcode, session_id, test_code, sn = unpack_from('<LLLHl', buf, 1)
        if buf_len < msg_len:
            continue
        eq_('\xff', buf[0])
        eq_('\x00', buf[msg_len-1])
        #crc = zlib.crc32(buf[:19], 58861227)
        #eq_(msg[-5:-1], pack('<l', crc))
        print '\nmsg received: ' + binascii.b2a_hex(buf[:msg_len])
        buf = buf[msg_len:]
        if 131293 == funcode:
            if test_code in test_data_dict:
                rsp_body = test_data_dict[test_code][3]
                rsp_msg = pack('<BLLLHl', 0xff, 19+len(rsp_body), 131294, session_id, test_code, sn) + rsp_body
                conn.sendall(rsp_msg)
                print 'msg sent, dt=%f, msg=' % (time.time()-rt), binascii.b2a_hex(rsp_msg)
            else:
                print 'Invalid test_code: %d'%test_code
        elif 0 == funcode:
            print '.'
        else:
            assert False, 'Invalid funcode: %d'%funcode


if __name__ == '__main__':
    start_proxy_mock()
