import time, multiprocessing, logging, Queue
from haigha.connection import Connection
from haigha.message import Message
from nose.tools import *
import msgbus

#2016.01.13 In order to improve performance of publishing, use Haigha to replace Pika

#ReportType
ProcessStarted = 0
ConsumerStarted = 1
DriverReqReport = 2
DriverRspReport = 3
DriverEndNotice = 4
MockReport = 5

#StateValue
StateInit = 0
StateRunning = 1
StateStop = 2

class Tester(object):
    created = False
    def __init__(self, codec, display_interval):
        assert not Tester.created
        Tester.created = True
        assert_is_instance(codec, msgbus.Codec)
        assert_is_instance(display_interval, int)
        self.codec, self.display_interval = codec, display_interval
        self.state = multiprocessing.Value('b', StateInit)
        self.report_queue = multiprocessing.Queue()        
        self.driver_dict, self.mock_dict = {}, {} # name -> proc
        self.running_driver_set, self.running_consumer_set = set(), set() #process set
        self.driver_reports_last_period, self.driver_reports_cur_period = {}, {}
        self.mock_reports_last_period, self.mock_reports_cur_period = {}, {}

    def add_mock(self, name, bus_ip, bus_port, vhost, username, password, exchange,
                    consume_queue, req_routing_key, durable,
                    rsp_routing_key, mock_func):
        assert_not_in(name, self.mock_dict)
        eq_(StateInit, self.state.value)
        p = multiprocessing.Process(target=mock_main, args=(name,
            bus_ip, bus_port, vhost, username, password, exchange,
            consume_queue, req_routing_key, durable,
            rsp_routing_key, mock_func, self.report_queue, self.state, self.codec))
        p.start()
        self.running_consumer_set.add(p)
        self.mock_dict[name] = p
        pname, ts, report_type, report_data = self.report_queue.get(True, 3.0)
        eq_(name, pname)
        eq_(ProcessStarted, report_type)
        print name + ' started'

    def add_driver(self, name, bus_ip, bus_port, vhost, username, password, exchange,
                         req_routing_key, req_data_list, send_interval,
                         rsp_queue, rsp_routing_key, consume_proc_num):
        assert_is_instance(send_interval, float)
        assert_greater_equal(send_interval, 0.0)
        assert_not_in(name, self.driver_dict)
        eq_(StateInit, self.state.value)
        req_msg_list = map(lambda req_data : self.codec.encode(1, req_data), req_data_list)
        for i in range(consume_proc_num):
            p = multiprocessing.Process(target=driver_cunsume_func, args=(name,
                bus_ip, bus_port, vhost, username, password, exchange, rsp_queue, rsp_routing_key, 
                self.report_queue, self.state, self.codec))
            p.start()
            self.running_consumer_set.add(p)
            pname, ts, report_type, report_data = self.report_queue.get(True, 3.0)
            eq_(name, pname)
            eq_(ConsumerStarted, report_type)
            print 'consumer of %s started'%name
        p = multiprocessing.Process(target=driver_main, args=(name,
                bus_ip, bus_port, vhost, username, password,
                exchange, req_routing_key, req_msg_list, send_interval,
                self.report_queue, self.state, self.codec))
        p.start()
        self.running_driver_set.add(p)
        self.driver_dict[name] = p
        pname, ts, report_type, report_data = self.report_queue.get(True, 3.0)
        eq_(name, pname)
        eq_(ProcessStarted, report_type)
        print name + ' started'

    def start_test(self):
        print 'start test'
        assert StateInit==self.state.value
        self.state.value = StateRunning
        self.start_time = int(time.time())
        self.next_next_print_time = self.start_time + self.display_interval
        try:
            self.process_loop()
        finally:
            self.state.value = StateStop
            for p in  self.running_driver_set:
                p.join()
            for p in  self.running_consumer_set:
                p.join()
            self.last_process()

    def process_loop(self):
        counter = 0
        while True:
            if self.report_queue.empty():
                time.sleep(0.01)
                continue
            pname, ts, report_type, report_data = self.report_queue.get(False)
            counter += 1
            #print '%s report: type=%d, data=%r'%(pname, report_type, report_data)
            if DriverEndNotice == report_type:
                p = self.driver_dict[pname]
                p.join()
                self.running_driver_set.remove(p)
                logging.debug(pname + ' joined')
                if 0 == len(self.running_driver_set):
                    logging.debug('all driver process terminated, total_num=%d'%counter)
                    break
            else:
                self.process_report(pname, ts, report_type, report_data)

            if time.time() >= self.next_next_print_time:
                self.display()
                self.next_next_print_time += self.display_interval
                self.driver_reports_last_period = self.driver_reports_cur_period
                self.mock_reports_last_period = self.mock_reports_cur_period
                self.driver_reports_cur_period, self.mock_reports_cur_period = {}, {}

    def process_report(self, pname, ts, report_type, report_data):
        if DriverReqReport == report_type:
            req_num = report_data[0]
            if ts <= self.next_next_print_time - self.display_interval*2: # last print time
                logging.debug('throw away: %s ts=%d'%(pname, ts))
            elif ts <= self.next_next_print_time - self.display_interval: # next print time
                if pname in self.driver_reports_last_period:
                    self.driver_reports_last_period[pname][0] += req_num
                else:
                    self.driver_reports_last_period[pname] = [req_num, 0, 0, 0]
            elif ts <= self.next_next_print_time: # next next print time
                if pname in self.driver_reports_cur_period:
                    self.driver_reports_cur_period[pname][0] += req_num
                else:
                    self.driver_reports_cur_period[pname] = [req_num, 0, 0, 0]
            else:
                assert False, 'ts(%d) > self.next_next_print_time(%d)'%(ts, self.next_next_print_time)
        elif DriverRspReport == report_type:
            rsp_num, err_num = report_data
            if ts <= self.next_next_print_time - self.display_interval*2: # last print time
                logging.debug('throw away: %s ts=%d'%(pname, ts))
            elif ts <= self.next_next_print_time - self.display_interval: # next print time
                if pname in self.driver_reports_last_period:
                    self.driver_reports_last_period[pname][1] += rsp_num
                    self.driver_reports_last_period[pname][2] += err_num
                else:
                    self.driver_reports_last_period[pname] = [0, rsp_num, err_num, 0]
            elif ts <= self.next_next_print_time: # next next print time
                if pname in self.driver_reports_cur_period:
                    self.driver_reports_cur_period[pname][1] += rsp_num
                    self.driver_reports_cur_period[pname][2] += err_num
                else:
                    self.driver_reports_cur_period[pname] = [0, rsp_num, err_num, 0]
            else:
                assert False, 'ts(%d) > self.next_next_print_time(%d)'%(ts, self.next_next_print_time)
        elif MockReport == report_type:
            req_num, err_num = report_data
            if ts <= self.next_next_print_time - self.display_interval*2: # last print time
                logging.debug('throw away: %s ts=%d'%(pname, ts))
            elif ts <= self.next_next_print_time - self.display_interval: # next print time
                if pname in self.mock_reports_last_period:
                    self.mock_reports_last_period[pname][0] += req_num
                    self.mock_reports_last_period[pname][2] += err_num
                else:
                    self.mock_reports_last_period[pname] = [req_num, 0, err_num, 0]
            elif ts <= self.next_next_print_time: # next next print time
                if pname in self.mock_reports_cur_period:
                    self.mock_reports_cur_period[pname][0] += req_num
                    self.mock_reports_cur_period[pname][2] += err_num
                else:
                    self.mock_reports_cur_period[pname] = [req_num, 0, err_num, 0]
            else:
                assert False, 'ts(%d) > self.next_next_print_time(%d)'%(ts, self.next_next_print_time)
        else:
            assert False, 'Invalid proc name: ' + pname
        
    def display(self):
        s = '\n%20s %8s %8s %8s %8s %8d'%('ProcName', 'Total', 'Pass', 'Error', 'Timeout',
           self.next_next_print_time-self.start_time-self.display_interval)
        for pname in self.driver_reports_last_period:
            req_num, pass_num, error_num, timeout_num = self.driver_reports_last_period[pname]
            s += '\n%20s %8d %8d %8d %8d'%(pname, req_num, pass_num, error_num, timeout_num)
        for pname in self.mock_reports_last_period:
            req_num, pass_num, error_num, timeout_num = self.mock_reports_last_period[pname]
            s += '\n%20s %8d %8d %8d %8d'%(pname, req_num, pass_num, error_num, timeout_num)
        print s + '\n'

    def last_process(self):
        try:
            while True:
                pname, ts, report_type, report_data = self.report_queue.get(True, 1.0)
                if DriverEndNotice != report_type:
                    self.process_report(pname, ts, report_type, report_data)
        except Queue.Empty as e:
            pass
        self.display()
        self.driver_reports_last_period = self.driver_reports_cur_period
        self.mock_reports_last_period = self.mock_reports_cur_period
        self.next_next_print_time += self.display_interval
        self.display()

def mock_main(name, bus_ip, bus_port, vhost, username, password, exchange,
              consume_queue, req_routing_key, durable,
              rsp_routing_key, mock_func, report_queue, state, codec):
    conn, next_report_time = None, int(time.time()) +1
    req_num, rsp_num, err_num = 0, 0, 0
    try:
        conn = Connection(user=username, password=password, host=bus_ip, port=bus_port, vhost=vhost)
        ch = conn.channel()
        ch.exchange.declare(exchange, 'direct')
        ch.queue.declare(consume_queue, durable=durable, auto_delete=False)
        ch.queue.bind(consume_queue, exchange, req_routing_key)
        ch.basic.qos(prefetch_size=0, prefetch_count=1000)
        
        i = 0
        while True:
            msg = ch.basic.get()
            if None == msg: break
            i += 1
        print 'Consumer of %s read %d msgs before test'%(name, i)
        report_queue.put((name, 0, ProcessStarted, None))

        while StateInit == state.value:
            time.sleep(0.01)
        assert_in(state.value, (StateRunning, StateStop))

        while StateRunning == state.value:
            msg = ch.basic.get()
            if msg: 
                req_num += 1
                if 'heartbeat' == msg.body:
                    session_id, protobuf_data = 0, body
                else:
                    session_id, protobuf_data = self.codec.decode(msg.body)
                rsp_data = mock_func(session_id, protobuf_data)
                if rsp_data:
                    rsp_msg = codec.encode(session_id, rsp_data)
                    ch.basic.publish(rsp_msg, exchange, routing_key)
            else:
                time.sleep(0.01)
            if time.time() >= next_report_time:
                report_queue.put((pname, next_report_time, MockReport, (req_num, err_num)))
                req_num, err_num = 0, 0
                next_report_time += 1
                #print pname + ' report_queue.put() counter=%d'%req_num
        logging.debug(name + ': end of loop')
    except KeyboardInterrupt as e:
        pass
    finally:
        if conn:
            timeout_time = time.time() + 1
            while time.time() < timeout_time:
                msg = ch.basic.get()
                if msg:
                    timeout_time = time.time() + 1
                    req_num += 1
                    if 'heartbeat' == msg.body:
                        session_id, protobuf_data = 0, body
                    else:
                        session_id, protobuf_data = self.codec.decode(msg.body)
                    rsp_data = mock_func(session_id, protobuf_data)
                    if rsp_data:
                        rsp_msg = codec.encode(session_id, rsp_data)
                        ch.basic.publish(rsp_msg, exchange, routing_key)                
            report_queue.put((pname, next_report_time, MockReport, (req_num, err_num)))
            conn.close()
        logging.debug('End of ' + name)

def driver_main(name, bus_ip, bus_port, vhost, username, password, exchange, req_routing_key,
                req_msg_list, send_interval, report_queue, state, codec):
    assert_is_instance(send_interval, float)
    assert_greater_equal(send_interval, 0.0)
    conn, next_log_time, req_num = None, 0, 0
    try:
        conn = Connection(user=username, password=password, host=bus_ip, port=bus_port, vhost=vhost)
        pch = conn.channel()
        report_queue.put((name, 0, ProcessStarted, None))

        #waiting for tester set state to 1(means to start test)
        while StateInit == state.value:
            time.sleep(0.01)
        eq_(StateRunning, state.value)

        req_num, total_sent = 0, 0
        start_time = time.time()
        next_send_time = start_time + send_interval
        next_log_time = int(start_time) + 1
        for app_msg in req_msg_list:
            if 0 < send_interval:
                dt = next_send_time - time.time()
                if dt > 0.0:
                    time.sleep(dt)
            pch.basic.publish(Message(app_msg), exchange, req_routing_key)
            next_send_time += send_interval
            req_num += 1
            if time.time() >= next_log_time:
                report_queue.put((name, next_log_time, DriverReqReport, (req_num,)))
                total_sent += req_num
                req_num = 0
                next_log_time += 1
            if StateRunning != state.value: break
    except KeyboardInterrupt as e:
        pass
    finally:
        total_sent += req_num
        print name + ': end of loop, total %d msgs sent'%total_sent
        report_queue.put((name, next_log_time, DriverReqReport, (req_num,)))
        report_queue.put((name, next_log_time, DriverEndNotice, (total_sent,)))
        if conn:
            conn.close()

def driver_cunsume_func(name, bus_ip, bus_port, vhost, username, password, exchange,
                        rsp_queue, rsp_routing_key, report_que, state, codec):
    conn = None
    next_log_time = int(time.time()) + 1
    rsp_num, err_num, total_num = 0, 0, 0
    try:
        conn = Connection(user=username, password=password, host=bus_ip, port=bus_port, vhost=vhost)
        ch = conn.channel()
        ch.exchange.declare(exchange, 'direct')
        ch.queue.declare(rsp_queue, auto_delete=False)
        ch.queue.bind(rsp_queue, exchange, rsp_routing_key)
        ch.basic.qos(prefetch_size=0, prefetch_count=1000)

        #read all msgs in the consume queue before test
        i = 0
        msg = ch.basic.get(rsp_queue)
        while msg:
            msg = ch.basic.get(rsp_queue)
            i += 1
        print name + ': %d msgs read before test'%i
        report_que.put((name, 0, ConsumerStarted, None))

        #waiting for tester set state to 1(means to start test)
        while StateInit == state.value:
            time.sleep(0.01)
        eq_(StateRunning, state.value)

        next_log_time = int(time.time()) + 1
        while StateRunning == state.value:
            msg = ch.basic.get(rsp_queue)
            if msg:
                s = ''.join(map(lambda b: chr(b), msg.body))
                if 'heartbeat' == s:
                    session_id, protobuf_data = 0, s
                    rsp_num += 1
                else:
                    session_id, protobuf_data = codec.decode(s)
                    if 0 == protobuf_data.RetCode:
                        rsp_num += 1
                    else:
                        err_num += 1
            else:
                time.sleep(0.01)
            if time.time() >= next_log_time:
                report_que.put((name, next_log_time, DriverRspReport, (rsp_num, err_num)))
                total_num += rsp_num+err_num
                rsp_num, err_num = 0, 0
                next_log_time += 1
    except KeyboardInterrupt as e:
        pass
    finally:
        if conn:
            timeout_time = time.time() + 1.0
            while time.time() < timeout_time:
                msg = ch.basic.get(rsp_queue)
                if msg:
                    timeout_time = time.time() + 1.0
                    s = ''.join(map(lambda b: chr(b), msg.body))
                    if 'heartbeat' == s:
                        session_id, protobuf_data = -1, s
                        rsp_num += 1
                    else:
                        session_id, protobuf_data = codec.decode(s)
                    if 0 == protobuf_data.RetCode:
                        rsp_num += 1
                    else:
                        err_num += 1
            conn.close()
            report_que.put((name, next_log_time, DriverRspReport, (rsp_num, err_num)))
            total_num += rsp_num+err_num
            print name + ': end of loop, total %d rsp'%total_num

def clear_msgbus_queue(bus_ip, bus_port, vhost, username, password,
                       exchange, queue, routing_key, durable=False):
    N = 5
    alist = []
    for i in range(N):
        alist.append((bus_ip, bus_port, vhost, username, password, exchange, queue, routing_key, durable))
    p = multiprocessing.Pool(5)
    p.map(__clear__, alist)

def __clear__(args):
    bus_ip, bus_port, vhost, username, password, exchange, queue, routing_key, durable = args
    conn = Connection(user=username, password=password, host=bus_ip, port=bus_port, vhost=vhost)
    counter, timeout_time = 0, time.time()+1    
    try:
        ch = conn.channel()
        ch.exchange.declare(exchange, 'direct')
        ch.queue.declare(queue, durable=durable, auto_delete=False)
        ch.queue.bind(queue, exchange, routing_key)
        ch.basic.qos(prefetch_size=0, prefetch_count=1000)
        while time.time() < timeout_time:
            msg = ch.basic.get(queue)
            if msg:
                timeout_time = time.time() + 1
            else:
                time.sleep(0.01)
            counter += 1
    finally:
        conn.close()
        #print '%d msgs read from '%counter + queue
 