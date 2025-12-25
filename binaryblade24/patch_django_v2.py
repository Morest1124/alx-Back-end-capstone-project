import os

file_path = r"C:\Users\mores\BinaryBlade24\alx-Back-end-capstone-project\venv\Lib\site-packages\django\template\context.py"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    patched = False
    for i, line in enumerate(lines):
        # We are looking for the __copy__ method in BaseContext class
        # Based on previous check, it's around line 38
        if "duplicate =" in line and "super()" in line and "copy" in line:
            # Matches 'duplicate = copy(super())' or 'duplicate = super().__copy__()'
            print(f"Found match at line {i+1}: {line.strip()}")
            
            # Preserve indentation
            indent = line[:line.find("duplicate")]
            
            # Replace with compatible instantiation
            lines[i] = f"{indent}duplicate = self.__class__()\n"
            print(f"Replaced with: {lines[i].strip()}")
            patched = True
            break
    
    if patched:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("Successfully applied patch v2.")
    else:
        print("Could not find the line to patch.")

except Exception as e:
    print(f"Error: {e}")
