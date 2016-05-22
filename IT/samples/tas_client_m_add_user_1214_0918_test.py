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
    #QueryAccountInfoReq
    data = tas_client_m_pb2.QueryAccountInfoReq()
    data.Header.FunCode = 17105590
    data.PageInfo.PageNumber = 1
    data.PageInfo.RecordPerPage = 100
    data.PageInfo.NeedTotalCount = 1
    data.AccountType = 0
    client.send(data)

    data = client._expect("QueryAccountInfoRsp", 0, 3.0)

    #QueryAccountInfoReq
    data = tas_client_m_pb2.QueryAccountInfoReq()
    data.Header.FunCode = 17105590
    data.PageInfo.PageNumber = -2147483647
    data.PageInfo.RecordPerPage = 100
    data.PageInfo.NeedTotalCount = 1
    data.CardType = 1
    data.CardNum = u"120123456788"
    client.send(data)

    data = client._expect("QueryAccountInfoRsp", 0, 3.0)

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
    data.MemberCode = u"120"
    data.QryIncParentArea = 1
    client.send(data)

    data = client._expect("QueryAreaRsp", 0, 3.0)

    #QueryAccountCountReq
    data = tas_client_m_pb2.QueryAccountCountReq()
    data.Header.FunCode = 17105714
    data.LoginCode = u"120012345678"
    client.send(data)

    data = client._expect("QueryAccountCountRsp", 0, 3.0)

    #AddAccountInfoReq
    data = tas_client_m_pb2.AddAccountInfoReq()
    data.Header.FunCode = 393908
    data.ExchID = 100
    data.MemberCode = u"120"
    data.AreaCode = u"11"
    data.ParentBrokerID = 0
    data.BrokerID = 0
    data.CustomerId = 0
    data.CustomerName = u"投资者2"
    data.AccountType = 0
    data.AccountStatus = 0
    data.ContRightCode = 3
    data.RiskRateId = 4
    data.LoginCode = u"120012345678"
    data.LoginPWD = u"E10ADC3949BA59ABBE56E057F20F883E"
    data.TaPWD = u"E10ADC3949BA59ABBE56E057F20F883E"
    data.BankId = u"011"
    data.BankAccountNo = u""
    data.BankAccountName = u""
    data.FuncMenu = u""
    data.Sex = 1
    data.Country = u""
    data.Province = u""
    data.City = u""
    data.CardType = 1
    data.CardNum = u"120123456788"
    data.IDAddress = u""
    data.CurrentAddress = u""
    data.PostalCode = u""
    data.TelePhone = u""
    data.OfficePhone = u""
    data.MobilePhone = u"123456"
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

    data = client._expect("AddAccountInfoRsp", 11117, 3.0)

    #QueryMemberReq
    data = tas_client_m_pb2.QueryMemberReq()
    data.Header.FunCode = 17105011
    data.PageInfo.PageNumber = 1
    data.PageInfo.RecordPerPage = 100
    data.PageInfo.NeedTotalCount = 1
    client.send(data)

    data = client._expect("QueryMemberRsp", 0, 3.0)

    #QueryExchStatusReq
    data = tas_client_m_pb2.QueryExchStatusReq()
    data.Header.FunCode = 17105242
    client.send(data)

    data = client._expect("QueryExchStatusRsp", 0, 3.0)

    #QueryAccountInfoReq
    data = tas_client_m_pb2.QueryAccountInfoReq()
    data.Header.FunCode = 17105590
    data.PageInfo.PageNumber = -2147483647
    data.PageInfo.RecordPerPage = 100
    data.PageInfo.NeedTotalCount = 1
    data.CardType = 1
    data.CardNum = u"9999666"
    client.send(data)

    data = client._expect("QueryAccountInfoRsp", 0, 3.0)

    #QueryAccountCountReq
    data = tas_client_m_pb2.QueryAccountCountReq()
    data.Header.FunCode = 17105714
    data.LoginCode = u"012345678"
    client.send(data)

    data = client._expect("QueryAccountCountRsp", 0, 3.0)

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
    data.MemberCode = u"121"
    data.QryIncParentArea = 1
    client.send(data)

    data = client._expect("QueryAreaRsp", 0, 3.0)

    #QueryAccountCountReq
    data = tas_client_m_pb2.QueryAccountCountReq()
    data.Header.FunCode = 17105714
    data.LoginCode = u"121012345678"
    client.send(data)

    data = client._expect("QueryAccountCountRsp", 0, 3.0)

    #AddAccountInfoReq
    data = tas_client_m_pb2.AddAccountInfoReq()
    data.Header.FunCode = 393908
    data.ExchID = 100
    data.MemberCode = u"121"
    data.AreaCode = u"15"
    data.ParentBrokerID = 0
    data.BrokerID = 0
    data.CustomerId = 0
    data.CustomerName = u"投资者2"
    data.AccountType = 0
    data.AccountStatus = 0
    data.ContRightCode = 3
    data.RiskRateId = 4
    data.LoginCode = u"121012345678"
    data.LoginPWD = u"E10ADC3949BA59ABBE56E057F20F883E"
    data.TaPWD = u"E10ADC3949BA59ABBE56E057F20F883E"
    data.BankId = u"011"
    data.BankAccountNo = u""
    data.BankAccountName = u""
    data.FuncMenu = u""
    data.Sex = 1
    data.Country = u"123456"
    data.Province = u""
    data.City = u""
    data.CardType = 1
    data.CardNum = u"9999666"
    data.IDAddress = u""
    data.CurrentAddress = u""
    data.PostalCode = u""
    data.TelePhone = u""
    data.OfficePhone = u""
    data.MobilePhone = u"123456"
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

    #QueryAccountInfoReq
    data = tas_client_m_pb2.QueryAccountInfoReq()
    data.Header.FunCode = 17105590
    data.PageInfo.PageNumber = -2147483647
    data.PageInfo.RecordPerPage = 100
    data.PageInfo.NeedTotalCount = 1
    data.LoginCode = u"121012345678"
    client.send(data)

    data = client._expect("QueryAccountInfoRsp", 0, 3.0)

    #QueryAccountInfoReq
    data = tas_client_m_pb2.QueryAccountInfoReq()
    data.Header.FunCode = 17105590
    data.PageInfo.PageNumber = 1
    data.PageInfo.RecordPerPage = 100
    data.PageInfo.NeedTotalCount = 1
    data.AccountType = 0
    client.send(data)

    data = client._expect("QueryAccountInfoRsp", 0, 3.0)

    #QListBankParamReq
    data = tas_client_m_pb2.QListBankParamReq()
    data.Header.FunCode = 336265514
    data.DealType = 3
    client.send(data)

    data = client._expect("QListBankParamRsp", 0, 3.0)

    #QueryBankCustomerSignReq
    data = tas_client_m_pb2.QueryBankCustomerSignReq()
    data.Header.FunCode = 17105101
    data.PageInfo.PageNumber = -2147483647
    data.PageInfo.RecordPerPage = 100
    data.PageInfo.NeedTotalCount = 1
    data.AccountCode = u"000015000000018"
    client.send(data)

    data = client._expect("QueryBankCustomerSignRsp", 0, 3.0)

    #QueryContentRightReq
    data = tas_client_m_pb2.QueryContentRightReq()
    data.Header.FunCode = 17104913
    data.PageInfo.PageNumber = -2147483647
    data.PageInfo.RecordPerPage = 10000000
    data.PageInfo.NeedTotalCount = 1
    client.send(data)

    #QueryContentRightReq
    data = tas_client_m_pb2.QueryContentRightReq()
    data.Header.FunCode = 17104913
    data.PageInfo.PageNumber = -2147483647
    data.PageInfo.RecordPerPage = 10000000
    data.PageInfo.NeedTotalCount = 1
    client.send(data)

    #QueryContentRightReq
    data = tas_client_m_pb2.QueryContentRightReq()
    data.Header.FunCode = 17104913
    data.PageInfo.PageNumber = -2147483647
    data.PageInfo.RecordPerPage = 10000000
    data.PageInfo.NeedTotalCount = 1
    client.send(data)

    data = client._expect("QueryContentRightRsp", 0, 3.0)

    data = client._expect("QueryContentRightRsp", 0, 3.0)

    data = client._expect("QueryContentRightRsp", 0, 3.0)

    #QListBankParamReq
    data = tas_client_m_pb2.QListBankParamReq()
    data.Header.FunCode = 336265514
    data.DealType = 3
    client.send(data)

    data = client._expect("QListBankParamRsp", 0, 3.0)

    #QueryForceBankCustomerSignReq
    data = tas_client_m_pb2.QueryForceBankCustomerSignReq()
    data.Header.FunCode = 17105277
    data.AccountCode = u"000015000000018"
    client.send(data)

    data = client._expect("QueryForceBankCustomerSignRsp", 0, 3.0)

    #BankForceSignReq
    data = tas_client_m_pb2.BankForceSignReq()
    data.Header.FunCode = 655721
    data.ExtOperatorID = 4723353577358454478
    data.AccountCode = u"000015000000018"
    data.CusBankID = u"0"
    data.Currency = u"RMB"
    data.BankAccountNo = u"124738274327410"
    data.BankAccountName = u"投资者2"
    data.BankId = u"102"
    data.PaymentNo = u"1112220098570983467348096"
    data.ProtocolNo = u"432523456"
    data.OpenBankNo = u"aaaaaaaa"
    data.OpenBankName = u"aaaaaaa"
    data.CertType = 0
    data.BankChildAccount = u""
    data.AgentName = u""
    data.AgentCertType = -1
    data.AgentCertID = u""
    data.BankAccountType = 1
    client.send(data)
