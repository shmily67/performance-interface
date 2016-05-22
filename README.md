# performance-interface
1.目录结构：
   acess_tests:是接入服务测试相关文件，通过socket协议对接入服务进行查询、市价等功能进行接口测试。
   mm_tests:是资金服务，通过protobuf+socket进行市、限价下单进行测试。
   server_login:是登录服务
   IT:就是本套接口测试的的框架，功能主要是数据发送的封装、以及接口测试用例的生成。
   tas2.0接口测试方案我们设计的接口测试方案。
   TASperformance：是通过loadrunner进行系统性能测试的报告。
2.接口测试框架简介
   主要采用python+socket编写服务驱动，然后在于Nosetest测试框架下编写测试用例，对服务进行接口和性能测试。
