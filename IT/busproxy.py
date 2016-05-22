#coding=utf8
import pika
from nose.tools import *
import BusproxyTas1_pb2, RealtimeMonitorTas1_pb2, UserTas1_pb2
import msgbus

class BusProxy(object):
    def __init__(self, m_ip, m_port, vhost, username, password):
        self.conn_heartbeat = msgbus.Connection('self.conn_heartbeat', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
        self.chan_heartbeat = self.conn_heartbeat.channel()
        self.chan_heartbeat.confirm_delivery()

        self.conn_publish = msgbus.Connection('self.conn_publish', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
        self.chan_publish = self.conn_publish.channel()
        self.chan_publish.confirm_delivery()

        self.conn_consume = msgbus.Connection('self.conn_consume', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
        
        self.chan_user_rsp1 = self.conn_consume.channel()
        self.chan_user_rsp1.confirm_delivery()
        self.chan_user_rsp1.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False)
        self.chan_user_rsp1.queue_declare(queue='busproxyuser_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_user_rsp1.queue_bind(queue='busproxyuser_rsp1', exchange='entry', routing_key='user_rsp')
        self.chan_user_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_user_rsp1, 'busproxyuser_rsp1', 'user_rsp')
        
        self.chan_mgr_rsp1 = self.conn_consume.channel()
        self.chan_mgr_rsp1.queue_declare(queue='busproxymgr_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_mgr_rsp1.queue_bind(queue='busproxymgr_rsp1', exchange='entry', routing_key='mgr_rsp')
        self.chan_mgr_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_mgr_rsp1, 'busproxymgr_rsp1', 'mgr_rsp')
        
        self.chan_query_rsp1 = self.conn_consume.channel()
        self.chan_query_rsp1.queue_declare(queue='busproxyquery_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_query_rsp1.queue_bind(queue='busproxyquery_rsp1', exchange='entry', routing_key='query_rsp')
        self.chan_query_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_query_rsp1, 'busproxyquery_rsp1', 'query_rsp')
        
        self.chan_order_rsp1 = self.conn_consume.channel()
        self.chan_order_rsp1.queue_declare(queue='busproxyorder_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_order_rsp1.queue_bind(queue='busproxyorder_rsp1', exchange='entry', routing_key='order_rsp')
        self.chan_order_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_query_rsp1, 'busproxyorder_rsp1', 'order_rsp')
        
        self.chan_bank_rsp1 = self.conn_consume.channel()
        self.chan_bank_rsp1.queue_declare(queue='busproxybank_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_bank_rsp1.queue_bind(queue='busproxybank_rsp1', exchange='entry', routing_key='bank_rsp')
        self.chan_bank_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_bank_rsp1, 'busproxybank_rsp1', 'bank_rsp')
        
        self.chan_cash_rsp1 = self.conn_consume.channel()
        self.chan_cash_rsp1.queue_declare(queue='busproxycash_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_cash_rsp1.queue_bind(queue='busproxycash_rsp1', exchange='entry', routing_key='cash_rsp')
        self.chan_cash_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_bank_rsp1, 'busproxycash_rsp1', 'cash_rsp')
        
        self.chan_notify_rsp1 = self.conn_consume.channel()
        self.chan_notify_rsp1.queue_declare(queue='busproxynotify_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_notify_rsp1.queue_bind(queue='busproxynotify_rsp1', exchange='entry', routing_key='notify_rsp')
        self.chan_notify_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_notify_rsp1, 'busproxynotify_rsp1', 'notify_rsp')
        
        self.chan_moneymodify_rsp1 = self.conn_consume.channel()
        self.chan_moneymodify_rsp1.queue_declare(queue='busproxymoneymodify_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_moneymodify_rsp1.queue_bind(queue='busproxymoneymodify_rsp1', exchange='entry', routing_key='moneymodify_rsp')
        self.chan_moneymodify_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_moneymodify_rsp1, 'busproxymoneymodify_rsp1',  'moneymodify_rsp')
        
        self.chan_bank_query_rsp1 = self.conn_consume.channel()
        self.chan_bank_query_rsp1.queue_declare(queue='busproxybank_query_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_bank_query_rsp1.queue_bind(queue='busproxybank_query_rsp1', exchange='entry', routing_key='bank_query_rsp')
        self.chan_bank_query_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_bank_query_rsp1, 'busproxybank_query_rsp1', 'bank_query_rsp')
        
        self.chan_bank_mgr_rsp1 = self.conn_consume.channel()
        self.chan_bank_mgr_rsp1.queue_declare(queue='busproxybank_mgr_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_bank_mgr_rsp1.queue_bind(queue='busproxybank_mgr_rsp1', exchange='entry', routing_key='bank_mgr_rsp')
        self.chan_bank_mgr_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_bank_mgr_rsp1, 'busproxybank_mgr_rsp1', 'bank_mgr_rsp')
        
        self.chan_report_rsp1 = self.conn_consume.channel()
        self.chan_report_rsp1.queue_declare(queue='busproxyreport_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_report_rsp1.queue_bind(queue='busproxyreport_rsp1', exchange='entry', routing_key='report_rsp')
        self.chan_report_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_report_rsp1, 'busproxyreport_rsp1', 'report_rsp')
        
        self.chan_newsfeed_rsp1 = self.conn_consume.channel()
        self.chan_newsfeed_rsp1.queue_declare(queue='busproxynewsfeed_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_newsfeed_rsp1.queue_bind(queue='busproxynewsfeed_rsp1', exchange='entry', routing_key='newsfeed_rsp')
        self.chan_newsfeed_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_newsfeed_rsp1, 'busproxynewsfeed_rsp1', 'newsfeed_rsp')
        
        self.chan_log_rsp1 = self.conn_consume.channel()
        self.chan_log_rsp1.queue_declare(queue='busproxylog_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_log_rsp1.queue_bind(queue='busproxylog_rsp1', exchange='entry', routing_key='log_rsp')
        self.chan_log_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_log_rsp1, 'busproxylog_rsp1', 'log_rsp')
        
        self.chan_rt_monitor_publish1 = self.conn_consume.channel()
        self.chan_rt_monitor_publish1.queue_declare(queue='busproxyrt_monitor_publish1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_rt_monitor_publish1.queue_bind(queue='busproxyrt_monitor_publish1', exchange='entry', routing_key='rt_monitor_publish')
        self.chan_rt_monitor_publish1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_rt_monitor_publish1, 'busproxyrt_monitor_publish1', 'rt_monitor_publish')
        
        self.chan_risk_rsp1 = self.conn_consume.channel()
        self.chan_risk_rsp1.queue_declare(queue='busproxyrisk_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_risk_rsp1.queue_bind(queue='busproxyrisk_rsp1', exchange='entry', routing_key='risk_rsp')
        self.chan_risk_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_risk_rsp1, 'busproxyrisk_rsp1', 'risk_rsp')
        
        self.chan_wetas_rsp1 = self.conn_consume.channel()
        self.chan_wetas_rsp1.queue_declare(queue='busproxywetas_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_wetas_rsp1.queue_bind(queue='busproxywetas_rsp1', exchange='entry', routing_key='wetas_rsp')
        self.chan_wetas_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_wetas_rsp1, 'busproxywetas_rsp1', 'wetas_rsp')
        
        self.chan_ex_qkernel_rsp1 = self.conn_consume.channel()
        self.chan_ex_qkernel_rsp1.queue_declare(queue='busproxyex_qkernel_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_ex_qkernel_rsp1.queue_bind(queue='busproxyex_qkernel_rsp1', exchange='entry', routing_key='ex_qkernel_rsp')
        self.chan_ex_qkernel_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_ex_qkernel_rsp1, 'busproxyex_qkernel_rsp1', 'ex_qkernel_rsp')
        
        self.chan_ex_report_rsp1 = self.conn_consume.channel()
        self.chan_ex_report_rsp1.queue_declare(queue='busproxyex_report_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_ex_report_rsp1.queue_bind(queue='busproxyex_report_rsp1', exchange='entry', routing_key='ex_report_rsp')
        self.chan_ex_report_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_ex_report_rsp1, 'busproxyex_report_rsp1', 'ex_report_rsp')

        self.chan_delivery2_rsp1 = self.conn_consume.channel()
        self.chan_delivery2_rsp1.queue_declare(queue='busproxydelivery2_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_delivery2_rsp1.queue_bind(queue='busproxydelivery2_rsp1', exchange='entry', routing_key='delivery2_rsp')
        self.chan_delivery2_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_ex_report_rsp1, 'busproxydelivery2_rsp1', 'delivery2_rsp')
        
        self.chan_settle_rsp1 = self.conn_consume.channel()
        self.chan_settle_rsp1.queue_declare(queue='busproxysettle_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_settle_rsp1.queue_bind(queue='busproxysettle_rsp1', exchange='entry', routing_key='settle_rsp')
        self.chan_settle_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_settle_rsp1, 'busproxysettle_rsp1', 'settle_rsp')
        
        self.chan_finance_rsp1 = self.conn_consume.channel()
        self.chan_finance_rsp1.queue_declare(queue='busproxyfinance_rsp1', passive=False, durable=False, exclusive=False, auto_delete=False)
        self.chan_finance_rsp1.queue_bind(queue='busproxyfinance_rsp1', exchange='entry', routing_key='finance_rsp')
        self.chan_finance_rsp1.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.conn_consume.basic_consume(self.chan_settle_rsp1, 'busproxyfinance_rsp1', 'finance_rsp')
        #self.chan_heartbeat.basic_publish('entry', 'heartbeat', 'heartbeat')
        
        """
        protobuf_data = UserTas1_pb2.P2LStatusSync()
        protobuf_data.Header.FunCode = 131632
        protobuf_data.ProxyID = 1
        protobuf_data.SessinIDStart = 268435456
        protobuf_data.SessinIDEnd = 536870911
        app_msg = msgbus.encode(131632, 0, protobuf_data)
        self.chan_publish.basic_publish('entry', 'user_req', app_msg)"""
    
        """
        exp_data = BusproxyTas1_pb2.L2PStatusSync()
        exp_data.Header.FunCode = 66097
        exp_data.Nop = 0
        #def expect(self, chan, exp_method, exp_session_id, exp_protobuf_data, timeout):
        chan = self.conn_consume.get_channel(1)
        self.conn_consume.expect(chan, 'Deliver', 1, exp_data, 3.0)"""
        
        #self.chan_heartbeat.basic_publish('entry', 'heartbeat', 'heartbeat')
    
    def close():
        self.conn_heartbeat.close()
        self.conn_publish.close()
        self.conn_consume.close()
