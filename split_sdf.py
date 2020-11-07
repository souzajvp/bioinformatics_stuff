########################################################
f = input('Input file name (without extension):')
split_number = int(input('Desired number of molecules in each file:')) 

########################################################

number_of_sdfs = split_number
i=0
j=0
count = []
f2=open(f+'_'+str(j)+'.sdf','w')
for line in open(f+'.sdf'):
	f2.write(line)
	if line[:4] == "$$$$":
		i+=1
	if i > number_of_sdfs:
		count.append(i)
		number_of_sdfs += split_number 
		f2.close()
		j+=1
		f2=open(f+'_'+str(j)+'.sdf','w')

for g in range(len(count)):
	if g == 0:
		print(f"The {f}_{str(g)}.sdf file contains {count[g]} molecules")
	else:
		print(f"The {f}_{str(g)}.sdf file contains {count[g]-count[g-1]} molecules")

print('The total number of molecules in the original file was', i)
print(f'You have just split {f}.sdf into chunks of {split_number} molecules')



