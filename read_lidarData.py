import numpy as np
import os
import matplotlib.pyplot as plt
import channel_data

def list_files(directory):
    """列出指定目录下的所有 .dat 文件"""
    files = []
    for file in os.listdir(directory):
        if file.endswith(".dat"):
            files.append(os.path.join(directory, file))
    return files

def extract_para(file_path):
    """从 .dat 文件中提取高度和信号数据"""
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
                        altitude = float(columns[0])  # 第一列作为高度
                        signal = float(columns[1])    # 第二列作为信号
                        altitude_array.append(altitude)
                        signal_array.append(signal)
                    except (ValueError, IndexError):
                        continue
                    
    return np.array(altitude_array), np.array(signal_array)

def image_plot(altitude, signal, save_path=None):
    """绘制高度-信号图，可选择保存"""
    plt.figure(figsize=(10, 6))
    plt.semilogy(altitude, signal)
    plt.xlim(0, 250)  # 设置x轴范围
    plt.ylim(1, 1e4)
    plt.xlabel('Altitude (km)')
    plt.ylabel('Signal')
    plt.grid()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Image saved to {save_path}")
    else:
        plt.show()
    plt.close()  # 关闭图表以释放内存

if __name__ == "__main__":
    data_path = r"D:\paper2\data"
    channel = "K"  # 通道名称
    # 保存图像的目录
    save_base_path = os.path.join(r"D:\paper2\pic", channel)
    if not os.path.exists(save_base_path):
        os.makedirs(save_base_path)  # 如果保存路径不存在，创建它
        
    directory = os.path.join(data_path, channel)
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        exit(1)
    # 获取所有子文件夹
    folders = [f.path for f in os.scandir(directory) if f.is_dir()]
    # 遍历每个子文件夹
    for folder in folders:
        class_channel = channel_data.Channel(folder, channel)
        
        rows, cols = class_channel.altitude.shape
        if rows != 0 and cols != 0:  # 确保数据不为空
            for i in range(rows):
                # 生成保存路径
                folder_path = os.path.join(save_base_path, os.path.basename(folder))
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                save_path = os.path.join(folder_path, f"{os.path.basename(folder)}_{i}.jpg")
                image_plot(class_channel.altitude[i], class_channel.signal[i], save_path=save_path)
