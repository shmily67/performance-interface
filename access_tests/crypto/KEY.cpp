#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#include "cmm.h"
#include "SafeMInterface.h"
#ifdef WIN32
#include <Windows.h>
#else
#include <sys/time.h>
#endif

// 得到计算机启动到现在的时钟周期
static I64 getCPUCycleCount()
{
    
#ifdef WIN32
    LARGE_INTEGER nFreq;
    LARGE_INTEGER lastTime;

    if (!QueryPerformanceFrequency(&nFreq))
    {
        return 0;
    }

    QueryPerformanceCounter(&lastTime); 
    return I64(lastTime.QuadPart);

    
#else
	struct timeval t;
	
	gettimeofday(&t, NULL);
	
	return t.tv_usec;

#endif // _WIN32
}

bool rand_key(char *key, size_t len)
{
	size_t i;
	int c;

	srand((unsigned)getCPUCycleCount());

	for (i = 0; i < len; ++i)
	{
		c = abs(rand() % 16);

		if (10 <= c)
		{
			c = 'A' + (c - 10);
		}
		else
		{
			c = '0' + c;
		}

		key[i] = c;
	}

	return true;
}
