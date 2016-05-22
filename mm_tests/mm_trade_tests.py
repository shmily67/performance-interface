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

class RequestIDGenerator(object): #客户端的流水ID，（缺省从0开始）递增
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
        FunCode = 196809,           # 功能号
	    RequestID = request_id,     # 客户端的流水ID
	    AccountId = 3,              # 账号ID
	    AccessId = 0,               # 二级分配给客户端的接入ID
	    ClientTime = int(t*1000)    # 消息发起时间 时间戳 毫秒
        )
    req_data = TkernelTas1_pb2.MMOrderReq(
        Header = header,   
	    OrderHead = TkernelTas1_pb2.OrderHead( # OrderHead 委托消息头
	        #Header = header, # MessageHead 重复，所以这里不需要？
	        #int32 RetCode = 2, # int32 返回码
	        OrderID = order_generator.gen(t), #optional int64 OrderID = 3, # int64 委托单号
	        ClientSerialNo = str(request_id), #optional string = 4, # string 客户端流水号
	        ClientOrderTime = gen_client_order_time(t), #optional string 5, # string 客户端委托时间
	        ClientFlag = 'PC Client',#optional string 6, # string 终端标示, 手机，PC端等
	        AccountID = 7, #optional int32  # int32 交易账号
	        #AccountStatus = 8,#optional int32  # int32 账户状态
	        GoodsID = 9, #optional int32 # int32 商品ID
	        #optional int32 ValidType = 10, # int32 校验类型
	        #optional string ValidTime = 11, # string 有效期限
	        OperateType = 0, #optional int32 # int32 操作类型: 委托, 强平，代客
	        #OperatorID = 1, #optional int32 # int32 操作员账号ID
	        AccountType = 1, #optional int32 # int32 账户类型
	        OrderSrc = 15, #optional int32 # int32 单据来源:交易端，管理端，风控
	        #optional string AttachParam = 16, # string 附加参数(JSON字符串,协议待定,用于临时新增字段定)	        )
	        ),
	    MemberID = 3,       #optional int32 # int32 所属会员
        OrderPrice = 10.0,  #optional double # double 委托价格
	    OrderQty = 10.0,    #optional double # double 委托数量
	    BuyOrSell = 0,      #optional int32 # int32 买卖方向
	    BuildType = 0101020101, #optional int32 # int32 下单类型:建仓，平仓, dev_doc\交易业务\订单类型.docx
	    AllowTradeSub = 1.0,  #optional double # double 允许成交偏差范围
	    #optional int32 SpecialAccount = 9, # int32 特别会员账号ID
	    #optional double BuyOrSellPtSub = 10, # double 买卖点差
	    #optional double SpPrice = 11, # double 止盈价格
	    #optional double SlPrice = 12, # double 止损价格
	    #optional int32 MarketID = 13, # int32 市场ID
	    #optional string StartTime = 14, # string 开始时间
	    #optional string EndTime = 15, # string 结束时间
	    #optional int32 ReOpenFlag = 16, # int32 反手建仓标记
        )
    conn.publish('entry', 'order_req', 1, req_data)

    exp_rsp_data = TkernelTas1_pb2.MMOrderRsp( #做市委托单应答 0 3 202 -> 196810
        Header = header,
	    RetCode = 0, #optional int32 # int32 返回码
	    #optional string RetDesc = 3, # string 描述信息
	    OrderID = 4, #optional int64 # int64 一级生成的订单号
	    OrderTime = gen_client_order_time(time.time()), #optional string 5, # 接受委托交易的时间
	    OrderType = 0101020101, #optional int32  dev_doc\交易业务\订单类型.docx
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
委托服请求冻结资金：1
委托服请求冻结资金返回: 2

委托服请求解冻资金: 3
委托服请求解冻资金返回: 4

资金占用请求：2007
资金占用响应: 2009

资金平仓请求: 2008
资金平仓响应: 2010"""

def test_MMOrderReq():# 做市委托单请求 0 3 201 -> funcode=196809
    t = time.time()
    header = common_pb2.MessageHead(
        FunCode = 196809,                       # 功能号
	    RequestID = request_id_generator.gen(), # 客户端的流水ID
	    AccountId = 3,                          # 账号ID
	    AccessId = 0,                           # 二级分配给客户端的接入ID
	    ClientTime = int(t*1000)                #消息发起时间 时间戳 毫秒
        )
    data = TkernelTas1_pb2.MMOrderReq(
        Header = header,
	    OrderHead = TkernelTas1_pb2.OrderHead( # OrderHead 委托消息头
	        Header = header, # MessageHead
	        #int32 RetCode = 2, # int32 返回码
	        OrderID = order_generator.gen(t), #optional int64 OrderID = 3, # int64 委托单号
	        ClientSerialNo = '1', #optional string = 4, # string 客户端流水号
	        ClientOrderTime = gen_client_order_time(t), #optional string 5, # string 客户端委托时间
	        ClientFlag = 'PC Client',#optional string 6, # string 终端标示, 手机，PC端等
	        AccountID = 7, #optional int32  # int32 交易账号
	        #AccountStatus = 8,#optional int32  # int32 账户状态
	        GoodsID = 9, #optional int32 # int32 商品ID
	        #optional int32 ValidType = 10, # int32 校验类型
	        #optional string ValidTime = 11, # string 有效期限
	        OperateType = 1, #optional int32 # int32 操作类型: 委托, 强平，代客
	        #OperatorID = 1, #optional int32 # int32 操作员账号ID
	        AccountType = 1, #optional int32 # int32 账户类型
	        OrderSrc = 15, #optional int32 # int32 单据来源:交易端，管理端，风控
	        #optional string AttachParam = 16, # string 附加参数(JSON字符串,协议待定,用于临时新增字段定)	        )
	        ),
	    MemberID = 3, #optional int32 # int32 所属会员
        OrderPrice = 10.0, #optional double # double 委托价格
	    OrderQty = 5, #optional double # double 委托数量
	    BuyOrSell = 0, #optional int32 # int32 买卖方向
	    OpenType = 0, #optional int32 # int32 下单类型:建仓，平仓,
	    AllowTradeSub = 8, #optional double # double 允许成交偏差范围
	    #optional int32 SpecialAccount = 9, # int32 特别会员账号ID
	    #optional double BuyOrSellPtSub = 10, # double 买卖点差
	    #optional double SpPrice = 11, # double 止盈价格
	    #optional double SlPrice = 12, # double 止损价格
	    #optional int32 MarketID = 13, # int32 市场ID
	    #optional string StartTime = 14, # string 开始时间
	    #optional string EndTime = 15, # string 结束时间
	    #optional int32 ReOpenFlag = 16, # int32 反手建仓标记
        )
    s = data.SerializeToString()
    data2 = TkernelTas1_pb2.MMOrderReq()
    data2.ParseFromString(s)
    protobuf.assert_equal(data, data2)

def test_MMOrderRsp():
    t = time.time()
    header = common_pb2.MessageHead(
        FunCode = 196809,                       # 功能号
	    RequestID = request_id_generator.gen(), # 客户端的流水ID
	    AccountId = 3,                          # 账号ID
	    AccessId = 0,                           # 二级分配给客户端的接入ID
	    ClientTime = int(t*1000)                #消息发起时间 时间戳 毫秒
        )
    req_data = TkernelTas1_pb2.MMOrderReq(
        Header = header,
	    OrderHead = TkernelTas1_pb2.OrderHead( # OrderHead 委托消息头
	        Header = header, # MessageHead
	        #int32 RetCode = 2, # int32 返回码
	        OrderID = order_generator.gen(t), #optional int64 OrderID = 3, # int64 委托单号
	        ClientSerialNo = '1', #optional string = 4, # string 客户端流水号
	        ClientOrderTime = gen_client_order_time(t), #optional string 5, # string 客户端委托时间
	        ClientFlag = 'PC Client',#optional string 6, # string 终端标示, 手机，PC端等
	        AccountID = 7, #optional int32  # int32 交易账号
	        #AccountStatus = 8,#optional int32  # int32 账户状态
	        GoodsID = 9, #optional int32 # int32 商品ID
	        #optional int32 ValidType = 10, # int32 校验类型
	        #optional string ValidTime = 11, # string 有效期限
	        OperateType = 1, #optional int32 # int32 操作类型: 委托, 强平，代客
	        #OperatorID = 1, #optional int32 # int32 操作员账号ID
	        AccountType = 1, #optional int32 # int32 账户类型
	        OrderSrc = 15, #optional int32 # int32 单据来源:交易端，管理端，风控
	        #optional string AttachParam = 16, # string 附加参数(JSON字符串,协议待定,用于临时新增字段定)	        )
	        ),
	    MemberID = 3, #optional int32 # int32 所属会员
        OrderPrice = 10.0, #optional double # double 委托价格
	    OrderQty = 5, #optional double # double 委托数量
	    BuyOrSell = 0, #optional int32 # int32 买卖方向
	    OpenType = 0, #optional int32 # int32 下单类型:建仓，平仓,
	    AllowTradeSub = 8, #optional double # double 允许成交偏差范围
	    #optional int32 SpecialAccount = 9, # int32 特别会员账号ID
	    #optional double BuyOrSellPtSub = 10, # double 买卖点差
	    #optional double SpPrice = 11, # double 止盈价格
	    #optional double SlPrice = 12, # double 止损价格
	    #optional int32 MarketID = 13, # int32 市场ID
	    #optional string StartTime = 14, # string 开始时间
	    #optional string EndTime = 15, # string 结束时间
	    #optional int32 ReOpenFlag = 16, # int32 反手建仓标记
        )
    data = TkernelTas1_pb2.MMOrderRsp( #做市委托单应答 0 3 202 -> 196810
        Header = common_pb2.MessageHead(
            FunCode = 196810,       # 功能号
	        RequestID = int(t)+random.randint(0, 9999),   # 客户端的流水ID  对于一级服务，只要不重复即可
	        AccountId = 3,          # 账号ID
    	    AccessId = 4,           #二级分配给客户端的接入ID
	        ClientTime = int(t*1000)   #消息发起时间 时间戳 秒
            ),
	    RetCode = 0, #optional int32 # int32 返回码
	    #optional string RetDesc = 3, # string 描述信息
	    OrderID = 4, #optional int64 # int64 一级生成的订单号
	    OrderTime = 'ssssss',#optional string 5, # string 接受委托交易的时间
	    OrderType = 6, #optional int32 # int32 单据类型
	    OrderReq = req_data,#optional TkernelTas1.MMOrderReq OrderReq = 7, # MMOrderReq 委托请求带回
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
            AccountID = 100101, # 与下面的AccountID是什么关系？
            ),
        OrderID = order_id,                     # 单号   int64
        OrderType = 0101020101,          # 单据类型 int64 做市/买/市价/建仓/保证金
        OperateID = 4,                   # 操作员ID int64
        AccountID = 5,                   # 资金账户ID int64
        GoodID = 7,                      # 商品ID int32
        Qty = 1.0,                       # 数量 double
        Price = 1.0,                     # 价格 double
        BuyOrSell = 0,                   # 买卖方向 int32
        )
    """CloseDetails = 11, # 平仓明细 repeated MMCloseDetail
    #optional   int64 OrderID = 1,                # (被平)单号
    #optional  double Qty = 2,                    # 平仓数量
    #optional  double UserMargin = 3,             # 释放占用保证金
    #optional  double ReleaseHoldAmount = 4,      # 释放持仓金额
    #optional  double CloseCharge = 5,            # 平仓手续费
    #optional  double WarehouseCharge = 6,        # 仓单服务费
    #optional  double ClosePL = 7,                # 平仓盈亏"""
    req_data.CloseDetails.add(Qty=10.0)
    req_data.CloseDetails.add(Qty=10.0, UserMargin=10.0)
    s = req_data.SerializeToString()
    data2 = trade_pb2.MMTradeProto()
    data2.ParseFromString(s)
    protobuf.assert_equal(req_data, data2)

def test_msgbus_h_order_req():
    t = time.time()
    header = common_pb2.MessageHead(
        FunCode = 196809,                       # 功能号
	    RequestID = request_id_generator.gen(), # 客户端的流水ID
	    AccountId = 3,                          # 账号ID
	    AccessId = 0,                           # 二级分配给客户端的接入ID
	    ClientTime = int(t*1000)                #消息发起时间 时间戳 毫秒
        )
    data = TkernelTas1_pb2.MMOrderReq(
        Header = header,
	    OrderHead = TkernelTas1_pb2.OrderHead( # OrderHead 委托消息头
	        Header = header, # MessageHead
	        #int32 RetCode = 2, # int32 返回码
	        OrderID = order_generator.gen(t), #optional int64 OrderID = 3, # int64 委托单号
	        ClientSerialNo = '1', #optional string = 4, # string 客户端流水号
	        ClientOrderTime = gen_client_order_time(t), #optional string 5, # string 客户端委托时间
	        ClientFlag = 'PC Client',#optional string 6, # string 终端标示, 手机，PC端等
	        AccountID = 7, #optional int32  # int32 交易账号
	        #AccountStatus = 8,#optional int32  # int32 账户状态
	        GoodsID = 9, #optional int32 # int32 商品ID
	        #optional int32 ValidType = 10, # int32 校验类型
	        #optional string ValidTime = 11, # string 有效期限
	        OperateType = 1, #optional int32 # int32 操作类型: 委托, 强平，代客
	        #OperatorID = 1, #optional int32 # int32 操作员账号ID
	        AccountType = 1, #optional int32 # int32 账户类型
	        OrderSrc = 15, #optional int32 # int32 单据来源:交易端，管理端，风控
	        #optional string AttachParam = 16, # string 附加参数(JSON字符串,协议待定,用于临时新增字段定)	        )
	        ),
	    MemberID = 3, #optional int32 # int32 所属会员
        OrderPrice = 10.0, #optional double # double 委托价格
	    OrderQty = 5, #optional double # double 委托数量
	    BuyOrSell = 0, #optional int32 # int32 买卖方向
	    OpenType = 0, #optional int32 # int32 下单类型:建仓，平仓,
	    AllowTradeSub = 8, #optional double # double 允许成交偏差范围
	    #optional int32 SpecialAccount = 9, # int32 特别会员账号ID
	    #optional double BuyOrSellPtSub = 10, # double 买卖点差
	    #optional double SpPrice = 11, # double 止盈价格
	    #optional double SlPrice = 12, # double 止损价格
	    #optional int32 MarketID = 13, # int32 市场ID
	    #optional string StartTime = 14, # string 开始时间
	    #optional string EndTime = 15, # string 结束时间
	    #optional int32 ReOpenFlag = 16, # int32 反手建仓标记
        )
    conn.publish('entry', 'order_req', 1, data)
    conn.expect2('testorder_req', data, 1.0)

def test_msgbus_h_order_rsp():
    t = time.time()
    request_id = request_id_generator.gen()
    order_id = order_generator.gen(t)
    header = common_pb2.MessageHead(
        FunCode = 196809,                       # 功能号
	    RequestID = request_id, # 客户端的流水ID
	    AccountId = 3,                          # 账号ID
	    AccessId = 0,                           # 二级分配给客户端的接入ID
	    ClientTime = int(t*1000)                #消息发起时间 时间戳 毫秒
        )
    req_data = TkernelTas1_pb2.MMOrderReq(
        Header = header,
	    OrderHead = TkernelTas1_pb2.OrderHead( # OrderHead 委托消息头
	        Header = header, # MessageHead
	        #int32 RetCode = 2, # int32 返回码
	        OrderID = order_id, #optional int64 OrderID = 3, # int64 委托单号
	        ClientSerialNo = str(request_id), #optional string = 4, # string 客户端流水号
	        ClientOrderTime = gen_client_order_time(t), #optional string 5, # string 客户端委托时间
	        ClientFlag = 'PC Client',#optional string 6, # string 终端标示, 手机，PC端等
	        AccountID = 7, #optional int32  # int32 交易账号
	        #AccountStatus = 8,#optional int32  # int32 账户状态
	        GoodsID = 9, #optional int32 # int32 商品ID
	        #optional int32 ValidType = 10, # int32 校验类型
	        #optional string ValidTime = 11, # string 有效期限
	        OperateType = 1, #optional int32 # int32 操作类型: 委托, 强平，代客
	        #OperatorID = 1, #optional int32 # int32 操作员账号ID
	        AccountType = 1, #optional int32 # int32 账户类型
	        OrderSrc = 15, #optional int32 # int32 单据来源:交易端，管理端，风控
	        #optional string AttachParam = 16, # string 附加参数(JSON字符串,协议待定,用于临时新增字段定)	        )
	        ),
	    MemberID = 3, #optional int32 # int32 所属会员
        OrderPrice = 10.0, #optional double # double 委托价格
	    OrderQty = 5, #optional double # double 委托数量
	    BuyOrSell = 0, #optional int32 # int32 买卖方向
	    BuildType = 0, #optional int32 # int32 下单类型:建仓，平仓,
	    AllowTradeSub = 8, #optional double # double 允许成交偏差范围
	    #optional int32 SpecialAccount = 9, # int32 特别会员账号ID
	    #optional double BuyOrSellPtSub = 10, # double 买卖点差
	    #optional double SpPrice = 11, # double 止盈价格
	    #optional double SlPrice = 12, # double 止损价格
	    #optional int32 MarketID = 13, # int32 市场ID
	    #optional string StartTime = 14, # string 开始时间
	    #optional string EndTime = 15, # string 结束时间
	    #optional int32 ReOpenFlag = 16, # int32 反手建仓标记
        )
    data = TkernelTas1_pb2.MMOrderRsp( #做市委托单应答 0 3 202 -> 196810
        Header = common_pb2.MessageHead(
            FunCode = 196810,       # 功能号
	        RequestID = request_id,   # 客户端的流水ID  对于一级服务，只要不重复即可
	        AccountId = 3,          # 账号ID
    	    AccessId = 4,           #二级分配给客户端的接入ID
	        ClientTime = int(t*1000)   #消息发起时间 时间戳 秒
            ),
	    RetCode = 0, #optional int32 # int32 返回码
	    #optional string RetDesc = 3, # string 描述信息
	    OrderID = 4, #optional int64 # int64 一级生成的订单号
	    OrderTime = 'ssssss',#optional string 5, # string 接受委托交易的时间
	    OrderType = 6, #optional int32 # int32 单据类型
	    OrderReq = req_data,#optional TkernelTas1.MMOrderReq OrderReq = 7, # MMOrderReq 委托请求带回
	    )   
    
    conn.clear_queue_before_tests('testorder_rsp')

    conn.publish('entry', 'order_rsp', 1, data)
    tmp, rsp_data = conn.expect('testorder_rsp', TkernelTas1_pb2.MMOrderRsp, 1, 1.0)

    exp_data = TkernelTas1_pb2.MMOrderRsp( #做市委托单应答 0 3 202 -> 196810
        Header = common_pb2.MessageHead(
            FunCode = 196810,       # 功能号
	        RequestID = request_id,   # 客户端的流水ID  对于一级服务，只要不重复即可
	        AccountId = 3,          # 账号ID
    	    AccessId = 4,           #二级分配给客户端的接入ID
	        ClientTime = int(t*1000)   #消息发起时间 时间戳 秒
            ),
	    RetCode = 0, #optional int32 # int32 返回码
	    #optional string RetDesc = 3, # string 描述信息
	    OrderID = 4, #optional int64 # int64 一级生成的订单号
	    OrderTime = 'ssssss',#optional string 5, # string 接受委托交易的时间
	    OrderType = 66, #optional int32 # int32 单据类型
	    OrderReq = req_data,#optional TkernelTas1.MMOrderReq OrderReq = 7, # MMOrderReq 委托请求带回
	    )
    conn.publish('entry', 'order_rsp', 1, data)
    conn.expect2('testorder_rsp', exp_data, 1.0)

def test_OrderDealedNtf():
    data = TkernelTas1_pb2.OrderDealedNtf()
    data.CloseInfos.add(ClosedOrderID=1)
    data2 = TkernelTas1_pb2.OrderDealedNtf()
    data2.CloseInfos.add(ClosedOrderID=1, TradeCharge=1.0)
    protobuf.assert_equal(data, data2)