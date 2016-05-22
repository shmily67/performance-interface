#include "AESEncryptHandle.h"
#include "evp.h"

///////////////////////////////////////////////////////////////////////////////////////
// AES
AESEncryptHandle::AESEncryptHandle() :
m_strKey("MISM@muchinfo20151216abcdefg1234")
{
}

AESEncryptHandle::~AESEncryptHandle()
{

}

int32_t AESEncryptHandle::Encrypt(char *pDst, int32_t &iDstLen, const char *pSrc, const int32_t &iSrcLen)
{
    int32_t encUpdateLen = 0;
    int32_t encFinalLen = 0;
    int32_t encryptLen = 0;
    
    int32_t iRev = SAFEMOD_ERR;
    int32_t iResult = SAFEMOD_ERR;
    
    do
    {
        iResult = GetEncryptDataLen(encryptLen, pSrc, iSrcLen);
        if (iResult != SAFEMOD_OK
                || iDstLen < encryptLen)
        {
            break;
        }
        
        EVP_CIPHER_CTX ctx;
        EVP_EncryptInit(&ctx, EVP_aes_256_ecb(), (unsigned char*)m_strKey.c_str(), nullptr);
        EVP_EncryptUpdate(&ctx, (unsigned char*)pDst, &encUpdateLen, (const unsigned char*)pSrc, iSrcLen);
        EVP_EncryptFinal(&ctx, (unsigned char*)(pDst + encUpdateLen), &encFinalLen);
        
        iDstLen = encUpdateLen + encFinalLen;
        iRev = SAFEMOD_OK;
    }while(0);
    
    return iRev;
}

int32_t AESEncryptHandle::Decrypt(char *pDst, int32_t &iDstLen, const char *pSrc, const int32_t &iSrcLen)
{
    int32_t decUpdateLen = 0;
    int32_t decFinalLen = 0;
    int32_t decryptLen = 0;
    
    int32_t iRev = SAFEMOD_ERR;
    int32_t iResult = SAFEMOD_ERR;
    
    do
    {
        iResult = GetDecryptDataLen(decryptLen, pSrc, iSrcLen);
        if (iResult != SAFEMOD_OK
                || iDstLen < decryptLen)
        {
            break;
        }
        
        EVP_CIPHER_CTX ctx;
        EVP_DecryptInit(&ctx, EVP_aes_256_ecb(), (unsigned char*)m_strKey.c_str(), nullptr);
        EVP_DecryptUpdate(&ctx, (unsigned char*)pDst, &decUpdateLen, (const unsigned char*)pSrc, iSrcLen);
        EVP_DecryptFinal(&ctx, (unsigned char*)(pDst + decUpdateLen), &decFinalLen);
        
        iDstLen = decUpdateLen + decFinalLen;
        iRev = SAFEMOD_OK;
    }while(0);
    
    return iRev;
}

int32_t AESEncryptHandle::GetEncryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen)
{
    int32_t iRev = SAFEMOD_ERR;

    if (iLen > 0)
    {
        iRev = SAFEMOD_OK;
        iRevLen = (iLen / 16 + 1) * 16;        
    }
    
    return iRev;
}

int32_t AESEncryptHandle::GetDecryptDataLen(int32_t &iRevLen, const char *pData, const int32_t &iLen)
{
    int32_t iRev = SAFEMOD_ERR;

    if (iLen > 0)
    {
        iRev = SAFEMOD_OK;
        iRevLen = iLen;
    }
    
    return iRev;
}

void AESEncryptHandle::SetParam(const char *pParam)
{
    m_strKey = pParam;
}
