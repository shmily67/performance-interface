import msgbus_test_generator, client_m_test_generator

parameter_list = (
    (
        'message_bus', # generation_type
        '192.168.31.160', 5679, # serv_ip, serv_port
        'pcap\\1222_1554_startmytas.pcap', # pcap_path
        'linux-tcpdump', # pcap_type
        'pcap\\1222_1554_startmytas_connection_dict.txt', # connection_service_dict_path
        'output\\1222_1554_startmytas_test.py', # output_path
        (('192.168.31.160', 26475),), # ignored_addr
    ), # 0
    (
        'message_bus', # generation_type
        '192.168.31.160', 5679, # serv_ip, serv_port
        'pcap\\1222_1755_start_bank.pcap', # pcap_path
        'windows-wireshark', # pcap_type
        'pcap\\1222_1755_start_bank_connection_dict.txt', # connection_service_dict_path
        'output\\1222_1755_start_bank_test.py', # output_path
    ), # 1
    (
        'message_bus', # generation_type
        '192.168.31.160', 5679, # serv_ip, serv_port
        'pcap\\1224_1720_client_m_login.pcap', # pcap_path
        'linux-tcpdump', # pcap_type
        'pcap\\1224_1720_connection_dict.txt', # connection_service_dict_path
        'output\\1224_1720_client_m_login_test.py', # output_path
        #(('192.168.31.160', 26475),), # ignored_addr
    ), # 2
    (
        'message_bus', # generation_type
        '192.168.31.160', 5679, # serv_ip, serv_port
        'pcap\\1225_1500_bank_query_start.pcap', # pcap_path
        'windows-wireshark', # pcap_type
        'pcap\\1225_1500_connection_dict.txt', # connection_service_dict_path
        'output\\1225_1500_bank_query_start_test.py', # output_path
    ), # 3
    (
        'message_bus', # generation_type
        '192.168.31.160', 5679, # serv_ip, serv_port
        'pcap\\1225_1750_bank_outin_start.pcap', # pcap_path
        'windows-wireshark', # pcap_type
        'pcap\\1225_1750_connection_dict.txt', # connection_service_dict_path
        'output\\1225_1750_bank_outin_start_test.py', # output_path
    ), # 4
    (
        'message_bus', # generation_type
        '192.168.31.160', 6680, # serv_ip, serv_port
        'pcap\\1229_1430_new_order.pcap', # pcap_path
        'linux-tcpdump', # pcap_type
        'pcap\\1229_1430_connection_service_dict.txt', # connection_service_dict_path
        'output\\1229_1430_new_order_test.py', # output_path
    ), # 5
    (
        'message_bus', # generation_type
        '192.168.31.160', 6680, # serv_ip, serv_port
        'pcap\\1229_1430_new_order_filtered.pcap', # pcap_path
        'linux-tcpdump', # pcap_type
        'pcap\\1229_1430_connection_service_dict.txt', # connection_service_dict_path
        'output\\1229_1430_order_test.py', # output_path
    ), # 6
)
parameters = parameter_list[6]

if 'message_bus' == parameters[0]:
    msgbus_test_generator.gen(*parameters[1:])
elif 'client_m' == parameters[0]:
    client_m_test_generator.gen(*parameters[1:])
else:
    assert False, 'Invalid generation_type: '+parameters[0]