#ifndef _ENCRYPTHANDLEDEFINE_H
#define _ENCRYPTHANDLEDEFINE_H

#include <string>
#include "IEncryptHandle.h"

using namespace std;

///////////////////////////////////////////////////////////////////////////////////////
// ECB
class CECBEncryptHandle : public IEncryptHandle
{
public:
    CECBEncryptHandle();
    virtual ~CECBEncryptHandle();
public:
    // 加密数据
    virtual int32_t Encrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // 解密数据
    virtual int32_t Decrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // 获取加密后的数据长度
    virtual int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // 获取解密后的数据长度
    virtual int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // 设置参数
    virtual void SetParam(const char *pParam);

private:
    string      m_strKey;
};
///////////////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////////////
// MD5
class CMD5EncryptHandle : public IEncryptHandle
{
public:
    CMD5EncryptHandle();
    virtual ~CMD5EncryptHandle();
public:
    // 加密数据
    virtual int32_t Encrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // 解密数据
    virtual int32_t Decrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // 获取加密后的数据长度
    virtual int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // 获取解密后的数据长度
    virtual int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // 设置参数
    virtual void SetParam(const char *pParam);
};
///////////////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////////////
// MAC
class CMACEncryptHandle : public IEncryptHandle
{
public:
    CMACEncryptHandle();
    virtual ~CMACEncryptHandle();
public:
    // 加密数据
    virtual int32_t Encrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // 解密数据
    virtual int32_t Decrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // 获取加密后的数据长度
    virtual int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // 获取解密后的数据长度
    virtual int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // 设置参数
    virtual void SetParam(const char *pParam);
private:
    string m_strIV;
    string m_strKey;
};

///////////////////////////////////////////////////////////////////////////////////////


#endif