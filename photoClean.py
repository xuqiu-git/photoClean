import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os
import glob
import sys
import webbrowser
from update import update_software

# 定义本地版本号
LOCAL_VERSION = "1.2.4"

# 获取当前程序的运行路径
def resource_path(relative_path):
    try:
        # PyInstaller创建临时文件夹存储路径
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 创建全局主窗口实例
root = tk.Tk()
root.withdraw()  # 初始隐藏主窗口

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
    folder_path = filedialog.askdirectory(parent=root)
    if not folder_path:
        messagebox.showinfo("取消", "操作已取消", parent=root)
        return
    confirm = messagebox.askyesno("确认操作", f"确认要清理 {folder_path} 文件夹吗？", parent=root)
    if confirm:
        cleanup_folder(folder_path, raw_extension)
    else:
        messagebox.showinfo("取消", "操作已取消", parent=root)

def open_help():
    """打开帮助文档的回调函数"""
    webbrowser.open("https://github.com/xuqiu-git/photoClean/blob/main/help.txt")  # 使用实际的帮助文档链接

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

    choose_window = tk.Toplevel(root)
    choose_window.title(f"photoCleaner v{LOCAL_VERSION}")  # 设置窗口标题
    choose_window.geometry("300x400")

    # 创建一个框架用于自定义标题栏
    title_frame = ttk.Frame(choose_window)
    title_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

    # 创建一个内框架用于居中对齐标题和问号按钮
    inner_frame = ttk.Frame(title_frame)
    inner_frame.grid(row=0, column=1)

    # 创建自定义样式
    style = ttk.Style()
    style.configure("Title.TLabel", font=("Arial", 10))

    title_label = ttk.Label(inner_frame, text="选择待清理的RAW格式", style="Title.TLabel")
    title_label.grid(row=0, column=0, padx=10)

    # 创建带问号的按钮
    help_btn = ttk.Button(inner_frame, text="?", command=open_help, width=3)
    help_btn.grid(row=0, column=1, padx=(0, 5))

    content_frame = ttk.Frame(choose_window)
    content_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    num_columns = 2
    num_rows = (len(raw_formats) // num_columns) + (len(raw_formats) % num_columns)
    for i in range(num_columns):
        content_frame.grid_columnconfigure(i, weight=1)
    for i in range(num_rows + 1):
        content_frame.grid_rowconfigure(i, weight=1)

    row = 0
    col = 0
    for format_name, extension in raw_formats.items():
        button = ttk.Button(
            content_frame,
            text=format_name,
            command=lambda ext=extension: select_folder_and_cleanup(ext)
        )
        button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        col += 1
        if col == num_columns:
            col = 0
            row += 1

    custom_btn = ttk.Button(content_frame, text="自定义格式", command=custom_format)
    custom_btn.grid(row=row, column=0, columnspan=num_columns, sticky='ew', padx=10, pady=10)
    row += 1

    update_btn = ttk.Button(content_frame, text="检查更新", command=lambda: update_software(LOCAL_VERSION))
    update_btn.grid(row=row, column=0, columnspan=num_columns, sticky='ew', padx=10, pady=10)

    choose_window.protocol("WM_DELETE_WINDOW", lambda: on_close(choose_window))

    # 使标题栏居中
    title_frame.grid_columnconfigure(0, weight=1)
    title_frame.grid_columnconfigure(2, weight=1)

    # 使内容框架和内部小部件扩展填充
    choose_window.grid_rowconfigure(0, weight=1)
    choose_window.grid_rowconfigure(1, weight=10)
    choose_window.grid_columnconfigure(0, weight=1)
    choose_window.grid_columnconfigure(1, weight=1)

def custom_format():
    raw_extension = simpledialog.askstring("输入RAW格式", "请输入RAW文件的后缀（例如raw）：", parent=root)
    if raw_extension:
        select_folder_and_cleanup(raw_extension)

def on_close(window):
    """关闭窗口并检查是否需要退出主程序"""
    window.destroy()
    if not any(win.winfo_exists() for win in root.winfo_children() if isinstance(win, tk.Toplevel)):
        root.destroy()
        root.quit()

if __name__ == "__main__":
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    choose_format()
    root.mainloop()
