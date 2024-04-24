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

    # 创建两个空列表，分别存储所有.jpg和.raw文件的名称（不包括扩展名）
    jpg_names = [os.path.splitext(os.path.basename(f))[0] for f in jpg_files]
    raw_names = [os.path.splitext(os.path.basename(f))[0] for f in raw_files]

    # 删除没有对应.jpg文件的.raw文件
    for raw_file, raw_name in zip(raw_files, raw_names):
        if raw_name not in jpg_names:
            os.remove(raw_file)
            print(f'已删除 {raw_file}，因为它没有对应的 .jpg 文件。')

    # 删除没有对应.raw文件的.jpg文件
    for jpg_file, jpg_name in zip(jpg_files, jpg_names):
        if jpg_name not in raw_names:
            os.remove(jpg_file)
            print(f'已删除 {jpg_file}，因为它没有对应的 .{raw_extension} 文件。')

    # 重新计算并打印处理后的.jpg和.raw文件的数量
    final_jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))
    final_raw_files = glob.glob(os.path.join(folder_path, f'*.{raw_extension}'))
    print(f'初始 .jpg 文件数量: {initial_jpg_count}')
    print(f'初始 .{raw_extension} 文件数量: {initial_raw_count}')
    print(f'最终 .jpg 文件数量: {len(final_jpg_files)}')
    print(f'最终 .{raw_extension} 文件数量: {len(final_raw_files)}')
    print('清理完成。文件现在一致。')


def select_folder_and_cleanup(raw_extension):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 让用户选择文件夹
    folder_path = filedialog.askdirectory()
    if not folder_path:
        messagebox.showinfo("取消", "操作已取消")
        return

    # 创建确认对话框
    confirm_window = tk.Tk()
    confirm_window.title("确认操作")

    # 创建提示信息
    label = tk.Label(confirm_window, text=f"确认清理 {folder_path} 文件夹吗？")
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # 创建“确定”和“取消”按钮
    def on_confirm():
        cleanup_folder(folder_path, raw_extension)
        messagebox.showinfo("完成", "文件夹清理完成！")
        confirm_window.destroy()  # 关闭确认窗口

    def on_cancel():
        messagebox.showinfo("取消", "操作已取消")
        confirm_window.destroy()  # 关闭确认窗口

    # 设置按钮
    button_confirm = tk.Button(confirm_window, text="确定", command=on_confirm)
    button_cancel = tk.Button(confirm_window, text="取消", command=on_cancel)

    button_confirm.grid(row=1, column=0, padx=10, pady=10)
    button_cancel.grid(row=1, column=1, padx=10, pady=10)

    confirm_window.mainloop()  # 开始事件循环


def choose_format():
    # 定义可用的RAW格式
    raw_formats = {
        "索尼 ARW": "ARW",
        "佳能 CR2": "CR2",
        "富士 RAF": "RAF",
        "尼康 NEF": "NEF",
        "松下 RW2": "RW2",
        "徕卡、理光、大疆 DNG": "DNG",
        "适马 X3F": "X3F",
        "奥林巴斯 ORF": "ORF",
    }

    root = tk.Tk()
    root.title("选择RAW文件格式")

    # 根据可用的RAW格式动态创建按钮
    row = 0
    col = 0
    for format_name, extension in raw_formats.items():
        button = tk.Button(
            root,
            text=format_name,
            command=lambda ext=extension: select_folder_and_cleanup(ext)
        )
        # 使用grid布局
        button.grid(row=row, column=col, padx=10, pady=10)  # 适当增加间距
        col += 1
        if col == 2:  # 每行两列
            col = 0
            row += 1  # 换行

    root.mainloop()  # 开始GUI事件循环


if __name__ == "__main__":
    choose_format()  # 让用户选择RAW文件格式
