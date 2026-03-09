#!/usr/bin/env python3
"""
Live Terminal Monitor - Real-time monitoring of terminal activity and system resources
"""

import psutil
import time
import os
import subprocess
from datetime import datetime
import threading
import queue

class LiveTerminalMonitor:
    def __init__(self):
        self.running = True
        self.update_queue = queue.Queue()
        self.monitoring_thread = None
        
    def get_system_info(self):
        """Get current system resource usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_used_gb': memory.used / (1024**3),
            'memory_total_gb': memory.total / (1024**3),
            'disk_percent': disk.percent,
            'disk_used_gb': disk.used / (1024**3),
            'disk_total_gb': disk.total / (1024**3)
        }
    
    def get_python_processes(self):
        """Get detailed information about Python processes"""
        python_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info', 'create_time']):
            try:
                if 'python' in proc.info['name'].lower():
                    # Get more detailed command line
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    
                    # Try to get the actual script being run
                    script_name = "Unknown"
                    if proc.info['cmdline'] and len(proc.info['cmdline']) > 1:
                        script_path = proc.info['cmdline'][1]
                        script_name = os.path.basename(script_path)
                    
                    python_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'script': script_name,
                        'cmdline': cmdline[:150] + '...' if len(cmdline) > 150 else cmdline,
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_mb': proc.info['memory_info'].rss / 1024 / 1024,
                        'create_time': datetime.fromtimestamp(proc.info['create_time']).strftime('%H:%M:%S')
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return python_processes
    
    def get_terminal_processes(self):
        """Get terminal-related processes"""
        terminal_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                if any(keyword in proc.info['name'].lower() for keyword in ['powershell', 'cmd', 'terminal', 'conhost']):
                    terminal_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_mb': proc.info['memory_info'].rss / 1024 / 1024
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return terminal_processes
    
    def monitor_loop(self):
        """Background monitoring loop"""
        while self.running:
            try:
                # Collect monitoring data
                system_info = self.get_system_info()
                python_processes = self.get_python_processes()
                terminal_processes = self.get_terminal_processes()
                
                # Put data in queue for main thread to display
                self.update_queue.put({
                    'timestamp': datetime.now(),
                    'system': system_info,
                    'python_processes': python_processes,
                    'terminal_processes': terminal_processes
                })
                
                time.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)
    
    def display_status(self, data):
        """Display current status"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print(f"🖥️  LIVE TERMINAL MONITOR - {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # System Resources
        sys = data['system']
        print(f"\n📊 SYSTEM RESOURCES:")
        print(f"   CPU Usage: {sys['cpu_percent']:.1f}%")
        print(f"   Memory: {sys['memory_percent']:.1f}% ({sys['memory_used_gb']:.1f}GB / {sys['memory_total_gb']:.1f}GB)")
        print(f"   Disk: {sys['disk_percent']:.1f}% ({sys['disk_used_gb']:.1f}GB / {sys['disk_total_gb']:.1f}GB)")
        
        # Python Processes
        print(f"\n🐍 PYTHON PROCESSES ({len(data['python_processes'])}):")
        if data['python_processes']:
            for proc in data['python_processes']:
                status = "🟢" if proc['cpu_percent'] > 0 else "⚪"
                print(f"   {status} {proc['script']} (PID: {proc['pid']})")
                print(f"      CPU: {proc['cpu_percent']:.1f}% | Memory: {proc['memory_mb']:.1f}MB | Started: {proc['create_time']}")
                if proc['cmdline']:
                    print(f"      Command: {proc['cmdline']}")
                print()
        else:
            print("   No Python processes found")
        
        # Terminal Processes
        print(f"\n💻 TERMINAL PROCESSES ({len(data['terminal_processes'])}):")
        if data['terminal_processes']:
            for proc in data['terminal_processes']:
                print(f"   {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']:.1f}% | Memory: {proc['memory_mb']:.1f}MB")
        else:
            print("   No terminal processes found")
        
        print("\n" + "=" * 80)
        print("Press Ctrl+C to stop monitoring")
    
    def start_monitoring(self):
        """Start the monitoring system"""
        print("🚀 Starting Live Terminal Monitor...")
        
        # Start background monitoring thread
        self.monitoring_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitoring_thread.start()
        
        try:
            while self.running:
                try:
                    # Get latest data from queue (with timeout)
                    data = self.update_queue.get(timeout=1)
                    self.display_status(data)
                except queue.Empty:
                    continue
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping monitor...")
            self.running = False
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=2)
            print("✅ Monitor stopped")

if __name__ == "__main__":
    monitor = LiveTerminalMonitor()
    monitor.start_monitoring()

