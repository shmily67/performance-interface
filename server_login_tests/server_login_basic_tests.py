#coding=GB2312
import time, random, uuid
from nose.tools import *
import common_pb2, UserTas1_pb2, funcode_dict, msgbus_h as msgbus
from protobuf import assert_equal

bus_ip, bus_port, vhost, username, password = '192.168.31.160', 5679, 'TAS2', 'guest', 'guest'

def clear_queue(conn):
    conn.clear_queue_after_tests('testuser_rsp', 1.0)
    
def login(conn, account_type, login_code, password):
    conn.clear_queue_before_tests('testuser_rsp')
    req_data = UserTas1_pb2.LoginReq(
	    AccountType = account_type,
    	LoginCode = login_code,
    	LoginPWD = password,
        )
    conn.publish('entry', 'user_req', 0, req_data)

    sess_id, rsp_data = conn.expect('testuser_rsp', UserTas1_pb2.LoginRsp, 1.0)
    print 'login_rsp='
    print rsp_data
    eq_(0, sess_id)
    eq_(0, rsp_data.RetCode)
    global account_id
    account_id = rsp_data.Header.AccountId
    return account_id, rsp_data.Token

def logout(account_id):
    logout_req = UserTas1_pb2.LogoutReq(Header = common_pb2.MessageHead(AccountId=account_id),)
    conn.publish('entry', 'user_req', 0, logout_req)
    sess_id, logout_rsp = conn.expect('testuser_rsp', UserTas1_pb2.LogoutRsp, 1.0)
    eq_(0, sess_id)
    eq_(0, logout_rsp.RetCode)

def setup():
    global conn
    conn = msgbus.Connection(bus_ip, bus_port, vhost, username, password, funcode_dict.funcode_dict)
    conn.bind_queue('entry', 'testuser_rsp', routing_key='user_rsp')
    clear_queue(conn)
    
    for account_id in range(20000, 20100):
        logout_req = UserTas1_pb2.LogoutReq(Header = common_pb2.MessageHead(AccountId=account_id))
        conn.publish('entry', 'user_req', 0, logout_req)
        conn.get('user_req', 1.0)
        #time.sleep(0.005)
    print 'setup() complete'

def teardown():
    msgbus.close_all()
    print 'teardown() complete'


@nottest
def test_member_login_logout():
    login_code = '20000'
    login_req = UserTas1_pb2.LoginReq(
	    AccountType = 1111,     #required int32     账户类型 <- table userinfo
    	LoginCode = login_code, #optional string    登录号码
    	LoginPWD = '123',       #optional string    登录密码, 应该是密文，暂时不检查
        )
    conn.publish('entry', 'user_req', 0, login_req)

    sess_id, login_rsp = conn.expect('testuser_rsp', UserTas1_pb2.LoginRsp, 1.0)
    eq_(0, sess_id)
    eq_(0, login_rsp.RetCode)
    eq_(0, login_rsp.AccountType)        #int32 账户类型
    eq_(0, login_rsp.CustomerCode)       #int32 用户编号
    eq_(login_code, login_rsp.LoginCode) #string 登录号码
    eq_(1, login_rsp.AccountStatus)      #int32 用户状态
    eq_('1', login_rsp.AreaCode)         #string 用户所属机构
    eq_('1', login_rsp.MemberCode)       #string 用户所属会员的会员代码
    eq_(int(login_code), login_rsp.Header.AccountId)

    logout_req = UserTas1_pb2.LogoutReq(Header = common_pb2.MessageHead(AccountId=int(login_code)),)
    conn.publish('entry', 'user_req', 0, logout_req)
    sess_id, logout_rsp = conn.expect('testuser_rsp', UserTas1_pb2.LogoutRsp, 1.0)
    eq_(0, sess_id)
    eq_(0, logout_rsp.RetCode)

@nottest
def test_login_invalid_password():
    clear_queue()
    login_code = '20001'
    req_data = UserTas1_pb2.LoginReq(
	    AccountType = 1, #required int32  int32 账户类型 <- table userinfo
    	LoginCode = login_code, #optional string   string 登录号码
    	LoginPWD = 'aaaaaa', #optional string  string 登录密码, 应该是密文，暂时不检查
        )
    conn.publish('entry', 'user_req', 0, req_data)

    exp_login_rsp = UserTas1_pb2.LoginRsp(
        Header = common_pb2.MessageHead(
            FunCode = 131294,
	        RequestID = 0,
	        AccountId = int(login_code),
            ),
    	RetCode = 3,
	    )
    conn.expect2('testuser_rsp', 0, exp_login_rsp, 1.0)

@nottest
def test_login_invalid_login_code():
    clear_queue()
    login_req = UserTas1_pb2.LoginReq(
	    AccountType = 1, #required int32  int32 账户类型 <- table userinfo
    	LoginCode = '66666', #optional string   string 登录号码
    	LoginPWD = '123', #optional string  string 登录密码, 应该是密文，暂时不检查
        )
    conn.publish('entry', 'user_req', 0, login_req)

    exp_login_rsp = UserTas1_pb2.LoginRsp(
        Header = common_pb2.MessageHead(
            FunCode = 131294,
	        RequestID = 0,
	        AccountId = 0,
            ),
    	RetCode = 2,
	    )
    conn.expect2('testuser_rsp', 0, exp_login_rsp, 1.0)

def test_token_check():
    login_code = '20003'
    account_id, token = login(conn, 1, login_code, '123')
    print 'account_id=', account_id, 'type=', type(account_id)
    req = UserTas1_pb2.TokenCheckReq(
        #Header = common_pb2.MessageHead(AccountId=int(login_code)),
        Header = common_pb2.MessageHead(AccountId=account_id),
        Token = token,
        )
    conn.publish('entry', 'user_req', 0, req)
    sess_id, rsp_data = conn.expect('testuser_rsp', UserTas1_pb2.TokenCheckRsp, 1.0)
    eq_(0, sess_id)
    eq_(0, rsp_data.RetCode)
    eq_(1, rsp_data.Status)

def test_login_invalid_funcode():
    clear_queue()
    login_code = '20002'
    login_req = UserTas1_pb2.LoginReq(
        Header = common_pb2.MessageHead(FunCode=100100),
	    AccountType = 1,
    	LoginCode = login_code,
    	LoginPWD = '123',
        )
    conn.publish('entry', 'user_req', 0, login_req)

    exp_login_rsp = UserTas1_pb2.LoginRsp(
        Header = common_pb2.MessageHead(
            FunCode = 131294,
	        RequestID = 0,
	        AccountId = int(login_code),
            ),
    	RetCode = 12,
	    )
    rsp_sess_id, login_rsp = conn.expect('testuser_rsp', UserTas1_pb2.LoginRsp, 1.0)
    eq_(0, rsp_sess_id)
    assert_not_equal(0, login_rsp.RetCode)

@nottest
def test_continue_login():
    clear_queue()
    for i in range(20010, 20015):
        login(conn, 1, str(i), '123')
    
@nottest
def test_token_check_invalid():
    clear_queue()
    login_code = '20004'
    account_id, token = login(conn, 1, login_code, '123')
    req = UserTas1_pb2.TokenCheckReq(
        Header = common_pb2.MessageHead(AccountId=account_id),
        Token = 'aaaaaaa',
        )
    conn.publish('entry', 'user_req', 0, req)
    sess_id, rsp_data = conn.expect('testuser_rsp', UserTas1_pb2.TokenCheckRsp, 1.0)
    eq_(0, sess_id)
    eq_(9, rsp_data.RetCode)

@nottest
def test_token_check_after_logout():
    clear_queue()
    login_code = '20005'
    account_id, token = login(conn, 1, login_code, '123')

    logout(account_id)

    req = UserTas1_pb2.TokenCheckReq(
        Header = common_pb2.MessageHead(AccountId=account_id),
        Token = token,
        )
    conn.publish('entry', 'user_req', 0, req)
    sess_id, rsp_data = conn.expect('testuser_rsp', UserTas1_pb2.TokenCheckRsp, 1.0)
    eq_(0, sess_id)
    eq_(9, rsp_data.RetCode)
