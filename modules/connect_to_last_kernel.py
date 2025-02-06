import os
import glob
import subprocess
from pathlib import Path

# Define the Jupyter runtime directory
runtime_dir = Path.home() / 'AppData' / 'Roaming' / 'jupyter' / 'runtime'

# Get a list of all kernel connection files
kernel_files = glob.glob(str(runtime_dir / 'kernel-*.json'))

# Check if there are any kernel files
if not kernel_files:
    print("No Jupyter kernel connection files found.")
    exit(1)

# Find the latest kernel file based on modification time
latest_kernel_file = max(kernel_files, key=os.path.getmtime)

# Print the latest kernel file
print(f"Connecting to the latest kernel: {latest_kernel_file}")

# Open the latest kernel using ipython console
subprocess.run(['jupyter', 'console', '--existing', latest_kernel_file])