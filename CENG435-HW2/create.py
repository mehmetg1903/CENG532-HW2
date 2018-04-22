import os
import random
import string

shire = open("deneme.bin","wb")


for i in range(10*1024*1024):
	shire.write(random.choice(string.letters))

shire.close()
