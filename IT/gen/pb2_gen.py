import os

os.chdir('..\\proto')
for fname in os.listdir('.'):
    print fname
    if '.proto' == fname[-6:]:
        os.system('protoc -I=./ --python_out=./output ./%s '%fname)
    