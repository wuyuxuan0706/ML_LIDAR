import channel_data
import threading
import time
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# 常量定义
CHANNELS = ["Na", "Ca", "K", "Fe"]
COLORS = {'Na': 'blue', 'Ca': 'red', 'K': 'green', 'Fe': 'purple'}
DATA_PATH = r"D:\paper2\data"
OUTPUT_PATH = r"D:\paper2\pic\multi_channel.jpg"

def process_channel(channel_obj, channel_name, index, results):
    """处理通道数据并存储结果。

    Args:
        channel_obj: Channel对象，包含通道数据
        channel_name: 通道名称 (如 'Na', 'Ca')
        index: 线程索引
        results: 存储结果的字典
    """
    print(f"线程 {index}: 开始处理 {channel_name} 通道")
    try:
        
        if channel_obj.altitude.size == 0 or channel_obj.signal.size == 0:
            print(f"线程 {index}: {channel_name} 通道没有有效数据")
            return
        
        # 存储结果，确保一维数组
        results[channel_name] = {
            'altitude': channel_obj.altitude,
            'signal': channel_obj.signal
        }
        print(f"线程 {index}: 完成处理 {channel_name} 通道")
    except Exception as e:
        print(f"线程 {index}: 处理 {channel_name} 通道时出错: {e}")

def plot_channels(results, output_path=OUTPUT_PATH):
    """绘制所有通道的信号并保存图像。

    Args:
        results: 包含通道数据的字典
        output_path: 图像保存路径
    """
    if not results:
        print("没有可用的数据用于绘图")
        return

    try:
        # 设置全局字体和大小
        plt.rcParams['font.family'] = 'Arial'  # 设置字体为 Arial
        plt.rcParams['font.size'] = 14         # 设置默认字体大小
        
        plt.figure(figsize=(12, 8))
        
        for channel, data in results.items():
            plt.semilogy(data['altitude'][0,:], data['signal'][0, :],
                    label=channel,
                    color=COLORS[channel],
                    linewidth=2)
        plt.xlim(0, 200)  # 设置x轴范围
        plt.ylim(1, 1e5)  # 设置y轴范围
        plt.xlabel('Altitude (km)', fontsize=16)
        plt.ylabel('PhotonCounts', fontsize=16)
        plt.tick_params(axis='both', labelsize=14)  # 设置刻度标签字体大小为 14
        plt.legend(fontsize=14)  # 图例字体大小
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"图像已保存到: {output_path}")
    except Exception as e:
        print(f"绘图时出错: {e}")

def main():
    """主函数，协调多线程数据处理和绘图。"""
    start_time = time.time()
    results = defaultdict(dict)
    
    # 使用 ThreadPoolExecutor 管理线程
    with ThreadPoolExecutor(max_workers=len(CHANNELS)) as executor:
        futures = []
        
        for i, chl in enumerate(CHANNELS):
            directory = Path(DATA_PATH) / chl
            if not directory.exists():
                print(f"目录 {directory} 不存在")
                continue
                
            folders = [f.path for f in os.scandir(directory) if f.is_dir()]
            if not folders:
                print(f"通道 {chl} 没有子文件夹")
                continue
                
            try:
                class_channel = channel_data.Channel(folders[0], chl)
                future = executor.submit(process_channel, class_channel, chl, i, results)
                futures.append(future)
            except ValueError as e:
                print(f"创建 {chl} 通道时出错: {e}")
                continue
        
        # 等待所有任务完成
        for future in futures:
            future.result()
    
    print("所有线程已完成！")
    plot_channels(results)
    
    end_time = time.time()
    print(f"程序总耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    main()