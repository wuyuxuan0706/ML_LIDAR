import h5py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def altitude_array(channel, length):
    """
    Generate an array of altitudes based on the channel and length. 
    """
    match channel:
        case "Na":
            return np.linspace(0.031, 0.031 * (length - 1), length)
        case "K":
            return np.linspace(0, 0.031 * (length - 1), length)
        case "Ca":
            return np.linspace(0, 0.031 * (length - 1), length)
        case "Fe":  
            return np.linspace(0, 0.031 * (length - 1), length)
        case _:
            raise ValueError("Unsupported channel type.")
        

if __name__ == "__main__":
    
    channel = "Na"
    # Load the HDF5 file
    hdf5_file = h5py.File(r"D:\paper2\code\datasets\Na.h5", 'r')
    
    # Read the data from the HDF5 file
    data = hdf5_file["signals"][:]
    print(data.shape)
    Time = hdf5_file["times"][:]
    # Close the HDF5 file
    hdf5_file.close()
    
    altitude_array = altitude_array("Na", data.shape[1])
    # Plot the data
    plt.semilogy(altitude_array, data[0, :])
    plt.title(Time[0].decode("utf-8"))
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.show()
    
    # k-means clustering
    # Elbow Method to find optimal k
    inertia = []
    for k in range(1, 11):  # Try k values from 1 to 10
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data)
        inertia.append(kmeans.inertia_)

    plt.plot(range(1, 11), inertia, marker='o')
    plt.title("Elbow Method")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Inertia")
    plt.show()


    
