#include <string.h>

#include "cmm.h"
#include "SafeMInterface.h"

static const int e_r[48]={
	31,0 ,1 ,2 ,3 ,4 ,3 ,4 ,
	5 ,6 ,7 ,8 ,7 ,8 ,9 ,10,
	11,12,11,12,13,14,15,16,
	15,16,17,18,19,20,19,20,
	21,22,23,24,23,24,25,26,
	27,28,27,28,29,30,31,0};

static const int P[32]={
	15, 6,19,20,28,11,27,16,
	0 ,14,22,25,4 ,17,30, 9,
	1 , 7,23,13,31,26,2 , 8,
	18,12,29,5 ,21,10,3 ,24};

int SSS[16][4][16]={
	14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
	0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,/* err on */
	4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
	15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13,

	15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
	3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
	0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
	13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9,

	10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
	13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
	13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
	1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12,

	7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
	13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
	10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
	3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14, /* err on */

	2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
	14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6, /* err on */
	4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
	11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3,

	12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
	10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
	9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
	4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13,

	4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
	13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
	1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
	6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12,

	13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
	1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
	7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
	2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11};

int pc_1_c[28]={
	57,49,41,33,25,17,9 ,
	1 ,58,50,42,34,26,18,
	10,2 ,59,51,43,35,27,
	19,11,3 ,60,52,44,36};

int pc_1_d[28]={
	63,55,47,39,31,23,15,
	7 ,62,54,46,38,30,22,
	14,6 ,61,53,45,37,29,
	21,13,5 ,28,20,12,4 };

int pc_2[48]={
	14,17,11,24,1 ,5 ,3 ,28,
	15,6 ,21,10,23,19,12,4 ,
	26,8 ,16,7 ,27,20,13,2 ,
	41,52,31,37,47,55,30,40,
	51,45,33,48,44,49,39,56,
	34,53,46,42,50,36,29,32};

int ip_tab[64]={
	58,50,42,34,26,18,10,2,
	60,52,44,36,28,20,12,4,
	62,54,46,38,30,22,14,6,
	64,56,48,40,32,24,16,8,
	57,49,41,33,25,17,9 ,1,
	59,51,43,35,27,19,11,3,
	61,53,45,37,29,21,13,5,
	63,55,47,39,31,23,15,7};

int _ip_tab[64]={
	40,8,48,16,56,24,64,32,
	39,7,47,15,55,23,63,31,
	38,6,46,14,54,22,62,30,
	37,5,45,13,53,21,61,29,
	36,4,44,12,52,20,60,28,
	35,3,43,11,51,19,59,27,
	34,2,42,10,50,18,58,26,
	33,1,41,9,49,17,57,25};

int ls_count[16]={1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1};


static void des_expand(utype *dst, const utype *src)
{
	int i;

	register utype c;

	for (i = 0; i < 8; ++i)
	{
		c = src[i];

		*dst++ = (c >> 7) & 1;
		*dst++ = (c >> 6) & 1;
		*dst++ = (c >> 5) & 1;
		*dst++ = (c >> 4) & 1;
		*dst++ = (c >> 3) & 1;
		*dst++ = (c >> 2) & 1;
		*dst++ = (c >> 1) & 1;
		*dst++ = (c)      & 1;
	}
}

static void des_ls(utype *dst, const utype *src, int count)
{
	int i;

	// for (i = 0; i < 28; ++i)
	for (i = 0; i < 7; ++i)
	{
		dst[i]      = src[(i + count) % 28];
		dst[i + 7]  = src[(i + 7 + count) % 28];
		dst[i + 14] = src[(i + 14 + count) % 28];
		dst[i + 21] = src[(i + 21 + count) % 28];
	}
}

static void des_son(utype *k, const utype *cc, const utype *d)
{
	int i;
	char buf[56];

	//for (i = 0; i < 28; ++i)
	//{
	//	buf[i] = (char)*cc++;

	//	buf[i + 28] = (char)*d++;
	//}
	memcpy(buf, cc, 28 * sizeof(char));
	memcpy(buf + 28, d, 28 * sizeof(char));

	for (i = 0; i < 8; ++i)
	{
		*(k + i)      = (utype)buf[pc_2[i] - 1];
		*(k + i + 8)  = (utype)buf[pc_2[i + 8] - 1];
		*(k + i + 16) = (utype)buf[pc_2[i + 16] - 1];
		*(k + i + 24) = (utype)buf[pc_2[i + 24] - 1];
		*(k + i + 32) = (utype)buf[pc_2[i + 32] - 1];
		*(k + i + 40) = (utype)buf[pc_2[i + 40] - 1];
	}
}

static void des_set_key(utype K[17][48], const utype *key)
{
	utype CCC[17][28] = {0};
	utype D[17][28] = {0};

	int i, j;

	for (i = 0; i < 28; ++i)
	{
		CCC[0][i] = key[pc_1_c[i] - 1];

		D[0][i] = key[pc_1_d[i] - 1];
	}

	for (j = 0; j < 16; ++j)
	{
		des_ls(CCC[j + 1], CCC[j], ls_count[j]);
		des_ls(D[j + 1], D[j], ls_count[j]);

		des_son(K[j + 1], CCC[j + 1], D[j + 1]);
	}
}

static void des_compress(utype *dst, utype *src)
{
	int i;
	register utype c;

	for (i = 0; i < 8; ++i)
	{
		c  = ((*src++) << 7);
		c += ((*src++) << 6);
		c += ((*src++) << 5);
		c += ((*src++) << 4);
		c += ((*src++) << 3);
		c += ((*src++) << 2);
		c += ((*src++) << 1);
		c += ((*src++));

		dst[i] = c;
	}
}

static void des_ip(utype *l, utype *r, const utype *txt)
{
	int i;
	utype buf[64];

	des_expand(buf, txt);


	for (i = 0; i < 8; ++i)
	{
		l[i] = buf[ip_tab[i] - 1];
		r[i] = buf[ip_tab[i + 32] - 1];

		l[i + 8] = buf[ip_tab[i + 8] - 1];
		r[i + 8] = buf[ip_tab[i + 8 + 32] - 1];

		l[i + 16] = buf[ip_tab[i + 16] - 1];
		r[i + 16] = buf[ip_tab[i + 16 + 32] - 1];

		l[i + 24] = buf[ip_tab[i + 24] - 1];
		r[i + 24] = buf[ip_tab[i + 24 + 32] - 1];
	}
}

static void des__ip(utype *txt, const utype *l, const utype *r)
{
	int i;
	char buf[64];

	//for (i = 0; i < 32; ++i)
	//{
	//	buf[i] = (char)l[i];

	//	buf[i + 32] = (char)r[i];
	//}
	memcpy(buf, l, 32 * sizeof(char));
	memcpy(buf + 32, r, 32 * sizeof(char));


	for (i = 0; i < 8; ++i)
	{
		txt[i] = (utype)buf[_ip_tab[i] - 1];
		txt[i + 8] = (utype)buf[_ip_tab[i + 8] - 1];
		txt[i + 16] = (utype)buf[_ip_tab[i + 16] - 1];
		txt[i + 24] = (utype)buf[_ip_tab[i + 24] - 1];
		txt[i + 32] = (utype)buf[_ip_tab[i + 32] - 1];
		txt[i + 40] = (utype)buf[_ip_tab[i + 40] - 1];
		txt[i + 48] = (utype)buf[_ip_tab[i + 48] - 1];
		txt[i + 56] = (utype)buf[_ip_tab[i + 56] - 1];
	}
}

static void des_s_box(utype *dst, const utype *src)
{
	int i, j, k, m;
	int y, z;
	utype buf[8];

	m = 0;

	for (i = 0; i < 8; ++i)
	{
		j = 6 * i;

		y = src[j] * 2 + src[j + 5];
		z = src[j + 1] * 8 + src[j + 2] * 4 + src[j + 3] * 2 + src[j + 4];

		buf[i] = (utype)SSS[i][y][z];

		y = 0x08;

		for (k = 0; k < 4; ++k)
		{
			dst[m++] = (buf[i] / y) & 1;

			y /= 2;
		}
	}
}

static void des_f(utype *L, utype *R, 
	const utype *l, utype K[17][48],
	const utype *r, int n)
{
	register int i, j;
	register int y, z;

	register utype c;
	utype buf[DEF_BUF_LEN];

	for (i = 0; i < 8; ++i)
	{
		j  = 6 * i;

		y  = (((r[e_r[j]    ] ^ K[n][j])    ) << 1);
		y |= ( (r[e_r[j + 5]] ^ K[n][j + 5]));

		z  = (((r[e_r[j + 1]] ^ K[n][j + 1])) << 3);
		z |= (((r[e_r[j + 2]] ^ K[n][j + 2])) << 2);
		z |= (((r[e_r[j + 3]] ^ K[n][j + 3])) << 1);
		z |= ( (r[e_r[j + 4]] ^ K[n][j + 4]));

		c  = SSS[i][y][z];

		*(int*)(buf + 4 * i) = (((c)      & 1) << 24) | 
							   (((c >> 1) & 1) << 16) | 
							   (((c >> 2) & 1) <<  8) | 
							   ( (c >> 3) & 1);
		//k          = i << 2;

		//buf[k]     = (c >> 3) & 1;
		//buf[k + 1] = (c >> 2) & 1;
		//buf[k + 2] = (c >> 1) & 1;
		//buf[k + 3] = (c)      & 1;
	}

	for (i = 0; i < 8; ++i)
	{
		j    = i << 2;

		//*R++ = buf[P[j]] ^ l[j];
		//*R++ = buf[P[j + 1]] ^ l[j + 1];
		//*R++ = buf[P[j + 2]] ^ l[j + 2];
		//*R++ = buf[P[j + 3]] ^ l[j + 3];
		
		*(int*)(R + j) = (((buf[P[j + 3]] ^ l[j + 3])) << 24) |
						 (((buf[P[j + 2]] ^ l[j + 2])) << 16) |
						 (((buf[P[j + 1]] ^ l[j + 1])) <<  8) |
						 (((buf[P[j]    ] ^ l[j])    ));
	}
}

static void des_encrypt(utype *cry, const utype *pln, utype K[17][48])
{
	utype l[DEF_BUF_LEN], r[DEF_BUF_LEN];
	utype L[DEF_BUF_LEN], R[DEF_BUF_LEN];
	utype tmp[DEF_BUF_LEN];

	int i;

	des_ip(l, r, pln);

	for (i = 1; i < 9; ++i)
	{
		des_f(L, R, l, K, r, 2 * i - 1);

		memcpy(l, r, 32 * sizeof(utype));
		memcpy(r, R, 32 * sizeof(utype));

		des_f(L, R, l, K, r, 2 * i);

		memcpy(l, r, 32 * sizeof(utype));
		memcpy(r, R, 32 * sizeof(utype));
	}

	des__ip(tmp, r, l);

	des_compress(cry, tmp);
}

static void des_discrypt(utype *pln, const utype *cry, utype K[17][48])
{
	utype l[DEF_BUF_LEN], r[DEF_BUF_LEN];
	utype L[DEF_BUF_LEN], R[DEF_BUF_LEN];
	utype tmp[DEF_BUF_LEN];

	int i;

	des_ip(l, r, cry);

	for (i = 8; 0 < i; --i)
	{
		des_f(L, R, l, K, r, 2 * i);

		memcpy(l, r, 32 * sizeof(utype));
		memcpy(r, R, 32 * sizeof(utype));

		des_f(L, R, l, K, r, 2 * i - 1);

		memcpy(l, r, 32 * sizeof(utype));
		memcpy(r, R, 32 * sizeof(utype));
	}

	des__ip(tmp, r, l);

	des_compress(pln, tmp);
}

void des_base(utype *oDat, const utype *iDat, const utype *key, int flag)
{
	utype K[17][48];
	utype tmp[DEF_BUF_LEN];

	des_expand(tmp, key);

	des_set_key(K, tmp);

	if (DES_ENCRYPT == flag)
	{
		des_encrypt(oDat, iDat, K);
	}
	else
	{
		des_discrypt(oDat, iDat, K);
	}
}

int __1des(char *oDat, const char *iDat, const char *key, int flag)
{
	utype bkey[DEF_3DES_LNE] = {0};
	utype bIDat[DEF_3DES_LNE] = {0};
	utype bODat[DEF_3DES_LNE] = {0};

	int len;

	asc2bcd(bkey, key, strlen(key));
	len = asc2bcd(bIDat, iDat, strlen(iDat));

	des_base(bODat, bIDat, bkey, flag);

	return bcd2asc(oDat, bODat, len);
}

static int __3des(char *oDat, const char *iDat, const char *key, int flag)
{
	utype bkey1[UNIT_KEY_LEN] = {0}, bkey2[UNIT_KEY_LEN] = {0};
	utype bIDat[UNIT_KEY_LEN] = {0};
	utype bODat1[UNIT_KEY_LEN] = {0}, bODat2[UNIT_KEY_LEN] = {0}, bODat3[UNIT_KEY_LEN] = {0};

	int uflag = (DES_ENCRYPT == flag ? DES_DECRYPT : DES_ENCRYPT);

	asc2bcd(bkey1, key, 16);
	asc2bcd(bkey2, key + 16, 16);

	asc2bcd(bIDat, iDat, 16);

	des_base(bODat1, bIDat, bkey1, flag);
	des_base(bODat2, bODat1, bkey2, uflag);
	des_base(bODat3, bODat2, bkey1, flag);

	return bcd2asc(oDat, bODat3, UNIT_KEY_LEN);
}

static int __3des__(char *oDat, const char *iDat, utype bkey1[17][48], utype bkey2[17][48], int flag)
{
	utype bIDat[UNIT_KEY_LEN] = {0}, bODat3[UNIT_KEY_LEN] = {0};

	utype l[DEF_BUF_LEN], r[DEF_BUF_LEN];
	utype L[DEF_BUF_LEN], R[DEF_BUF_LEN];
	utype tmp[DEF_BUF_LEN];

	int j, i;

	asc2bcd(bIDat, iDat, 16);

	des_ip(l, r, bIDat);

	for (j = 1; j <= 3; ++j)
	{
		if (DES_ENCRYPT == flag)
		{
			for (i = 1; i < 9; ++i)
			{
				des_f(L, R, l, ((j % 2 == 0) ? bkey2 : bkey1), r, 2 * i - 1);

				memcpy(l, r, 32 * sizeof(utype));
				memcpy(r, R, 32 * sizeof(utype));

				des_f(L, R, l, ((j % 2 == 0) ? bkey2 : bkey1), r, 2 * i);

				memcpy(l, r, 32 * sizeof(utype));
				memcpy(r, R, 32 * sizeof(utype));
			}
		}
		else
		{
			for (i = 8; 0 < i; --i)
			{
				des_f(L, R, l, ((j % 2 == 0) ? bkey2 : bkey1), r, 2 * i);

				memcpy(l, r, 32 * sizeof(utype));
				memcpy(r, R, 32 * sizeof(utype));

				des_f(L, R, l, ((j % 2 == 0) ? bkey2 : bkey1), r, 2 * i - 1);

				memcpy(l, r, 32 * sizeof(utype));
				memcpy(r, R, 32 * sizeof(utype));
			}
		}

		if (j + 1 <= 3)
		{
			memcpy(R, l, 32 * sizeof(utype));
			memcpy(l, r, 32 * sizeof(utype));
			memcpy(r, R, 32 * sizeof(utype));
		}

		flag = (DES_ENCRYPT == flag ? DES_DECRYPT : DES_ENCRYPT);
	}

	des__ip(tmp, r, l);

	des_compress(bODat3, tmp);

	return bcd2asc(oDat, bODat3, UNIT_KEY_LEN);
}

static int __ecb(char *oDat, const char *iDat, const char *key, int flag)
{
	int oDat_offset = 0;

	char bIDat[UNIT_1DES_KEY_LNE + 1] = {0};
	int iDat_len = 0, iDat_offset = 0;

	char bkey[DEF_3DES_LNE + 1] = {0};
	int key_len;

	utype bkey1[UNIT_KEY_LEN] = {0}, bkey2[UNIT_KEY_LEN] = {0};
	utype K1[17][48], K2[17][48];
	utype tmp[DEF_BUF_LEN];

	int i, ret = 0;

	if (NULL == oDat || NULL == iDat || NULL == key)
	{
		return SM_CMM_BAD_PARAM;
	}

	key_len = (int)strlen(key);
	if (UNIT_1DES_KEY_LNE != key_len && 
		UNIT_3DES_KEY_LEN != key_len)
	{
		return SM_DES_KEY_LEN;
	}

	iDat_len = (int)strlen(iDat);
	if (0 != iDat_len % UNIT_1DES_KEY_LNE)
	{
		return SM_DES_DAT_LEN;
	}

	str_toupper(bkey, key, (size_t)key_len);

	iDat_offset = 0;
	oDat_offset = 0;

	if (32 == key_len)
	{
		asc2bcd(bkey1, bkey, 16);
		asc2bcd(bkey2, bkey + 16, 16);

		des_expand(tmp, bkey1);
		des_set_key(K1, tmp);

		des_expand(tmp, bkey2);
		des_set_key(K2, tmp);
	}


	for (i = 0; i < iDat_len / 16; ++i)
	{
		str_toupper(bIDat, iDat + iDat_offset, UNIT_1DES_KEY_LNE);

		if (16 == key_len)
		{
			ret = __1des(oDat + oDat_offset, bIDat, bkey, flag);
			if (0 > ret)
			{
				return ret;
			}
		}
		else
		{
			ret = __3des__(oDat + oDat_offset, bIDat, K1, K2, flag);

			if (0 > ret)
			{
				return ret;
			}
		}

		oDat_offset += ret;
		iDat_offset += ret;
	}

	return oDat_offset;
}

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
int ecb_encrypt(char *cry, const char *pln, const char *key)
{
	return __ecb(cry, pln, key, DES_ENCRYPT);
}

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
int ecb_decrypt(char *pln, const char *cry, const char *key)
{
	return __ecb(pln, cry, key, DES_DECRYPT);
}
