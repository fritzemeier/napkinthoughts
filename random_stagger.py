import random

i = 0

while i <= 100:

	j = random.randint(1,3) * 10
	k = random.randint(0,j)

	print(i)
	print(k)
	print(j)
	print("--------------------")
	i = i+k


