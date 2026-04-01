import requests
import os
import sys
import subprocess

# ===================== 你的配置 =====================
GITHUB_USER = "SIbouy-33"
GITHUB_REPO = "python-excel-tools-chongdong"
LOCAL_VERSION = "1.0.0"  # 本地版本
# ====================================================

def is_exe():
    # 判断是不是 exe 模式
    return getattr(sys, 'frozen', False)

def check_update():
    # 只有打包成 exe 才检查更新
    if not is_exe():
        print("[调试模式] 不检查更新")
        return

    try:
        print("正在检查更新...")
        url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.txt"
        resp = requests.get(url, timeout=5)

        if resp.status_code != 200:
            print("获取版本失败")
            return

        latest_version = resp.text.strip()
        print(f"本地版本: {LOCAL_VERSION}")
        print(f"最新版本: {latest_version}")

        if latest_version > LOCAL_VERSION:
            print("发现新版本，开始更新...")
            do_update(latest_version)
        else:
            print("已是最新版本")

    except Exception as e:
        print(f"检查更新失败: {e}")

def do_update(latest_ver):
    try:
        exe_name = "main.exe"
        new_exe = "new_main.exe"

        # 下载最新版 exe
        download_url = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/releases/download/v{latest_ver}/{exe_name}"

        r = requests.get(download_url, stream=True, timeout=30)
        with open(new_exe, "wb") as f:
            f.write(r.content)

        # 安全替换脚本
        bat = f"""
        @echo off
        timeout /t 1 /nobreak > nul
        del /f "{exe_name}"
        ren "{new_exe}" "{exe_name}"
        start "" "{exe_name}"
        del "%~f0"
        """

        with open("update.bat", "w", encoding="gbk") as f:
            f.write(bat)

        subprocess.Popen("update.bat", shell=True)
        sys.exit()

    except Exception as e:
        print(f"更新失败: {e}")

if __name__ == "__main__":
    check_update()