import pika
from nose.tools import *
import tas_msgbus_client

def test_xxx():

    global client_0
    #client_name, serv_ip, serv_port, vhost, username, password
    client_0 = tas_msgbus_client.Client('client_0', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40191

    global client_1
    #client_name, serv_ip, serv_port, vhost, username, password
    client_1 = tas_msgbus_client.Client('client_1', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40192

    channel_0_1 = client_0.channel()

    channel_1_1 = client_1.channel()

    channel_1_1.confirm_delivery()

    channel_0_1.confirm_delivery()

    global client_2
    #client_name, serv_ip, serv_port, vhost, username, password
    client_2 = tas_msgbus_client.Client('client_2', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40193

    channel_2_1 = client_2.channel()

    channel_2_1.confirm_delivery()

    global client_3
    #client_name, serv_ip, serv_port, vhost, username, password
    client_3 = tas_msgbus_client.Client('client_3', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40194

    channel_3_1 = client_3.channel()

    global client_4
    #client_name, serv_ip, serv_port, vhost, username, password
    client_4 = tas_msgbus_client.Client('client_4', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40196

    channel_3_1.confirm_delivery()

    channel_4_1 = client_4.channel()

    channel_4_1.confirm_delivery()

    channel_4_1.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, arguments={})

    global client_5
    #client_name, serv_ip, serv_port, vhost, username, password
    client_5 = tas_msgbus_client.Client('client_5', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40198

    channel_5_1 = client_5.channel()

    global client_6
    #client_name, serv_ip, serv_port, vhost, username, password
    client_6 = tas_msgbus_client.Client('client_6', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40199

    channel_6_1 = client_6.channel()

    channel_5_1.confirm_delivery()

    channel_5_1.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, arguments={})

    channel_6_1.confirm_delivery()

    global client_7
    #client_name, serv_ip, serv_port, vhost, username, password
    client_7 = tas_msgbus_client.Client('client_7', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40200

    channel_7_1 = client_7.channel()

    channel_7_1.confirm_delivery()

    global client_8
    #client_name, serv_ip, serv_port, vhost, username, password
    client_8 = tas_msgbus_client.Client('client_8', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40201

    channel_8_1 = client_8.channel()

    channel_8_1.confirm_delivery()

    channel_8_1.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, arguments={})

    channel_8_1.queue_declare(queue='reckonservicesettle_req1', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})

    channel_8_1.queue_bind(queue='reckonservicesettle_req1', exchange='entry', routing_key='settle_req', arguments={})

    channel_8_1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_8_1.basic_consume(consumer_callback=client_8.callback, queue='reckonservicesettle_req1', no_ack=False, exclusive=False, consumer_tag='settle_req', arguments={})

    channel_8_2 = client_8.channel()

    channel_8_2.queue_declare(queue='reckonservicesettle_rsp1', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})

    channel_8_2.queue_bind(queue='reckonservicesettle_rsp1', exchange='entry', routing_key='settle_rsp', arguments={})

    channel_8_2.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_8_2.basic_consume(consumer_callback=client_8.callback, queue='reckonservicesettle_rsp1', no_ack=False, exclusive=False, consumer_tag='settle_rsp', arguments={})

    channel_8_3 = client_8.channel()

    channel_8_3.queue_declare(queue='reckonservicesettleprice_query_rsp1', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})

    channel_8_3.queue_bind(queue='reckonservicesettleprice_query_rsp1', exchange='entry', routing_key='settleprice_query_rsp', arguments={})

    channel_8_3.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_8_3.basic_consume(consumer_callback=client_8.callback, queue='reckonservicesettleprice_query_rsp1', no_ack=False, exclusive=False, consumer_tag='settleprice_query_rsp', arguments={})

    channel_5_1.queue_declare(queue='loglog_req', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_1.queue_bind(queue='loglog_req', exchange='entry', routing_key='log_req', arguments={})

    channel_5_1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_1.basic_consume(consumer_callback=client_5.callback, queue='loglog_req', no_ack=True, exclusive=False, consumer_tag='log_req', arguments={})

    channel_5_2 = client_5.channel()

    channel_5_2.queue_declare(queue='logmgr_req', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_2.queue_bind(queue='logmgr_req', exchange='entry', routing_key='mgr_req', arguments={})

    channel_5_2.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_2.basic_consume(consumer_callback=client_5.callback, queue='logmgr_req', no_ack=True, exclusive=False, consumer_tag='mgr_req', arguments={})

    channel_5_3 = client_5.channel()

    channel_5_3.queue_declare(queue='logmgr_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_3.queue_bind(queue='logmgr_rsp', exchange='entry', routing_key='mgr_rsp', arguments={})

    channel_5_3.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_3.basic_consume(consumer_callback=client_5.callback, queue='logmgr_rsp', no_ack=True, exclusive=False, consumer_tag='mgr_rsp', arguments={})

    channel_5_4 = client_5.channel()

    channel_5_4.queue_declare(queue='loguser_req', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_4.queue_bind(queue='loguser_req', exchange='entry', routing_key='user_req', arguments={})

    channel_5_4.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_4.basic_consume(consumer_callback=client_5.callback, queue='loguser_req', no_ack=True, exclusive=False, consumer_tag='user_req', arguments={})

    channel_5_5 = client_5.channel()

    channel_5_5.queue_declare(queue='loguser_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_5.queue_bind(queue='loguser_rsp', exchange='entry', routing_key='user_rsp', arguments={})

    channel_5_5.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_5.basic_consume(consumer_callback=client_5.callback, queue='loguser_rsp', no_ack=True, exclusive=False, consumer_tag='user_rsp', arguments={})

    channel_5_6 = client_5.channel()

    channel_5_6.queue_declare(queue='logcash_req', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_6.queue_bind(queue='logcash_req', exchange='entry', routing_key='cash_req', arguments={})

    channel_5_6.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_6.basic_consume(consumer_callback=client_5.callback, queue='logcash_req', no_ack=True, exclusive=False, consumer_tag='cash_req', arguments={})

    channel_5_7 = client_5.channel()

    channel_5_7.queue_declare(queue='logcash_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_7.queue_bind(queue='logcash_rsp', exchange='entry', routing_key='cash_rsp', arguments={})

    channel_5_7.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_7.basic_consume(consumer_callback=client_5.callback, queue='logcash_rsp', no_ack=True, exclusive=False, consumer_tag='cash_rsp', arguments={})

    channel_5_8 = client_5.channel()

    channel_5_8.queue_declare(queue='logmoneymodify_req', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_8.queue_bind(queue='logmoneymodify_req', exchange='entry', routing_key='moneymodify_req', arguments={})

    channel_5_8.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_8.basic_consume(consumer_callback=client_5.callback, queue='logmoneymodify_req', no_ack=True, exclusive=False, consumer_tag='moneymodify_req', arguments={})

    channel_5_9 = client_5.channel()

    channel_5_9.queue_declare(queue='logmoneymodify_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_9.queue_bind(queue='logmoneymodify_rsp', exchange='entry', routing_key='moneymodify_rsp', arguments={})

    channel_5_9.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_9.basic_consume(consumer_callback=client_5.callback, queue='logmoneymodify_rsp', no_ack=True, exclusive=False, consumer_tag='moneymodify_rsp', arguments={})

    channel_5_10 = client_5.channel()

    channel_5_10.queue_declare(queue='logorder_req', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_10.queue_bind(queue='logorder_req', exchange='entry', routing_key='order_req', arguments={})

    channel_5_10.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_10.basic_consume(consumer_callback=client_5.callback, queue='logorder_req', no_ack=True, exclusive=False, consumer_tag='order_req', arguments={})

    channel_5_11 = client_5.channel()

    channel_5_11.queue_declare(queue='logorder_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_11.queue_bind(queue='logorder_rsp', exchange='entry', routing_key='order_rsp', arguments={})

    channel_5_11.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_11.basic_consume(consumer_callback=client_5.callback, queue='logorder_rsp', no_ack=True, exclusive=False, consumer_tag='order_rsp', arguments={})

    channel_5_12 = client_5.channel()

    channel_5_12.queue_declare(queue='lognewsfeed_req', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_12.queue_bind(queue='lognewsfeed_req', exchange='entry', routing_key='newsfeed_req', arguments={})

    channel_5_12.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_12.basic_consume(consumer_callback=client_5.callback, queue='lognewsfeed_req', no_ack=True, exclusive=False, consumer_tag='newsfeed_req', arguments={})

    channel_5_13 = client_5.channel()

    channel_5_13.queue_declare(queue='lognewsfeed_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_5_13.queue_bind(queue='lognewsfeed_rsp', exchange='entry', routing_key='newsfeed_rsp', arguments={})

    channel_5_13.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_5_13.basic_consume(consumer_callback=client_5.callback, queue='lognewsfeed_rsp', no_ack=True, exclusive=False, consumer_tag='newsfeed_rsp', arguments={})

    channel_0_1.basic_publish('entry', 'heartbeat', 'heartbeat')

    global client_9
    #client_name, serv_ip, serv_port, vhost, username, password
    client_9 = tas_msgbus_client.Client('client_9', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40208

    channel_9_1 = client_9.channel()

    channel_9_1.confirm_delivery()

    global client_10
    #client_name, serv_ip, serv_port, vhost, username, password
    client_10 = tas_msgbus_client.Client('client_10', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40209

    channel_10_1 = client_10.channel()

    global client_11
    #client_name, serv_ip, serv_port, vhost, username, password
    client_11 = tas_msgbus_client.Client('client_11', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40210

    channel_11_1 = client_11.channel()

    channel_10_1.confirm_delivery()

    channel_11_1.confirm_delivery()

    global client_12
    #client_name, serv_ip, serv_port, vhost, username, password
    client_12 = tas_msgbus_client.Client('client_12', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40213

    channel_12_1 = client_12.channel()

    channel_12_1.confirm_delivery()

    global client_13
    #client_name, serv_ip, serv_port, vhost, username, password
    client_13 = tas_msgbus_client.Client('client_13', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40214

    channel_13_1 = client_13.channel()

    global client_14
    #client_name, serv_ip, serv_port, vhost, username, password
    client_14 = tas_msgbus_client.Client('client_14', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40215

    channel_14_1 = client_14.channel()

    channel_13_1.confirm_delivery()

    channel_13_1.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, arguments={})

    global client_15
    #client_name, serv_ip, serv_port, vhost, username, password
    client_15 = tas_msgbus_client.Client('client_15', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40216

    channel_15_1 = client_15.channel()

    channel_14_1.confirm_delivery()

    channel_14_1.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, arguments={})

    channel_15_1.confirm_delivery()

    global client_16
    #client_name, serv_ip, serv_port, vhost, username, password
    client_16 = tas_msgbus_client.Client('client_16', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40218

    channel_16_1 = client_16.channel()

    channel_14_1.queue_declare(queue='busproxyuser_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_16_1.confirm_delivery()

    channel_14_1.queue_bind(queue='busproxyuser_rsp1', exchange='entry', routing_key='user_rsp', arguments={})

    channel_14_1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_1.basic_consume(consumer_callback=client_14.callback, queue='busproxyuser_rsp1', no_ack=True, exclusive=False, consumer_tag='user_rsp', arguments={})

    channel_14_2 = client_14.channel()

    global client_17
    #client_name, serv_ip, serv_port, vhost, username, password
    client_17 = tas_msgbus_client.Client('client_17', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 40220

    channel_17_1 = client_17.channel()

    channel_14_2.queue_declare(queue='busproxymgr_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_2.queue_bind(queue='busproxymgr_rsp1', exchange='entry', routing_key='mgr_rsp', arguments={})

    channel_17_1.confirm_delivery()

    channel_17_1.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, arguments={})

    channel_17_1.queue_declare(queue='news_feednewsfeed_req', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_17_1.queue_bind(queue='news_feednewsfeed_req', exchange='entry', routing_key='newsfeed_req', arguments={})

    channel_17_1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_2.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_17_1.basic_consume(consumer_callback=client_17.callback, queue='news_feednewsfeed_req', no_ack=True, exclusive=False, consumer_tag='newsfeed_req', arguments={})

    channel_14_2.basic_consume(consumer_callback=client_14.callback, queue='busproxymgr_rsp1', no_ack=True, exclusive=False, consumer_tag='mgr_rsp', arguments={})

    channel_17_2 = client_17.channel()

    channel_14_3 = client_14.channel()

    channel_17_2.queue_declare(queue='news_feednotify_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_17_2.queue_bind(queue='news_feednotify_rsp', exchange='entry', routing_key='notify_rsp', arguments={})

    channel_17_2.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_17_2.basic_consume(consumer_callback=client_17.callback, queue='news_feednotify_rsp', no_ack=True, exclusive=False, consumer_tag='notify_rsp', arguments={})

    channel_17_3 = client_17.channel()

    channel_17_3.queue_declare(queue='news_feedsettle_req', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_17_3.queue_bind(queue='news_feedsettle_req', exchange='entry', routing_key='settle_req', arguments={})

    channel_17_3.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_17_3.basic_consume(consumer_callback=client_17.callback, queue='news_feedsettle_req', no_ack=True, exclusive=False, consumer_tag='settle_req', arguments={})

    channel_17_4 = client_17.channel()

    channel_17_4.queue_declare(queue='news_feedmgr_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_17_4.queue_bind(queue='news_feedmgr_rsp', exchange='entry', routing_key='mgr_rsp', arguments={})

    channel_17_4.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_17_4.basic_consume(consumer_callback=client_17.callback, queue='news_feedmgr_rsp', no_ack=True, exclusive=False, consumer_tag='mgr_rsp', arguments={})

    channel_15_1.basic_publish('entry', 'heartbeat', 'heartbeat')

    channel_14_3.queue_declare(queue='busproxyquery_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_3.queue_bind(queue='busproxyquery_rsp1', exchange='entry', routing_key='query_rsp', arguments={})

    channel_14_3.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_3.basic_consume(consumer_callback=client_14.callback, queue='busproxyquery_rsp1', no_ack=True, exclusive=False, consumer_tag='query_rsp', arguments={})

    channel_14_4 = client_14.channel()

    channel_14_4.queue_declare(queue='busproxyorder_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_4.queue_bind(queue='busproxyorder_rsp1', exchange='entry', routing_key='order_rsp', arguments={})

    channel_14_4.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_4.basic_consume(consumer_callback=client_14.callback, queue='busproxyorder_rsp1', no_ack=True, exclusive=False, consumer_tag='order_rsp', arguments={})

    channel_14_5 = client_14.channel()

    channel_14_5.queue_declare(queue='busproxybank_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_5.queue_bind(queue='busproxybank_rsp1', exchange='entry', routing_key='bank_rsp', arguments={})

    channel_14_5.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_5.basic_consume(consumer_callback=client_14.callback, queue='busproxybank_rsp1', no_ack=True, exclusive=False, consumer_tag='bank_rsp', arguments={})

    channel_14_6 = client_14.channel()

    channel_14_6.queue_declare(queue='busproxycash_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_6.queue_bind(queue='busproxycash_rsp1', exchange='entry', routing_key='cash_rsp', arguments={})

    channel_14_6.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_6.basic_consume(consumer_callback=client_14.callback, queue='busproxycash_rsp1', no_ack=True, exclusive=False, consumer_tag='cash_rsp', arguments={})

    channel_14_7 = client_14.channel()

    channel_14_7.queue_declare(queue='busproxynotify_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_7.queue_bind(queue='busproxynotify_rsp1', exchange='entry', routing_key='notify_rsp', arguments={})

    channel_14_7.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_7.basic_consume(consumer_callback=client_14.callback, queue='busproxynotify_rsp1', no_ack=True, exclusive=False, consumer_tag='notify_rsp', arguments={})

    channel_14_8 = client_14.channel()

    channel_14_8.queue_declare(queue='busproxymoneymodify_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_8.queue_bind(queue='busproxymoneymodify_rsp1', exchange='entry', routing_key='moneymodify_rsp', arguments={})

    channel_14_8.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_8.basic_consume(consumer_callback=client_14.callback, queue='busproxymoneymodify_rsp1', no_ack=True, exclusive=False, consumer_tag='moneymodify_rsp', arguments={})

    channel_14_9 = client_14.channel()

    channel_14_9.queue_declare(queue='busproxybank_query_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_9.queue_bind(queue='busproxybank_query_rsp1', exchange='entry', routing_key='bank_query_rsp', arguments={})

    channel_14_9.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_9.basic_consume(consumer_callback=client_14.callback, queue='busproxybank_query_rsp1', no_ack=True, exclusive=False, consumer_tag='bank_query_rsp', arguments={})

    channel_14_10 = client_14.channel()

    channel_14_10.queue_declare(queue='busproxybank_mgr_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_10.queue_bind(queue='busproxybank_mgr_rsp1', exchange='entry', routing_key='bank_mgr_rsp', arguments={})

    channel_14_10.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_10.basic_consume(consumer_callback=client_14.callback, queue='busproxybank_mgr_rsp1', no_ack=True, exclusive=False, consumer_tag='bank_mgr_rsp', arguments={})

    channel_14_11 = client_14.channel()

    channel_14_11.queue_declare(queue='busproxyreport_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_11.queue_bind(queue='busproxyreport_rsp1', exchange='entry', routing_key='report_rsp', arguments={})

    channel_14_11.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_11.basic_consume(consumer_callback=client_14.callback, queue='busproxyreport_rsp1', no_ack=True, exclusive=False, consumer_tag='report_rsp', arguments={})

    channel_14_12 = client_14.channel()

    channel_14_12.queue_declare(queue='busproxynewsfeed_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_12.queue_bind(queue='busproxynewsfeed_rsp1', exchange='entry', routing_key='newsfeed_rsp', arguments={})

    channel_14_12.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_12.basic_consume(consumer_callback=client_14.callback, queue='busproxynewsfeed_rsp1', no_ack=True, exclusive=False, consumer_tag='newsfeed_rsp', arguments={})

    channel_14_13 = client_14.channel()

    channel_14_13.queue_declare(queue='busproxylog_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_13.queue_bind(queue='busproxylog_rsp1', exchange='entry', routing_key='log_rsp', arguments={})

    channel_14_13.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_13.basic_consume(consumer_callback=client_14.callback, queue='busproxylog_rsp1', no_ack=True, exclusive=False, consumer_tag='log_rsp', arguments={})

    channel_14_14 = client_14.channel()

    channel_14_14.queue_declare(queue='busproxyrt_monitor_publish1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_14.queue_bind(queue='busproxyrt_monitor_publish1', exchange='entry', routing_key='rt_monitor_publish', arguments={})

    channel_14_14.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_14.basic_consume(consumer_callback=client_14.callback, queue='busproxyrt_monitor_publish1', no_ack=True, exclusive=False, consumer_tag='rt_monitor_publish', arguments={})

    channel_14_15 = client_14.channel()

    channel_14_15.queue_declare(queue='busproxyrisk_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_15.queue_bind(queue='busproxyrisk_rsp1', exchange='entry', routing_key='risk_rsp', arguments={})

    channel_14_15.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_15.basic_consume(consumer_callback=client_14.callback, queue='busproxyrisk_rsp1', no_ack=True, exclusive=False, consumer_tag='risk_rsp', arguments={})

    channel_14_16 = client_14.channel()

    channel_14_16.queue_declare(queue='busproxywetas_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_16.queue_bind(queue='busproxywetas_rsp1', exchange='entry', routing_key='wetas_rsp', arguments={})

    channel_14_16.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_16.basic_consume(consumer_callback=client_14.callback, queue='busproxywetas_rsp1', no_ack=True, exclusive=False, consumer_tag='wetas_rsp', arguments={})

    channel_14_17 = client_14.channel()

    channel_14_17.queue_declare(queue='busproxyex_qkernel_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_17.queue_bind(queue='busproxyex_qkernel_rsp1', exchange='entry', routing_key='ex_qkernel_rsp', arguments={})

    channel_14_17.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_17.basic_consume(consumer_callback=client_14.callback, queue='busproxyex_qkernel_rsp1', no_ack=True, exclusive=False, consumer_tag='ex_qkernel_rsp', arguments={})

    channel_14_18 = client_14.channel()

    channel_14_18.queue_declare(queue='busproxyex_report_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_18.queue_bind(queue='busproxyex_report_rsp1', exchange='entry', routing_key='ex_report_rsp', arguments={})

    channel_14_18.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_18.basic_consume(consumer_callback=client_14.callback, queue='busproxyex_report_rsp1', no_ack=True, exclusive=False, consumer_tag='ex_report_rsp', arguments={})

    channel_14_19 = client_14.channel()

    channel_14_19.queue_declare(queue='busproxydelivery2_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_19.queue_bind(queue='busproxydelivery2_rsp1', exchange='entry', routing_key='delivery2_rsp', arguments={})

    channel_14_19.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_19.basic_consume(consumer_callback=client_14.callback, queue='busproxydelivery2_rsp1', no_ack=True, exclusive=False, consumer_tag='delivery2_rsp', arguments={})

    channel_14_20 = client_14.channel()

    channel_14_20.queue_declare(queue='busproxysettle_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_20.queue_bind(queue='busproxysettle_rsp1', exchange='entry', routing_key='settle_rsp', arguments={})

    channel_14_20.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_20.basic_consume(consumer_callback=client_14.callback, queue='busproxysettle_rsp1', no_ack=True, exclusive=False, consumer_tag='settle_rsp', arguments={})

    channel_14_21 = client_14.channel()

    channel_14_21.queue_declare(queue='busproxyfinance_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_14_21.queue_bind(queue='busproxyfinance_rsp1', exchange='entry', routing_key='finance_rsp', arguments={})

    channel_14_21.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_14_21.basic_consume(consumer_callback=client_14.callback, queue='busproxyfinance_rsp1', no_ack=True, exclusive=False, consumer_tag='finance_rsp', arguments={})

    channel_10_1.basic_publish('entry', 'heartbeat', 'heartbeat')

    print 'HHHHHHHHHHHHHHH'
# 3.398000 seconds spent