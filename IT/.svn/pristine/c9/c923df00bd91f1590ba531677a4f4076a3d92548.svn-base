import time, Queue
from nose.tools import *
import pika
import msgbus, bank

def setup():
    pika.callback.LOGGER.setLevel('DEBUG')
    #pika.channel.LOGGER.setLevel('WARNING')
    #pika.connection.LOGGER.setLevel('WARNING')
    #pika.adapters.blocking_connection.LOGGER.setLevel('WARNING')
    #pika.adapters.select_connection.LOGGER.setLevel('WARNING')
    #pika.adapters.base_connection.LOGGER.setLevel('WARNING')
    global bank
    bank = None
    
@nottest        
def test_heartbeat():
    recv_conn = msgbus.Connection('conn_main', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
    recv_chan = recv_conn.channel()
    recv_chan.confirm_delivery()
    recv_chan.queue_declare(queue='entry')
    recv_chan.basic_consume(recv_conn.callback, queue='entry', no_ack=True)
    
    bank = server_bank.Bank('192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
    bank.chan_heartbeat.basic_publish('entry', 'heartbeat', 'heartbeat')
    
    print recv_conn.recv(3.0)     

def test_bank_req_2():
    global bank
    bank = server_bank.Bank('192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
    #print 'bank created'
    
    send_conn = msgbus.Connection('sc', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
    send_chan = send_conn.channel()
    send_chan.exchange_declare(exchange='entry', type='direct')
    print 'sender created'
    
    send_chan.basic_publish(exchange='entry', routing_key='bank_req_2', body='heartbeat')
    send_chan.basic_publish(exchange='entry', routing_key='bank_req_2', body='heartbeat')
    send_chan.basic_publish(exchange='entry', routing_key='bank_req_2', body='heartbeat')
    print 'published'

    time.sleep(1.0)
    try:
        while True:
            method, properties, funcode, session_id, protobuf_data =\
                bank.conn_main.recv(bank.chan_bank_req_2, 1.0)
            print 'received'
            print method
            print funcode, session_id
            print protobuf_data
    except Queue.Empty, e:
        pass
            
def teardown():
    msgbus.Connection.close_all()    
