import time, Queue
from nose.tools import *
import pika
import UserTas1_pb2
import msgbus, busproxy

def setup():
    pika.callback.LOGGER.setLevel('WARNING')
    pika.channel.LOGGER.setLevel('WARNING')
    pika.connection.LOGGER.setLevel('WARNING')
    pika.adapters.blocking_connection.LOGGER.setLevel('WARNING')
    pika.adapters.select_connection.LOGGER.setLevel('WARNING')
    pika.adapters.base_connection.LOGGER.setLevel('WARNING')

    global proxy
    proxy = busproxy.BusProxy('192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
    print 'proxy created'

def test_heartbeat(): #pass
    recv_conn = msgbus.Connection('sc', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
    recv_chan = recv_conn.channel()
    recv_chan.exchange_declare(exchange='entry', exchange_type='direct')
    recv_chan.queue_declare(queue='heartbeat', durable=True)
    recv_conn.basic_consume(recv_chan, 'heartbeat', 'heartbeat')
    
    for i in range(5):
        proxy.chan_heartbeat.basic_publish('entry', 'heartbeat', 'heartbeat')

    try:
        while True:
            print recv_conn.recv(recv_chan, 1.0)
    except Queue.Empty as e:
        pass

def test_user_req_publish():#pass
    recv_conn = msgbus.Connection('sc', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
    recv_chan = recv_conn.channel()
    recv_chan.exchange_declare(exchange='entry', exchange_type='direct')
    recv_chan.queue_declare(queue='user_req', durable=True)
    recv_chan.queue_bind(queue='user_req', exchange='entry', routing_key='user_req')
    consumer_tag = recv_conn.basic_consume(recv_chan, 'user_req')
    print 'consumer_tag = ', consumer_tag
        
    protobuf_data = UserTas1_pb2.P2LStatusSync()
    protobuf_data.Header.FunCode = 131632
    protobuf_data.ProxyID = 1
    protobuf_data.SessinIDStart = 268435456
    protobuf_data.SessinIDEnd = 536870911
    app_msg = msgbus.encode(131632, 0, protobuf_data)
    for i in range(6):
        proxy.chan_publish.basic_publish('entry', 'user_req', app_msg)    

    try:
        while True:
            recv_conn.expect(recv_chan, 0, protobuf_data, 1.0)
    except Queue.Empty as e:
        pass

def test_user_rsp_consume():
    send_conn = msgbus.Connection('sc', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
    send_chan = send_conn.channel()
    for i in range(5):
        send_chan.basic_publish('entry', 'user_rsp', 'heartbeat')
    time.sleep(1.0)
    try:
        while True:
            meth, prop, funcode, session_id, data = proxy.conn_consume.recv(proxy.chan_user_rsp1, 1.0)
            print meth.delivery_tag, session_id
            print data
    except Queue.Empty as e:
        raise e
                
def teardown():
    msgbus.Connection.close_all()    
