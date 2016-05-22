import hashlib, random, binascii
from Crypto.Cipher import AES
from nose.tools import *

class openssl_aes:
    def gen_keyiv(self, passwd, salt, bits):
        data00 = passwd + salt
        result = ''
        keymaterial = []
        loop = 0
        keymaterial.append(data00)

        for i in range(3): # 3 for openssl
            if i == 0:
                result = data00
            else:
                result += data00
            for c in range(1): # 1 for openssl
                result = hashlib.md5(result).digest()
                keymaterial.append(result)
        if bits == 256:
            self.key = keymaterial[1] + keymaterial[2]
            self.iv = keymaterial[3]
        elif bits == 192:
            self.key = keymaterial[1] + keymaterial[2][0:8]
            self.iv = keymaterial[3]
        else:
            self.key = keymaterial[1]
            self.iv = keymaterial[2]

    def decrypt(self, ct, passwd, bits=256):
        salt = ct[8:16]
        cb = ct[16:]
        self.gen_keyiv(passwd,salt,bits)

        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        pt = aes.decrypt(cb)
        l=len(pt)
        trail=ord(pt[(l-1)])
        return pt[0:l-trail-1]

    def encrypt(self, pt, passwd, salt, bits=256):
        print 'passwd=', passwd
        print 'salt=', binascii.b2a_hex(salt)
        
        self.gen_keyiv(passwd, salt, bits)
        key, iv = self.key, self.iv
        #key, iv = EVP_ByteToKey(passwd, salt, 32, 16)
        print 'key=', binascii.b2a_hex(key)
        print 'iv=', binascii.b2a_hex(iv)
        aes = AES.new(key, AES.MODE_CBC, iv)

        #A0_PAD
        char =aes.block_size-((len(pt)+1)%aes.block_size);
        pt += chr(10)
        for i in range(char):
            pt  += chr(char)
        ct = aes.encrypt(pt)
        ct = 'Salted__%s%s' % (salt, ct)
        return ct

def EVP_ByteToKey(password, salt, key_len, iv_len): # the same as gen_keyiv
    #key_len is 32 and iv_len is 16 for AES-256. The function returns the key and the IV
    dtot = hashlib.md5(password + salt).digest()
    d = [ dtot ]
    while len(dtot) < (iv_len+key_len):
        d.append(hashlib.md5(d[-1] + password + salt).digest() )
        dtot += d[-1]
    return dtot[:key_len], dtot[key_len:key_len+iv_len]

def rands(l, m=0, M=255, uflag=False):
    fchr= unichr if uflag or M>255 else chr
    n   = M-m+1
    s   = ''
    for i in range(l):
        s += fchr(random.randint(0, 2147483647)%n+m)
    return s

def main():
    oaes = openssl_aes()
    passwd = '123456'
    
    s_ct='6153746c64655f5f0201040306050807bc9220ab6c07501cd47ea4af7d9eaa7faeff1400a6cd6147d69ed4ed48f144b4'
    ct = binascii.a2b_hex(s_ct)
    pt = oaes.decrypt(ct, passwd, 128)
    print pt
    
    return
    
    pt = 'The answer is no'
    #ct = oaes.encrypt(pt, '\x01\x02\x03\x04\x05\x06\x07\x08', passwd)
    ct = oaes.encrypt(pt, passwd, '\x01\x02\x03\x04\x05\x06\x07\x08', 128)
    #pt2 = oaes.decrypt(ct, passwd)
    #print "'" + pt2 + "'"
    #eq_(pt, pt2)
    s = binascii.b2a_hex(ct)
    s2, i, j = '', 4, 0
    while i < len(s):
        s2 += s[i-4: i] + ' '
        i += 4
        j += 1
        if 8 == j:
            j = 0
            s2 += '\n'
    print s2
    return
    
    for i in range(100):
        passwd = rands(32)
        l = random.randint(0, 256)
        pt = rands(l)

        ct = oaes.encrypt(pt, passwd)
        pt2 = oaes.decrypt(ct, passwd)
        if pt2!= pt:
            print 'x',
        else:
            print '.',
    print '\n-'
    for i in range(100):
        passwd  = rands(32)
        l       = random.randint(0, 256)
        pt      = rands(l, M=0xffff)

        ct      = oaes.encrypt(pt.encode('utf8'), passwd)
        pt2     = oaes.decrypt(ct, passwd)
        if pt2.decode('utf8')!= pt:
            print 'x',
        else:
            print '.',

if __name__ == "__main__":
    main()
            