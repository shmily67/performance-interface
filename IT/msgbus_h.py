import time, struct, binascii, threading, time, sys
import haigha.connection, haigha.message
from nose.tools import *
import protobuf, util
#import logging
#logger = logging.getLogger(__name__)

_connection_list_ = []
def close_all():
    for conn in _connection_list_:
        conn.close()

class Connection(object):
    def __init__(self, host, port, vhost, username, password, funcode_dict):
        self.codec = protobuf.Codec(funcode_dict)
        self.connection = haigha.connection.Connection(user=username, password=password, vhost=vhost, host=host, port=port)
        _connection_list_.append(self.connection)
        self.ch = self.connection.channel()
        #self.ch.confirm_delivery()
        self.queue_set = set()

    def close(self):
        self.connection.close()

    def bind_queue(self, exchange, queue, routing_key, durable=False):
        assert_not_in(queue, self.queue_set)
        self.ch.exchange.declare(exchange, 'direct')
        self.ch.queue.declare(queue, durable=durable, auto_delete=False)
        self.ch.queue.bind(queue, exchange, routing_key)
        self.queue_set.add(queue)

    def clear_all_queues_after_tests(self, period, wait_interval=None):
        if 'before_testing' == period:
            for q in self.queue_set:
                self.clear_queue_before_tests(q)
        elif 'after_testing' == period:
            assert_greater(wait_interval, 0.0)
            for q in self.queue_set:
                self.clear_queue_after_tests(q, wait_interval)
        else:
            assert False, period

    def clear_queue_before_tests(self, queue):
        assert_in(queue, self.queue_set)
        msg = self.ch.basic.get(queue)
        while msg:
            msg = self.ch.basic.get(queue)

    def clear_queue_after_tests(self, queue, wait_interval):
        assert_in(queue, self.queue_set)
        t0, i = time.time(), 0
        timeout_time = time.time() + wait_interval
        while time.time() < timeout_time:
            if self.ch.basic.get(queue):
                timeout_time = time.time() + wait_interval
                i += 1
                #print 'clear_queue_after_tests() got'
            else:
                time.sleep(0.5)
                #print 'clear_queue_after_tests() sleep %f'%(time.time()-t0)
        print 'clear_queue_after_tests(): %d msg got'%i

    def publish(self, exchange, routing_key, funcode, session_id, protobuf_data):
        app_msg = self.codec.encode(funcode, session_id, protobuf_data)
        msg = haigha.message.Message(app_msg)
        self.ch.basic.publish(msg, exchange, routing_key)
        t = time.time()
        print '%f msgbus_h.Connect.publish()'%t
        print 'funcode=%d, session_id=%d, protobuf_data(%s)='%(funcode, session_id, type(protobuf_data))
        print protobuf_data
        
    def get(self, queue, timeout):
        assert_in(queue, self.queue_set)
        endtime = time.time() + timeout
        while time.time() < endtime:
            msg = self.ch.basic.get(queue)
            t = time.time()
            if msg:
                print '%f msgbus_h.Connect.get()'%t
                s = ''.join(map(lambda b: chr(b), msg.body)) #bytearray -> str
                if 'heartbeat' == s:
                    return -1, -1, 'heartbeat'
                else:
                    funcode, session_id, protobuf_data = self.codec.decode(s)
                    print 'funcode=%d session_id=%d'%(funcode, session_id)
                    print 'protobuf_data(%s)='%type(protobuf_data)
                    print protobuf_data
                    return funcode, session_id, protobuf_data
            else:
                time.sleep(0.01)
        raise Timeout('Connection.get() timeout(%f)'%timeout)

    def expect(self, queue, exp_funcode, exp_session_id, timeout=1.0):
        assert_in(queue, self.queue_set)
        print 'msgbus_h.Connect.expect()'
        funcode, session_id, protobuf_data = self.get(queue, timeout)
        eq_(exp_funcode, funcode)
        eq_(exp_session_id, session_id)
        return protobuf_data

    def expect2(self, queue, exp_funcode, exp_session_id, exp_protobuf_data, timeout=1.0):
        assert_in(queue, self.queue_set)
        funcode, session_id, protobuf_data = self.get(queue, timeout)
        print 'expect2() protobuf_data(%s)='%type(protobuf_data)
        print protobuf_data
        eq_(exp_funcode, funcode)
        assert_is_instance(protobuf_data, type(exp_protobuf_data))
        if exp_session_id:
            eq_(exp_session_id, session_id)
        protobuf.assert_equal(exp_protobuf_data, protobuf_data)
        return protobuf_data
        
    def publish_t(self, exchange, routing_key, funcode, session_id, protobuf_data):
        app_msg = self.codec.encode(funcode, session_id, protobuf_data)
        msg = haigha.message.Message(app_msg)
        self.ch.basic.publish(msg, exchange, routing_key)
        t = time.time()
        #print '%f msgbus_h.Connect.publish()'%t
        #print 'funcode=%d, session_id=%d, protobuf_data(%s)='%(funcode, session_id, type(protobuf_data))
        #print protobuf_data
        return t

    def expect_t(self, queue, exp_funcode, exp_session_id, timeout=1.0):
        assert_in(queue, self.queue_set)
        endtime = time.time() + timeout
        while time.time() < endtime:
            msg = self.ch.basic.get(queue)
            t = time.time()
            if msg:
                s = ''.join(map(lambda b: chr(b), msg.body)) #bytearray -> str
                if 'heartbeat' == s:
                    return -1, -1, 'heartbeat'
                else:
                    funcode, session_id, protobuf_data = self.codec.decode(s)
                    #print '%f msgbus_h.Connect.get()'%t
                    #print 'funcode=%d session_id=%d'%(funcode, session_id)
                    #print 'protobuf_data(%s)='%type(protobuf_data)
                    #print protobuf_data
        raise Timeout('Connection.get() timeout(%f)'%timeout)
        
        eq_(exp_funcode, funcode)
        eq_(exp_session_id, session_id)
        return protobuf_data, t
        
class Timeout(Exception):pass
