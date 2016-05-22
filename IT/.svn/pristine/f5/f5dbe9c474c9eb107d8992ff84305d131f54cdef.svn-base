#ifndef __SAFE_M_INTERFACE_H__
#define __SAFE_M_INTERFACE_H__

// dll 导出
#ifdef _WIN32
	#ifndef _DLL_EXP_API
	#define _DLL_EXP_API __declspec(dllexport)
	#else
	#define _DLL_EXP_API __declspec(dllimport)
	#endif // _DLL_EXP_API
#else
	#ifndef _DLL_EXP_API
	#define _DLL_EXP_API
	#endif // _DLL_EXP_API
#endif // _WIN32

// 调用约定
#ifndef _DEFCALL
#define _DEFCALL	__stdcall
#else
#define _DEFCALL
#endif // _DEFCALL

#ifdef __cplusplus
extern "C"
{
#endif // __cplusplus

// errno def
// 公共错误码
#define SM_CMM_ERR				-100
#define SM_CMM_BAD_PARAM		(SM_CMM_ERR - 1)

// DES 错误
#define SM_DES_ERR				-200
#define SM_DES_KEY_LEN			(SM_DES_ERR - 1)
#define SM_DES_DAT_LEN			(SM_DES_ERR - 2)

#define	SM_OK					0


/***
函 数 名  : 
	ecb_encrypt
功能描述  : 
	ECB 加密
输入参数  : 
	pln     加密明文, BCD码, 长度必须是 16 的倍数, 允许大小写混用
	key		加密密钥, BCD码, 长度必须是 16 或者 32, 允许大小写混用
输出参数  :
	cry		加密密文, (自身)长度必须大于 pln 长度
返 回 值  : int(密文长度)
	>=0（成功） 
	-1（失败）

作    者  : chenliang     日    期   : 2014年07月08日
*/
int ecb_encrypt(char *cry, const char *pln, const char *key);

/***
函 数 名  : 
	ecb_decrypt
功能描述  : 
	ECB 解密
输入参数  : 
	cry     需解密密文, BCD码, 长度必须是 16 的倍数, 允许大小写混用
	key		加密密钥, BCD码, 长度必须是 16 或者 32, 允许大小写混用
输出参数  :
	pln		解密明文, 长度必须大于 cry 长度
返 回 值  : int(明文长度)
	>=0（成功） 
	-1（失败）

作    者  : chenliang     日    期   : 2014年07月08日
*/
int ecb_decrypt(char *pln, const char *cry, const char *key);

/*
函 数 名  : 
	rand_key
功能描述  : 
	产生随机密钥
输入参数  : 
	len     密钥长度, 长度必须是 16 的倍数
输出参数  :
	key		随机密钥明文
返 回 值  : bool(成功或失败)
	true（成功） 
	false（失败）

作    者  : chenliang     日    期   : 2014年07月08日
*/
bool rand_key(char *key, unsigned long len);


/***
函 数 名  : 
	mac
功能描述  : 
	计算 MAC
输入参数  : 
	dat     mac 数据, ansi码, 长度不够 16 的倍数时，将补 0
	iv      初始向量
	key     mac 密钥
输出参数  :
	mac     计算的 mac 值, 长度必须大于 16
返 回 值  : int(mac长度)
	>=0（成功） 
	-1（失败）

作    者  : chenliang     日    期   : 2014年07月08日
*/
int mac_ansi(char *mac, const char *dat, const char *iv, const char *key);

/***
函 数 名  : 
	md5
功能描述  : 
	计算 MD5
输入参数  : 
	pdat    数据, ansi码
	len     数据长度
输出参数  :
	digest  计算的 md5 值
返 回 值  : int(mac长度)
	>=0（成功） 
	-1（失败）

作    者  : chenliang     日    期   : 2014年07月08日
*/
void md5(char *digest, const char *pdat, unsigned long len);


#ifdef __cplusplus
};
#endif // __cplusplus

#endif // __SAFE_M_INTERFACE_H__
