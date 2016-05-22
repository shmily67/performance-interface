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
函 数 名  : 
	mac_ansi
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
