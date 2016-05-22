import pika
from nose.tools import *
import tas_msgbus_client

def test_xxx():

    global client_0
    #client_name, serv_ip, serv_port, vhost, username, password
    client_0 = tas_msgbus_client.Client('client_0', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 17696

    channel_0_1 = client_0.channel()

    channel_0_1.confirm_delivery()

    global client_1
    #client_name, serv_ip, serv_port, vhost, username, password
    client_1 = tas_msgbus_client.Client('client_1', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 17697

    channel_1_1 = client_1.channel()

    channel_1_1.confirm_delivery()

    global client_2
    #client_name, serv_ip, serv_port, vhost, username, password
    client_2 = tas_msgbus_client.Client('client_2', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 17698

    channel_2_1 = client_2.channel()

    channel_2_1.confirm_delivery()

    channel_2_1.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, arguments={})

    channel_2_1.queue_declare(queue='busproxyuser_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_1.queue_bind(queue='busproxyuser_rsp1', exchange='entry', routing_key='user_rsp', arguments={})

    channel_2_1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_1.basic_consume(consumer_callback=client_2.callback, queue='busproxyuser_rsp1', no_ack=True, exclusive=False, consumer_tag='user_rsp', arguments={})

    channel_2_2 = client_2.channel()

    channel_2_2.queue_declare(queue='busproxymgr_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_2.queue_bind(queue='busproxymgr_rsp1', exchange='entry', routing_key='mgr_rsp', arguments={})

    channel_2_2.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_2.basic_consume(consumer_callback=client_2.callback, queue='busproxymgr_rsp1', no_ack=True, exclusive=False, consumer_tag='mgr_rsp', arguments={})

    channel_2_3 = client_2.channel()

    channel_2_3.queue_declare(queue='busproxyquery_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_3.queue_bind(queue='busproxyquery_rsp1', exchange='entry', routing_key='query_rsp', arguments={})

    channel_2_3.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_3.basic_consume(consumer_callback=client_2.callback, queue='busproxyquery_rsp1', no_ack=True, exclusive=False, consumer_tag='query_rsp', arguments={})

    channel_2_4 = client_2.channel()

    channel_2_4.queue_declare(queue='busproxyorder_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_4.queue_bind(queue='busproxyorder_rsp1', exchange='entry', routing_key='order_rsp', arguments={})

    channel_2_4.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_4.basic_consume(consumer_callback=client_2.callback, queue='busproxyorder_rsp1', no_ack=True, exclusive=False, consumer_tag='order_rsp', arguments={})

    channel_2_5 = client_2.channel()

    channel_2_5.queue_declare(queue='busproxybank_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_5.queue_bind(queue='busproxybank_rsp1', exchange='entry', routing_key='bank_rsp', arguments={})

    channel_2_5.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_5.basic_consume(consumer_callback=client_2.callback, queue='busproxybank_rsp1', no_ack=True, exclusive=False, consumer_tag='bank_rsp', arguments={})

    channel_2_6 = client_2.channel()

    channel_2_6.queue_declare(queue='busproxycash_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_6.queue_bind(queue='busproxycash_rsp1', exchange='entry', routing_key='cash_rsp', arguments={})

    channel_2_6.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_6.basic_consume(consumer_callback=client_2.callback, queue='busproxycash_rsp1', no_ack=True, exclusive=False, consumer_tag='cash_rsp', arguments={})

    channel_2_7 = client_2.channel()

    channel_2_7.queue_declare(queue='busproxynotify_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_7.queue_bind(queue='busproxynotify_rsp1', exchange='entry', routing_key='notify_rsp', arguments={})

    channel_2_7.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_7.basic_consume(consumer_callback=client_2.callback, queue='busproxynotify_rsp1', no_ack=True, exclusive=False, consumer_tag='notify_rsp', arguments={})

    channel_2_8 = client_2.channel()

    channel_2_8.queue_declare(queue='busproxymoneymodify_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_8.queue_bind(queue='busproxymoneymodify_rsp1', exchange='entry', routing_key='moneymodify_rsp', arguments={})

    channel_2_8.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_8.basic_consume(consumer_callback=client_2.callback, queue='busproxymoneymodify_rsp1', no_ack=True, exclusive=False, consumer_tag='moneymodify_rsp', arguments={})

    channel_2_9 = client_2.channel()

    channel_2_9.queue_declare(queue='busproxybank_query_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_9.queue_bind(queue='busproxybank_query_rsp1', exchange='entry', routing_key='bank_query_rsp', arguments={})

    channel_2_9.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_9.basic_consume(consumer_callback=client_2.callback, queue='busproxybank_query_rsp1', no_ack=True, exclusive=False, consumer_tag='bank_query_rsp', arguments={})

    channel_2_10 = client_2.channel()

    channel_2_10.queue_declare(queue='busproxybank_mgr_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_10.queue_bind(queue='busproxybank_mgr_rsp1', exchange='entry', routing_key='bank_mgr_rsp', arguments={})

    channel_2_10.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_10.basic_consume(consumer_callback=client_2.callback, queue='busproxybank_mgr_rsp1', no_ack=True, exclusive=False, consumer_tag='bank_mgr_rsp', arguments={})

    channel_2_11 = client_2.channel()

    channel_2_11.queue_declare(queue='busproxyreport_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_11.queue_bind(queue='busproxyreport_rsp1', exchange='entry', routing_key='report_rsp', arguments={})

    channel_2_11.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_11.basic_consume(consumer_callback=client_2.callback, queue='busproxyreport_rsp1', no_ack=True, exclusive=False, consumer_tag='report_rsp', arguments={})

    channel_2_12 = client_2.channel()

    channel_2_12.queue_declare(queue='busproxynewsfeed_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_12.queue_bind(queue='busproxynewsfeed_rsp1', exchange='entry', routing_key='newsfeed_rsp', arguments={})

    channel_2_12.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_12.basic_consume(consumer_callback=client_2.callback, queue='busproxynewsfeed_rsp1', no_ack=True, exclusive=False, consumer_tag='newsfeed_rsp', arguments={})

    channel_2_13 = client_2.channel()

    channel_2_13.queue_declare(queue='busproxylog_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_13.queue_bind(queue='busproxylog_rsp1', exchange='entry', routing_key='log_rsp', arguments={})

    channel_2_13.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_13.basic_consume(consumer_callback=client_2.callback, queue='busproxylog_rsp1', no_ack=True, exclusive=False, consumer_tag='log_rsp', arguments={})

    channel_2_14 = client_2.channel()

    channel_2_14.queue_declare(queue='busproxyrt_monitor_publish1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_14.queue_bind(queue='busproxyrt_monitor_publish1', exchange='entry', routing_key='rt_monitor_publish', arguments={})

    channel_2_14.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_14.basic_consume(consumer_callback=client_2.callback, queue='busproxyrt_monitor_publish1', no_ack=True, exclusive=False, consumer_tag='rt_monitor_publish', arguments={})

    channel_2_15 = client_2.channel()

    channel_2_15.queue_declare(queue='busproxyrisk_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_15.queue_bind(queue='busproxyrisk_rsp1', exchange='entry', routing_key='risk_rsp', arguments={})

    channel_2_15.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_15.basic_consume(consumer_callback=client_2.callback, queue='busproxyrisk_rsp1', no_ack=True, exclusive=False, consumer_tag='risk_rsp', arguments={})

    channel_2_16 = client_2.channel()

    channel_2_16.queue_declare(queue='busproxywetas_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_16.queue_bind(queue='busproxywetas_rsp1', exchange='entry', routing_key='wetas_rsp', arguments={})

    channel_2_16.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_16.basic_consume(consumer_callback=client_2.callback, queue='busproxywetas_rsp1', no_ack=True, exclusive=False, consumer_tag='wetas_rsp', arguments={})

    channel_2_17 = client_2.channel()

    channel_2_17.queue_declare(queue='busproxyex_qkernel_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_17.queue_bind(queue='busproxyex_qkernel_rsp1', exchange='entry', routing_key='ex_qkernel_rsp', arguments={})

    channel_2_17.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_17.basic_consume(consumer_callback=client_2.callback, queue='busproxyex_qkernel_rsp1', no_ack=True, exclusive=False, consumer_tag='ex_qkernel_rsp', arguments={})

    channel_2_18 = client_2.channel()

    channel_2_18.queue_declare(queue='busproxyex_report_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_18.queue_bind(queue='busproxyex_report_rsp1', exchange='entry', routing_key='ex_report_rsp', arguments={})

    channel_2_18.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_18.basic_consume(consumer_callback=client_2.callback, queue='busproxyex_report_rsp1', no_ack=True, exclusive=False, consumer_tag='ex_report_rsp', arguments={})

    channel_2_19 = client_2.channel()

    channel_2_19.queue_declare(queue='busproxydelivery2_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_19.queue_bind(queue='busproxydelivery2_rsp1', exchange='entry', routing_key='delivery2_rsp', arguments={})

    channel_2_19.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_19.basic_consume(consumer_callback=client_2.callback, queue='busproxydelivery2_rsp1', no_ack=True, exclusive=False, consumer_tag='delivery2_rsp', arguments={})

    channel_2_20 = client_2.channel()

    channel_2_20.queue_declare(queue='busproxysettle_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_20.queue_bind(queue='busproxysettle_rsp1', exchange='entry', routing_key='settle_rsp', arguments={})

    channel_2_20.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_20.basic_consume(consumer_callback=client_2.callback, queue='busproxysettle_rsp1', no_ack=True, exclusive=False, consumer_tag='settle_rsp', arguments={})

    channel_2_21 = client_2.channel()

    channel_2_21.queue_declare(queue='busproxyfinance_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})

    channel_2_21.queue_bind(queue='busproxyfinance_rsp1', exchange='entry', routing_key='finance_rsp', arguments={})

    channel_2_21.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)

    channel_2_21.basic_consume(consumer_callback=client_2.callback, queue='busproxyfinance_rsp1', no_ack=True, exclusive=False, consumer_tag='finance_rsp', arguments={})

    channel_0_1.basic_publish('entry', 'heartbeat', 'heartbeat')

# 0.861000 seconds spent