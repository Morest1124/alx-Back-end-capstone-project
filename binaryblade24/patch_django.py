import os
import sys

# Path provided in traceback
file_path = r"C:\Users\mores\BinaryBlade24\alx-Back-end-capstone-project\venv\Lib\site-packages\django\template\context.py"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Read {len(content)} bytes from {file_path}")
    
    # Locate the verify specific problematic area
    # Looking for BaseContext.__copy__
    
    snippet = "duplicate = super().__copy__()"
    if snippet in content:
        print("Found 'duplicate = super().__copy__()'")
        
        # We need to replace this specific call inside BaseContext (which is usually near the top)
        # Note: Context.__copy__ also calls super().__copy__(), but the traceback says error is at line 39
        # which is likely BaseContext.
        
        lines = content.splitlines()
        for i, line in enumerate(lines):
             # Just a heuristic to find the class BaseContext block
            if "class BaseContext" in line:
                print(f"Found BaseContext at line {i+1}")
            
            # The specific line 39 (approx)
            if "duplicate = super().__copy__()" in line:
                print(f"Found target at line {i+1}: {line.strip()}")
                
                # Check if this looks like the one in BaseContext (it's early in the file)
                if i < 100: # BaseContext is usually first
                    print("Patching line...")
                    # Indentation usually 8 spaces
                    indent = line[:line.find("duplicate")]
                    # Replace with instantiation
                    lines[i] = f"{indent}duplicate = self.__class__()"
                    print(f"Replaced with: {lines[i].strip()}")
        
        new_content = "\n".join(lines)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully patched context.py")
        
    else:
        print("Could not find the specific snippet to patch.")

except Exception as e:
    print(f"Error: {e}")
