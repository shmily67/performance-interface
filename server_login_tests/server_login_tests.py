#coding=GB2312
import time, random, uuid, multiprocessing
from nose.tools import *
import common_pb2, UserTas1_pb2
import msgbus_h as msgbus, funcode_dict
from protobuf import assert_equal

bus_ip, bus_port, vhost, username, password = '192.168.31.160', 5679, 'TAS2', 'guest', 'guest'

next_account_id = 20050
def get_login_code():
    global next_account_id
    account_id = next_account_id
    next_account_id += 1
    print 'get_login_code(): %d'%account_id
    return str(account_id)

def login(account_type, login_code, password):
    req_data = UserTas1_pb2.LoginReq(
	    AccountType = account_type, #required int32 // int32 �˻����� <- table userinfo
    	LoginCode = login_code, #optional string  // string ��¼����
    	LoginPWD = password, #optional string // string ��¼����, Ӧ�������ģ���ʱ�����
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
    logout_req = UserTas1_pb2.LogoutReq(
        Header = common_pb2.MessageHead(AccountId=account_id),
        )
    conn.publish('entry', 'user_req', 0, logout_req)
    sess_id, logout_rsp = conn.expect('testuser_rsp', UserTas1_pb2.LogoutRsp, 1.0)
    eq_(0, sess_id)
    #eq_(0, logout_rsp.RetCode)
    
def setup():
    global conn
    conn = msgbus.Connection(bus_ip, bus_port, vhost, username, password, funcode_dict.funcode_dict)
    conn.bind_queue('entry', 'testuser_rsp', routing_key='user_rsp')
    for account_id in range(20000, 20100):
        logout_req = UserTas1_pb2.LogoutReq(Header = common_pb2.MessageHead(AccountId=account_id))
        conn.publish('entry', 'user_rsp', 0, logout_req)
        time.sleep(0.01) # �����ٶ�̫�죬�����Ϣ����ӵ���Ͷ�����
    clear_queue()
    print 'setup() complete'

def teardown():
    msgbus.close_all()
    print 'teardown()'

def clear_queue():
    conn.clear_queue_after_tests('testuser_rsp', 1.0)

def test_self_performance():
    t0 = time.time()
    for account_id in range(20000, 22000):
        logout_req = UserTas1_pb2.LogoutReq(Header = common_pb2.MessageHead(AccountId=account_id))
        conn.publish('entry', 'user_rsp', 0, logout_req)
        time.sleep(0.01) # �����ٶ�̫�죬�����Ϣ����ӵ���Ͷ�����
    dt = time.time() - t0
    print 'all sent in %f, speed=%f'%(dt, 1000/dt)

    t0, i = time.time(), 0
    breaktime = t0 + 5.0
    while time.time() < breaktime:
        if conn.ch.basic.get('testuser_rsp'):
            breaktime = time.time() + 5.0
            i += 1
            if 0==i%100:
                print 'got at %f'%(time.time()-t0)
        else:
            time.sleep(0.01)
            #print 'sleep'
    dt = time.time()-t0-5
    print 'total %d got in %s, speed=%f'%(i, dt, i/dt)    
    
def publish_main(bus_ip, bus_port, vhost, username, password):
    conn = msgbus.Connection(bus_ip, bus_port, vhost, username, password, funcode_dict.funcode_dict)
    t0 = time.time()
    for account_id in range(20000, 21000):
        logout_req = UserTas1_pb2.LogoutReq(Header = common_pb2.MessageHead(AccountId=account_id))
        conn.publish('entry', 'user_rsp', 0, logout_req)
        time.sleep(0.01) # �����ٶ�̫�죬�����Ϣ����ӵ���Ͷ�����
    dt = time.time() - t0
    print 'all sent in %f, speed=%f'%(dt, 1000/dt)


"""�˻�����
enum eAccountType {
	INVESTOR_TRADE_ACCOUNT = 0,  // Ͷ���߽����˻�
	MEMBER_TRADE_ACCOUNT = 1,  // ��Ա�����˻�
	SPECIAL_MEMBER_ACCOUNT = 2,  // �ر��Ա�˻�(�����˻�)
	MEMBER_ADMIN_ACCOUNT = 3,  // ��Ա����Ա�˻�
	EXCHANGE_ADMIN_ACCOUNT = 4,  // ����������Ա�ʺ�
	BROKER_MEMBER_ACCOUNT = 5,  // ���ͻ�Ա�ʺ�(�����˻�)
	MEMBER_BROKER_ACCOUNT = 6,  // ��Ա�������˻�
	EXCH_ACCOUNT = 7,  // �������˻�
	SYSTEM_MANAGER = 9,  // ϵͳ����Ա
	SPEC_MEM_ADMIN_ACCOUNT = 10,  // �ر��Ա����Ա�˻�
	HANGTAG_MEM_A_LEGAL_ACCOUNT = 11,  // ���ƻ�ԱA�����˻�
	HANGTAG_MEM_A_ADMIN_ACCOUNT = 12,  // ���ƻ�ԱA����Ա�˻�
	HANGTAG_MEM_B_LEGAL_ACCOUNT = 13,  // ���ƻ�ԱB�����˻�
	HANGTAG_MEM_B_ADMIN_ACCOUNT = 14,  // ���ƻ�ԱB����Ա�˻�
	BROKER_MEMBER_ADMIN_ACCOUNT = 15,  // ���ͻ�Ա����Ա�ʺ�
	MEMBER_ACCOUNT = 16,  // �ۺϻ�Ա�˻�(�����˻�)
	SETTLE_MEMBER_ACCOUNT = 17,  // �����Ա�˻�(�����˻�)
	WAREHOUSE_MANAGER = 21,  // �ֿ����Ա
	INTERMEDIATE_HOPPER_MANAGER = 22,  // �м�ֹ���Ա
	CAPITAL_CENTER = 31,  // �ʱ�����
	FINANCIAL_SERVICES_CENTER = 32,  // ���ڷ�������
	DEALERS = 33,  // ������
	ADMIN_OPERATING_CENTER = 34,  // ��Ӫ���Ĺ���Ա
	LEGAL_OPERATING_CENTER = 35,  // ��Ӫ���ķ����˻�
	LEGAL_SPEC_OPERATING_CENTER = 36 // �ر���Ӫ���ķ����˻�
};"""
test_data_list = (
    (0, '777771', '123'),
    (2, '777772', '123'),
    (3, '777773', '123'),
)
@nottest
def test_login_for_all_account_type():
    clear_queue()
    sess_id = 1
    for account_type, login_code, password in test_data_list:
        yield step_login_logout, sess_id, account_type, login_code, password
        sess_id += 1

def step_login_logout(sess_id, account_type, login_code, password):
    req_data = UserTas1_pb2.LoginReq(
	    AccountType = account_type,
    	LoginCode = login_code,
    	LoginPWD = password,
        )
    conn.publish('entry', 'user_req', sess_id, req_data)

    rsp_sess_id, rsp_data = conn.expect('testuser_rsp', UserTas1_pb2.LoginRsp, 1.0)
    eq_(sess_id, rsp_sess_id)
    eq_(0, rsp_data.RetCode)

    logout_req = UserTas1_pb2.LogoutReq(
        Header = common_pb2.MessageHead(AccountId=rsp_data.Header.AccountId),
        )
    conn.publish('entry', 'user_req', 1, logout_req)
    rsp_sess_id, logout_rsp = conn.expect('testuser_rsp', UserTas1_pb2.LogoutRsp, 1.0)
    print 'logout_rsp='
    print logout_rsp
    eq_(sess_id, rsp_sess_id)
    eq_(0, logout_rsp.RetCode)


def test_login_invalid_funcode_and_token_check():
    clear_queue()
    login_code = '20002'
    login_req = UserTas1_pb2.LoginReq(
        Header = common_pb2.MessageHead(FunCode=100100),
	    AccountType = 1,
    	LoginCode = login_code,
    	LoginPWD = '123',
        )
    conn.publish('entry', 'user_req', 0, login_req)
    rsp_sess_id, login_rsp = conn.expect('testuser_rsp', UserTas1_pb2.LoginRsp, 1.0)
    eq_(0, rsp_sess_id)

    login_code = '20003'
    account_id, token = login(1, login_code, '123')
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


def test_logout():
    logout(10012)    