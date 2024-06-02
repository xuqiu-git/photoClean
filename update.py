import tkinter as tk
from tkinter import messagebox, filedialog
import requests

def check_for_updates():
    """检查 GitHub 上的新版本并获取.exe文件的下载链接"""
    repo_owner = "xuqiu-git"
    repo_name = "photoClean"
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)
    data = response.json()

    if response.status_code == 200 and 'tag_name' in data:
        latest_version = data['tag_name']
        download_url = None
        for asset in data['assets']:
            if asset['name'].endswith('.exe'):
                download_url = asset['browser_download_url']
                break
        return latest_version, download_url
    else:
        return None, None

def download_update(download_url, version):
    """让用户选择下载路径并下载新版本的文件"""
    default_filename = f"photoClean_v{version}.exe"
    save_path = filedialog.asksaveasfilename(
        title="保存新版本为",
        initialfile=default_filename,
        filetypes=[("Executable files", "*.exe")],
        defaultextension=".exe"
    )
    if save_path:
        response = requests.get(download_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            messagebox.showinfo("下载成功", "新版本已下载完成！")
        else:
            messagebox.showerror("下载失败", "无法下载新版本。")
    else:
        messagebox.showinfo("取消下载", "更新下载已取消。")

def update_software(local_version):
    latest_version, download_url = check_for_updates()
    if latest_version is None:
        messagebox.showerror("检查失败", "无法检查更新。")
        return

    if latest_version == local_version:
        messagebox.showinfo("无新版本", f"当前已是最新版本 {local_version}。")
    elif download_url:
        response = messagebox.askyesno("发现新版本", f"最新版本 {latest_version} 可用。是否下载？")
        if response:
            download_update(download_url, latest_version)
    else:
        messagebox.showinfo("无可用更新", f"最新版本是 {latest_version}，但没有可下载的 .exe 文件。")
