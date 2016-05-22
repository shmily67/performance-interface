#coding = utf8
import struct, binascii, traceback, sys, threading, Queue, importlib
import dpkt.pcap, dpkt.ethernet, google.protobuf
from nose.tools import *
import ManagerTas1_pb2, ManagerTas2_pb2, ManagerTas3_pb2
import MoneyManagerTas1_pb2, NewsFeedTas1_pb2
import BusproxyTas1_pb2, CashTas1_pb2, common_pb2, Delivery2Tas1_pb2, DeliveryTas1_pb2
import ExterQkernelTas1_pb2, ExterReportTas1_pb2, Finance1_pb2, IssueTas1_pb2, LogTas1_pb2
import MoneyManagerTas1_pb2, NewsFeedTas1_pb2
import PublicTas1_pb2, QkernelTas1_pb2, QkernelTas2_pb2, QkernelTas3_pb2, QuoteTas1_pb2
import RealtimeMonitorTas1_pb2, ReportTas1_pb2, ReportTas2_pb2, RiskTas1_pb2, SettleTas1_pb2
import TkernelTas1_pb2, UserTas1_pb2
import protobuf_dict, tas_client_m, parse_pcap, util

#pcap_type: 'windows-wireshark', 'linux-tcpdump'
def gen(_serv_ip, serv_port, pcap_path, pcap_type, connection_service_dict_path, output_path):
    print '\n'*60
    reload(sys)
    sys.setdefaultencoding('utf8')
    tup_list = parse_pcap.parse_pcap(pcap_path, pcap_type, _serv_ip, serv_port) 
    print 'parse_pcap() complete'    
    
    pb2_set, actions = parse_tcp_data(tup_list)
    print 'parse_tcp_data() complete pb2_set = ', pb2_set
    write_test(_serv_ip, serv_port, pb2_set, actions, output_path)
        
class TcpMessageExtractor(object):
    def __init__(self):
        self.buf = ''

    def append(self, tcp_data):
        self.buf += tcp_data
        
    def parse(self):
        if len(self.buf) < 5: return None
        eq_('\xff', self.buf[0])
        msg_len = struct.unpack_from('<L', self.buf, 1)[0]
        if len(self.buf) < msg_len: return None
        msg = self.buf[:msg_len]
        self.buf = self.buf[msg_len:]
        return msg

def act(q, writer, _serv_ip, serv_port):
    print 'Enter act()'
    reload(sys)
    sys.setdefaultencoding('utf8')
    start_statements = '#coding=utf8\nfrom nose.tools import *\nimport tas1_pb2, util'
    start_statements += "\n\nserver_ip, server_port = '%s', %d"%(_serv_ip, serv_port)
    start_statements += "\n\ndef test_xxx():"
    writer.write(start_statements)
    
    client_id_list = []

    while True:
        tup = q.get(True, 5.0)
        if None == tup: break
        direction, client_ip, client_port, app_msg = tup
        if len(app_msg) > 24:
            data_type, header, protobuf_data = tas_client_m.decode(app_msg)
            tag, msg_len, funcode, sessionid, mode, version, sn = header
            assert_not_equal(0, funcode, binascii.b2a_hex(app_msg))
            pb2_name = protobuf_dict.data_class_dict[funcode].__module__
            pb2 = importlib.import_module(pb2_name)
        elif len(app_msg) == 24: # heartbeat
            data_type, header, protobuf_data = None, None, None
        else:
            assert False

        assert_in(direction, ('to_server', 'from_server'))
        if 'to_server' == direction:
            print type(protobuf_data).__name__
            print ''
            if data_type:
                s = test_generator.gen_protobuf_data(protobuf_data, 'data', 4)
                writer.write('\n    #%s'%type(protobuf_data).__name__)
                try:
                    writer.write(s)
                except UnicodeEncodeError as e:
                    print 'type(s) = ', type(s)
                    print 'header = ', header
                    print 'data(%s) = '%msg_name
                    print protobuf_data
                    raise e                    
                writer.write('\n    client.send(data)\n')
            else:
                writer.write('\n    client.send_heartbeat()\n')
        else: # from_server
            if protobuf_data.HasField('RetCode'):
                ret_code = getattr(protobuf_data, 'RetCode')
            else:
                ret_code = None
            writer.write('\n    data = client._expect("%s", %d, 3.0)\n'%\
                (type(protobuf_data).__name__, ret_code))
