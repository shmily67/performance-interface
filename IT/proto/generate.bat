copy /y ..\..\common.proto common.proto
"../../../../library/Debug/protoc.exe" -I=./ --cpp_out=./  UserTas1.proto  TkernelTas1.proto  SettleTas1.proto  RiskTas1.proto  ReportTas2.proto  ReportTas1.proto  RealtimeMonitorTas1.proto  QuoteTas1.proto  QkernelTas3.proto  QkernelTas2.proto  QkernelTas1.proto   PublicTas1.proto  NewsFeedTas1.proto  MoneyManagerTas1.proto  ManagerTas3.proto  ManagerTas2.proto  ManagerTas1.proto  LogTas1.proto  IssueTas1.proto  ExterReportTas1.proto  ExterQkernelTas1.proto  DeliveryTas1.proto  Delivery2Tas1.proto  CashTas1.proto  BusproxyTas1.proto  Finance1.proto 
move /y *.h ..\DetailHead\
move /y *.cc ..\DetailSource\
pause
