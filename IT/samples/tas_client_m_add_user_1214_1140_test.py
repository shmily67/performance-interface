#coding=utf8
from nose.tools import *
import tas_client_m_pb2, bank_pb2, tas_client_m, util

server_ip, server_port = '192.168.31.160', 10077

def setup():
    global client
    client = tas_client_m.TASManagementClient(server_ip, server_port)
    client.login('manager1', '123456')

def teardown():
    client.close()

def test_xxx():
    #Heartbeat to server
    #Heartbeat to server
    #Heartbeat to server
    #QueryAccountInfoReq
    data = tas_client_m_pb2.QueryAccountInfoReq()
    data.Header.FunCode = 17105590
    data.PageInfo.PageNumber = 1
    data.PageInfo.RecordPerPage = 100
    data.PageInfo.NeedTotalCount = 1
    data.AccountType = 0
    client.send(data)

    data = client._expect("QueryAccountInfoRsp", 0, 3.0)

    #Heartbeat to server
    #Heartbeat to server
    #Heartbeat to server
    #QueryAccountInfoReq
    data = tas_client_m_pb2.QueryAccountInfoReq()
    data.Header.FunCode = 17105590
    data.PageInfo.PageNumber = -2147483647
    data.PageInfo.RecordPerPage = 100
    data.PageInfo.NeedTotalCount = 1
    data.CardType = 1
    data.CardNum = u"123880"
    client.send(data)

    data = client._expect("QueryAccountInfoRsp", 0, 3.0)

    #Heartbeat to server
    #Heartbeat to server
    #Heartbeat to server
    #Heartbeat to server
    #QueryAccountCountReq
    data = tas_client_m_pb2.QueryAccountCountReq()
    data.Header.FunCode = 17105714
    data.LoginCode = u"888111123"
    client.send(data)

    data = client._expect("QueryAccountCountRsp", 0, 3.0)

    #Heartbeat to server
    #Heartbeat to server
    #QueryContentRightReq
    data = tas_client_m_pb2.QueryContentRightReq()
    data.Header.FunCode = 17104913
    data.PageInfo.PageNumber = -2147483647
    data.PageInfo.RecordPerPage = 10000000
    data.PageInfo.NeedTotalCount = 1
    client.send(data)

    data = client._expect("QueryContentRightRsp", 0, 3.0)

    #QueryAreaReq
    data = tas_client_m_pb2.QueryAreaReq()
    data.Header.FunCode = 17105019
    data.PageInfo.PageNumber = 1
    data.PageInfo.RecordPerPage = 2147483647
    data.PageInfo.NeedTotalCount = 1
    data.MemberCode = u"123"
    data.QryIncParentArea = 1
    client.send(data)

    data = client._expect("QueryAreaRsp", 0, 3.0)

    #Heartbeat to server
    #QueryAccountCountReq
    data = tas_client_m_pb2.QueryAccountCountReq()
    data.Header.FunCode = 17105714
    data.LoginCode = u"123888111123"
    client.send(data)

    data = client._expect("QueryAccountCountRsp", 0, 3.0)

    #AddAccountInfoReq
    data = tas_client_m_pb2.AddAccountInfoReq()
    data.Header.FunCode = 393908
    data.ExchID = 100
    data.MemberCode = u"123"
    data.AreaCode = u"17"
    data.ParentBrokerID = 0
    data.BrokerID = 0
    data.CustomerId = 0
    data.CustomerName = u"投资者4"
    data.AccountType = 0
    data.AccountStatus = 0
    data.ContRightCode = 3
    data.RiskRateId = 4
    data.LoginCode = u"123888111456"
    data.LoginPWD = u"E10ADC3949BA59ABBE56E057F20F883E"
    data.TaPWD = u"E10ADC3949BA59ABBE56E057F20F883E"
    data.BankId = u"011"
    data.BankAccountNo = u""
    data.BankAccountName = u""
    data.FuncMenu = u""
    data.Sex = 0
    data.Country = u""
    data.Province = u""
    data.City = u""
    data.CardType = 1
    data.CardNum = u"123880"
    data.IDAddress = u""
    data.CurrentAddress = u""
    data.PostalCode = u""
    data.TelePhone = u""
    data.OfficePhone = u""
    data.MobilePhone = u"654321"
    data.Fax = u""
    data.Email = u""
    data.QQ = u""
    data.WeChat = u""
    data.WeBlog = u""
    data.Currency = u"RMB"
    data.MaxAgreeAmount = 0.000000
    data.DeliveryrightID = 0
    data.TransferStatus = 1
    client.send(data)

    data = client._expect("AddAccountInfoRsp", 0, 3.0)

    #Heartbeat to server
    #QueryAccountInfoReq
    data = tas_client_m_pb2.QueryAccountInfoReq()
    data.Header.FunCode = 17105590
    data.PageInfo.PageNumber = 1
    data.PageInfo.RecordPerPage = 100
    data.PageInfo.NeedTotalCount = 1
    data.AccountType = 0
    client.send(data)

    data = client._expect("QueryAccountInfoRsp", 0, 3.0)
