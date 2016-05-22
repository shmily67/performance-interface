import time, struct, Queue, pika, google.protobuf
from nose.tools import *
import protobuf_dict

class Client(object): # 1 client, i connection
    obj_list = []
    def __init__(self, name, serv_ip, serv_port, virtual_host, username, password):
        self.name, self.q = name, Queue.Queue()
        credentials = pika.connection.Parameters()._credentials(username, password)
        conn_params = pika.connection.ConnectionParameters(serv_ip, serv_port, virtual_host, credentials)
        print 'conn_params = ', conn_params
        time.sleep(0.1)
        self.connection = pika.BlockingConnection(conn_params)
        self.channels = {} # channel_number -> channel_obj
        Client.obj_list.append(self)
        
    def close(self):
        #for ch in self.channels:
        #    ch.close()
        self.connection.close()
        print self.name + ' closed'
    
    @classmethod
    def close_all(cls):
        for obj in Client.obj_list:
            obj.close()        

    def channel(self):
        ch = self.connection.channel()
        self.channels[ch.channel_number] = ch
        return ch

    def recv(self, timeout):        
        return self.q.get(True, timeout)

    def expect(self, exp_channel, exp_method, exp_session_id, exp_protobuf_data):
        ch, method, properties, session_id, protobuf_data = self.q.get(True, timeout)
        eq_(exp_channel, ch)
        eq_(exp_method, method)
        eq_(exp_session_id, session_id)
        exp_protobuf_data.__eq__(protobuf_data)

    def callback(self, ch, method, properties, body):
        session_id, protobuf_data = decode(body)
        self.q.put((ch, method, properties, session_id, protobuf_data))

def encode(session_id, protobuf_data):
    funcode = protobuf_dict.get_funcode(protobuf_data)
    return struct.pack('<ll', funcode, session_id) + protobuf_data.SerializeToString()

    
def decode(msg):
    assert_greater_equal(len(msg), 8)
    funcode, session_id = struct.unpack_from('<ll', msg, 0)
    if funcode not in protobuf_dict.data_class_dict:
        raise FuncodeError(funcode)
    protobuf_data = protobuf_dict.data_class_dict[funcode]()
    protobuf_data.ParseFromString(msg[8:])
    return session_id, protobuf_data

class FuncodeError(Exception): pass    