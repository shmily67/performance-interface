#ifndef __AESENCRYPTHANLDE_HPP__
#define __AESENCRYPTHANLDE_HPP__

#include <string>
#include "IEncryptHandle.h"

class AESEncryptHandle : public IEncryptHandle
{
public:
    AESEncryptHandle();
    virtual ~AESEncryptHandle();
public:
    // 加密数据
    virtual int32_t Encrypt(char *pDst, int32_t &iDstLen, const char *pSrc, const int32_t &iSrcLen);
    // 解密数据
    virtual int32_t Decrypt(char *pDst, int32_t &iDstLen, const char *pSrc, const int32_t &iSrcLen);
    // 获取加密后的数据长度
    virtual int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // 获取解密后的数据长度
    virtual int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // 设置参数
    virtual void SetParam(const char *pParam);

private:
    string      m_strKey;
};

#endif
