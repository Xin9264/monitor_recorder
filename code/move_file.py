import os
import shutil
import sys

def move_txt_files_from_previous_directory():

    
    # print(f"Script directory: {script_directory}")
    previous_directory = os.path.dirname(os.path.abspath(__file__))
    # print(f"Previous directory: {previous_directory}")
    save_directory = os.path.join('..', 'save')
    # save_directory = os.path.join(previous_directory, 'save')
    
    # 如果 save 文件夹不存在，提示错误
    if not os.path.exists(save_directory):
        print(f"Save directory '{save_directory}' does not exist.")
        return
    
    # 找到 save 文件夹中创建时间最新的子文件夹
    subfolders = [f.path for f in os.scandir(save_directory) if f.is_dir()]
    
    if not subfolders:
        print(f"No subfolders found in '{save_directory}'.")
        return
    
    latest_folder = max(subfolders, key=os.path.getctime)
    
    # 遍历上一级目录下的所有文件
    for filename in os.listdir(previous_directory):
        # 仅处理 .txt 文件
        if filename.endswith('.txt'):
            # 源文件路径
            source_file = os.path.join(previous_directory, filename)
            # 目标文件路径
            destination_file = os.path.join(latest_folder, filename)
            
            # 移动文件
            shutil.move(source_file, destination_file)
            print(f'Moved: {filename} to {latest_folder}')

# 调用函数
move_txt_files_from_previous_directory()
