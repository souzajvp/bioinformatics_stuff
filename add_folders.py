#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 17:26:54 2021

@author: joao-souza
"""

# Imports
import os
import shutil

'''
Script to input the folder name into sdf files in the current folder. That is helpful for future
identifications of top hit molecules.

Returns new files with the addition of "_foldername" to file names.
'''


def get_curr_directory_top_sdf():
    """ 
    Gets current directory, creates a list of .sdf files
    in current directory
    """
    files_path = os.getcwd()
    file_list = []
    for filename in os.listdir(files_path):
        if filename.startswith("top50"):
            file_list.append(filename)
    return file_list   


def modify_sdf():
    file_list = get_curr_directory_top_sdf()
    for i in file_list:
        # folder = i[-8:-4]
        for sdf_file in file_list:
            folder = sdf_file[-8:-4]
            with open(sdf_file, 'r') as temp_file:
                with open(sdf_file[:-4]+'_foldername.sdf', 'w') as processed_file:
                    for line in temp_file:
                        if line.startswith('$$$$'):
                            processed_file.write('>  <folder_name>\n')
                            processed_file.write(folder)
                            processed_file.write('\n')
                            processed_file.write('\n')
                            processed_file.write('$$$$\n')
                        else:
                            processed_file.write(line)
                    
    
                            
                
modify_sdf()




