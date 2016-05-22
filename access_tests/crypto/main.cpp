//#include<windows.h>
#include<stdio.h>
#include<winsock2.h>
#include "ISafeInterface.h"
//#include "SafeMInterface.h"
//#include "cmm.h"
//#include "MISafeModComm.h"

int server_main();
SOCKET create_listen_socket(const int port);
int recv_at_least(SOCKET s, char* buf, int buf_size, int len);
int test_ISafeInterface();
void hex_print(const unsigned char* buf, int len);

typedef intptr_t (__cdecl *FP_MIGetSafeHandle)();  // intptr_t MIGetSafeHandle()
typedef int32_t (__cdecl *FP_MILoad)(char *pDst, int32_t iDst, intptr_t pSafeHandle);
typedef int32_t (__cdecl *FP_MIGetEncryptDataLen)(int32_t &iRevLen, const char *pData, int32_t iLen, intptr_t pSafeHandle);
typedef int32_t (__cdecl *FP_MITransEncrypt)(char *pDst, int32_t iDst, const char *pSrc, int32_t iSrc, intptr_t pSafeHandle);
typedef int32_t (__cdecl *FP_MIGetDecryptDataLen)(int32_t &iRevLen, const char *pData, int32_t iLen, intptr_t pSafeHandle);
typedef int32_t (__cdecl *FP_MITransDecrypt)(char *pDst, int32_t iDst, const char *pSrc, int32_t iSrc, intptr_t pSafeHandle);

const int port = 21000;
const int buf_size = 65536;

int main(int argc, char* argv[])
{
	return server_main();
}

int server_main(){
	HINSTANCE hInstance = LoadLibrary(TEXT("crypto32.dll"));
	if(NULL == hInstance){
		printf("\nLoadLibrary() faild");
		return -1;
	}
	printf("\nPass 1");
	FP_MIGetSafeHandle pGetSafeHandle = (FP_MIGetSafeHandle) GetProcAddress(hInstance, "MIGetSafeHandle");
	if(NULL == pGetSafeHandle){
		return -2;
	}
	printf("\nPass 2");
	FP_MILoad pMILoad = (FP_MILoad)GetProcAddress(hInstance, "MILoad");
	if(NULL == pMILoad){
		return -3;
	}
	printf("\nPass 3");
	FP_MIGetEncryptDataLen pMIGetEncryptDataLen = (FP_MIGetEncryptDataLen)GetProcAddress(hInstance, "MIGetEncryptDataLen");
	if(NULL == pMIGetEncryptDataLen){
		return -4;
	}
	printf("\nPass 4");
	FP_MITransEncrypt pMITransEncrypt = (FP_MITransEncrypt)GetProcAddress(hInstance, "MITransEncrypt");
	if(NULL == pMITransEncrypt){
		return -5;
	}
	printf("\nPass 5");
	FP_MIGetDecryptDataLen pMIGetDecryptDataLen = (FP_MIGetDecryptDataLen)GetProcAddress(hInstance, "MIGetDecryptDataLen");
	if(NULL == pMIGetDecryptDataLen){
		return -6;
	}
	printf("\nPass 6");
	FP_MITransDecrypt pMITransDecrypt = (FP_MITransDecrypt)GetProcAddress(hInstance, "MITransDecrypt");
	if(NULL == pMITransDecrypt){
		return -7;
	}
	printf("\nPass 7");

	intptr_t pSafeHandle = (pGetSafeHandle)();
	if(0 == pSafeHandle){
		printf("\nGetSafeHandle() failed");
		return -8;
	}

	int32_t ret_val = (pMILoad)(NULL, 0, pSafeHandle);
	if(0 != ret_val){
		printf("\nMILoad() failed, returns %d", ret_val);
		return -9;
	}
	printf("\nMISM initialized sucessfully");

	SOCKET sockSrv = create_listen_socket(port);
    listen(sockSrv, 10);
	printf("\nBegin to listen at port %d", port);
  
    SOCKADDR_IN  addrClient;  
    int len = sizeof(SOCKADDR);

    char in_buf[buf_size]="", out_buf[buf_size]="";
    while(true){ // 短连接，一次连接处理一次编解码请求   
        SOCKET sockConn = accept(sockSrv, (SOCKADDR*)&addrClient, &len);
		printf("\n\nNew connection");

		//Receive tag(1字节) and length(4字节, 网络序)
		UINT32 recv_len = recv_at_least(sockConn, in_buf, buf_size, 5);
		char tag = in_buf[0];
		if('e' != tag && 'd' != tag){
			printf("\nInvalid tag: '%c'", tag);
			closesocket(sockConn);
			continue;
		}
		UINT32 msg_len = ntohl(*((UINT32*)(in_buf+1)));
		if(65536 <= msg_len){
			printf("msg_len(%d) > 65536. Close connection!");
			closesocket(sockConn);
		}
		if(recv_len < msg_len) {
			recv_len += recv_at_least(sockConn, in_buf+recv_len, buf_size-recv_len, msg_len-recv_len);
		}
		printf("\nMsg received, tag='%c', msg_len=%d", tag, msg_len);
	    hex_print((unsigned char*)in_buf, recv_len);

		int out_msg_len = -1;
		if('d' == tag){
			ret_val = (pMIGetDecryptDataLen)(out_msg_len, in_buf+5, msg_len, pSafeHandle);
			if(0 != ret_val){
				printf("\nMIGetDecryptDataLen() failed, returns %d", ret_val);
				closesocket(sockConn);
				return -1;
			}
			printf("\nout_msg_len=%d", out_msg_len);

			char resp_msg[buf_size] = "";	
			ret_val = (pMITransDecrypt)(out_buf+4, out_msg_len, in_buf+5, msg_len, pSafeHandle);
			if(0 != ret_val){
				printf("\nMITransDecrypt() failed, returns %d", ret_val);
				closesocket(sockConn);
				return -1;
			}
			printf("\nDecrypt() sucess\ncry_proto_msg=");
			hex_print((const unsigned char*)in_buf+5, msg_len);
			printf("\nout_msg=");
			hex_print((const unsigned char*)out_buf+4, out_msg_len);

			UINT32 *pLen = (UINT32 *)out_buf;
			*pLen = htonl(out_msg_len);
			send(sockConn, out_buf, out_msg_len+4, 0);
			printf("\nmsg sent");
		} else {
			ret_val = (pMIGetEncryptDataLen)(out_msg_len, in_buf+5, msg_len, pSafeHandle);
			if(0 != ret_val){
				printf("\nMIGetEncryptDataLen() failed, returns %d", ret_val);
				closesocket(sockConn);
				return -1;
			}
			printf("\nout_msg_len=%d", out_msg_len);

			char resp_msg[buf_size] = "";	
			ret_val = (pMITransEncrypt)(out_buf+4, out_msg_len, in_buf+5, msg_len, pSafeHandle);
			if(0 != ret_val){
				printf("\MITransEncrypt() failed, returns %d", ret_val);
				closesocket(sockConn);
				return -1;
			}
			printf("\nEncrypt() sucess\ncry_proto_msg=");
			hex_print((const unsigned char*)in_buf+5, msg_len);
			printf("\nout_msg=");
			hex_print((const unsigned char*)out_buf+4, out_msg_len);

			UINT32 *pLen = (UINT32 *)out_buf;
			*pLen = htonl(out_msg_len);
			send(sockConn, out_buf, out_msg_len+4, 0);
			printf("\nmsg sent");
		}
		Sleep(1000);
		closesocket(sockConn);
    }  
    printf("\n");  
    //system("pause");
	return 0; 
}

SOCKET create_listen_socket(const int port){
	WORD wVersionRequested;  
    WSADATA wsaData;    // 这结构是用于接收Wjndows Socket的结构信息的   
    int err;  
       
    wVersionRequested = MAKEWORD( 1, 1 );   // 请求1.1版本的WinSock库       
    err = WSAStartup( wVersionRequested, &wsaData );  
    if ( err != 0 ) {  // 返回值为零的时候是表示成功申请WSAStartup
        return -1;             
    }       
    if ( LOBYTE( wsaData.wVersion ) != 1 || HIBYTE( wsaData.wVersion ) != 1 ) {  
        WSACleanup( );  
        return -1;   
    }

    SOCKET sockSrv = socket(AF_INET, SOCK_STREAM, 0);     
    SOCKADDR_IN addrSrv;  
    addrSrv.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
    addrSrv.sin_family = AF_INET;  
    addrSrv.sin_port = htons(port);  
    bind(sockSrv, (SOCKADDR*)&addrSrv, sizeof(SOCKADDR));
	return sockSrv;
}

int recv_at_least(SOCKET s, char* buf, int buf_size, int len)
{
	int bytes_received = 0;
	while(bytes_received<len) {
		int ret = recv(s, buf, buf_size, 0);
		bytes_received += ret;
	}
	return bytes_received;
}

void hex_print(const unsigned char* buf, int len0){
	char str[65536] = "";
	int j = 0, len = -1;
	if(1024 >= len0){
		len = len0;
	} else {
		len = 1024;
	}
	for(int i=0; i<len; i++){
		sprintf(str+j, "%02x\x20", buf[i]);
		j += 3;
		if(39 == i%40){
			sprintf(str+j, "\n");
			//strcat(str, "\n");
			j += 1;
		}
	}
	if(1024>len){
		str[len*3+1] = '\0';
	} else {
		str[len*3+1] = '.';
		str[len*3+2] = '.';
		str[len*3+3] = '.';
		str[len*3+4] = '\0';
	}
	printf("\n%s", str);	
}
