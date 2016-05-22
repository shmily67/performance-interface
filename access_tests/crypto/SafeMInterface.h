#ifndef __SAFE_M_INTERFACE_H__
#define __SAFE_M_INTERFACE_H__

// dll ����
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

// ����Լ��
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
// ����������
#define SM_CMM_ERR				-100
#define SM_CMM_BAD_PARAM		(SM_CMM_ERR - 1)

// DES ����
#define SM_DES_ERR				-200
#define SM_DES_KEY_LEN			(SM_DES_ERR - 1)
#define SM_DES_DAT_LEN			(SM_DES_ERR - 2)

#define	SM_OK					0


/***
�� �� ��  : 
	ecb_encrypt
��������  : 
	ECB ����
�������  : 
	pln     ��������, BCD��, ���ȱ����� 16 �ı���, �����Сд����
	key		������Կ, BCD��, ���ȱ����� 16 ���� 32, �����Сд����
�������  :
	cry		��������, (����)���ȱ������ pln ����
�� �� ֵ  : int(���ĳ���)
	>=0���ɹ��� 
	-1��ʧ�ܣ�

��    ��  : chenliang     ��    ��   : 2014��07��08��
*/
int ecb_encrypt(char *cry, const char *pln, const char *key);

/***
�� �� ��  : 
	ecb_decrypt
��������  : 
	ECB ����
�������  : 
	cry     ���������, BCD��, ���ȱ����� 16 �ı���, �����Сд����
	key		������Կ, BCD��, ���ȱ����� 16 ���� 32, �����Сд����
�������  :
	pln		��������, ���ȱ������ cry ����
�� �� ֵ  : int(���ĳ���)
	>=0���ɹ��� 
	-1��ʧ�ܣ�

��    ��  : chenliang     ��    ��   : 2014��07��08��
*/
int ecb_decrypt(char *pln, const char *cry, const char *key);

/*
�� �� ��  : 
	rand_key
��������  : 
	���������Կ
�������  : 
	len     ��Կ����, ���ȱ����� 16 �ı���
�������  :
	key		�����Կ����
�� �� ֵ  : bool(�ɹ���ʧ��)
	true���ɹ��� 
	false��ʧ�ܣ�

��    ��  : chenliang     ��    ��   : 2014��07��08��
*/
bool rand_key(char *key, unsigned long len);


/***
�� �� ��  : 
	mac
��������  : 
	���� MAC
�������  : 
	dat     mac ����, ansi��, ���Ȳ��� 16 �ı���ʱ������ 0
	iv      ��ʼ����
	key     mac ��Կ
�������  :
	mac     ����� mac ֵ, ���ȱ������ 16
�� �� ֵ  : int(mac����)
	>=0���ɹ��� 
	-1��ʧ�ܣ�

��    ��  : chenliang     ��    ��   : 2014��07��08��
*/
int mac_ansi(char *mac, const char *dat, const char *iv, const char *key);

/***
�� �� ��  : 
	md5
��������  : 
	���� MD5
�������  : 
	pdat    ����, ansi��
	len     ���ݳ���
�������  :
	digest  ����� md5 ֵ
�� �� ֵ  : int(mac����)
	>=0���ɹ��� 
	-1��ʧ�ܣ�

��    ��  : chenliang     ��    ��   : 2014��07��08��
*/
void md5(char *digest, const char *pdat, unsigned long len);


#ifdef __cplusplus
};
#endif // __cplusplus

#endif // __SAFE_M_INTERFACE_H__
