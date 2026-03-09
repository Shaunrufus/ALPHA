#!/usr/bin/env python3
import argparse
import os
import re
import sys
import time
from datetime import datetime

ERROR_PATTERNS = [
    # PowerShell/general
    (re.compile(r"The term 'pyenv' is not recognized", re.I),
     "pyenv is referenced in your PowerShell profile but not installed. Either install pyenv, or edit your profile to remove its init lines: `$PROFILE` → comment out pyenv init lines and restart PowerShell."),
    (re.compile(r"is not recognized as the name of a cmdlet|CommandNotFoundException", re.I),
     "Command not found. Verify the tool is installed and on PATH. If it's a venv tool, use the full path like `C:\path\to\venv\Scripts\python.exe`."),

    # Python/Traceback
    (re.compile(r"Traceback \(most recent call last\):", re.I),
     "Python exception detected. Scroll to the last line of the traceback for the exact error type/message. Common fixes: install missing packages, check file paths, and environment variables."),
    (re.compile(r"ModuleNotFoundError: No module named '([\w\.\-]+)'", re.I),
     "Missing Python module. Install it in the correct venv: `python -m pip install <module>`. Ensure you are using the intended interpreter."),
    (re.compile(r"ImportError|DLL load failed|could not be resolved", re.I),
     "Import/DLL load error. Ensure compatible package versions and that system dependencies (e.g., Visual C++ Redistributable, CUDA/CUDNN) are installed."),
    (re.compile(r"FileNotFoundError: \[Errno 2\]", re.I),
     "File not found. Verify the path exists and is correct relative to the working directory."),
    (re.compile(r"PermissionError: \[Errno 13\]", re.I),
     "Permission denied. Try a different directory, adjust permissions, or avoid writing into protected locations."),

    # pip
    (re.compile(r"ERROR: Could not find a version that satisfies the requirement ([^ ]+)", re.I),
     "Package version not found. Pin a compatible version or check Python version/OS/arch compatibility."),
    (re.compile(r"Failed building wheel for ([^\s]+)", re.I),
     "Wheel build failed. Install build tools (e.g., `pip install wheel`), or use a prebuilt wheel/compatible Python version."),

    # PyTorch/CUDA
    (re.compile(r"CUDA out of memory", re.I),
     "CUDA OOM. Reduce batch size, use smaller model, clear cache with `torch.cuda.empty_cache()`, or close other GPU apps."),
    (re.compile(r"CUDA driver version is insufficient|CUDA initialization error|Found no NVIDIA driver", re.I),
     "CUDA driver/runtime issue. Install/update NVIDIA driver and ensure CUDA runtime version matches the PyTorch build."),
]

def follow(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        # Seek to end
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield line

def suggest(line):
    for pattern, tip in ERROR_PATTERNS:
        m = pattern.search(line)
        if m:
            matched = m.group(0)
            return tip
    return None

def main():
    parser = argparse.ArgumentParser(description='Watch a PowerShell transcript file and suggest fixes for errors.')
    parser.add_argument('-f', '--file', required=True, help='Path to transcript file to watch')
    args = parser.parse_args()

    transcript = args.file
    if not os.path.isfile(transcript):
        print(f"Transcript not found: {transcript}")
        sys.exit(1)

    print(f"Watching transcript: {transcript}")
    print("Will display suggestions when errors are detected. Press Ctrl+C to stop.")

    suggestions_log = os.path.join(os.path.dirname(transcript), 'error_suggestions.log')

    try:
        for line in follow(transcript):
            tip = suggest(line)
            if tip:
                timestamp = datetime.now().strftime('%H:%M:%S')
                msg = f"[{timestamp}] Suggestion: {tip}"
                print(msg)
                try:
                    with open(suggestions_log, 'a', encoding='utf-8') as out:
                        out.write(f"{msg}\n")
                        out.write(f"  Trigger: {line.strip()}\n\n")
                except Exception:
                    pass
    except KeyboardInterrupt:
        print("Stopped watching.")

if __name__ == '__main__':
    main()
