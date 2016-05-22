#ifndef __CMM_H__
#define __CMM_H__


#ifdef __cplusplus
extern "C"
{
#endif // __cplusplus

#define UNIT_KEY_LEN		8
#define UNIT_1DES_KEY_LNE	16
#define UNIT_3DES_KEY_LEN	32
#define DEF_3DES_LNE		32
#define DEF_BUF_LEN			64

enum DES_DIRECT
{
	DES_ENCRYPT = 0, // º”√‹
	DES_DECRYPT = 1, // Ω‚√‹
};

// type def
typedef unsigned char utype;

#ifdef _WIN32
typedef __int64 I64;
#else
typedef long long I64;
#endif // _WIN32

int asc2bcd(utype *bcd, const char *asc, int len);
int bcd2asc(char *asc, const utype *bcd, int len);

int asc2hex(char *hex, const unsigned char *asc, size_t len);
int hex2asc(unsigned char *asc, const char *hex, size_t len);

void str_toupper(char *dst, const char *src, size_t len);


int bcd_xor(char *rst, const char *dat1, const char *dat2, size_t len);


#ifdef __cplusplus
};
#endif // __cplusplus

#endif // __CMM_H__
