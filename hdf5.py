import h5py
import os
import read_channel_data_module

if __name__ == "__main__":
    data_path = r"D:\paper2\data"
    
    Channel = "Ca"  # 通道名称
    
    # 在指定目录下创建 HDF5 文件
    file_path = os.path.join("D:\paper2\code\datasets", Channel + '.h5')

    directory = os.path.join(data_path, Channel)
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        exit(1)
        
    # 获取所有子文件夹
    folders = [f.path for f in os.scandir(directory) if f.is_dir()]
    
    # 打开 HDF5 文件进行追加模式，若文件不存在会自动创建
    with h5py.File(file_path, 'w') as f:
        # 如果文件中没有 signals 和 times 数据集，创建这些数据集
        if 'signals' not in f:
            # 创建一个二维数据集，适应 signal_data 的形状 (600, 8192)
            f.create_dataset('signals', (0, 16384), maxshape=(None, 16384), dtype='f', compression="gzip", compression_opts=9)
        
        if 'times' not in f:
            f.create_dataset('times', (0,), maxshape=(None,), dtype=h5py.string_dtype(encoding='utf-8'), compression="gzip", compression_opts=9)

        # 遍历每个子文件夹
        for folder in folders:
            class_channel = read_channel_data_module.Channel(folder, Channel)
            
            # 获取每次循环的 signal 和 time 数据
            signal_data = class_channel.signal
            time_data = class_channel.Time
            
            # 获取 signal_data 的长度
            signal_length = signal_data.shape[0]  # 直接使用 .shape[0] 获取信号数据长度
            
            # 获取 time_data 的长度
            time_length = len(time_data)  # 使用 len() 获取时间数据长度

            # 扩展 signals 和 times 数据集的大小
            f['signals'].resize(f['signals'].shape[0] + signal_length, axis=0)
            f['times'].resize(f['times'].shape[0] + time_length, axis=0)
            
            # 追加数据
            f['signals'][-signal_length:] = signal_data  # signal_data 是一个二维数组
            f['times'][-time_length:] = time_data
            
            print(f"{folder} 数据已成功追加到 {file_path} 文件中。")

    print(f"数据已成功追加到 {file_path} 文件中。")