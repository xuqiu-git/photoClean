import Tkinter as teak
from tkinter import filedialog
from tkinter import messagebox
import os
import glob
import sys


def cleanup_folder(folder_path):
    # 获取文件夹中所有的.jpg和.raw文件
    jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))
    raw_files = glob.glob(os.path.join(folder_path, '*.arw'))

    # 初始化jpg和raw文件的计数器
    initial_jpg_count = len(jpg_files)
    initial_raw_count = len(raw_files)

    # 创建两个空列表，分别存储所有.jpg和.raw文件的名称（不包括扩展名）
    jpg_names = [os.path.splitext(os.path.basename(f))[0] for f in jpg_files]
    raw_names = [os.path.splitext(os.path.basename(f))[0] for f in raw_files]

    # 删除没有对应.jpg文件的.raw文件
    for raw_file, raw_name in zip(raw_files, raw_names):
        if raw_name not in jpg_names:
            os.remove(raw_file)
            print(f'Deleted {raw_file} because it has no corresponding .jpg file.')

    # 删除没有对应.raw文件的.jpg文件
    for jpg_file, jpg_name in zip(jpg_files, jpg_names):
        if jpg_name not in raw_names:
            os.remove(jpg_file)
            print(f'Deleted {jpg_file} because it has no corresponding .arw file.')

    # 重新计算并打印处理后的.jpg和.raw文件的数量
    final_jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))
    final_raw_files = glob.glob(os.path.join(folder_path, '*.arw'))
    print(f'Initial .jpg file count: {initial_jpg_count}')
    print(f'Initial .arw file count: {initial_raw_count}')
    print(f'Final .jpg file count: {len(final_jpg_files)}')
    print(f'Final .arw file count: {len(final_raw_files)}')
    print('Cleanup complete. Files are now consistent.')


def select_folder_and_cleanup():
    root = tk.Tk()
    root.withdraw()  # 不显示主窗口
    folder_path = filedialog.askdirectory()  # 弹出对话框让用户选择文件夹
    if folder_path:  # 如果用户选择了文件夹
        cleanup_folder(folder_path)
        tk.messagebox.showinfo("完成", "文件夹清理完成！")
    else:
        tk.messagebox.showinfo("取消", "操作已取消")


if __name__ == "__main__":
    select_folder_and_cleanup()

