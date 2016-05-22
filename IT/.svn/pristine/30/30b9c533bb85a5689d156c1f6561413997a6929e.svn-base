#coding = utf8
import struct, binascii, traceback, sys, threading, Queue, time, os, importlib
import dpkt.pcap, dpkt.ethernet, pika.frame, pika.spec, google.protobuf.message
from nose.tools import *
import msgbus_test_generator, client_m_test_generator, util

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
        #print direction, client_ip, client_port
        tup_list.append((direction, client_ip, client_port, ip.tcp.data))
    return tup_list
