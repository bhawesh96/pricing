import subprocess

# List of Python files to execute
python_files = ['bigbasket.py', 'swiggy.py', 'dunzo.py', 'deeprooted.py', 'chennai_grocers.py', 'gourmet_garden.py']

# Execute each Python file
for file in python_files:
    try:
        subprocess.run(["python3", file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {file}: {e}")