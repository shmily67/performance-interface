#ifndef _ISAFEINTERFACE_H
#define _ISAFEINTERFACE_H

#ifdef WIN32
#ifdef EXPORTDLL
#define _DLL_EXP_API extern "C" __declspec(dllexport)  
#else
#define _DLL_EXP_API extern "C" __declspec(dllimport)  
#endif
#else
#define _DLL_EXP_API
#endif

#include <stdint.h>

    // 函数名 
    //   MIGetSafeHandle
    // 功能 
    //   获取接口实例
    // 参数 
    //   无
    // 返回值 
    //   0   --- 失败
    //   非0 --- 成功

_DLL_EXP_API intptr_t MIGetSafeHandle();

    // 函数名 
    //   MIFreeSafeHandle
    // 功能 
    //   释放接口实例
    // 参数 
    //   0) [in] pSafeHandle : 实例对象的地址
    // 返回值 
    //   无

_DLL_EXP_API void MIFreeSafeHandle(intptr_t pSafeHandle);

    // 函数名 
    //   MILoad
    // 功能 
    //   加载密钥
    // 参数 
    //   0) [in] pDst : 消息内存地址
    //   1) [in] iDst : 消息长度
    //   2) [in] pSafeHandle : 实例对象的地址
    // 返回值 
    //   0   --- 成功
    //   非0 --- 失败

_DLL_EXP_API int32_t MILoad(char *pDst, int32_t iDst, intptr_t pSafeHandle);

    // 函数名 
    //   MIAlterTransPwd
    // 功能 
    //   修改传输密钥
    // 参数 
    //   0) [in] pPwd : 密钥字符串
    //   1) [in] pSafeHandle : 实例对象的地址
    // 返回值 
    //   0   --- 成功
    //   非0 --- 失败

_DLL_EXP_API int32_t MIAlterTransPwd(const char *pPwd, intptr_t pSafeHandle);

    // 函数名 
    //   MITransEncrypt
    // 功能 
    //   传输数据加密
    // 参数 
    //   0) [in] pDst : 加密后的数据内存地址
    //   1) [in] iDst : 加密后的数据内存长度
    //   2) [in] pSrc : 待加密数据内存地址
    //   3) [in] iSrc : 待加密数据内存长度
    //   4) [in] pSafeHandle : 实例对象的地址
    // 返回值 
    //   0   --- 成功
    //   非0 --- 失败

_DLL_EXP_API int32_t MITransEncrypt(char *pDst, int32_t iDst, const char *pSrc, int32_t iSrc, intptr_t pSafeHandle);

    // 函数名 
    //   MITransDecrypt
    // 功能 
    //   解密数据
    // 参数 
    //   0) [in] pDst : 解密后的数据内存地址
    //   1) [in] iDst : 解密后的数据内存长度
    //   2) [in] pSrc : 待解密数据内存地址
    //   3) [in] iSrc : 待解密数据内存长度
    //   4) [in] pSafeHandle : 实例对象的地址
    // 返回值 
    //   0   --- 成功
    //   非0 --- 失败

_DLL_EXP_API int32_t MITransDecrypt(char *pDst, int32_t iDst, const char *pSrc, int32_t iSrc, intptr_t pSafeHandle);

    // 函数名 
    //   MIGetEncryptDataLen
    // 功能 
    //   获取加密后的数据长度
    // 参数 
    //   0) [in,out] iRevLen : 存储加密后数据的数据长度
    //   1) [in] pData : 待加密的数据
    //   2) [in] iLen : 待加密的数据的长度
    //   3) [in] pSafeHandle : 实例对象的地址
    // 返回值 
    //   0   --- 成功
    //   非0 --- 失败

_DLL_EXP_API int32_t MIGetEncryptDataLen(int32_t &iRevLen, const char *pData, int32_t iLen, intptr_t pSafeHandle);

    // 函数名 
    //   MIGetDecryptDataLen
    // 功能 
    //   获取解密后的数据长度
    // 参数 
    //   0) [in,out] iRevLen : 存储解密后数据的数据长度
    //   1) [in] pData : 待解密的数据
    //   2) [in] iLen : 待解密的数据的长度
    //   3) [in] pSafeHandle : 实例对象的地址
    // 返回值 
    //   0   --- 成功
    //   非0 --- 失败

_DLL_EXP_API int32_t MIGetDecryptDataLen(int32_t &iRevLen, const char *pData, int32_t iLen, intptr_t pSafeHandle);

    // 函数名 
    //   MIMD5Encrypt
    // 功能 
    //   MD5数据加密
    // 参数 
    //   0) [in] pDst : 加密后的数据内存地址
    //   1) [in] iDst : 加密后的数据内存长度
    //   2) [in] pSrc : 待加密数据内存地址
    //   3) [in] iSrc : 待加密数据内存长度
    // 返回值 
    //   0   --- 成功
    //   非0 --- 失败

_DLL_EXP_API int32_t MIMD5Encrypt(char *pDst, int32_t &iDst, const char *pSrc, int32_t iSrc);

    // 函数名 
    //   MIMD5Decrypt
    // 功能 
    //   MD5解密数据
    // 参数 
    //   0) [in] pDst : 解密后的数据内存地址
    //   1) [in] iDst : 解密后的数据内存长度
    //   2) [in] pSrc : 待解密数据内存地址
    //   3) [in] iSrc : 待解密数据内存长度   
    // 返回值 
    //   0   --- 成功
    //   非0 --- 失败

_DLL_EXP_API int32_t MIMD5Decrypt(char *pDst, int32_t &iDst, const char *pSrc, int32_t iSrc);

    // 函数名 
    //   MIMD5GetEncryptDataLen
    // 功能 
    //   MD5获取加密后的数据长度
    // 参数 
    //   0) [in,out] iRevLen : 存储加密后数据的数据长度
    //   1) [in] pData : 待加密的数据
    //   2) [in] iLen : 待加密的数据的长度
    // 返回值 
    //   0   --- 成功
    //   非0 --- 失败

_DLL_EXP_API int32_t MIMD5GetEncryptDataLen(int32_t &iRevLen, const char *pData, int32_t iLen);

    // 函数名 
    //   MIMD5GetDecryptDataLen
    // 功能 
    //   MD5获取解密后的数据长度
    // 参数 
    //   0) [in,out] iRevLen : 存储解密后数据的数据长度
    //   1) [in] pData : 待解密的数据
    //   2) [in] iLen : 待解密的数据的长度
    //   3) [in] pSafeHandle : 实例对象的地址
    // 返回值 
    //   0   --- 成功
    //   非0 --- 失败

_DLL_EXP_API int32_t MIMD5GetDecryptDataLen(int32_t &iRevLen, const char *pData, int32_t iLen);

#endif
