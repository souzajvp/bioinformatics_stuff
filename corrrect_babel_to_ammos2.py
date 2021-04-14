#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Dec 18 2020

---Step 3/3 on file preparation for AMMOS2 post-docking analysis

This python script is designed to reformat the output .mol2 files from openbabel,
so they can be read by AMMOS2 webserver.

---STEPS FOR COMPLETION:
    1. rm_lone_pairs_ammos2.py script;
    2. **Manual operation**OpenBabel mol2 file conversion using GASTEIGER 
    charges and individual output;
    3. This script
    
---DESCRIPTION OF THIS SCRIPT
    1. Identifies .mol2 files from the OpenBabel output;
    2. Makes the necessary changes for every line;
    3. Generates new ligxx_topxx_xxK.mol2 files.
    
    NOTE: this script is built to work with any ammount of files and in
    any directory (as long as the script file is in the babel folder)
    
    

v1  - Error and minimal file corrections
@author: João Vítor Perez de Souza - /souzajvp on GitHub

REQUIREMENTS
    1. Python 3.8 or similar;
    2. os module;
    3. shutil module;
    4. The script file MUST be in present in the same folder as the babel 
    output.

"""
# Imports
import os
from os.path import dirname
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
    for name in get_curr_directory_files_mol2():
        skip_start = None
        for n, line in enumerate(open(name,"r")):
            if "@<TRIPOS>BOND" in line: 
                end = n 
            if "@<TRIPOS>UNITY_ATOM_ATTR" in line: 
                skip_start = n  
        start = 7
        file = open(name, 'r').readlines()
        f_name = (f'{(file[1].split("|")[-2])}')  
        file[1] = (f'{(file[1].split("|")[0].split(" ")[0])}\n')
        # file[1] = (f'lig{int(name[:-5]) + 1}\n')
        for line in range(start,end):
            number = file[line][4:7].strip()
            element = file[line][8:9].strip()
            x_coor = file[line][18:26].strip()
            y_coor = file[line][28:36].strip()
            z_coor = file[line][38:46].strip()
            elem_num = file[line][48:51]
            charges = file[line][68:76].strip()
            if len(element+number) == 3:
                new_line = (f'{number:>7}  {element+number:<}{x_coor:>14}{y_coor:>10}{z_coor:>10}{element:>2}{elem_num}{"1  UNL1":>11}{charges:>14}\n')
            elif len(element+number) == 2:
                new_line = (f'{number:>7}  {element+number:<}{x_coor:>15}{y_coor:>10}{z_coor:>10}{element:>2}{elem_num}{"1  UNL1":>11}{charges:>14}\n')
            elif len(element+number) == 4:
                new_line = (f'{number:>7}  {element+number:<}{x_coor:>13}{y_coor:>10}{z_coor:>10}{element:>2}{elem_num}{"1  UNL1":>11}{charges:>14}\n')
            file[line] = new_line
        # cur_dir = os.getcwd()
        # prefix = dirname(dirname(cur_dir))[-11:]
        final_file = open(f_name +'_for_ammos2'+'.mol2', "w") # Rewrite file
        if skip_start:
            new_file = [file[i] for i in range(len(file)) if i not in [j for j in range(skip_start,end)]]
            final_file.writelines(new_file)
        else:   
            final_file.writelines(file)        
            final_file.close()

def execute_all_folders():
    folders  = ['100k', '200k', '242k', '347k', '452k', '470k']
    folder_paths = [f'/media/newhd/joao-souza/projects/aroD/chemical_libraries/virtual_screening/virtual_screening_analysis/hit_files/{i}/lone_pairs_ammos2/babel' for i in folders]
    for folder_name in folder_paths:
        os.chdir(folder_name)
        process_mol2_files() 
    
#     print(f'A total of {file_count} files were processed and moved to the --lone_pairs_ammos2-- folder')
######### Calling Functions #########

execute_all_folders()


# move_processed_files()

