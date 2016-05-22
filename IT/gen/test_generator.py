#coding = utf8
import struct, binascii, traceback, sys, threading, Queue, time, os, importlib
import dpkt.pcap, dpkt.ethernet, pika.frame, pika.spec, google.protobuf.message
from nose.tools import *
import protobuf_dict, msgbus_test_generator, client_m_test_generator, util

#gen_type: 'message_bus', 'client_m'
#pcap_type: 'windows-wireshark', 'linux-tcpdump'
def gen(gen_type, _serv_ip, serv_port, pcap_path, pcap_type, connection_service_dict_path, output_path,\
    ignored_addr_list=None):
    print '\n'*60
    reload(sys)
    sys.setdefaultencoding('utf8')
    tup_list = parse_pcap(pcap_path, pcap_type, _serv_ip, serv_port) 
    print 'parse_pcap() complete'    
    
    if 'message_bus' == gen_type:
        pb2_set, connection_set, actions = msgbus_test_generator.parse_tcp_data(tup_list)
        print 'parse_tcp_data() complete pb2_set = ', pb2_set
        msgbus_test_generator.write_test(_serv_ip, serv_port, pb2_set, connection_set, actions, output_path, connection_service_dict_path)
    elif 'client_m' == gen_type:
        pb2_set, actions = client_m_test_generator.parse_tcp_data(tup_list)
        print 'parse_tcp_data() complete pb2_set = ', pb2_set
        client_m_test_generator.write_test(_serv_ip, serv_port, pb2_set, actions, output_path)

def parse_pcap(pcap_path, pcap_type, _serv_ip, serv_port, ignored_addr_list=None):
    pb2_set = set()
    for fname in os.listdir('..\\pb2'):
        if '_pb2.py' == fname[-7:]:
            pb2_set.add(importlib.import_module(fname[:-3]))

    serv_ip = util.iphex(_serv_ip)
    serv_addr = (serv_ip, serv_port)
    reader = open(pcap_path, 'rb')    
    pcap = dpkt.pcap.Reader(reader)
    connection_extractor_dict = {}
    tup_list = [] # [('ToServer', client_ip, client_port, appmsg), (),...]
    counter = 0
    for ts, buf in pcap:            
        counter += 1
        #print 'counter = ', counter
        #print 'buf = '
        #util.hexprint(buf)
        if 'windows-wireshark' == pcap_type:
            ip = dpkt.ethernet.Ethernet(buf).ip
        elif 'linux-tcpdump' == pcap_type:
            ip = dpkt.ip.IP()
            ip.unpack(buf[16:])
        else:
            assert False, pcap_type
            
        if len(ip.tcp.data) == 0: continue        
        #if addr_ignored in ((ip.dst, ip.tcp.dport), (ip.src, ip.tcp.sport)): continue
            
        if serv_addr == (ip.dst, ip.tcp.dport): # client -> msgbus
            direction, client_ip, client_port = 'to_server', ip.src, ip.tcp.sport
        elif serv_addr == (ip.src, ip.tcp.sport): # msgbus -> client
            direction, client_ip, client_port = 'from_server', ip.dst, ip.tcp.dport
        else:
            assert False, 'serv_addr not found in IP packget'
        
        print direction, client_ip, client_port
        tup_list.append((direction, client_ip, client_port, ip.tcp.data))
        
    return tup_list
    
