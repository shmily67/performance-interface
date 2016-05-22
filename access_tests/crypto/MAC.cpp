#include <string.h>
#include <stdlib.h>
#include <malloc.h>
#include <errno.h>

#include "cmm.h"
#include "SafeMInterface.h"

#ifdef _WIN32
#pragma warning(disable:4996)
#endif

extern int __1des(char *oDat, const char *iDat, const char *key, int flag);
extern void des_base(utype *oDat, const utype *iDat, const utype *key, int flag);

int mac_ansi_x99(char *mac, const char *dat, const char *iv, const char *key)
{
	char pmac[16 + 4] = {0};
	char pbuf[16 + 4] = {0}, ptmp[16 + 4];

	char *bcddat = NULL;

	int i, dat_len, len;

	int ret;

	dat_len = (int)strlen(dat);
	len = 2 * dat_len + 1;
	if (NULL == (bcddat = (char*)malloc(len * sizeof(char))))
	{
		return 0 - errno;
	}

	memset(bcddat, 0, (size_t)len * sizeof(char));
	dat_len = asc2hex(bcddat, (const utype*)dat, dat_len);

	if (NULL != iv)
	{
		strcpy(pmac, iv);
	}
	else
	{
		memset(pmac, '0', sizeof(pmac));
	}

	for (i = 0; i < dat_len / 16; ++i)
	{
		bcd_xor(pbuf, pmac, bcddat + i * 16, 16);

		ret = __1des(pmac, pbuf, key, DES_ENCRYPT);
		if (0 > ret)
		{
			return ret;
		}
	}

	if (0 != dat_len % 16)
	{
		memset(ptmp, '0', 16);
		memcpy(ptmp, bcddat + i * 16, (size_t)dat_len % 16);

		bcd_xor(pbuf, pmac, ptmp, 16);

		ret = __1des(pmac, pbuf, key, DES_ENCRYPT);
		if (0 > ret)
		{
			return ret;
		}
	}

	free(bcddat);
	bcddat = NULL;

	memcpy(mac, pmac, 16);

	return 16;
}

int mac_ansi_x919(char *mac, const char *dat, const char *iv, const char *key)
{
	char pkey[16 + 1] = {0}, tkey[16 + 1] = {0};
	char pmac[16 + 1] = {0};
	char pbuf[16 + 1] = {0};

	int ret;

	memcpy(pkey, key, 16);
	memcpy(tkey, key + 16, 16);

	ret = mac_ansi_x99(pmac, dat, iv, pkey);
	if (0 > ret)
	{
		return ret;
	}

	ret = __1des(pbuf, pmac, tkey, DES_DECRYPT);
	if (0 > ret)
	{
		return ret;
	}

	ret = __1des(mac, pbuf, pkey, DES_ENCRYPT);
	if (0 > ret)
	{
		return ret;
	}

	return 16;
}

/***
�� �� ��  : 
	mac_ansi
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
int mac_ansi(char *mac, const char *dat, const char *iv, const char *key)
{
	int key_len;

	if (NULL == mac || NULL == dat || NULL == key)
	{
		return SM_CMM_BAD_PARAM;
	}

	key_len = (int)strlen(key);

	if (16 == key_len)
	{
		return mac_ansi_x99(mac, dat, iv, key);
	}
	else if (32 == key_len)
	{
		return mac_ansi_x919(mac, dat, iv, key);
	}
	else
	{
		return SM_DES_KEY_LEN;
	}
}
