import sys, re
from nose.tools import *
import BusproxyTas1_pb2, CashTas1_pb2, Delivery2Tas1_pb2, DeliveryTas1_pb2, ExterQkernelTas1_pb2, ExterReportTas1_pb2, Finance1_pb2, IssueTas1_pb2, LogTas1_pb2, ManagerTas1_pb2, ManagerTas2_pb2, ManagerTas3_pb2, MoneyManagerTas1_pb2, NewsFeedTas1_pb2, PublicTas1_pb2, QkernelTas1_pb2, QkernelTas2_pb2, QkernelTas3_pb2, QuoteTas1_pb2, RealtimeMonitorTas1_pb2, ReportTas1_pb2, ReportTas2_pb2, RiskTas1_pb2, SettleTas1_pb2, TkernelTas1_pb2, UserTas1_pb2

pb2_list = (BusproxyTas1_pb2, CashTas1_pb2, Delivery2Tas1_pb2, DeliveryTas1_pb2, ExterQkernelTas1_pb2, ExterReportTas1_pb2, Finance1_pb2, IssueTas1_pb2, LogTas1_pb2, ManagerTas1_pb2, ManagerTas2_pb2, ManagerTas3_pb2, MoneyManagerTas1_pb2, NewsFeedTas1_pb2, PublicTas1_pb2, QkernelTas1_pb2, QkernelTas2_pb2, QkernelTas3_pb2, QuoteTas1_pb2, RealtimeMonitorTas1_pb2, ReportTas1_pb2, ReportTas2_pb2, RiskTas1_pb2, SettleTas1_pb2, TkernelTas1_pb2, UserTas1_pb2)

def main():
    funcode_dict = {}
    funcode_set = set()
    with open(sys.argv[1]) as f:
        last_line_is_empty = False
        for line in f:
            l = line.strip()
            if last_line_is_empty:
                assert '' != l, l
                m1 = re.search(r'\([A-Z][A-Za-z0-9_]+\)', l)
                MsgTypeName = m1.group(0)[1:-1]
                assert_not_in(MsgTypeName, funcode_dict)
                m2 = re.search(r'\d+,\s*\d+\s+\d+', l)
                codes = m2.group(0).replace(',', ' ').split()
                code0, code1, code2 = map(lambda x: int(x), codes)
                #print codes, code0, code1, code2
                funcode = (((code0<<8)+code1)<<16)+code2
                funcode_dict[MsgTypeName] = funcode
                assert_not_in(funcode, funcode_set)
                funcode_set.add(funcode)
                last_line_is_empty = False
            elif '' == line.strip():
                last_line_is_empty = True
            else:
                last_line_is_empty = False

    s = 'import '
    s += ', '.join(map(lambda pb2: pb2.__name__, pb2_list))
    print s + '\n'
               
    print 'funcode_dict = {'
    for pb2 in pb2_list:
        for aname in dir(pb2):
            if aname[0].isupper() and 'DESCRIPTOR' != aname and '_pb2' != aname[-4:]:
                if aname in funcode_dict:
                    funcode = funcode_dict[aname]
                    print '    %d: %s.%s,'%(funcode, pb2.__name__, aname)
                else:
                    print '    #?: %s.%s,'%(pb2.__name__, aname)
    print '    }'

if '__main__' == __name__:
    main()