import os

### Functions
def get_curr_directory_files_mol2():
	""" Gets current directory, creates a list of .mol2 files
		in current directory
	"""
	files_path = os.getcwd()
	file_list = []
	for filename in os.listdir(files_path):
		if filename.endswith(".mol2"):
			file_list.append(filename)
	return file_list

def process_files():
	""" For each mol2 file in current directory:
	Finds what atoms are lone pairs, Finds what bonds come from lone pairs,
	Writes all lines, but the ones with bonds or atoms from lone pairs to a temporary file
	Opens the temporary file, gets each line into a list,
	Changes the 10th (11) to the correct atom and bond numbers
	Writes the final file.
	"""
	n_files = 0
	for name in get_curr_directory_files_mol2():
		n_files += 1
		lp_atoms = [] # List containing the Lone Pair Atom numbers
		bonds_12_15 = [] # List containing the Bond Numbers found using the ln_atoms in the right column
		bonds_2_5 = [] # List containing the Bond Numbers found using the ln_atoms in the left column
		na_removed = -1 # Variable to count how many atoms were removed. Starts with -1
		nb_removed = 0 # Variable to count how many bonds were removed
		temp_file = open(name[:-5]+'_processed'+'.mol2','w')
		for line in open(name, 'r'): # For each line in the original mol2 file,
			if line[8:12] == "****": # If that slice contains "****"
				lp_atoms.append(line[4:7]) # Add the atom numbers to lp_atoms
				na_removed +=1 
			elif line[12:15] in lp_atoms: # If the bond atoms are in the lp_atoms:
				bonds_12_15.append(line[12:15]) # If one wants to know what atoms were removed from the right column 
				# na_removed +=1 # Increase atom number by each one.
				nb_removed +=1 # Increase bond number by each one
			# elif line[2:5] in lp_atoms[:-1]: # Same as before, but working only with the left column
			# 	bonds_2_5.append(line[2:5]) 
			# 	nb_removed +=1
			else:
				temp_file.write(line) # Write all other lines that are not specified before.
		temp_file.close() # close file

		temp_file  = open(name[:-5]+'_processed'+'.mol2', 'r') # Open processed file to renumber atoms and bond numbers.
		list_lines = temp_file.readlines()
		list_lines[10] = (f'   {int(list_lines[10][3:6])-na_removed}   {int(list_lines[10][9:12])-nb_removed}     1\n')


		final_file = open(name[:-5]+'_processed'+'.mol2', "w") # Rewrite file

		final_file.writelines(list_lines)

		final_file.close()
	print(f'A total of {n_files} files were processed')


# Calling Functions

# print(len(get_curr_directory_files_mol2()))
get_curr_directory_files_mol2()
process_files()