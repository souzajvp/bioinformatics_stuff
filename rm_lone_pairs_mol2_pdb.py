"""
Created on Sun Dec 13 2020

This python script is designed to remove lone pairs atoms and bonds
   from .mol2 and corresponding .pdb files resulting from GOLD virtual screen protocols.
   Briefly, what it does is:
       1. Identifies .mol2 files, opens them, and writes only the lines
          not from LP to a new file, {filename}_processed.mol2;
       2. Matches the respective pdb and processed.mol2 files and inputs
          the correct atoms and coordinates into the pdb file, resulting
          in a new one, calle {filename}_processed.pdb;
       3. Finally, it creates a new directory --clean_LonePairs and moves
          all *_processed.mol2 and *_processed.pdb files to it.
       
    NOTE: this script is built to work with any ammount of files and in
    any directory (since the script file is in the same file as the results)

v0  - Baseline Version
@author: João Vítor Perez de Souza - /souzajvp on GitHub

REQUIREMENTS
    1. Python 3.8 or similar;
    2. os module;
    3. shutil module
    4. The script file MUST be in present in the same folder as the hits.

"""
# Imports
import os
import shutil


# Functions to remove lone pairs from .mol2 files.

def get_curr_directory_files_mol2():
    """ 
    Gets current directory, creates a list of .mol2 files
    in current directory
    """
    files_path = os.getcwd()
    file_list = []
    for filename in os.listdir(files_path):
        if filename.endswith(".mol2"):
            file_list.append(filename)
    return file_list   

def process_mol2_files():
    """ 
    For each mol2 file in current directory:
    Finds what atoms are lone pairs, Finds what bonds come from lone pairs,
    Changes the 10th (11) to the correct atom and bond numbers
    Writes all lines, but the ones with bonds or atoms from lone pairs to a 
    new {filename}_processed.mol2 file
    """
    n_files = 0
    for name in get_curr_directory_files_mol2():
        n_files += 1
        lp_atoms = [] # List containing the Lone Pair Atom numbers
        bonds_12_15 = [] # List containing the Bond Numbers found using the ln_atoms in the right column
        na_removed = 0 # Variable to count how many atoms were removed. Starts with -1
        nb_removed = 0 # Variable to count how many bonds were removed
        line_total = []
        for n, line in enumerate(open(name,"r")):
            # if "@<TRIPOS>ATOM" in line: 
            #     start = n
            if "@<TRIPOS>SUBSTRUCTURE" in line: 
                end = n 
        start = 16
        file = open(name, 'r').readlines()
        for line in range(start,end):
            if file[line][8:12] == "****": # If that slice contains "****"
                lp_atoms.append(file[line][4:7]) # Add the atom numbers to lp_atoms
                na_removed +=1 
                line_total.append(file[line])
            elif file[line][12:15] in lp_atoms: # If the bond atoms are in the lp_atoms:
                bonds_12_15.append(file[line][12:15]) # If one wants to know what atoms were removed from the right column 
                nb_removed +=1 # Increase bond number by each one
                line_total.append(file[line])
                
        final_file = open(name[:-5]+'_processed'+'.mol2', "w") # Rewrite file
        file[10] = (f'   {int(file[10][3:6])-na_removed}   {int(file[10][9:12])-nb_removed}     1\n')
        for i in line_total:
            file.remove(i)
        final_file.writelines(file)
                
        final_file.close()


### Functions to input the mol2 informatio into the pdb files
def get_curr_directory_files_mol2_pdb():
    """ 
    Gets current directory, creates a list of .mol2 and pdb files
    in current directory
    """
    files_path = os.getcwd()
    files  = []
    
    for filename in os.listdir(files_path):
        if filename.endswith("processed.mol2"):
            files.append(filename)
        for i in range(1,4):
            if filename.endswith(f"conf0{i}.pdb"):
                files.append(filename)

    return files

def count_pdb():
    """
    Counts how many pdb (protein) files are in the directory
    """
    files_path = os.getcwd()
    pdb = 0  
    for filename in os.listdir(files_path):
        for i in range(1,4):
            if filename.endswith(f"conf0{i}.pdb"):
                pdb += 1
    return pdb

def match_files():
    """
    Considering the results in the folder, creates a matrix of the format
    [[mol_number, mol_number_pdb, mol_number_mol2][...]], containing every file 
    name, colected before.
    """
    matrix = [[("00" + str(i)) if len(str(i)) == 1 else ('0' + str(i))] for i in range(1, count_pdb()+1)]
    for item in range(len(matrix)):
        for file in get_curr_directory_files_mol2_pdb():
            if file.startswith(matrix[item][0]):
                matrix[item].append(file)
    return matrix


def process_pdb_files():
    """
    Will read the file 'combos' inside the match_files function
    and will make the correct changes in the pdb, writing new pdb files as well.
    In the mol2 file, 4 decimal points are used for each xyz coordinates,
    I tried rounding the number to 3, but the function may round to 1 decimal
    if it's possible. Decided to just not select the last digit
    """
    for hit in match_files():
        if hit[1].endswith('.pdb'):
            protein = hit[1]
            ligand = hit[2]
        else:
            protein = hit[2]
            ligand = hit[1]
        ligand_lines = open(ligand, 'r').readlines()
        for n, line in enumerate(open(ligand,"r")):
            if "@<TRIPOS>BOND" in line: 
                end = n
        molecules = ''
        mol_lines = []
        start = 16
        for i in range(start,end):
            features = []
            features.append(ligand_lines[i][4:7].strip())
            features.append(ligand_lines[i][8:9].strip())
            features.append(ligand_lines[i][19:26].strip())
            features.append(ligand_lines[i][28:35].strip())
            features.append(ligand_lines[i][37:44].strip())
            molecules = (f"HETATM{features[0] :>5}{features[1]:>3}{'LIG':>6}{'1':>6}{features[2] :>12}{features[3] :>8}{features[4] :>8}{'  1.00  0.00'}{features[1]:>12}\n")
            mol_lines.append(molecules)   

        protein_lines = open(protein, 'r').readlines()
        final_file = open(f'{protein[:-4]}_processed.pdb', 'w')
        final_file.writelines(protein_lines[:2219])
        final_file.writelines(mol_lines)
        final_file.writelines('END')
        final_file.close()

            
def move_processed_files():
    """
    After all is done, creates a new directory and 
    moves all processed files to it
    """
    cur_dir = os.getcwd()
    try:
        os.mkdir('clean_LonePairs')
    except:
        shutil.rmtree(cur_dir+'/clean_LonePairs')
        os.mkdir('clean_LonePairs')
        
    file_count = 0
    for filename in os.listdir(cur_dir):
        if (filename.endswith('processed.pdb') or filename.endswith('processed.mol2')):
            shutil.move(cur_dir+'/' + filename, cur_dir+'/' +'clean_LonePairs/'+ filename)
            file_count +=1
    
    
    print(f'A total of {file_count} files were processed and moved to the --clean_LonePairs-- folder')
######### Calling Functions #########

process_mol2_files()

process_pdb_files()

move_processed_files()

