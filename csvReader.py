import os
import glob
import csv

folders = glob.glob('e0_*')  # 获取所有名字以'e0_'开头的文件夹
data = {}  # 创建一个字典用来存储所有数据

for folder in folders:  # 遍历每一个文件夹
    folder_data = []  # 用来存储当前文件夹下的所有数据的三维列表
    files = sorted(glob.glob(os.path.join(folder, 'result\\*_slope.csv')))  # 获取当前文件夹下的所有.csv文件
    for file in files:  # 遍历每一个文件
        with open(file, 'r') as f:  # 打开文件
            reader = csv.reader(f)  # 创建csv.reader
            file_data = [list(map(float, row)) for row in reader]  # 读取文件中的数据并转换为float类型
            folder_data.append(file_data)  # 将文件中的数据添加到folder_data中
    key = int(folder.split('_')[1])  # 将文件夹名'eo_xx'中的'xx'部分作为键
    data[key] = folder_data  # 将folder_data添加到字典data中，其键为key

# 现在，data就是一个字典，其中每个键对应一个文件夹（'e0_xx'中的'xx'部分），每个值是一个三维列表，每一维对应一个文件，每一维对应一行数据，每一维对应一个数据点
