#coding=utf8
import threading
import pika
from nose.tools import *
import msgbus

class Bank(object):
    def __init__(self, m_ip, m_port, vhost, username, password):
        self.conn_heartbeat = msgbus.Connection('conn_heartbeat', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
        self.chan_heartbeat = self.conn_heartbeat.channel()
        self.chan_heartbeat.confirm_delivery()

        self.conn_1 = msgbus.Connection('conn_1', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
        self.conn1_chan1 = self.conn_1.channel()
        self.conn1_chan1.confirm_delivery()

        self.conn_main = msgbus.Connection('conn_main', '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')

        self.chan_bank_req_2 = self.conn_main.channel()
        self.chan_bank_req_2.confirm_delivery()
        self.chan_bank_req_2.exchange_declare(exchange='entry', exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, arguments={})
        self.chan_bank_req_2.queue_declare(queue='bankbank_req_2', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})
        self.chan_bank_req_2.queue_bind(queue='bankbank_req_2', exchange='entry', routing_key='bank_req_2', arguments={})
        self.chan_bank_req_2.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        self.chan_bank_req_2.basic_consume(consumer_callback=self.conn_main.callback, queue='bankbank_req_2', no_ack=False, exclusive=False, consumer_tag='bank_req_2', arguments={})
        #thr = threading.Thread(target=self.consume_thread_func, args=(self.chan_bank_req_2,))
        #thr.start()
        #print 'thr.start'
        #self.conn_main.start_consuming(self.chan_bank_req_2, queue='bankbank_req_2', no_ack=False, exclusive=False, consumer_tag='bank_req_2', arguments={})

        self.chan_bankioproxy_rsp_2 = self.conn_main.channel()
        self.chan_bankioproxy_rsp_2.queue_declare(queue='bankbankioproxy_rsp_2', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})
        self.chan_bankioproxy_rsp_2.queue_bind(queue='bankbankioproxy_rsp_2', exchange='entry', routing_key='bankioproxy_rsp_2', arguments={})
        self.chan_bankioproxy_rsp_2.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        #self.chan_bankioproxy_rsp_2.basic_consume(consumer_callback=self.conn_main.callback, queue='bankbankioproxy_rsp_2', no_ack=False, exclusive=False, consumer_tag='bankioproxy_rsp_2', arguments={})
        #thr = threading.Thread(target=self.consume_thread_func, args=(self.chan_bankioproxy_rsp_2,))
        #thr.start()
        #print 'thr.start'
        #self.conn_main.start_consuming(self.chan_bankioproxy_rsp_2, queue='bankbankioproxy_rsp_2', no_ack=False, exclusive=False, consumer_tag='bankioproxy_rsp_2', arguments={})

        self.chan_bankinner_2 = self.conn_main.channel()
        self.chan_bankinner_2.queue_declare(queue='bankbankinner_2', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})
        self.chan_bankinner_2.queue_bind(queue='bankbankinner_2', exchange='entry', routing_key='bankinner_2', arguments={})
        self.chan_bankinner_2.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        #self.chan_bankinner_2.basic_consume(consumer_callback=self.conn_main.callback, queue='bankbankinner_2', no_ack=False, exclusive=False, consumer_tag='bankinner_2', arguments={})
        #thr = threading.Thread(target=self.consume_thread_func, args=(self.chan_bankinner_2,))
        #thr.start()
        #print 'thr.start'
        #self.conn_main.start_consuming(self.chan_bankinner_2, queue='bankbankinner_2', no_ack=False, exclusive=False, consumer_tag='bankinner_2', arguments={})

        self.chan_bankcommunicate_req_2 = self.conn_main.channel()
        self.chan_bankcommunicate_req_2.queue_declare(queue='bankbankcommunicate_req_2', passive=False, durable=True, exclusive=False, auto_delete=False, arguments={})
        self.chan_bankcommunicate_req_2.queue_bind(queue='bankbankcommunicate_req_2', exchange='entry', routing_key='bankcommunicate_req_2', arguments={})
        self.chan_bankcommunicate_req_2.basic_qos(prefetch_size=0, prefetch_count=5000, all_channels=False)
        #self.chan_bankcommunicate_req_2.basic_consume(consumer_callback=self.conn_main.callback, queue='bankbankcommunicate_req_2', no_ack=False, exclusive=False, consumer_tag='bankcommunicate_req_2', arguments={})
        #thr = threading.Thread(target=self.consume_thread_func, args=(self.chan_bankcommunicate_req_2,))
        #thr.start()
        #print 'thr.start'
        #self.conn_main.start_consuming(self.chan_bankcommunicate_req_2, queue='bankbankcommunicate_req_2', no_ack=False, exclusive=False, consumer_tag='bankcommunicate_req_2', arguments={})

    def close(self):
        self.chan_bank_req_2.stop_consuming()
        self.chan_bankioproxy_rsp_2.stop_consuming()
        self.chan_bankinner_2.stop_consuming()
        self.chan_bankcommunicate_req_2.stop_consuming()
                
        self.conn_heartbeat.close()
        self.conn_1.close()
        self.conn_main.close()

            