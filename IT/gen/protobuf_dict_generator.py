# -*- coding: cp936 -*-
import importlib, os, struct, re, Queue
from nose.tools import *
import os

def gen(input_path, input_type, output_path): # input_type: 'tas_funcodes.h'
    f_in = open(input_path, 'r')
    f_out = open(output_path, 'w')
    try:
        if 'tas_funcodes.h' == input_type:
            gen_from_tas_funcodes_h(f_in, f_out)
        else:
            assert False, 'Invalid input_type: ' + input_type
    finally:
        f_in.close()
        f_out.close()
    
def gen_from_tas_funcodes_h(f_in, f_out): # parse tas_funcodes.h
    pb2_name_list, pb2_list = [], []
    for fname in os.listdir('..\\pb2'):
        print fname
        if '_pb2.py' == fname[-7:]:
            pb2_name_list.append(fname[:-3])
            print  os.getcwd()
            pb2_list.append(importlib.import_module(fname[:-3]))
 
    print '\n\n'            
    s = 'import ' + ', '.join(pb2_name_list)
    f_out.write(s)
    
    f_out.write('\n\ndata_class_dict = {')
    name_funcode_dict = {}
    for line in f_in: # #define FID_AddFinancingChargeShareConfigReq    MAKE_FID(0, 6, 1091) // 注释
        if not re.match('#define\s+FID_[a-zA-Z][a-zA-Z0-9_]+', line): continue #'#define' == line[:7]:
        name_match = re.search('FID_[a-zA-Z][a-zA-Z0-9_]+', line)
        msg_name = name_match.group(0)[4:]
        total_class_name = ''
        for pb2 in pb2_list:
            if hasattr(pb2, msg_name):
                total_class_name = pb2.__name__ + '.' + msg_name
                break
        assert_not_equal(total_class_name, '', 'msg_name="%s"\n'%msg_name + line)
        funcode_match = re.search('MAKE_FID\(\d+,\s+\d+,\s+\d+\)', line)
        if not funcode_match:
            assert False, "Invalid line: " + line
        alist = re.findall("\d+", funcode_match.group(0))
        assert 3 == len(alist)
        funcode = (int(alist[0])<<24) + (int(alist[1])<<16) + int(alist[2])
        print '%d: %s,'%(funcode, msg_name)
        f_out.write('\n    %d: %s,'%(funcode, total_class_name))
    f_out.write('\n}')
