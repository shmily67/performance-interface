import pika
from nose.tools import *
import tas_msgbus_connection

# Msgbus connection for server_busproxy

class ServerBusProxy(object):
    def __init__(self, client_name, serv_ip, serv_port, vhost, username, password):
        self.client_name, self.serv_ip, self.serv_port, self.vhost, self.username, self.password = \
            client_name, serv_ip, serv_port, vhost, username, password
        self.channel_dict = {}

        #connection_name, serv_ip, serv_port, vhost, username, password
        self.connection_heartbeat = msgbus_connection.Connection('connection_heartbeat', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 17696
        self.connection_req = msgbus_connection.Connection('connection_req', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 17697
        self.connection_rsp = msgbus_connection.Connection('connection_rsp', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest') # 192.168.31.160 17698

        self.channel_heartbeat = connection_heartbeat.channel()
        self.channel_dict['heartbeat'] = channel_heartbeat
        self.channel_heartbeat.confirm_delivery()
        #self.channel_heartbeat.basic_publish('entry', 'heartbeat', 'heartbeat')

        channel_xxx_req = connection_req.channel()
        self.channel_dict['xxx_req'] = channel_xxx_req
        channel_xxx_req.confirm_delivery()

        self.channel_user_rsp = connection_rsp.channel()
        self.channel_dict['user_rsp'] = self.channel_user_rsp
        self.channel_user_rsp.confirm_delivery()
        self.channel_user_rsp.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, arguments={})
        self.channel_user_rsp.queue_declare(queue='busproxyuser_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_user_rsp.queue_bind(queue='busproxyuser_rsp', exchange='entry', routing_key='user_rsp', arguments={})
        self.channel_user_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_user_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxyuser_rsp', no_ack=True, exclusive=False, consumer_tag='user_rsp', arguments={})

        self.channel_mgr_rsp = connection_rsp.channel()
        self.channel_dict['mgr_rsp'] = self.channel_mgr_rsp
        self.channel_mgr_rsp.queue_declare(queue='busproxymgr_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_mgr_rsp.queue_bind(queue='busproxymgr_rsp', exchange='entry', routing_key='mgr_rsp', arguments={})
        self.channel_mgr_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_mgr_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxymgr_rsp', no_ack=True, exclusive=False, consumer_tag='mgr_rsp', arguments={})

        self.channel_query_rsp = connection_rsp.channel()
        self.channel_dict['query_rsp'] = self.channel_query_rsp
        self.channel_query_rsp.queue_declare(queue='busproxyquery_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_query_rsp.queue_bind(queue='busproxyquery_rsp', exchange='entry', routing_key='query_rsp', arguments={})
        self.channel_query_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_query_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxyquery_rsp', no_ack=True, exclusive=False, consumer_tag='query_rsp', arguments={})

        self.channel_order_rsp = connection_rsp.channel()
        self.channel_dict['order_rsp'] = self.channel_order_rsp
        self.channel_order_rsp.queue_declare(queue='busproxyorder_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_order_rsp.queue_bind(queue='busproxyorder_rsp', exchange='entry', routing_key='order_rsp', arguments={})
        self.channel_order_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_order_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxyorder_rsp', no_ack=True, exclusive=False, consumer_tag='order_rsp', arguments={})

        self.channel_bank_rsp = connection_rsp.channel()
        self.channel_dict['bank_rsp'] = self.channel_bank_rsp
        self.channel_bank_rsp.queue_declare(queue='busproxybank_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_bank_rsp.queue_bind(queue='busproxybank_rsp', exchange='entry', routing_key='bank_rsp', arguments={})
        self.channel_bank_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_bank_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxybank_rsp', no_ack=True, exclusive=False, consumer_tag='bank_rsp', arguments={})

        self.channel_cash_rsp = connection_rsp.channel()
        self.channel_dict['cash_rsp'] = self.channel_cash_rsp
        self.channel_cash_rsp.queue_declare(queue='busproxycash_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_cash_rsp.queue_bind(queue='busproxycash_rsp', exchange='entry', routing_key='cash_rsp', arguments={})
        self.channel_cash_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_cash_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxycash_rsp', no_ack=True, exclusive=False, consumer_tag='cash_rsp', arguments={})

        self.channel_notify_rsp = connection_rsp.channel()
        self.channel_dict['notify_rsp'] = self.channel_notify_rsp
        self.channel_notify_rsp.queue_declare(queue='busproxynotify_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_notify_rsp.queue_bind(queue='busproxynotify_rsp', exchange='entry', routing_key='notify_rsp', arguments={})
        self.channel_notify_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_notify_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxynotify_rsp', no_ack=True, exclusive=False, consumer_tag='notify_rsp', arguments={})

        self.channel_moneymodify_rsp = connection_rsp.channel()
        self.channel_dict['moneymodify_rsp'] = self.channel_moneymodify_rsp
        self.channel_moneymodify_rsp.queue_declare(queue='busproxymoneymodify_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_moneymodify_rsp.queue_bind(queue='busproxymoneymodify_rsp', exchange='entry', routing_key='moneymodify_rsp', arguments={})
        self.channel_moneymodify_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_moneymodify_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxymoneymodify_rsp', no_ack=True, exclusive=False, consumer_tag='moneymodify_rsp', arguments={})

        self.channel_bank_query_rsp = connection_rsp.channel()
        self.channel_dict['bank_query_rsp'] = self.channel_bank_query_rsp
        self.channel_bank_query_rsp.queue_declare(queue='busproxybank_query_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_bank_query_rsp.queue_bind(queue='busproxybank_query_rsp', exchange='entry', routing_key='bank_query_rsp', arguments={})
        self.channel_bank_query_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_bank_query_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxybank_query_rsp', no_ack=True, exclusive=False, consumer_tag='bank_query_rsp', arguments={})

        self.channel_bank_mgr_rsp = connection_rsp.channel()
        self.channel_dict['bank_mgr_rsp'] = self.channel_bank_mgr_rsp
        self.channel_bank_mgr_rsp.queue_declare(queue='busproxybank_mgr_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_bank_mgr_rsp.queue_bind(queue='busproxybank_mgr_rsp', exchange='entry', routing_key='bank_mgr_rsp', arguments={})
        self.channel_bank_mgr_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_bank_mgr_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxybank_mgr_rsp', no_ack=True, exclusive=False, consumer_tag='bank_mgr_rsp', arguments={})

        self.channel_report_rsp = connection_rsp.channel()
        self.channel_dict['report_rsp'] = self.channel_report_rsp
        self.channel_report_rsp.queue_declare(queue='busproxyreport_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_report_rsp.queue_bind(queue='busproxyreport_rsp', exchange='entry', routing_key='report_rsp', arguments={})
        self.channel_report_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_report_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxyreport_rsp', no_ack=True, exclusive=False, consumer_tag='report_rsp', arguments={})

        self.channel_newsfeed_rsp = connection_rsp.channel()
        self.channel_dict['newsfeed_rsp'] = self.channel_newsfeed_rsp
        self.channel_newsfeed_rsp.queue_declare(queue='busproxynewsfeed_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_newsfeed_rsp.queue_bind(queue='busproxynewsfeed_rsp', exchange='entry', routing_key='newsfeed_rsp', arguments={})
        self.channel_newsfeed_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_newsfeed_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxynewsfeed_rsp', no_ack=True, exclusive=False, consumer_tag='newsfeed_rsp', arguments={})

        self.channel_log_rsp = connection_rsp.channel()
        self.channel_dict['log_rsp'] = self.channel_log_rsp
        self.channel_log_rsp.queue_declare(queue='busproxylog_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_log_rsp.queue_bind(queue='busproxylog_rsp', exchange='entry', routing_key='log_rsp', arguments={})
        self.channel_log_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_log_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxylog_rsp', no_ack=True, exclusive=False, consumer_tag='log_rsp', arguments={})

        self.channel_rt_monitor_publish1 = connection_rsp.channel()
        self.channel_dict['rt_monitor_publish1'] = self.channel_rt_monitor_publish1
        self.channel_rt_monitor_publish1.queue_declare(queue='busproxyrt_monitor_publish1', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_rt_monitor_publish1.queue_bind(queue='busproxyrt_monitor_publish1', exchange='entry', routing_key='rt_monitor_publish', arguments={})
        self.channel_rt_monitor_publish1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_rt_monitor_publish1.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxyrt_monitor_publish1', no_ack=True, exclusive=False, consumer_tag='rt_monitor_publish', arguments={})

        self.channel_risk_rsp = connection_rsp.channel()
        self.channel_dict['risk_rsp'] = self.channel_risk_rsp
        self.channel_risk_rsp.queue_declare(queue='busproxyrisk_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_risk_rsp.queue_bind(queue='busproxyrisk_rsp', exchange='entry', routing_key='risk_rsp', arguments={})
        self.channel_risk_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_risk_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxyrisk_rsp', no_ack=True, exclusive=False, consumer_tag='risk_rsp', arguments={})

        self.channel_wetas_rsp = connection_rsp.channel()
        self.channel_dict['wetas_rsp'] = self.channel_wetas_rsp
        self.channel_wetas_rsp.queue_declare(queue='busproxywetas_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_wetas_rsp.queue_bind(queue='busproxywetas_rsp', exchange='entry', routing_key='wetas_rsp', arguments={})
        self.channel_wetas_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_wetas_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxywetas_rsp', no_ack=True, exclusive=False, consumer_tag='wetas_rsp', arguments={})

        self.channel_ex_qkernel_rsp = connection_rsp.channel()
        self.channel_dict['ex_qkernel_rsp'] = self.channel_ex_qkernel_rsp
        self.channel_ex_qkernel_rsp.queue_declare(queue='busproxyex_qkernel_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_ex_qkernel_rsp.queue_bind(queue='busproxyex_qkernel_rsp', exchange='entry', routing_key='ex_qkernel_rsp', arguments={})
        self.channel_ex_qkernel_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_ex_qkernel_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxyex_qkernel_rsp', no_ack=True, exclusive=False, consumer_tag='ex_qkernel_rsp', arguments={})

        self.channel_ex_report_rsp = connection_rsp.channel()
        self.channel_dict['ex_report_rsp'] = self.channel_ex_report_rsp
        self.channel_ex_report_rsp.queue_declare(queue='busproxyex_report_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_ex_report_rsp.queue_bind(queue='busproxyex_report_rsp', exchange='entry', routing_key='ex_report_rsp', arguments={})
        self.channel_ex_report_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_ex_report_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxyex_report_rsp', no_ack=True, exclusive=False, consumer_tag='ex_report_rsp', arguments={})

        self.channel_delivery2_rsp = connection_rsp.channel()
        self.channel_dict['delivery2_rsp'] = self.channel_delivery2_rsp
        self.channel_delivery2_rsp.queue_declare(queue='busproxydelivery2_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_delivery2_rsp.queue_bind(queue='busproxydelivery2_rsp', exchange='entry', routing_key='delivery2_rsp', arguments={})
        self.channel_delivery2_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_delivery2_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxydelivery2_rsp', no_ack=True, exclusive=False, consumer_tag='delivery2_rsp', arguments={})

        self.channel_settle_rsp = connection_rsp.channel()
        self.channel_dict['settle_rsp'] = self.channel_settle_rsp
        self.channel_settle_rsp.queue_declare(queue='busproxysettle_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_settle_rsp.queue_bind(queue='busproxysettle_rsp', exchange='entry', routing_key='settle_rsp', arguments={})
        self.channel_settle_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_settle_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxysettle_rsp', no_ack=True, exclusive=False, consumer_tag='settle_rsp', arguments={})

        self.channel_finance_rsp = connection_rsp.channel()
        self.channel_dict['finance_rsp'] = self.channel_finance_rsp
        self.channel_finance_rsp.queue_declare(queue='busproxyfinance_rsp', passive=False, durable=False, exclusive=False, auto_delete=False, arguments={})
        self.channel_finance_rsp.queue_bind(queue='busproxyfinance_rsp', exchange='entry', routing_key='finance_rsp', arguments={})
        self.channel_finance_rsp.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.channel_finance_rsp.basic_consume(consumer_callback=connection_rsp.callback, queue='busproxyfinance_rsp', no_ack=True, exclusive=False, consumer_tag='finance_rsp', arguments={})

        return self.connection_req, self.connection_rsp, self.connection_heartbeat

    def close(self):
        self.connection_0.close()
        self.connection_1.close()
        self.connection_rsp.close()

    def get_channel(self, channel_name):
        return self.channel_dict[channel_name]

# 0.861000 seconds spent