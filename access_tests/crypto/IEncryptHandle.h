#ifndef _IENCRYPTHANDLE_H
#define _IENCRYPTHANDLE_H

#include "MISafeModComm.h"

class IEncryptHandle
{
public:
    IEncryptHandle(){}
    virtual ~IEncryptHandle(){}
public:
    // 加密数据
    virtual int32_t Encrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc) = 0;
    // 解密数据
    virtual int32_t Decrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc) = 0;
    // 获取加密后的数据长度
    virtual int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen) = 0;
    // 获取解密后的数据长度
    virtual int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen) = 0;
    // 设置参数
    virtual void SetParam(const char *pParam) = 0;
};

#endif