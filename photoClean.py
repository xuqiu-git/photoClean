import tkinter as tk
from tkinter import filedialog, messagebox
import os
import glob


def cleanup_folder(folder_path, raw_extension):
    # 获取文件夹中所有的.jpg和指定的.raw文件
    jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))
    raw_files = glob.glob(os.path.join(folder_path, f'*.{raw_extension}'))

    # 初始化.jpg和.raw文件的计数器
    initial_jpg_count = len(jpg_files)
    initial_raw_count = len(raw_files)

    # 创建两个空列表，分别存储所有.jpg和.raw文件的名称
    jpg_names = [os.path.splitext(os.path.basename(f))[0] for f in jpg_files]
    raw_names = [os.path.splitext(os.path.basename(f))[0] for f in raw_files]

    # 删除没有对应.jpg文件的.raw文件
    deleted_raw_count = 0
    for raw_file, raw_name in zip(raw_files, raw_names):
        if raw_name not in jpg_names:
            os.remove(raw_file)
            deleted_raw_count += 1

    # 删除没有对应.raw文件的.jpg文件
    deleted_jpg_count = 0
    for jpg_file, jpg_name in zip(jpg_files, jpg_names):
        if jpg_name not in raw_names:
            os.remove(jpg_file)
            deleted_jpg_count += 1

    # 计算最终的.jpg和.raw文件数量
    final_jpg_count = len(glob.glob(os.path.join(folder_path, '*.jpg')))
    final_raw_count = len(glob.glob(os.path.join(folder_path, f'*.{raw_extension}')))

    # 汇总信息并显示在一个消息框中
    message = (
        f"初始 .jpg 文件数量: {initial_jpg_count}\n"
        f"初始 .{raw_extension} 文件数量: {initial_raw_count}\n"
        f"最终 .jpg 文件数量: {final_jpg_count}\n"
        f"最终 .{raw_extension} 文件数量: {final_raw_count}\n"
        f"清理完成。文件现在一致。"
    )

    # 使用 messagebox 显示消息
    messagebox.showinfo("文件夹清理报告", message)


def select_folder_and_cleanup(raw_extension):
    root = tk.Tk()
    root.withdraw()

    # 让用户选择文件夹
    folder_path = filedialog.askdirectory()
    if not folder_path:
        messagebox.showinfo("取消", "操作已取消")
        return

    # 确认是否要继续清理
    confirm = messagebox.askyesno(
        "确认操作", f"确认要清理 {folder_path} 文件夹吗？"
    )
    if confirm:
        cleanup_folder(folder_path, raw_extension)
    else:
        messagebox.showinfo("取消", "操作已取消")


def choose_format():
    raw_formats = {
        "JPEG & ARW": "ARW",
        "JPEG & CR2": "CR2",
        "JPEG & RAF": "RAF",
        "JPEG & NEF": "NEF",
        "JPEG & RW2": "RW2",
        "JPEG & DNG": "DNG",
        "JPEG & X3F": "X3F",
        "JPEG & ORF": "ORF",
    }

    root = tk.Tk()
    root.title("选择待清理的RAW格式")

    root.geometry("300x250")  # 调整窗口大小

    # 配置列和行的权重以居中
    num_columns = 2  # 每行两个按钮
    num_rows = (len(raw_formats) // num_columns) + (len(raw_formats) % num_columns)  # 确定总行数
    for i in range(num_columns):
        root.grid_columnconfigure(i, weight=1)  # 为每列设置权重
    for i in range(num_rows):
        root.grid_rowconfigure(i, weight=1)  # 为每行设置权重

    # 根据可用的RAW格式动态创建按钮
    row = 0
    col = 0
    for format_name, extension in raw_formats.items():
        button = tk.Button(
            root,
            text=format_name,
            command=lambda ext=extension: select_folder_and_cleanup(ext)
        )
        button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")  # 让按钮填满网格
        col += 1
        if col == num_columns:  # 每行两个按钮
            col = 0
            row += 1  # 换行

    root.mainloop()


if __name__ == "__main__":
    choose_format()
