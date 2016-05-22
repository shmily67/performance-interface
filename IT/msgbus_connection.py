import time, struct, Queue, logging, binascii, threading, time
import pika, google.protobuf
from nose.tools import *
import protobuf_dict, util

#LOGGER = logging.getLogger(__name__)

class Connection(object):
    _list_ = []
    @classmethod
    def close_all(cls):
        for obj in Connection._list_:
            if obj.connection.is_open:
                obj.close()

    def __init__(self, name, serv_ip, serv_port, virtual_host, username, password):
        self.name, self.q = name, Queue.Queue()
        credentials = pika.connection.Parameters()._credentials(username, password)
        conn_params = pika.connection.ConnectionParameters(serv_ip, serv_port, virtual_host,\
            credentials)#, heartbeat_interval=2)
        #LOGGER.debug('conn_params = %s'%str(conn_params))
        time.sleep(0.1)
        self.connection = pika.BlockingConnection(conn_params)
        self.channels = {} # channel_number -> channel_obj
        Connection._list_.append(self)
        self.no_ack_dict = {} # chan -> no_ack
        self.que_dict = {}
        
    def close(self):
        #for ch in self.channels:
        #    ch.close()
        self.connection.close()
        #LOGGER.debug(self.name + ' closed')

    def channel(self):
        ch = self.connection.channel()
        self.channels[ch.channel_number] = ch
        self.que_dict[ch] = Queue.Queue()
        return ch

    def get_channel(self, chan_num):
        return self.channels[chan_num]
        
    def basic_consume(self, chan, queue, tag=None):
        """           consumer_callback,
                      queue,
                      no_ack=False,
                      exclusive=False,
                      consumer_tag=None,
                      arguments=None):"""
        _tag = chan.basic_consume(self.callback, queue, consumer_tag=tag)
        #print 'basic_consume() consumer_tag = ', _tag
        return _tag

    def recv(self, chan, timeout):
        t0 = time.time()
        self.connection.process_data_events()
        q = self.que_dict[chan]
        return q.get(True, timeout)

    def expect(self, chan, exp_session_id, exp_protobuf_data, timeout):
        method, properties, funcode, session_id, protobuf_data = self.recv(chan, timeout)
        eq_('Deliver', type(method).__name__)
        eq_(protobuf_dict.data_class_dict[funcode], type(exp_protobuf_data))
        eq_(exp_session_id, session_id)
        exp_protobuf_data.__eq__(protobuf_data)
    
    def callback(self, ch, method, properties, body):                
        #print self.name+'.callback()'
        #print 'callback() ch = ', ch
        #print 'callback() method = ', method        
        ch.basic_ack(method.delivery_tag)
        funcode, session_id, protobuf_data = decode(body)
        q = self.que_dict[ch]        
        q.put((method, properties, funcode, session_id, protobuf_data))
        
def encode(funcode, session_id, protobuf_data):
    return struct.pack('<ll', funcode, session_id) + protobuf_data.SerializeToString()
    
def decode(msg):
    if 'heartbeat' == msg:
        return None, None, None
    assert_greater_equal(len(msg), 8, binascii.b2a_hex(msg))
    funcode, session_id = struct.unpack_from('<ll', msg, 0)
    if funcode in protobuf_dict.data_class_dict:
        protobuf_data = protobuf_dict.data_class_dict[funcode]()
        protobuf_data.ParseFromString(msg[8:])
        return funcode, session_id, protobuf_data
    else:
        return funcode, None, None

class FuncodeError(Exception): pass