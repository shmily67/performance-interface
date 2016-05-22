#coding=utf-8
import time
import random
from nose.tools import *
import funcode_dict, msgbus_h as msgbus
from common_pb2 import MessageHead
from Trade_pb2 import MMTradeProto
from protobuf import assert_equal

bus_ip, bus_port, vhost, username, password = '192.168.31.160', 5679, 'TAS2', 'guest', 'guest'


def clear_queue(conn):
    conn.clear_queue_after_tests('testmoney_rsp', 1.0)


def setup():
    global conn
    conn = msgbus.Connection(bus_ip, bus_port, vhost, username, password, funcode_dict.funcode_dict)
    conn.bind_queue('entry', 'testmoney_rsp', routing_key='money_rsp')
    clear_queue(conn)
    print 'setup() complete'

def teardown():
    msgbus.close_all()
    print 'teardown() complete'


def before_each():
    global request_id, order_id, trade_day
    t = time.time()
    i = int(t*1000)-1450000000000  # 66.9���ڲ��ظ�
    request_id = i
    order_id = i
    tm = time.localtime(t)
    trade_day = '%04d%02d%02d'%(tm.tm_year, tm.tm_mon, tm.tm_mday)


"""message MMTradeProto {
    required MessageHead Header = 1;       // ��Ϣͷ
    optional int64 OrderID = 2;                 // ����
    optional int64 OperateID = 3;               // ����ԱID
    optional int64 AccountID = 4;               // �ʽ��˻�ID
    optional int64 MatchID = 5;                 // �����ʽ��˻�ID
    optional int32 GoodsID = 6;                  // ��ƷID
    optional double Qty = 7;                    // ����
    optional double Price = 8;                  // �۸�
    optional int32 BuyOrSell = 9;               // ��������
    optional int32 OrderType = 10;               // ��������
    optional int32 BuildType = 11;               // �µ�����, ���֣�ƽ��
    
    repeated MMCloseDetail CloseDetails = 12;   // ƽ����ϸ
    
    optional int32 RetCode = 13;                // ������
    optional int64 MoneyTicket = 14;           // �ʽ���ˮ��
    
    optional double FreezeMargin = 15;          // ������
    optional double UnfreezeMargin = 16;        // [�ⶳ|����]�ⶳ��֤��
    optional double UsedMargin = 17;            // [����|ƽ���ͷ�]ռ�ñ�֤��
    optional double OpenCharge = 18;            // ����������
    optional double CloseCharge = 19;           // ƽ��������
    optional double WarehouseCharge = 20;       // [����|ƽ��]�ֵ������
    optional double TradeAmount = 21;           // [����|ƽ���ͷ�]�ɽ����
    optional double ClosePL = 22;               // ƽ��ӯ��
    
    optional string TradeDate = 23;             // ������
    optional string TradeTime = 24;             // ����ʱ��
    optional int32 SettleStatus = 25;           // ����״̬
}"""


@nottest
def test_unfreeze_some_account():    
    #�ⶳ����: ������, ������ί�е���, ����ԱID, �ʽ��˻�ID, ����ⶳ����
    unfreeze_req = MMTradeProto(
        Header = MessageHead(),
        OrderID = 1, #optional int64 OrderID = 2;                 // ����
        AccountID = 8888, #optional int64 AccountID = 4;               // �ʽ��˻�ID
    )
    with open('order_id.txt', 'r') as f:
        for line in f:
            str_order_id, str_freemargin = line.split()
            unfreeze_req.OrderID = int(str_order_id)
            unfreeze_req.UnfreezeMargin = float(str_freemargin)
            conn.publish('entry', 'money_req', 3, 0, unfreeze_req)
            conn.get('testmoney_rsp', 3.0)


@with_setup(before_each, None)
def test_freeze_unfreeze_from_spec():
    #���ᱣ֤������: �ʽ��˻�ID, ����ԱID, ��ƷID, ��������, ����, �۸�, ������, ί�е���, ��������, ��Ʒ�����г�ID
    freeze_req = MMTradeProto(
        Header = MessageHead(FunCode=1, RequestID=request_id),
        OrderID = order_id,
        AccountID = 8888, #optional int64 AccountID = 4;               // �ʽ��˻�ID
        GoodsID = 8888, #optional int32 GoodsID = 6;                  // ��ƷID        
        Qty = 2.0,       #optional double Qty = 7;                    // ����
        Price = 1.0,     #optional double Price = 8;                  // �۸�
        BuyOrSell = 1,     #optional int32 BuyOrSell = 9;               // ��������
        TradeDate = trade_day, #optional string TradeDate = 23;             // ������
        OrderType = 100,
        BuildType = 0,
    )
    conn.publish('entry', 'money_req', 1, 0, freeze_req)
    rsp_data = conn.expect('testmoney_rsp', 2, 0, 1.0)
    eq_(0, rsp_data.RetCode)
    eq_(2, rsp_data.Header.FunCode)
    eq_(order_id, rsp_data.OrderID)

    # �ⶳ����: ��Ϣͷ, ������, ������ί�е���, ����ԱID, �ʽ��˻�ID, ����ⶳ����, ����״̬
    unfreeze_req = MMTradeProto(
        Header = MessageHead(FunCode=3, RequestID=request_id),
        TradeDate = trade_day, #optional string TradeDate = 23;             // ������
        OrderID = order_id,  # optional int64 OrderID = 2;         // ����
        AccountID = 8888,  # optional int64 AccountID = 4;  // �ʽ��˻�ID
        Qty = 2.0,       #optional double Qty = 7;                    // ����
        SettleStatus = 1, #optional int32 SettleStatus = 25;           // ����״̬            
    )
    conn.publish('entry', 'money_req', 3, 0, unfreeze_req)
    rsp_data = conn.expect('testmoney_rsp', 4, 0, 1.0)
    eq_(0, rsp_data.RetCode)
    eq_(4, rsp_data.Header.FunCode)
    eq_(order_id, rsp_data.OrderID)


@with_setup(before_each, None)
def test_freeze_unfreeze_smallest():    
    #���ᱣ֤������: �ʽ��˻�ID, ����ԱID, ��ƷID, ��������, ����, �۸�, ������, ί�е���, ��������, ��Ʒ�����г�ID
    freeze_req = MMTradeProto(
        Header = MessageHead(FunCode=1, RequestID=request_id),
        OrderID = order_id,
        AccountID = 8888, #optional int64 AccountID = 4;               // �ʽ��˻�ID
        GoodsID = 8888, #optional int32 GoodsID = 6;                  // ��ƷID        
    )
    conn.publish('entry', 'money_req', 1, 0, freeze_req)
    rsp_data = conn.expect('testmoney_rsp', 2, 0, 1.0)
    eq_(0, rsp_data.RetCode)
    eq_(2, rsp_data.Header.FunCode)

    unfreeze_req = MMTradeProto(
        Header = MessageHead(),
        OrderID = order_id,  # optional int64 OrderID = 2;         // ����
        AccountID = 8888,  # optional int64 AccountID = 4;  // �ʽ��˻�ID
    )
    conn.publish('entry', 'money_req', 3, 0, unfreeze_req)
    rsp_data = conn.expect('testmoney_rsp', 4, 0, 1.0)
    eq_(0, rsp_data.RetCode)
    eq_(4, rsp_data.Header.FunCode)


@with_setup(before_each, None)
def test_freeze_unfreeze():    
    #���ᱣ֤������: �ʽ��˻�ID,	����ԱID, ��ƷID, ��������, ����, �۸�, ������, ί�е���, ��������, ��Ʒ�����г�ID
    freeze_req = MMTradeProto(
        Header = MessageHead(),
        OrderID = order_id,
        AccountID = 8888, #optional int64 AccountID = 4;               // �ʽ��˻�ID
        GoodsID = 8888, #optional int32 GoodsID = 6;                  // ��ƷID        
    )
    conn.publish('entry', 'money_req', 1, 0, freeze_req)
    rsp_data = conn.expect('testmoney_rsp', 2, 0, 1.0)
    eq_(2, rsp_data.Header.FunCode)
    eq_(order_id, rsp_data.OrderID)
    eq_(0, rsp_data.RetCode)
    
    unfreeze_req = MMTradeProto(
        Header = MessageHead(),
        OrderID = order_id, #optional int64 OrderID = 2;         // ����
        AccountID = 8888, #optional int64 AccountID = 4;  // �ʽ��˻�ID
    )
    conn.publish('entry', 'money_req', 3, 0, unfreeze_req)
    rsp_data = conn.expect('testmoney_rsp', 4, 0, 1.0)
    eq_(4, rsp_data.Header.FunCode)
    eq_(order_id, rsp_data.OrderID)
    eq_(0, rsp_data.RetCode)


@with_setup(before_each, None)
def test_freeze_open():
    #���ᱣ֤������: �ʽ��˻�ID, ����ԱID, ��ƷID, ��������, ����, �۸�, ������, ί�е���, ��������, ��Ʒ�����г�ID
    freeze_req = MMTradeProto(
        Header = MessageHead(FunCode=1),
        OrderID = order_id,
        AccountID = 8888,  #optional int64 AccountID = 4;               // �ʽ��˻�ID
        GoodsID = 8888,    #optional int32 GoodsID = 6;                  // ��ƷID        
        Qty = 12.34,       #optional double Qty = 7;                    // ����
        Price = 12.34,     #optional double Price = 8;                  // �۸�
        BuyOrSell = 1,     #optional int32 BuyOrSell = 9;               // ��������
        TradeDate = trade_day, #optional string TradeDate = 23;             // ������
        OrderType = 100,
        BuildType = 0,
    )
    conn.publish('entry', 'money_req', 1, 0, freeze_req)
    
    rsp_data = conn.expect('testmoney_rsp', 2, 0, 1.0)
    eq_(0, rsp_data.RetCode)
    eq_(2, rsp_data.Header.FunCode)
        
    #ռ������: ������, ί�е���, ����ԱID, �ʽ��˻�ID, �����ʽ��˻�ID, ��ƷID, ��Ʒ����, �۸�, ��������, ����״̬
    open_req = MMTradeProto(
        Header = MessageHead(FunCode=2007),
        OrderID = order_id, #optional int64 OrderID = 2;                 // ����
        AccountID = 8888, #optional int64 AccountID = 4;               // �ʽ��˻�ID
        GoodsID = 8888, #optional int32 GoodsID = 6;                  // ��ƷID
        Qty = 12.34, #optional double Qty = 7;                    // ����
        Price = 12.34, #optional double Price = 8;                  // �۸�
        BuyOrSell = 1, #optional int32 BuyOrSell = 9;               // ��������
        TradeDate = trade_day, #optional string TradeDate = 23;             // ������
        SettleStatus = 1, #optional int32 SettleStatus = 25;           // ����״̬            
    )
    conn.publish('entry', 'money_req', 2007, 0, open_req)
    rsp_data = conn.expect('testmoney_rsp', 2009, 0, 1.0)
    eq_(order_id, rsp_data.OrderID)
    eq_(2009, rsp_data.Header.FunCode)
    eq_(0, rsp_data.RetCode)


@with_setup(before_each, None)
def test_freeze_open_close():
    #���ᱣ֤������: �ʽ��˻�ID, ����ԱID, ��ƷID, ��������, ����, �۸�, ������, ί�е���, ��������, ��Ʒ�����г�ID
    freeze_req = MMTradeProto(
        Header = MessageHead(FunCode=1),
        OrderID = order_id,
        AccountID = 8888,  #optional int64 AccountID = 4;               // �ʽ��˻�ID
        GoodsID = 8888,    #optional int32 GoodsID = 6;                  // ��ƷID        
        Qty = 1.0,       #optional double Qty = 7;                    // ����
        Price = 1.0,     #optional double Price = 8;                  // �۸�
        BuyOrSell = 1,     #optional int32 BuyOrSell = 9;               // ��������
        TradeDate = trade_day, #optional string TradeDate = 23;             // ������
        OrderType = 100,
        BuildType = 0,
    )
    conn.publish('entry', 'money_req', 1, 0, freeze_req)
    
    rsp_data = conn.expect('testmoney_rsp', 2, 0, 1.0)
    eq_(0, rsp_data.RetCode)
    eq_(2, rsp_data.Header.FunCode)
        
    #ռ������: ������, ί�е���, ����ԱID, �ʽ��˻�ID, �����ʽ��˻�ID, ��ƷID, ��Ʒ����, �۸�, ��������, ����״̬
    open_req = MMTradeProto(
        Header = MessageHead(FunCode=2007),
        OrderID = order_id, #optional int64 OrderID = 2;                 // ����
        AccountID = 8888, #optional int64 AccountID = 4;               // �ʽ��˻�ID
        GoodsID = 8888, #optional int32 GoodsID = 6;                  // ��ƷID
        Qty = 1.0, #optional double Qty = 7;                    // ����
        Price = 1.0, #optional double Price = 8;                  // �۸�
        BuyOrSell = 1, #optional int32 BuyOrSell = 9;               // ��������
        TradeDate = trade_day, #optional string TradeDate = 23;             // ������
        SettleStatus = 1, #optional int32 SettleStatus = 25;           // ����״̬            
    )
    conn.publish('entry', 'money_req', 2007, 0, open_req)
    rsp_data = conn.expect('testmoney_rsp', 2009, 0, 1.0)
    eq_(order_id, rsp_data.OrderID)
    eq_(2009, rsp_data.Header.FunCode)
    eq_(0, rsp_data.RetCode)
    
    # ƽ������: ������, �ʽ��˻�ID, �����ʽ��˻�ID, ����ԱID, ��ƷID, �ɽ�����, �ɽ��۸�, ��������, ί�е���, ƽ����ϸ, ����״̬
    # ƽ����ϸ: ��ƽ�ֲֵ���, ƽ������
    close_req = MMTradeProto(
        Header = MessageHead(),
        OrderID = order_id, #optional int64 OrderID = 2;       // ����
        AccountID = 8888, #optional int64 AccountID = 4;   // �ʽ��˻�ID
        GoodsID = 8888, #optional int32 GoodsID = 6;       // ��ƷID
        Qty = 1.0, #optional double Qty = 7;          // ����
        Price = 1.0, #optional double Price = 8;      // �۸�
        BuyOrSell = 1, #optional int32 BuyOrSell = 9;   // ��������
        TradeDate = trade_day, #optional string TradeDate = 23;  // ������
        SettleStatus = 1, #optional int32 SettleStatus = 25;        // ����״̬
    )
    #close_req.CloseDetails.add(OrderID=1, Qty=1)  # ƽ����ϸ
    conn.publish('entry', 'money_req', 2008, 0, close_req)
    rsp_data = conn.expect('testmoney_rsp', 2010, 0, 1.0)
    eq_(0, rsp_data.RetCode)
    eq_(2010, rsp_data.Header.FunCode)
    eq_(order_id, rsp_data.OrderID)
