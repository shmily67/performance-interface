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
    // �������ݼ���
    int32_t TransEncrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);

    // ��������
    int32_t TransDecrypt(char *pDst, int32_t &iDst, const char *pSrc, const int32_t &iSrc);

    // ��ȡ���ܺ�����ݳ���
    int32_t GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);

    // ��ȡ���ܺ�����ݳ���
    int32_t GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen);

    // ���ô�����Կ
    int32_t SetTransKey(char *pKey);

private:
    IEncryptHandle *m_pTransHandle;
};

#endif