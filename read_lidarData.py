import numpy 
import os 
import struct as st

def extract_para(file_path):
    file_path = os.listdir(file_path)
    print(file_path)
    
if "__name__" == "__main__":
    extract_para("/Users/siohbon/paper2/Data/Na20250314114647531.dat")