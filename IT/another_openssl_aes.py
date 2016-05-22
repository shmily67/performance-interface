import hashlib, binascii, os, random
from Crypto.Cipher import AES
from Crypto import Random
from nose.tools import *

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(pt, password, key_length=32, salt=None): #32->256bits, 16->128bits
    bs = AES.block_size #16
    if None == salt:
        salt = Random.new().read(bs - len('Salted__'))
    else:
        assert_is_instance(salt, str)
        eq_(bs-8, len(salt))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    print 'key=', binascii.b2a_hex(key)
    print 'iv=', binascii.b2a_hex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    finished = False
    ct, offset = 'Salted__' + salt, 0
    while not finished:
        chunk = pt[offset:offset+1024*bs]
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        ct += cipher.encrypt(chunk)
        offset += 1024*bs
    return ct

def decrypt(ct, password, key_length=32): #32->256bits, 16->128bits
    bs = AES.block_size
    salt = ct[len('Salted__'):bs]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    #print 'key=', binascii.b2a_hex(key)
    #print 'iv=', binascii.b2a_hex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    pt, offset = '', bs
    while not finished:
        s = ct[offset:offset+1024*bs]
        chunk, next_chunk = next_chunk, cipher.decrypt(s)
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        #out_file.write(chunk)
        pt += chunk
        offset += 1024*bs
    return pt

def test_decrypt():
    pt = 'This is abcdefgh'
    password = '123456'    
    salt = '\x01\x02\x03\x04\x05\x06\x07\x08'

    with open('ptf', 'w') as ptf:
        ptf.write(pt)
    os.system('openssl enc -e -in ptf -out ctf -aes-256-cbc -S %s -p -k %s'%(binascii.b2a_hex(salt), password))
    with open('ctf', 'rb') as ctf:
        ct = ctf.read()
        pt2 = decrypt(ct, password)
    print pt2
    eq_(pt, pt2)

def test_encrypt():    
    pt = 'This is abcdefgh'
    password = '123456'    
    salt = '\x01\x02\x03\x04\x05\x06\x07\x08'
    
    ct = encrypt(pt, password, salt)
    with open('ctf', 'wb') as ctf:
        ctf.write(ct)

    os.system('openssl enc -d -in ctf -out ptf2 -aes-256-cbc -p -k %s'%password)
    with open('ptf2', 'rb') as f:
        pt2 = f.read()
    eq_(pt, pt2)
    
def step_encrypt():
    pt = ''
    for i in range(16):
        pt += chr(random.randint(0, 255)) 
    password = ''
    for i in range(8):
        password += chr(random.randint(48, 57)) #'0'-'9'
    salt = ''
    for i in range(8):
        salt += chr(random.randint(0, 255)) 
    
    ct = encrypt(pt, password, salt)
    with open('ctf', 'wb') as f:
        f.write(ct)

    os.system('openssl enc -d -in ctf -out ptf2 -aes-256-cbc -p -k %s'%password)
    with open('ptf2', 'r') as f:
        pt2 = f.read()
    eq_(pt, pt2)


def loop_test_encrypt():
    for i in range(10):
        print 'loop-%d'%i
        yield step_encrypt

def step_decrypt():
    pt = ''
    for i in range(16):
        pt += chr(random.randint(0, 255))
    password = ''
    for i in range(8):
        password += chr(random.randint(48, 57)) #48-57, 65-122)) #'A'-'z'
    salt = ''
    for i in range(8):
        salt += chr(random.randint(0, 255))

    with open('ptf', 'w') as f:
        f.write(pt)
    os.system('openssl enc -e -in ptf -out ctf -aes-256-cbc -S %s -p -k %s'%(binascii.b2a_hex(salt), password))
    
    with open('ctf', 'rb') as ctf:
        ct = ctf.read()
        pt2 = decrypt(ct, password)
    eq_(pt, pt2)

def loop_test_decrypt():
    for i in range(10):
        print 'loop-%d'%i
        yield step_decrypt

def openssl_loop_write():
    fw = open('ct_data_list', 'w')
    for i in range(10):
        pt = ''
        for i in range(16):
            pt += chr(random.randint(0, 255))
        fw.write('\n\n'+binascii.b2a_hex(pt)+'\n')

        password = ''
        for i in range(8):
            password += chr(random.randint(48, 57)) #48-57, 65-122)) #'A'-'z'
        fw.write(password+'\n')

        salt = ''
        for i in range(8):
            salt += chr(random.randint(0, 255))
        fw.write(binascii.b2a_hex(salt)+'\n')

        with open('ptf', 'w') as f:
            f.write(pt)
        os.system('openssl enc -e -in ptf -out ctf -aes-256-cbc -S %s -p -k %s'%(binascii.b2a_hex(salt), password))
    
        with open('ctf', 'rb') as ctf:
            ct = ctf.read()
            fw.write(binascii.b2a_hex(ct))
    fw.close()

def python_loop_write():
    fw = open('py2ssl_data_list', 'w')
    for i in range(10):
        pt = ''
        for i in range(16):
            pt += chr(random.randint(0, 255))
        fw.write('\n\n'+binascii.b2a_hex(pt)+'\n')

        password = ''
        for i in range(8):
            password += chr(random.randint(48, 57)) #48-57, 65-122)) #'A'-'z'
        fw.write(password+'\n')

        salt = ''
        for i in range(8):
            salt += chr(random.randint(0, 255))
        fw.write(binascii.b2a_hex(salt)+'\n')

        ct = encrypt(pt, password, salt)
        fw.write(binascii.b2a_hex(ct))
    fw.close()

def test_decrypt_to_openssl_ct():
    f = open('ct_data_list', 'r')
    line = f.readline()
    while line:
        line = f.readline()
        if '' == line: break
        eq_('\n', line)        
        pt = f.readline().rstrip()
        print 'pt=', pt
        pt = binascii.a2b_hex(pt)
        password = f.readline().rstrip()
        print 'password=', password
        salt = f.readline().rstrip()
        print 'salt=', salt
        salt = binascii.a2b_hex(salt)
        ct = f.readline().rstrip()
        print 'ct=', ct
        ct = binascii.a2b_hex(ct)
        pt2 = decrypt(ct, password)
        eq_(pt, pt2)        
    f.close()

if '__main__' == __name__:
    #openssl_loop_write()
    python_loop_write()

