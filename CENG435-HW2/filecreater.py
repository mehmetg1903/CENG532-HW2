import os

f = open('deneme.bin','wb')

for i in range(10*1000*1000):
    f.write(str(i%10))
f.close();
