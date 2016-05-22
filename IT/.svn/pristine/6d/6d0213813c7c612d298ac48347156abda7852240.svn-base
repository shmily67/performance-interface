from nose.tools import *
import bank_pb2
import msgbus

msgbus.set_pika_logger_level('WARNING')

def setup():
    global conn, cch, hch
    conn = msgbus.Connection('192.168.31.160', 5679, 'XBCHEN', 'guest', 'guest')
    conn.create_publish_channel()
    cch = conn.queue_bind('entry', 'busproxybank_query_rsp1', 'bank_query_rsp')
    hch = conn.queue_bind('entry', 'heartbeat', 'heartbeat', True)
    conn.clear_consume()

def teardown():
    msgbus.close_all()

def test_QListBankParamReq():    
    req_data = bank_pb2.QListBankParamReq(
        Header=bank_pb2.MessageHead(
            FunCode=336265514,
            RequestID=4,
            AccountCode=u"100005",
            Ip=u"192.168.31.21",
            ),
        DealType=3,
        CusBankID=u"0",
        )
    conn.publish('entry', 'bank_query_req', 336265514, 268435457, req_data)

    exp_rsp_data = bank_pb2.QListBankParamRsp(
        Header = bank_pb2.MessageHead(
            FunCode = 336265515,
            RequestID = 4,
            AccountCode = u"100005",
            Ip = u"192.168.31.21",
            ),
        RetCode = 0,
        ParamType = 0,
        )
    exp_rsp_data.ParamList.add(cusBankID=u"0", ShowField=u"1,2,3,4,5,6,7", LessOutAmount=0.000000,
        LessOutAmountType=0, AuditSignFunc=0, AuditEndFunc=0, MinInAmountType=0, MinInAmount=0.010000,
        MaxInAmountType=0, MaxInAmount=50000.000000, AmountInNumType=0, AmountInNum=5000,
        MinOutAmountType=0, MinOutAmount=0.010000, MaxOutAmountType=0, MaxOutAmount=50000.000000,
        AmountOutNumType=0, AmountOutNum=50000, TotalMaxAmountOutType=0,
        TotalMaxAmountOut=500000.000000, InMoneyStartTime=u"6:00:00", InMoneyEndTime=u"22:00:00",
        OutMoneyStartTime=u"6:00:00", OutMoneyEndTime=u"22:00:00", IsAllowInMoney=0, IsAllowOutMoney=0,
        ModifyBankNoType=0, SettleTime=u"04:00:00", AutoSignInTime=u"08:31:00",
        AutoSignOutTime=u"15:41:00",
        BankListId=u"011,102,103,104,105,201,202,203,301,302,303,304,305,306,307,308,309,310,313,314,315,316,317,318,319,320,321,322,401,402,403,501,502,503,504,505,506",\
        CusBankParamId=0, ParamType=0, riskinfo=u"", inshowfield=u"", outshowfield=u"",)
    conn.expect(cch, 268435457, exp_rsp_data, 3.0)

    req_data = bank_pb2.QListBankParamReq(
        Header = bank_pb2.MessageHead(
            FunCode = 336265514,
            RequestID = 2147483647,
            AccountCode = u"100005",
            Ip = u"192.168.31.21",
            ),
        DealType = 3,
        )
    conn.publish('entry', 'bank_query_req', 336265514, 268435457, req_data)

    exp_rsp_data = bank_pb2.QListBankParamRsp(
        Header = bank_pb2.MessageHead(
            FunCode = 336265515,
            RequestID = 2147483647,
            AccountCode = u"100005",
            Ip = u"192.168.31.21",
            ),
        RetCode = 0,
        ParamType = 0,)
    exp_rsp_data.ParamList.add(cusBankID=u"0", ShowField=u"1,2,3,4,5,6,7", LessOutAmount=0.000000,
        LessOutAmountType=0,
        AuditSignFunc=0, AuditEndFunc=0, MinInAmountType=0, MinInAmount=0.010000, MaxInAmountType=0,
        MaxInAmount=50000.000000, AmountInNumType=0, AmountInNum=5000, MinOutAmountType=0,
        MinOutAmount=0.010000, MaxOutAmountType=0, MaxOutAmount=50000.000000, AmountOutNumType=0,
        AmountOutNum=50000, TotalMaxAmountOutType=0, TotalMaxAmountOut=500000.000000,
        InMoneyStartTime=u"6:00:00", InMoneyEndTime=u"22:00:00", OutMoneyStartTime=u"6:00:00",
        OutMoneyEndTime=u"22:00:00", IsAllowInMoney=0, IsAllowOutMoney=0, ModifyBankNoType=0,
        SettleTime=u"04:00:00", AutoSignInTime=u"08:31:00", AutoSignOutTime=u"15:41:00", BankListId= u"011,102,103,104,105,201,202,203,301,302,303,304,305,306,307,308,309,310,313,314,315,316,317,318,319,320,321,322,401,402,403,501,502,503,504,505,506",
        CusBankParamId=0, ParamType=0, riskinfo=u"", inshowfield=u"", outshowfield=u"",)
    conn.expect(cch, 268435457, exp_rsp_data, 3.0)

def test_recv_heartbeat():
    for i in range(5):
        meth, prop, funcode, session_id, data = conn.recv(hch, 6.0)
        print meth.delivery_tag, session_id
        print data
