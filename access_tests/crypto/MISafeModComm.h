#ifndef _MISAFEMODCOMM_H
#define _MISAFEMODCOMM_H

#include <stdint.h>
#include <iostream>
using namespace std;

const int32_t SAFEMOD_OK  = 0;
const int32_t SAFEMOD_ERR = -1;

const int32_t SAFEMOD_DATALEN = 8;

const int32_t SAFEMOD_HEXLEN  = 2;  // Hex Len
const int32_t SAFEMOD_MD5LEN  = 32; // MD5 Len 
const int32_t SAFEMOD_HEADLEN = 4;  // 包头长度
const int32_t SAFEMOD_MACLEN  = 8;  // MAC长度

#define MAXKEY    "B0FB83E39A5EBFAABE471362A58393FF"
#define TRANSKEY  "F7A72DE7D6264530F01BA49BC73EB873"

inline int32_t AscToHex(string &strHex, const char *pAsc, int32_t iLenAsc)
{
    char szTemp[9] = {0};
    int32_t iRev = SAFEMOD_OK;

    for (int32_t i = 0; i < iLenAsc; i++)
    {
        unsigned char cTemp = pAsc[i];
        sprintf(szTemp, "%02x", cTemp);
        strHex += szTemp;
    }

    return iRev;
}

inline int32_t HexToAsc(string strHex, char *pAsc, int32_t &iLenAsc)
{
    int32_t iTempAsc = 0;
    int32_t iRev = SAFEMOD_ERR;
    int32_t iLen = strHex.length();
    char szTemp[3] = {0};

    if ( (iLen % SAFEMOD_HEXLEN) == 0 && iLenAsc >= (iLen / 2) )
    {
        for (int32_t i = 0; i < iLen; i+=2)
        {
            szTemp[0] = strHex[i];
            szTemp[1] = strHex[i+1];
            char *pEnd;
            pAsc[iTempAsc] = (char)strtol(szTemp, &pEnd, 16);
            //sscanf(szTemp,  "%02x", &pAsc[iTempAsc]);
            iTempAsc++;
        }

        iRev = SAFEMOD_OK;
    }

    return iRev;
}
#endif