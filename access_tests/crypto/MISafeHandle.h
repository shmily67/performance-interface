#ifndef _CLIENTHANDLE_H 
#define _CLIENTHANDLE_H

#include "MISafeModComm.h"

class IEncryptHandle;

class MISafeHandle
{
public:
    MISafeHandle();
    ~MISafeHandle();
public:
    // 传输数据加密
    int32_t TransEncrypt(char *pDst, int32_t iDst, const char *pSrc, const int32_t &iSrc);

    // 解密数据
    int32_t TransDecrypt(char *pDst, int32_t iDst, const char *pSrc, const int32_t &iSrc);

    // 获取加密后的数据长度
    int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);

    // 获取解密后的数据长度
    int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);

    // 设置传输密钥
    int32_t SetTransKey(const char *pKey);

    // 设置MAC密钥
    int32_t SetMacKey(const char *pKey);
private:
    string m_strMacKey;
    string m_strTransKey;
    IEncryptHandle *m_pTransHandle; // 传输加解密类
};

#endif