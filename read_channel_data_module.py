import os 
import numpy as np

def list_files(directory):
    """列出指定目录下的所有 .dat 文件"""
    files = []
    for file in os.listdir(directory):
        if file.endswith(".dat") or file.endswith(".TXT"):
            files.append(os.path.join(directory, file))
    return files

class Channel:
    def __init__(self, file_path, channel=""):
        if channel == "Na": 
            self.altitude, self.signal = self.Na_channel(file_path)
        elif channel == "Ca":
            self.altitude, self.signal = self.Ca_channel(file_path)
        elif channel == "K":
            self.altitude, self.signal = self.K_channel(file_path)
        elif channel == "Fe":
            self.altitude, self.signal = self.Fe_channel(file_path)
        else:
            raise ValueError(f"Unsupported channel: {channel}")

    def Na_channel(self, file_path):
        """提取Na通道数据"""
        na_path = os.path.join(file_path, "Na")
        if not os.path.exists(na_path):
            print(f"Path {na_path} does not exist.")
            return np.array([]), np.array([])

        dat_files = list_files(na_path)
        if not dat_files:
            print(f"No .dat files found in {na_path}.")
            return np.array([]), np.array([])

        altitude_array = []
        signal_array = []

        for dat_file in dat_files:
            start_reading = False
            altitude = []
            signal = []
            with open(dat_file, 'r') as file:
                for line in file:
                    if line.strip().startswith('km'):
                        start_reading = True
                        continue

                    if start_reading:
                        columns = line.strip().split()
                        if len(columns) >= 2:  # Ensure there are at least two columns
                            try:
                                altitude.append(float(columns[0]))  # 第一列作为高度
                                signal.append(float(columns[1]))    # 第二列作为信号
                            except ValueError:
                                print(f"Skipping invalid line in {dat_file}: {line.strip()}")
                                continue

            if altitude and signal:  # Ensure data is not empty
                altitude_array.append(altitude)
                signal_array.append(signal)

        return np.array(altitude_array), np.array(signal_array)
    
    def Ca_channel(self, file_path):
        """提取Ca通道数据"""
        subfolders = [os.path.join(file_path, f) for f in os.listdir(file_path) if os.path.isdir(os.path.join(file_path, f))]
        if not subfolders:
            print("No subfolders found.")
            return np.array([]), np.array([])

        combined_signal = None  # 用于存储所有子文件夹的信号数据
        altitude_array = []  # 用于存储所有子文件夹的高度数据
        idx = 0  # 用于标记第一个子文件夹

        for subfolder in subfolders:
            dat_files = list_files(subfolder)
            folder_altitude = []  # 当前子文件夹的所有文件高度数据
            folder_signal = []    # 当前子文件夹的所有文件信号数据

            for dat_file in dat_files:
                start_reading = False
                altitude = []
                signal = []
                with open(dat_file, 'r') as file:
                    for line in file:
                        if line.strip().startswith('Range'):
                            start_reading = True
                            continue

                        if start_reading:
                            columns = line.strip().split()
                            if columns:
                                try:
                                    altitude.append(float(columns[0]))  # 第一列作为高度
                                    signal.append(float(columns[1]))    # 第二列作为信号
                                except (ValueError, IndexError):
                                    continue
                if altitude and signal:  # 确保数据不为空
                    folder_altitude.append(altitude)
                    folder_signal.append(signal)

            if folder_altitude and folder_signal:
                folder_signal = np.array(folder_signal)
                if idx == 0:  # 第一个子文件夹
                    altitude_array.extend(folder_altitude)
                    combined_signal = folder_signal
                else:
                    try:
                        combined_signal += folder_signal    
                    except ValueError as e:
                        print(f"Error adding signals from {subfolder}: {e}")
                        continue
                idx += 1

        return np.array(altitude_array), combined_signal

    def K_channel(self, file_path):
        """提取K通道数据"""
        k_path = os.path.join(file_path, "CH1")
        if not os.path.exists(k_path):
            print(f"Path {k_path} does not exist.")
            return np.array([]), np.array([])

        dat_files = list_files(k_path)
        if not dat_files:
            print(f"No .dat files found in {k_path}.")
            return np.array([]), np.array([])

        altitude_array = []
        signal_array = []

        for dat_file in dat_files:
            start_reading = False
            altitude = []
            signal = []
            with open(dat_file, 'r') as file:
                for line in file:
                    if line.strip().startswith('Range'):
                        start_reading = True
                        continue

                    if start_reading:
                        columns = line.strip().split()
                        if len(columns) >= 2:  # Ensure there are at least two columns
                            try:
                                altitude.append(float(columns[0]))  # 第一列作为高度
                                signal.append(float(columns[1]))    # 第二列作为信号
                            except ValueError:
                                print(f"Skipping invalid line in {dat_file}: {line.strip()}")
                                continue

            if altitude and signal:  # Ensure data is not empty
                altitude_array.append(altitude)
                signal_array.append(signal)

        return np.array(altitude_array), np.array(signal_array)
    
    def Fe_channel(self, file_path):
        """Fe通道数据"""
        fe_path = os.path.join(file_path, "CH1")
        if not os.path.exists(fe_path):
            print(f"Path {fe_path} does not exist.")
            return np.array([]), np.array([])

        dat_files = list_files(fe_path)
        if not dat_files:
            print(f"No .dat files found in {fe_path}.")
            return np.array([]), np.array([])

        altitude_array = []
        signal_array = []

        for dat_file in dat_files:
            start_reading = False
            altitude = []
            signal = []
            with open(dat_file, 'r') as file:
                for line in file:
                    if line.strip().startswith('Range'):
                        start_reading = True
                        continue

                    if start_reading:
                        columns = line.strip().split()
                        if len(columns) >= 2:  # Ensure there are at least two columns
                            try:
                                altitude.append(float(columns[0]))  # 第一列作为高度
                                signal.append(float(columns[1]))    # 第二列作为信号
                            except ValueError:
                                print(f"Skipping invalid line in {dat_file}: {line.strip()}")
                                continue

            if altitude and signal:  # Ensure data is not empty
                altitude_array.append(altitude)
                signal_array.append(signal)

        return np.array(altitude_array), np.array(signal_array)