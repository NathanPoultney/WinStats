#!/usr/bin/env python3
import os
import platform
import subprocess
import psutil
import time
import socket
import getpass
import re
import datetime
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

class WinStats:
    def __init__(self):
        self.os_name = self.get_os_name()
        self.hostname = socket.gethostname()
        self.kernel = platform.release()
        self.uptime = self.get_uptime()
        self.packages = self.get_package_count()
        self.shell = os.environ.get("SHELL", os.environ.get("ComSpec", "Unknown"))
        self.resolution = self.get_resolution()
        self.cpu = self.get_cpu_info()
        self.gpu = self.get_gpu_info()
        self.ram = self.get_ram_info()
        self.disk = self.get_disk_info()
        self.username = getpass.getuser()
        self.local_ip = self.get_local_ip()
        self.logo = self.get_windows_logo()
        self.theme = self.get_theme()

    def get_os_name(self):
        try:
            return f"Windows {platform.win32_ver()[0]} {platform.win32_ver()[1]}"
        except:
            return platform.system() + " " + platform.release()

    def get_uptime(self):
        try:
            boot_time = psutil.boot_time()
            uptime = time.time() - boot_time
            uptime_str = str(datetime.timedelta(seconds=int(uptime)))
            return uptime_str
        except:
            return "Unknown"

    def get_package_count(self):
        try:
            # Count installed programs from Windows Registry
            output = subprocess.check_output(
                'powershell "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName | Measure-Object | %{$_.Count}"',
                shell=True
            ).decode().strip()
            return output
        except:
            return "Unknown"

    def get_resolution(self):
        try:
            import ctypes
            user32 = ctypes.windll.user32
            width = user32.GetSystemMetrics(0)
            height = user32.GetSystemMetrics(1)
            return f"{width}x{height}"
        except:
            return "Unknown"

    def get_cpu_info(self):
        try:
            cpu_info = platform.processor()
            cpu_count = psutil.cpu_count(logical=True)
            cpu_usage = psutil.cpu_percent(interval=0.1)
            return f"{cpu_info} ({cpu_count} cores) - {cpu_usage}% used"
        except:
            return "Unknown"

    def get_gpu_info(self):
        try:
            output = subprocess.check_output(
                'wmic path win32_VideoController get Name',
                shell=True
            ).decode().strip().split('\n')[1].strip()
            return output
        except:
            return "Unknown"

    def get_ram_info(self):
        try:
            ram = psutil.virtual_memory()
            total_ram = ram.total / (1024 ** 3)  # Convert to GB
            used_ram = ram.used / (1024 ** 3)
            ram_percent = ram.percent
            return f"{used_ram:.2f} GB / {total_ram:.2f} GB ({ram_percent}% used)"
        except:
            return "Unknown"

    def get_disk_info(self):
        try:
            disk = psutil.disk_usage('/')
            total_disk = disk.total / (1024 ** 3)  # Convert to GB
            used_disk = disk.used / (1024 ** 3)
            disk_percent = disk.percent
            return f"{used_disk:.2f} GB / {total_disk:.2f} GB ({disk_percent}% used)"
        except:
            return "Unknown"

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "Unknown"

    def get_theme(self):
        try:
            # Check if dark mode is enabled
            output = subprocess.check_output(
                'powershell "Get-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme | Select-Object -ExpandProperty AppsUseLightTheme"',
                shell=True
            ).decode().strip()
            return "Dark Theme" if output == "0" else "Light Theme"
        except:
            return "Unknown"

    def get_windows_logo(self):
        logo = f"""
{Fore.RED}                    ....,,:;+ccllll
{Fore.RED}      ...,,+:;  cllllllllllllllllll
{Fore.RED},cclllllllllll  lllllllllllllllllll
{Fore.RED}llllllllllllll  lllllllllllllllllll
{Fore.RED}llllllllllllll  lllllllllllllllllll
{Fore.RED}llllllllllllll  lllllllllllllllllll
{Fore.GREEN}llllllllllllll  lllllllllllllllllll
{Fore.GREEN}llllllllllllll  lllllllllllllllllll
{Style.RESET_ALL}                                   
{Fore.BLUE}llllllllllllll  lllllllllllllllllll
{Fore.BLUE}llllllllllllll  lllllllllllllllllll
{Fore.BLUE}llllllllllllll  lllllllllllllllllll
{Fore.BLUE}llllllllllllll  lllllllllllllllllll
{Fore.YELLOW}llllllllllllll  lllllllllllllllllll
{Fore.YELLOW}`'ccllllllllll  lllllllllllllllllll
{Fore.YELLOW}       `' \\*::  :ccllllllllllllllll
{Fore.YELLOW}                       ````''*::cll
       {Style.RESET_ALL}"""
        return logo

    def display(self):
        # Split the logo into lines
        logo_lines = self.logo.split('\n')
        
        # Prepare information lines
        info_lines = [
            f"{Fore.CYAN}{self.username}@{self.hostname}{Style.RESET_ALL}",
            f"{Fore.WHITE}{'-' * (len(self.username) + len(self.hostname) + 1)}",
            f"{Fore.CYAN}OS:{Style.RESET_ALL} {self.os_name}",
            f"{Fore.CYAN}Kernel:{Style.RESET_ALL} {self.kernel}",
            f"{Fore.CYAN}Uptime:{Style.RESET_ALL} {self.uptime}",
            f"{Fore.CYAN}Packages:{Style.RESET_ALL} {self.packages}",
            f"{Fore.CYAN}Shell:{Style.RESET_ALL} {os.path.basename(self.shell)}",
            f"{Fore.CYAN}Resolution:{Style.RESET_ALL} {self.resolution}",
            f"{Fore.CYAN}Theme:{Style.RESET_ALL} {self.theme}",
            f"{Fore.CYAN}CPU:{Style.RESET_ALL} {self.cpu}",
            f"{Fore.CYAN}GPU:{Style.RESET_ALL} {self.gpu}",
            f"{Fore.CYAN}Memory:{Style.RESET_ALL} {self.ram}",
            f"{Fore.CYAN}Disk:{Style.RESET_ALL} {self.disk}",
            f"{Fore.CYAN}Local IP:{Style.RESET_ALL} {self.local_ip}",
            "",
            f"{Fore.RED}■{Fore.GREEN} ■{Fore.YELLOW} ■{Fore.BLUE} ■{Fore.MAGENTA} ■{Fore.CYAN} ■{Fore.WHITE} ■{Style.RESET_ALL}"
        ]
        
        # Determine the maximum number of lines to display (logo or info)
        max_lines = max(len(logo_lines), len(info_lines))
        
        # Print each line, combining logo and info
        for i in range(max_lines):
            logo_line = logo_lines[i] if i < len(logo_lines) else ' ' * 40
            info_line = info_lines[i] if i < len(info_lines) else ''
            print(f"{logo_line}  {info_line}")

if __name__ == "__main__":
    winstats = WinStats()
    winstats.display()