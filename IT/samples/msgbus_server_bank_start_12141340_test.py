import pika
from nose.tools import *
import tas_msgbus_client

def test_xxx():

    global client_0
    #client_name, serv_ip, serv_port, vhost, username, password
    client_0 = tas_msgbus_client.Client('client_0', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.21 2280

    channel_0_1 = client_0.channel()

    channel_0_1.confirm_delivery()

    global client_1
    #client_name, serv_ip, serv_port, vhost, username, password
    client_1 = tas_msgbus_client.Client('client_1', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.21 2281

    channel_1_1 = client_1.channel()

    channel_1_1.confirm_delivery()

    global client_2
    #client_name, serv_ip, serv_port, vhost, username, password
    client_2 = tas_msgbus_client.Client('client_2', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.21 2282

    channel_2_1 = client_2.channel()

    channel_2_1.confirm_delivery()

    channel_2_1.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, arguments={})

    channel_2_1.queue_declare(queue='bankbank_req_2', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})

    channel_2_1.queue_bind(queue='bankbank_req_2', exchange='entry', routing_key='bank_req_2', arguments={})

    channel_2_1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_1.basic_consume(consumer_callback=client_2.callback, queue='bankbank_req_2', no_ack=False, exclusive=False, consumer_tag='bank_req_2', arguments={})

    channel_2_2 = client_2.channel()

    channel_2_2.queue_declare(queue='bankbankioproxy_rsp_2', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})

    channel_2_2.queue_bind(queue='bankbankioproxy_rsp_2', exchange='entry', routing_key='bankioproxy_rsp_2', arguments={})

    channel_2_2.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_2.basic_consume(consumer_callback=client_2.callback, queue='bankbankioproxy_rsp_2', no_ack=False, exclusive=False, consumer_tag='bankioproxy_rsp_2', arguments={})

    channel_2_3 = client_2.channel()

    channel_2_3.queue_declare(queue='bankbankinner_2', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})

    channel_2_3.queue_bind(queue='bankbankinner_2', exchange='entry', routing_key='bankinner_2', arguments={})

    channel_2_3.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_3.basic_consume(consumer_callback=client_2.callback, queue='bankbankinner_2', no_ack=False, exclusive=False, consumer_tag='bankinner_2', arguments={})

    channel_2_4 = client_2.channel()

    channel_2_4.queue_declare(queue='bankbankcommunicate_req_2', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})

    channel_2_4.queue_bind(queue='bankbankcommunicate_req_2', exchange='entry', routing_key='bankcommunicate_req_2', arguments={})

    channel_2_4.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_4.basic_consume(consumer_callback=client_2.callback, queue='bankbankcommunicate_req_2', no_ack=False, exclusive=False, consumer_tag='bankcommunicate_req_2', arguments={})

    channel_0_1.basic_publish('entry', 'heartbeat', 'heartbeat')

    channel_0_1.basic_publish('entry', 'heartbeat', 'heartbeat')

    channel_0_1.basic_publish('entry', 'heartbeat', 'heartbeat')

    channel_0_1.basic_publish('entry', 'heartbeat', 'heartbeat')

    channel_0_1.basic_publish('entry', 'heartbeat', 'heartbeat')

def teardown():
    tas_msgbus_client.Client.close_all()

# 0.021000 seconds spent