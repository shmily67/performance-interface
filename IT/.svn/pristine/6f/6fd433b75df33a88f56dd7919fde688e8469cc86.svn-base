#ifndef _SERVERHANDLE_H
#define _SERVERHANDLE_H

#include "MISafeModComm.h"

class IEncryptHandle;

class ServerHandle
{
public:
    ServerHandle();
    ~ServerHandle();
public:
    // 传输数据加密
    int32_t TransEncrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);

    // 解密数据
    int32_t TransDecrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);

    // 获取加密后的数据长度
    int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);

    // 获取解密后的数据长度
    int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);

    // 设置传输密钥
    int32_t SetTransKey(char *pKey);

private:
    IEncryptHandle *m_pTransHandle;
};

#endif