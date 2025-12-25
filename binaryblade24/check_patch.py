import os

file_path = r"C:\Users\mores\BinaryBlade24\alx-Back-end-capstone-project\venv\Lib\site-packages\django\template\context.py"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    print(f"File has {len(lines)} lines.")
    start = max(0, 25)
    end = min(len(lines), 50)
    print(f"Lines {start+1} to {end}:")
    for i in range(start, end):
        print(f"{i+1}: {lines[i].rstrip()}")
        
except Exception as e:
    print(f"Error reading file: {e}")
