import numpy as np
import os
import matplotlib.pyplot as plt

def list_files(directory):
    files = []
    for file in os.listdir(directory):
        if file.endswith(".dat"):
            files.append(os.path.join
            (directory, file))
    return files
    

def extract_para(file_path):
    altitude_array = []
    signal_array = []
    start_reading = False
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith('km'):
                start_reading = True
                continue
            
            if start_reading:
                columns = line.strip().split()
                if columns:
                    try:
                        altitude = float(columns[0])  # First column as altitude
                        signal = float(columns[1])    # Second column as signal
                        altitude_array.append(altitude)
                        signal_array.append(signal)
                    except (ValueError, IndexError):
                        continue
                    
    return np.array(altitude_array), np.array(signal_array)

if __name__ == "__main__":
    directory = "D:\\paper2\\data\\Na\\20250101\\Na"
    files = list_files(directory)
    for file in files:
        altitude, signal = extract_para(file)
    
        # plot the Na lidar data
        plt.semilogy(altitude, signal)
        plt.ylabel('Signal')
        plt.xlabel('Altitude (km)')
        plt.show()
        plt.grid()
        plt.close()