### USAGE ###
# Executing this python script will prompt the user two times for inputs:
# 1. First, type the .sdf file name you want to split (without the .sdf extension);
# 2. Second, type the ammount of molecules you want to split into each file;

# The script will result in a number of files having an additional "_n" after the original filename prefix.

### Example: 
##### input file name                 = molecules.sdf
##### number of molecules to split    = 100.000
##### n. of mol. in the original file = 300.000
##### OUTPUT = three files, namely "molecules_0.sdf", "molecules_1.sdf", "molecules_2.sdf" with 100.000 molecules in each of them.

# At the end of splitting, the script will print:
# 1. The name of each output file and the ammount of molecules on them;
# 2. The ammount of molecules on the original input file;
# 3. A summary of the operation


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



