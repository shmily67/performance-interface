#from multiprocessing import Process, Queue, Value
import logging
from nose.tools import *
import pika
import TkernelTas1_pb2, common_pb2, PublicTas1_pb2, MoneyManagerTas1_pb2
import msgbus, msgbus_perf, protobuf_dict

msgbus.set_pika_logger_level('WARNING')

def money_req_mock_func(session_id, req_data): # money_req is routing_key
    if isinstance(req_data, MoneyManagerTas1_pb2.GetUsableMoneyReq):
        rsp_data = TkernelTas1_pb2.EntrustOrderRsp()
        rsp_msg = msgbus.encode(-1, session_id, rsp_data)
        return 'entry', 'money_rsp', rsp_msg
    else:
        assert False, req_data

def heartbeat_mock_func(session_id, data):
    #print 'heartbeat_mock_func() called'
    eq_('heartbeat', data)
    return None

def gen_default_entrust_order_req_data():
    req_data = TkernelTas1_pb2.EntrustOrderReq(
        Header = common_pb2.MessageHead(
            FunCode = 196833,
            RequestID = 1,
            AccountCode = u"001001",
            Ip = u"192.168.31.21",
        ),
        SecEntrustID = 5370471543427234882,
        AccountCode = u"001001",
        EntrustPrice = 40.200000,
        MemberCode = u"518",
        GoodsCode = u"100100",
        BuyOrSell = 0,
        OrderType = 100,
        EntrustQty = 10.000000,
        AllowTradeSub = 10.000000,
        ValidType = 0,
        OperatorCode = u"000018000000065",
        MarketID = 0,
        AccountType = 0,
        CurtQuotePrice = 40.200000,
        OrderMode = -1,
        CloseMode = -1,
        strategy = PublicTas1_pb2.Strategy(
            RetCode = 0,
            StrategyID = 0,
        ),
        Coupon = 0,
    )
    return req_data

def main():
    bus_ip, bus_port, vhost, username, password = '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest'
    codec = msgbus.Codec(protobuf_dict.data_class_dict)
    tester = msgbus_perf.Tester(codec, display_interval=2)
    #tester.add_mock('mock_money_req', bus_ip, bus_port, vhost, username, password, 'entry',
    #                'testmoney_req1', 'money_req', False,
    #                'money_rsp', money_req_mock_func)
    data_list = []
    i = 0
    while i < 10000:
        data = gen_default_entrust_order_req_data()
        data.Header.RequestID = i
        data_list.append(data)
        i += 1
    tester.add_driver('driver_order_req_1', bus_ip, bus_port, vhost, username, password, 'entry',
                      'order_req', data_list, 0.0,
                      'busproxyorder_rsp1', 'order_rsp', 1)
    try:
        tester.start_test()
    finally:
        msgbus_perf.clear_msgbus_queue(bus_ip, bus_port, vhost, username, password,
            'entry', 'logorder_req', 'order_req')
        msgbus_perf.clear_msgbus_queue(bus_ip, bus_port, vhost, username, password,
            'entry', 'logorder_rsp', 'order_rsp')
        msgbus_perf.clear_msgbus_queue(bus_ip, bus_port, vhost, username, password,
            'entry', 'heartbeat', 'heartbeat', durable=True)

if '__main__' == __name__:
    main()
