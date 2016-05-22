import pika
from nose.tools import *
import TkernelTas1_pb2, common_pb2, PublicTas1_pb2
import msgbus

msgbus.set_pika_logger_level('WARNING')

def setup():
    global conn, order_rsp_chan
    conn = msgbus.Connection('192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
    order_rsp_chan = conn.create_consume_queue('entry', 'testorder_rsp1', routing_key='order_rsp')

def teardown():
    msgbus.close_all()

def test_new_order_match_sucess():
    session_id = 11
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
    conn.publish('entry', 'order_req', 196833, session_id, req_data)

    ret = conn.expect(order_rsp_chan, 196834, session_id)
    print ret['data']
    eq_(0, ret['data'].RetCode)

def test_new_order_queued():
    assert False
