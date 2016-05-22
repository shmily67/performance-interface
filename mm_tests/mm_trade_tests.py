#coding=GB2312
import time, random
from nose.tools import *
import common_pb2, TkernelTas1_pb2
import msgbus_h as msgbus, protobuf, funcode

#testing object: server_order + server_money + server_match

bus_ip, bus_port, vhost, username, password = '192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest'
local_ip = u'192.168.31.21'

class OrderIDGenerator(object):
    def __init__(self, server_id, start=0):
        self.server_id = server_id
        self.timestamp = int(time.time()*1000)
        self.i = start-1
        
    def gen(self, t): # t = time.time()
        if int(t*1000) == self.timestamp:
            self.i += 1
        else:
            self.timestamp = int(time.time()*1000)
            self.i = 0
        #              56bits              5bits               3bits
        ret_val = (self.timestamp<<8) + (self.server_id<<3) + self.i
        return ret_val

class RequestIDGenerator(object): #�ͻ��˵���ˮID����ȱʡ��0��ʼ������
    def __init__(self, start=0):
        self.i = start-1
    def gen(self):
        self.i += 1
        return self.i

def gen_client_order_time(tt): # t = time.time() reslut: 2016-01-12 10:10:10
    t = time.localtime(tt)
    return '%04d-%02d-%02d %02d:%02d:%02d'%(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

def setup():
    global conn, order_rsp_chan, money_req_chan, sess_id, server_id
    global order_generator, request_id_generator
    conn = msgbus.Connection(bus_ip, bus_port, vhost, username, password, funcode.funcode_dict)
    conn.bind_queue('entry', 'testorder_rsp', routing_key='order_rsp')
    sess_id = 101
    server_id = 100100
    order_id = (int(time.time())<<32) + (server_id<<16)
    order_generator = OrderIDGenerator(1) #server_id=1
    request_id_generator = RequestIDGenerator()

def teardown():
    msgbus.close_all()

def before_test():
    conn.clear_queue_before_tests('testorder_rsp')

@with_setup(before_test, None)
def test_market_price_open_buy_and_match_sucess():
    t = time.time()
    request_id = request_id_generator.gen()
    header = common_pb2.MessageHead(
        FunCode = 196809,           # ���ܺ�
	    RequestID = request_id,     # �ͻ��˵���ˮID
	    AccountId = 3,              # �˺�ID
	    AccessId = 0,               # ����������ͻ��˵Ľ���ID
	    ClientTime = int(t*1000)    # ��Ϣ����ʱ�� ʱ��� ����
        )
    req_data = TkernelTas1_pb2.MMOrderReq(
        Header = header,   
	    OrderHead = TkernelTas1_pb2.OrderHead( # OrderHead ί����Ϣͷ
	        #Header = header, # MessageHead �ظ����������ﲻ��Ҫ��
	        #int32 RetCode = 2, # int32 ������
	        OrderID = order_generator.gen(t), #optional int64 OrderID = 3, # int64 ί�е���
	        ClientSerialNo = str(request_id), #optional string = 4, # string �ͻ�����ˮ��
	        ClientOrderTime = gen_client_order_time(t), #optional string 5, # string �ͻ���ί��ʱ��
	        ClientFlag = 'PC Client',#optional string 6, # string �ն˱�ʾ, �ֻ���PC�˵�
	        AccountID = 7, #optional int32  # int32 �����˺�
	        #AccountStatus = 8,#optional int32  # int32 �˻�״̬
	        GoodsID = 9, #optional int32 # int32 ��ƷID
	        #optional int32 ValidType = 10, # int32 У������
	        #optional string ValidTime = 11, # string ��Ч����
	        OperateType = 0, #optional int32 # int32 ��������: ί��, ǿƽ������
	        #OperatorID = 1, #optional int32 # int32 ����Ա�˺�ID
	        AccountType = 1, #optional int32 # int32 �˻�����
	        OrderSrc = 15, #optional int32 # int32 ������Դ:���׶ˣ�����ˣ����
	        #optional string AttachParam = 16, # string ���Ӳ���(JSON�ַ���,Э�����,������ʱ�����ֶζ�)	        )
	        ),
	    MemberID = 3,       #optional int32 # int32 ������Ա
        OrderPrice = 10.0,  #optional double # double ί�м۸�
	    OrderQty = 10.0,    #optional double # double ί������
	    BuyOrSell = 0,      #optional int32 # int32 ��������
	    BuildType = 0101020101, #optional int32 # int32 �µ�����:���֣�ƽ��, dev_doc\����ҵ��\��������.docx
	    AllowTradeSub = 1.0,  #optional double # double ����ɽ�ƫ�Χ
	    #optional int32 SpecialAccount = 9, # int32 �ر��Ա�˺�ID
	    #optional double BuyOrSellPtSub = 10, # double �������
	    #optional double SpPrice = 11, # double ֹӯ�۸�
	    #optional double SlPrice = 12, # double ֹ��۸�
	    #optional int32 MarketID = 13, # int32 �г�ID
	    #optional string StartTime = 14, # string ��ʼʱ��
	    #optional string EndTime = 15, # string ����ʱ��
	    #optional int32 ReOpenFlag = 16, # int32 ���ֽ��ֱ��
        )
    conn.publish('entry', 'order_req', 1, req_data)

    exp_rsp_data = TkernelTas1_pb2.MMOrderRsp( #����ί�е�Ӧ�� 0 3 202 -> 196810
        Header = header,
	    RetCode = 0, #optional int32 # int32 ������
	    #optional string RetDesc = 3, # string ������Ϣ
	    OrderID = 4, #optional int64 # int64 һ�����ɵĶ�����
	    OrderTime = gen_client_order_time(time.time()), #optional string 5, # ����ί�н��׵�ʱ��
	    OrderType = 0101020101, #optional int32  dev_doc\����ҵ��\��������.docx
	    OrderReq = req_data,#optional TkernelTas1.MMOrderReq OrderReq = 7
	    )
    #conn.expect2('testorder_rsp', 1, exp_rsp_data, 1.0)
    sess_id, rsp_data = conn.expect('testorder_rsp', TkernelTas1_pb2.MMOrderRsp, 1.0)    
    print rsp_data
    eq_(1, sess_id)
    eq_(0, rsp_data.RetCode)

    #proxy get order_dealed_notify from server_money
    sess_id, dealed_data = conn.expect('order_rsp', TkernelTas1_pb2.OrderDealedNtf, 1.0)
    print dealed_data
    eq_(1, sess_id)
    eq_(0, dealed_data.RetCode)

@with_setup(before_test, None)
def test_market_price_open_buy_and_inqueue(): #OrderType=0
    assert False

@with_setup(before_test, None)
def test_market_price_open_buy_and_revoke():#OrderType=0
    assert False

@with_setup(before_test, None)
def test_market_price_open_sell_and_match_sucess():#OrderType=0
    #send req

    with assert_raises(msgbus.Timeout): # No order_dealed_notify arrivied
        conn.recv(3.0)
    assert False

@with_setup(before_test, None)
def test_market_price_open_sell_and_inqueue():#OrderType=0
    assert False

@with_setup(before_test, None)
def test_market_price_open_sell_and_revoke():#OrderType=0
    assert False

@with_setup(before_test, None)
def test_open_position_sell_at_market_price_revoke():#OrderType=0
    assert False

@with_setup(before_test, None)
def test_open_position_buy_at_limit_price_sucess():#OrderType=1
    assert False

@with_setup(before_test, None)
def test_open_position_sell_at_limit_price_sucess():#OrderType=1
    assert False

@with_setup(before_test, None)
def test_open_position_buy_at_limit_price_queued():#OrderType=1
    assert False

@with_setup(before_test, None)
def test_open_position_sell_at_limit_price_queued():#OrderType=1
    assert False

@with_setup(before_test, None)
def test_open_position_buy_at_limit_price_revoke():#OrderType=1
    assert False

@with_setup(before_test, None)
def test_open_position_sell_at_limit_price_revoke():#OrderType=1
    assert False

@with_setup(before_test, None)
def test_close_position_buy_at_market_price_sucess():#OrderType=2
    assert False

@with_setup(before_test, None)
def test_close_position_sell_at_market_price_sucess():#OrderType=2
    assert False

@with_setup(before_test, None)
def test_close_position_buy_at_market_price_queued():#OrderType=2
    assert False

@with_setup(before_test, None)
def test_close_position_sell_at_market_price_queued():#OrderType=2
    assert False

@with_setup(before_test, None)
def test_close_position_buy_at_market_price_revoke():#OrderType=2
    assert False

@with_setup(before_test, None)
def test_close_position_sell_at_market_price_revoke():#OrderType=2
    assert False

@with_setup(before_test, None)
def test_close_position_buy_at_limit_price_sucess():#OrderType=3
    assert False

@with_setup(before_test, None)
def test_close_position_sell_at_limit_price_sucess():#OrderType=3
    assert False

@with_setup(before_test, None)
def test_close_position_buy_at_limit_price_queued():#OrderType=3
    assert False

@with_setup(before_test, None)
def test_close_position_sell_at_limit_price_queued():#OrderType=3
    assert False

@with_setup(before_test, None)
def test_close_position_buy_at_limit_price_revoke():#OrderType=3
    assert False

@with_setup(before_test, None)
def test_close_position_sell_at_limit_price_revoke():#OrderType=3
    assert False


"""funcode
ί�з����󶳽��ʽ�1
ί�з����󶳽��ʽ𷵻�: 2

ί�з�����ⶳ�ʽ�: 3
ί�з�����ⶳ�ʽ𷵻�: 4

�ʽ�ռ������2007
�ʽ�ռ����Ӧ: 2009

�ʽ�ƽ������: 2008
�ʽ�ƽ����Ӧ: 2010"""

def test_MMOrderReq():# ����ί�е����� 0 3 201 -> funcode=196809
    t = time.time()
    header = common_pb2.MessageHead(
        FunCode = 196809,                       # ���ܺ�
	    RequestID = request_id_generator.gen(), # �ͻ��˵���ˮID
	    AccountId = 3,                          # �˺�ID
	    AccessId = 0,                           # ����������ͻ��˵Ľ���ID
	    ClientTime = int(t*1000)                #��Ϣ����ʱ�� ʱ��� ����
        )
    data = TkernelTas1_pb2.MMOrderReq(
        Header = header,
	    OrderHead = TkernelTas1_pb2.OrderHead( # OrderHead ί����Ϣͷ
	        Header = header, # MessageHead
	        #int32 RetCode = 2, # int32 ������
	        OrderID = order_generator.gen(t), #optional int64 OrderID = 3, # int64 ί�е���
	        ClientSerialNo = '1', #optional string = 4, # string �ͻ�����ˮ��
	        ClientOrderTime = gen_client_order_time(t), #optional string 5, # string �ͻ���ί��ʱ��
	        ClientFlag = 'PC Client',#optional string 6, # string �ն˱�ʾ, �ֻ���PC�˵�
	        AccountID = 7, #optional int32  # int32 �����˺�
	        #AccountStatus = 8,#optional int32  # int32 �˻�״̬
	        GoodsID = 9, #optional int32 # int32 ��ƷID
	        #optional int32 ValidType = 10, # int32 У������
	        #optional string ValidTime = 11, # string ��Ч����
	        OperateType = 1, #optional int32 # int32 ��������: ί��, ǿƽ������
	        #OperatorID = 1, #optional int32 # int32 ����Ա�˺�ID
	        AccountType = 1, #optional int32 # int32 �˻�����
	        OrderSrc = 15, #optional int32 # int32 ������Դ:���׶ˣ�����ˣ����
	        #optional string AttachParam = 16, # string ���Ӳ���(JSON�ַ���,Э�����,������ʱ�����ֶζ�)	        )
	        ),
	    MemberID = 3, #optional int32 # int32 ������Ա
        OrderPrice = 10.0, #optional double # double ί�м۸�
	    OrderQty = 5, #optional double # double ί������
	    BuyOrSell = 0, #optional int32 # int32 ��������
	    OpenType = 0, #optional int32 # int32 �µ�����:���֣�ƽ��,
	    AllowTradeSub = 8, #optional double # double ����ɽ�ƫ�Χ
	    #optional int32 SpecialAccount = 9, # int32 �ر��Ա�˺�ID
	    #optional double BuyOrSellPtSub = 10, # double �������
	    #optional double SpPrice = 11, # double ֹӯ�۸�
	    #optional double SlPrice = 12, # double ֹ��۸�
	    #optional int32 MarketID = 13, # int32 �г�ID
	    #optional string StartTime = 14, # string ��ʼʱ��
	    #optional string EndTime = 15, # string ����ʱ��
	    #optional int32 ReOpenFlag = 16, # int32 ���ֽ��ֱ��
        )
    s = data.SerializeToString()
    data2 = TkernelTas1_pb2.MMOrderReq()
    data2.ParseFromString(s)
    protobuf.assert_equal(data, data2)

def test_MMOrderRsp():
    t = time.time()
    header = common_pb2.MessageHead(
        FunCode = 196809,                       # ���ܺ�
	    RequestID = request_id_generator.gen(), # �ͻ��˵���ˮID
	    AccountId = 3,                          # �˺�ID
	    AccessId = 0,                           # ����������ͻ��˵Ľ���ID
	    ClientTime = int(t*1000)                #��Ϣ����ʱ�� ʱ��� ����
        )
    req_data = TkernelTas1_pb2.MMOrderReq(
        Header = header,
	    OrderHead = TkernelTas1_pb2.OrderHead( # OrderHead ί����Ϣͷ
	        Header = header, # MessageHead
	        #int32 RetCode = 2, # int32 ������
	        OrderID = order_generator.gen(t), #optional int64 OrderID = 3, # int64 ί�е���
	        ClientSerialNo = '1', #optional string = 4, # string �ͻ�����ˮ��
	        ClientOrderTime = gen_client_order_time(t), #optional string 5, # string �ͻ���ί��ʱ��
	        ClientFlag = 'PC Client',#optional string 6, # string �ն˱�ʾ, �ֻ���PC�˵�
	        AccountID = 7, #optional int32  # int32 �����˺�
	        #AccountStatus = 8,#optional int32  # int32 �˻�״̬
	        GoodsID = 9, #optional int32 # int32 ��ƷID
	        #optional int32 ValidType = 10, # int32 У������
	        #optional string ValidTime = 11, # string ��Ч����
	        OperateType = 1, #optional int32 # int32 ��������: ί��, ǿƽ������
	        #OperatorID = 1, #optional int32 # int32 ����Ա�˺�ID
	        AccountType = 1, #optional int32 # int32 �˻�����
	        OrderSrc = 15, #optional int32 # int32 ������Դ:���׶ˣ�����ˣ����
	        #optional string AttachParam = 16, # string ���Ӳ���(JSON�ַ���,Э�����,������ʱ�����ֶζ�)	        )
	        ),
	    MemberID = 3, #optional int32 # int32 ������Ա
        OrderPrice = 10.0, #optional double # double ί�м۸�
	    OrderQty = 5, #optional double # double ί������
	    BuyOrSell = 0, #optional int32 # int32 ��������
	    OpenType = 0, #optional int32 # int32 �µ�����:���֣�ƽ��,
	    AllowTradeSub = 8, #optional double # double ����ɽ�ƫ�Χ
	    #optional int32 SpecialAccount = 9, # int32 �ر��Ա�˺�ID
	    #optional double BuyOrSellPtSub = 10, # double �������
	    #optional double SpPrice = 11, # double ֹӯ�۸�
	    #optional double SlPrice = 12, # double ֹ��۸�
	    #optional int32 MarketID = 13, # int32 �г�ID
	    #optional string StartTime = 14, # string ��ʼʱ��
	    #optional string EndTime = 15, # string ����ʱ��
	    #optional int32 ReOpenFlag = 16, # int32 ���ֽ��ֱ��
        )
    data = TkernelTas1_pb2.MMOrderRsp( #����ί�е�Ӧ�� 0 3 202 -> 196810
        Header = common_pb2.MessageHead(
            FunCode = 196810,       # ���ܺ�
	        RequestID = int(t)+random.randint(0, 9999),   # �ͻ��˵���ˮID  ����һ������ֻҪ���ظ�����
	        AccountId = 3,          # �˺�ID
    	    AccessId = 4,           #����������ͻ��˵Ľ���ID
	        ClientTime = int(t*1000)   #��Ϣ����ʱ�� ʱ��� ��
            ),
	    RetCode = 0, #optional int32 # int32 ������
	    #optional string RetDesc = 3, # string ������Ϣ
	    OrderID = 4, #optional int64 # int64 һ�����ɵĶ�����
	    OrderTime = 'ssssss',#optional string 5, # string ����ί�н��׵�ʱ��
	    OrderType = 6, #optional int32 # int32 ��������
	    OrderReq = req_data,#optional TkernelTas1.MMOrderReq OrderReq = 7, # MMOrderReq ί���������
	    )
    s = data.SerializeToString()
    data2 = TkernelTas1_pb2.MMOrderRsp()
    data2.ParseFromString(s)
    print data2
    protobuf.assert_equal(data, data2)

def test_MMTradeProto():
    req_data = trade_pb2.MMTradeProto(
        Header = trade_pb2.TradeMessageHead(
            FunCode = 0,
            RequestID = 0,
            AccountID = 100101, # �������AccountID��ʲô��ϵ��
            ),
        OrderID = order_id,                     # ����   int64
        OrderType = 0101020101,          # �������� int64 ����/��/�м�/����/��֤��
        OperateID = 4,                   # ����ԱID int64
        AccountID = 5,                   # �ʽ��˻�ID int64
        GoodID = 7,                      # ��ƷID int32
        Qty = 1.0,                       # ���� double
        Price = 1.0,                     # �۸� double
        BuyOrSell = 0,                   # �������� int32
        )
    """CloseDetails = 11, # ƽ����ϸ repeated MMCloseDetail
    #optional   int64 OrderID = 1,                # (��ƽ)����
    #optional  double Qty = 2,                    # ƽ������
    #optional  double UserMargin = 3,             # �ͷ�ռ�ñ�֤��
    #optional  double ReleaseHoldAmount = 4,      # �ͷųֲֽ��
    #optional  double CloseCharge = 5,            # ƽ��������
    #optional  double WarehouseCharge = 6,        # �ֵ������
    #optional  double ClosePL = 7,                # ƽ��ӯ��"""
    req_data.CloseDetails.add(Qty=10.0)
    req_data.CloseDetails.add(Qty=10.0, UserMargin=10.0)
    s = req_data.SerializeToString()
    data2 = trade_pb2.MMTradeProto()
    data2.ParseFromString(s)
    protobuf.assert_equal(req_data, data2)

def test_msgbus_h_order_req():
    t = time.time()
    header = common_pb2.MessageHead(
        FunCode = 196809,                       # ���ܺ�
	    RequestID = request_id_generator.gen(), # �ͻ��˵���ˮID
	    AccountId = 3,                          # �˺�ID
	    AccessId = 0,                           # ����������ͻ��˵Ľ���ID
	    ClientTime = int(t*1000)                #��Ϣ����ʱ�� ʱ��� ����
        )
    data = TkernelTas1_pb2.MMOrderReq(
        Header = header,
	    OrderHead = TkernelTas1_pb2.OrderHead( # OrderHead ί����Ϣͷ
	        Header = header, # MessageHead
	        #int32 RetCode = 2, # int32 ������
	        OrderID = order_generator.gen(t), #optional int64 OrderID = 3, # int64 ί�е���
	        ClientSerialNo = '1', #optional string = 4, # string �ͻ�����ˮ��
	        ClientOrderTime = gen_client_order_time(t), #optional string 5, # string �ͻ���ί��ʱ��
	        ClientFlag = 'PC Client',#optional string 6, # string �ն˱�ʾ, �ֻ���PC�˵�
	        AccountID = 7, #optional int32  # int32 �����˺�
	        #AccountStatus = 8,#optional int32  # int32 �˻�״̬
	        GoodsID = 9, #optional int32 # int32 ��ƷID
	        #optional int32 ValidType = 10, # int32 У������
	        #optional string ValidTime = 11, # string ��Ч����
	        OperateType = 1, #optional int32 # int32 ��������: ί��, ǿƽ������
	        #OperatorID = 1, #optional int32 # int32 ����Ա�˺�ID
	        AccountType = 1, #optional int32 # int32 �˻�����
	        OrderSrc = 15, #optional int32 # int32 ������Դ:���׶ˣ�����ˣ����
	        #optional string AttachParam = 16, # string ���Ӳ���(JSON�ַ���,Э�����,������ʱ�����ֶζ�)	        )
	        ),
	    MemberID = 3, #optional int32 # int32 ������Ա
        OrderPrice = 10.0, #optional double # double ί�м۸�
	    OrderQty = 5, #optional double # double ί������
	    BuyOrSell = 0, #optional int32 # int32 ��������
	    OpenType = 0, #optional int32 # int32 �µ�����:���֣�ƽ��,
	    AllowTradeSub = 8, #optional double # double ����ɽ�ƫ�Χ
	    #optional int32 SpecialAccount = 9, # int32 �ر��Ա�˺�ID
	    #optional double BuyOrSellPtSub = 10, # double �������
	    #optional double SpPrice = 11, # double ֹӯ�۸�
	    #optional double SlPrice = 12, # double ֹ��۸�
	    #optional int32 MarketID = 13, # int32 �г�ID
	    #optional string StartTime = 14, # string ��ʼʱ��
	    #optional string EndTime = 15, # string ����ʱ��
	    #optional int32 ReOpenFlag = 16, # int32 ���ֽ��ֱ��
        )
    conn.publish('entry', 'order_req', 1, data)
    conn.expect2('testorder_req', data, 1.0)

def test_msgbus_h_order_rsp():
    t = time.time()
    request_id = request_id_generator.gen()
    order_id = order_generator.gen(t)
    header = common_pb2.MessageHead(
        FunCode = 196809,                       # ���ܺ�
	    RequestID = request_id, # �ͻ��˵���ˮID
	    AccountId = 3,                          # �˺�ID
	    AccessId = 0,                           # ����������ͻ��˵Ľ���ID
	    ClientTime = int(t*1000)                #��Ϣ����ʱ�� ʱ��� ����
        )
    req_data = TkernelTas1_pb2.MMOrderReq(
        Header = header,
	    OrderHead = TkernelTas1_pb2.OrderHead( # OrderHead ί����Ϣͷ
	        Header = header, # MessageHead
	        #int32 RetCode = 2, # int32 ������
	        OrderID = order_id, #optional int64 OrderID = 3, # int64 ί�е���
	        ClientSerialNo = str(request_id), #optional string = 4, # string �ͻ�����ˮ��
	        ClientOrderTime = gen_client_order_time(t), #optional string 5, # string �ͻ���ί��ʱ��
	        ClientFlag = 'PC Client',#optional string 6, # string �ն˱�ʾ, �ֻ���PC�˵�
	        AccountID = 7, #optional int32  # int32 �����˺�
	        #AccountStatus = 8,#optional int32  # int32 �˻�״̬
	        GoodsID = 9, #optional int32 # int32 ��ƷID
	        #optional int32 ValidType = 10, # int32 У������
	        #optional string ValidTime = 11, # string ��Ч����
	        OperateType = 1, #optional int32 # int32 ��������: ί��, ǿƽ������
	        #OperatorID = 1, #optional int32 # int32 ����Ա�˺�ID
	        AccountType = 1, #optional int32 # int32 �˻�����
	        OrderSrc = 15, #optional int32 # int32 ������Դ:���׶ˣ�����ˣ����
	        #optional string AttachParam = 16, # string ���Ӳ���(JSON�ַ���,Э�����,������ʱ�����ֶζ�)	        )
	        ),
	    MemberID = 3, #optional int32 # int32 ������Ա
        OrderPrice = 10.0, #optional double # double ί�м۸�
	    OrderQty = 5, #optional double # double ί������
	    BuyOrSell = 0, #optional int32 # int32 ��������
	    BuildType = 0, #optional int32 # int32 �µ�����:���֣�ƽ��,
	    AllowTradeSub = 8, #optional double # double ����ɽ�ƫ�Χ
	    #optional int32 SpecialAccount = 9, # int32 �ر��Ա�˺�ID
	    #optional double BuyOrSellPtSub = 10, # double �������
	    #optional double SpPrice = 11, # double ֹӯ�۸�
	    #optional double SlPrice = 12, # double ֹ��۸�
	    #optional int32 MarketID = 13, # int32 �г�ID
	    #optional string StartTime = 14, # string ��ʼʱ��
	    #optional string EndTime = 15, # string ����ʱ��
	    #optional int32 ReOpenFlag = 16, # int32 ���ֽ��ֱ��
        )
    data = TkernelTas1_pb2.MMOrderRsp( #����ί�е�Ӧ�� 0 3 202 -> 196810
        Header = common_pb2.MessageHead(
            FunCode = 196810,       # ���ܺ�
	        RequestID = request_id,   # �ͻ��˵���ˮID  ����һ������ֻҪ���ظ�����
	        AccountId = 3,          # �˺�ID
    	    AccessId = 4,           #����������ͻ��˵Ľ���ID
	        ClientTime = int(t*1000)   #��Ϣ����ʱ�� ʱ��� ��
            ),
	    RetCode = 0, #optional int32 # int32 ������
	    #optional string RetDesc = 3, # string ������Ϣ
	    OrderID = 4, #optional int64 # int64 һ�����ɵĶ�����
	    OrderTime = 'ssssss',#optional string 5, # string ����ί�н��׵�ʱ��
	    OrderType = 6, #optional int32 # int32 ��������
	    OrderReq = req_data,#optional TkernelTas1.MMOrderReq OrderReq = 7, # MMOrderReq ί���������
	    )   
    
    conn.clear_queue_before_tests('testorder_rsp')

    conn.publish('entry', 'order_rsp', 1, data)
    tmp, rsp_data = conn.expect('testorder_rsp', TkernelTas1_pb2.MMOrderRsp, 1, 1.0)

    exp_data = TkernelTas1_pb2.MMOrderRsp( #����ί�е�Ӧ�� 0 3 202 -> 196810
        Header = common_pb2.MessageHead(
            FunCode = 196810,       # ���ܺ�
	        RequestID = request_id,   # �ͻ��˵���ˮID  ����һ������ֻҪ���ظ�����
	        AccountId = 3,          # �˺�ID
    	    AccessId = 4,           #����������ͻ��˵Ľ���ID
	        ClientTime = int(t*1000)   #��Ϣ����ʱ�� ʱ��� ��
            ),
	    RetCode = 0, #optional int32 # int32 ������
	    #optional string RetDesc = 3, # string ������Ϣ
	    OrderID = 4, #optional int64 # int64 һ�����ɵĶ�����
	    OrderTime = 'ssssss',#optional string 5, # string ����ί�н��׵�ʱ��
	    OrderType = 66, #optional int32 # int32 ��������
	    OrderReq = req_data,#optional TkernelTas1.MMOrderReq OrderReq = 7, # MMOrderReq ί���������
	    )
    conn.publish('entry', 'order_rsp', 1, data)
    conn.expect2('testorder_rsp', exp_data, 1.0)

def test_OrderDealedNtf():
    data = TkernelTas1_pb2.OrderDealedNtf()
    data.CloseInfos.add(ClosedOrderID=1)
    data2 = TkernelTas1_pb2.OrderDealedNtf()
    data2.CloseInfos.add(ClosedOrderID=1, TradeCharge=1.0)
    protobuf.assert_equal(data, data2)