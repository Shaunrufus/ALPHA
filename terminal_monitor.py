#!/usr/bin/env python3
"""
Terminal Monitor - Monitors terminal activity and running processes
"""

import subprocess
import time
import psutil
import os
from datetime import datetime

def get_running_processes():
    """Get currently running Python and terminal processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
        try:
            if any(keyword in proc.info['name'].lower() for keyword in ['python', 'cmd', 'powershell', 'terminal']):
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cmdline': ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else '',
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_mb': proc.info['memory_info'].rss / 1024 / 1024
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def get_current_directory():
    """Get current working directory"""
    return os.getcwd()

def monitor_terminal():
    """Main monitoring function"""
    print(f"=== Terminal Monitor Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    print(f"Current directory: {get_current_directory()}")
    print()
    
    while True:
        try:
            print(f"\n--- Check at {datetime.now().strftime('%H:%M:%S')} ---")
            
            # Get running processes
            processes = get_running_processes()
            if processes:
                print("Active processes:")
                for proc in processes:
                    print(f"  {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']:.1f}% - Memory: {proc['memory_mb']:.1f}MB")
                    if proc['cmdline']:
                        print(f"    Command: {proc['cmdline'][:100]}...")
            else:
                print("No relevant processes found")
            
            print("-" * 50)
            time.sleep(10)  # Check every 10 seconds
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            break
        except Exception as e:
            print(f"Error during monitoring: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_terminal()
