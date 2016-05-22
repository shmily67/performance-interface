#coding = utf8
import struct, binascii, traceback, sys, threading, Queue, time, importlib, subprocess, logging
import dpkt.pcap, dpkt.ethernet, pika.frame, pika.spec, google.protobuf.message
from nose.tools import *
import BusproxyTas1_pb2, CashTas1_pb2, common_pb2, Delivery2Tas1_pb2, DeliveryTas1_pb2
import ExterQkernelTas1_pb2, ExterReportTas1_pb2, Finance1_pb2, IssueTas1_pb2, LogTas1_pb2
import ManagerTas1_pb2, ManagerTas2_pb2, ManagerTas3_pb2, MoneyManagerTas1_pb2, NewsFeedTas1_pb2
import PublicTas1_pb2, QkernelTas1_pb2, QkernelTas2_pb2, QkernelTas3_pb2, QuoteTas1_pb2
import RealtimeMonitorTas1_pb2, ReportTas1_pb2, ReportTas2_pb2, RiskTas1_pb2, SettleTas1_pb2
import TkernelTas1_pb2, UserTas1_pb2
import msgbus, protobuf_dict, protobuf_util, parse_pcap, util

LOGGER = logging.getLogger(__name__)

def gen(_serv_ip, serv_port, pcap_path, pcap_type, connection_service_dict_path, output_path,\
    ignored_addr_list=None):
    reload(sys)
    sys.setdefaultencoding('utf8')
    tup_list = parse_pcap.parse_pcap(pcap_path, pcap_type, _serv_ip, serv_port) 
    print 'parse_pcap() complete'    
    
    pb2_set, connection_set, actions = parse_tcp_data(tup_list)
    print 'parse_tcp_data() complete pb2_set = ', pb2_set
    write_test(_serv_ip, serv_port, pb2_set, connection_set, actions, output_path, connection_service_dict_path)

def parse_tcp_data(tup_list):
    pb2_set, connection_set, actions = set(), set(), []
    connection_buf_dict = {} # (conn_ip, conn_port) -> buf
    for direction, conn_ip, conn_port, tcp_data in tup_list:
        #print 'new_tcp_data'
        if (conn_ip, conn_port) not in connection_set:
            connection_set.add((conn_ip, conn_port))                   
        if (conn_ip, conn_port) not in connection_buf_dict:
            connection_buf_dict[(conn_ip, conn_port)] = ''
        buf = connection_buf_dict[(conn_ip, conn_port)]
        buf += tcp_data
        while True:
            if len(buf) < 8: break
            if 'AMQP' == buf[:4]: #ProtocolHeader
                msg_len = 8
                connection_set.remove((conn_ip, conn_port))
            else: 
                msg_len = 8 + struct.unpack_from('>L', buf, 3)[0]
            if len(buf) < msg_len: break
            x, pika_data = pika.frame.decode_frame(buf[:msg_len])
            buf = buf[msg_len:]
            if isinstance(pika_data, pika.frame.Body):
                funcode, session_id, protobuf_data = msgbus.decode(pika_data.fragment)
                if protobuf_data:
                    pb2_set.add(protobuf_data.__module__)
            else: # ProtocolHeader, METHOD, HEADER, HEARTBEAT
                funcode, session_id, protobuf_data = None, None, None
            #print direction, conn_ip, conn_port
            actions.append((direction, conn_ip, conn_port, pika_data,\
                funcode, session_id, protobuf_data))
        connection_buf_dict[(conn_ip, conn_port)] = buf
    return pb2_set, connection_set, actions

def write_test(_serv_ip, serv_port, pb2_set, connection_set, actions, output_path, connection_service_dict_path):
    connection_service_dict = {}
    with open(connection_service_dict_path, 'r') as f:
        for line in f: # 192.168.31.160#46441: settlement_0
            ip_str, port_str, name = line.strip().split()
            ip, port = util.iphex(ip_str), int(port_str)
            assert_not_in((ip, port), connection_service_dict)
            connection_service_dict[(ip, port)] = name.strip()
            #print ip, port, name
    with open(output_path, 'w') as output:        
        write_header(output, pb2_set)        
        connection_dict = {}
        connection_name_dict = {}
        i = 0
        for action in actions:
            print 'write_test() %d'%i
            i += 1
            #print action
            direction, conn_ip, conn_port, pika_data, funcode, session_id, protobuf_data = action
            if (conn_ip, conn_port) in connection_dict:
                writer = connection_dict[(conn_ip, conn_port)]
            else:
                if (conn_ip, conn_port) in connection_service_dict:
                    service_name = connection_service_dict[(conn_ip, conn_port)]
                    if service_name not in connection_name_dict:
                        connection_name = service_name + '_conn0'
                        connection_name_dict[service_name] = [connection_name]
                    else:
                        i = len(connection_name_dict[service_name])
                        connection_name = service_name + '_conn%d'%i
                        connection_name_dict[service_name].append(connection_name)
                    writer = ConnectionWriter(connection_name, _serv_ip, serv_port,\
                        conn_ip, conn_port, output)
                    connection_dict[(conn_ip, conn_port)] = writer
                else:
                    assert False, (conn_ip, conn_port)
                
            if 'to_server' == direction:
                writer.write_send(pika_data, funcode, session_id, protobuf_data)
            else:
                writer.write_recv(pika_data, funcode, session_id, protobuf_data)
        
def write_header(output, pb2_set):
    print 'write_header() pb2_set = ', pb2_set
    import_text = """#coding=utf8
import pika
from nose.tools import *
import msgbus"""    
    if len(pb2_set) > 0:
        import_text += '\nimport ' + ', '.join(pb2_set)
    output.write(import_text)
    
    setup_text = """

def setup():
    msgbus.set_pika_logger_level('WARNING')
    #msgbus.LOGGER.setLevel('DEBUG')

def teardown():
    msgbus.close_all()

def test_xxx():"""
    output.write(setup_text)

class ConnectionWriter(object):
    def __init__(self, name, _serv_ip, serv_port, conn_ip, conn_port, output):        
        self.name, self._serv_ip, self.serv_port, self.output = name, _serv_ip, serv_port, output
        self.publish_data = {}
        self.deliver_dict = {}
        self.cred = {}
        self.type_set = set((
            pika.spec.Connection.Start,
            pika.spec.Connection.Tune,
            pika.spec.Connection.OpenOk,
            pika.spec.Channel.OpenOk,
            pika.spec.Confirm.SelectOk,
            pika.spec.Exchange.DeclareOk,
            pika.spec.Queue.DeclareOk,
            pika.spec.Queue.BindOk,
            pika.spec.Basic.QosOk,
            pika.spec.Basic.ConsumeOk,
            pika.spec.Basic.Ack,))
            
    def write_send(self, pika_data, funcode, session_id, protobuf_data):
        s = ''
        if isinstance(pika_data, pika.frame.ProtocolHeader):
            self.protocol_header = pika_data
        elif isinstance(pika_data, pika.frame.Method):
            channel_number, method = pika_data.channel_number, pika_data.method
            channel_name = '%s_chan%d'%(self.name, channel_number)
            if isinstance(method, pika.spec.Connection.StartOk):
                self.start_ok = method                
            elif isinstance(method, pika.spec.Connection.TuneOk):        
                self.tune_ok = method
            elif isinstance(method, pika.spec.Connection.Open):
                self.open = method
                x, username, password = self.start_ok.response.split('\x00')
                vhost = method.virtual_host
                s = "\n    global %s"%self.name
                s += "\n    %s = msgbus.Connection("%self.name
                s += "'%s', '%s', %d, '%s', '%s', '%s')"%(self.name, self._serv_ip, self.serv_port,\
                    vhost, username, password)
            elif isinstance(method, pika.spec.Channel.Open):
                s = "\n    %s = %s.channel()"%(channel_name, self.name)
            elif isinstance(method, pika.spec.Confirm.Select):
                s = "\n    %s.confirm_delivery()"%channel_name
            elif isinstance(method, pika.spec.Exchange.Declare):
                s = "\n    %s.exchange_declare("%channel_name
                s += "exchange='%s', exchange_type='%s', "%(method.exchange, method.type)
                s += "passive=%r, durable=%r, auto_delete=%r, "%(method.passive, method.durable, method.auto_delete)
                s += "internal=%r, arguments=%s)"%(method.internal, str(method.arguments))
            elif isinstance(method, pika.spec.Queue.Declare):
                #queue='', passive=False, durable=False,
                #exclusive=False, auto_delete=False, arguments=None
                s = "\n    %s.queue_declare("%channel_name
                s += "queue='%s', passive=%r, durable=%r, "%(method.queue, method.passive, method.durable)
                s += "exclusive=%r, auto_delete=%r, arguments=%s)"%(method.exclusive, method.auto_delete, str(method.arguments))
            elif isinstance(method, pika.spec.Queue.Bind):
                #queue, exchange, routing_key=None, arguments=None
                s = "\n    %s.queue_bind("%channel_name
                s += "queue='%s', exchange='%s', "%(method.queue, method.exchange)
                s += "routing_key='%s', arguments=%s)"%(method.routing_key, str(method.arguments))
            elif isinstance(method, pika.spec.Basic.Qos):
                s = "\n    %s.basic_qos("%channel_name
                s += "prefetch_size=%d, prefetch_count=%d, all_channels=%r)"%\
                    (method.prefetch_size, method.prefetch_count, method.global_)
            elif isinstance(method, pika.spec.Basic.Consume):
                #consumer_callback, queue, no_ack=False, exclusive=False, consumer_tag=None, arguments=None
                s = "\n    %s.basic_consume(%s, '%s', "%(self.name, channel_name, method.queue)
                s += "consumer_tag=%r)"%method.consumer_tag
            elif isinstance(method, pika.spec.Basic.Publish):
                #print 'Publish  ticket = '
                #util.hexprint(method.ticket)
                self.publish_data[pika_data.channel_number] = [method]
            elif isinstance(method, pika.spec.Basic.Ack):
                s = "\n    %s.basic_ack(%d, %r)"%(self.name, method.delivery_tag, method.multiple)
                #delivery_tag=0, multiple=False
            else:
                assert False, 'Invalid method type: %s'%type(method).__name__
        elif isinstance(pika_data, pika.frame.Header):
            self.publish_data[pika_data.channel_number].append(pika_data)
        elif isinstance(pika_data, pika.frame.Body):
            #if len(self.publish_data[pika_data.channel_number]) < 2:
            #    assert False, self.publish_data[pika_data.channel_number]
            method = self.publish_data[pika_data.channel_number][0]
            channel_name = '%s_chan%d'%(self.name, pika_data.channel_number)
            if 'heartbeat' == pika_data.fragment:
                pass
                #s = "\n    %s.basic_publish("%channel_name
                #s += "'%s', '%s', 'heartbeat')"%(method.exchange, method.routing_key)
            else: #protobuf
                if funcode in protobuf_dict.data_class_dict:
                    pb2 = importlib.import_module(protobuf_data.__module__)
                    #s = '\n    protobuf_data = ' + pb2.__name__ + '.' + type(protobuf_data).__name__ + '()'
                    #print 'msgbus_gen(): protobuf_data(%r)='%type(protobuf_data)
                    #print protobuf_data
                    s = '\n' + protobuf_util.gen_protobuf_data(protobuf_data, 'protobuf_data', 4)
                    #s += "\n    app_msg = msgbus.encode(%d, %d, protobuf_data)"%(funcode, session_id)
                    #s += "\n    %s.basic_publish("%channel_name
                    s += "\n    %s.publish('%s', '%s', "%(self.name, method.exchange, method.routing_key)
                    s += "%d, %d, protobuf_data, "%(funcode, session_id)
                    if method.mandatory:
                        s += ", mandatory=True"
                    if method.immediate:
                        s += ", immediate=True"
                    s += ')'
                else:
                    s += '\n\n    FuncodeError(%d)'%funcode
        else:
            assert False, pika_data
        if '' != s:
            self.output.write(s)
            
    def write_recv(self, pika_data, funcode, session_id, protobuf_data):
        s = ''
        if isinstance(pika_data, pika.frame.Method):
            if isinstance(pika_data.method, pika.spec.Basic.Deliver):
                assert pika_data.channel_number not in self.deliver_dict
                self.deliver_dict[pika_data.channel_number] = [pika_data.method]
            elif type(pika_data.method) in self.type_set:
                pass
            else:
                assert False, pika_data
        elif isinstance(pika_data, pika.frame.Header):
            self.deliver_dict[pika_data.channel_number].append(protobuf_data)                
        elif isinstance(pika_data, pika.frame.Body):
            deliver, head = self.deliver_dict[pika_data.channel_number]
            if funcode in protobuf_dict.data_class_dict:
                pb2 = importlib.import_module(protobuf_data.__module__)
                s = protobuf_util.gen_protobuf_data(protobuf_data, 'exp_data', 4)
                #def expect(self, chan, exp_session_id, exp_protobuf_data, timeout):
                s += "\n    chan = %s.get_channel(%d)"%(self.name, pika_data.channel_number)
                s += "\n    %s.expect(chan, %d, exp_data, 1.0)"%(self.name, session_id)
            else:
                s += '\n    FuncodeError(%d)'%funcode
            del self.deliver_dict[pika_data.channel_number]
        else:
            assert False, pika_data            
        if '' != s:
            self.output.write('\n'+s)
                
def iphex(ip_str): # "127.0.0.1" -> "\xff\x00\x00\x01"
    d=map(lambda s:int(s), ip_str.split('.'))
    return struct.pack('!BBBB', *d)

def ipstr(buf):
    eq_(4, len(buf))    
    return '.'.join(map(lambda c:str(ord(c)), buf))

