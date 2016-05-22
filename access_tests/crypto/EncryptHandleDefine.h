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
    // ��������
    virtual int32_t Encrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // ��������
    virtual int32_t Decrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // ��ȡ���ܺ�����ݳ���
    virtual int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // ��ȡ���ܺ�����ݳ���
    virtual int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // ���ò���
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
    // ��������
    virtual int32_t Encrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // ��������
    virtual int32_t Decrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // ��ȡ���ܺ�����ݳ���
    virtual int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // ��ȡ���ܺ�����ݳ���
    virtual int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // ���ò���
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
    // ��������
    virtual int32_t Encrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // ��������
    virtual int32_t Decrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);
    // ��ȡ���ܺ�����ݳ���
    virtual int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // ��ȡ���ܺ�����ݳ���
    virtual int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);
    // ���ò���
    virtual void SetParam(const char *pParam);
private:
    string m_strIV;
    string m_strKey;
};

///////////////////////////////////////////////////////////////////////////////////////


#endif