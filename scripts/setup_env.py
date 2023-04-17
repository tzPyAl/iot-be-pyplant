import os
import subprocess
import sys
import venv

venv_name= "venv"

def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix

# Determine the paths to the script and requirements.txt
script_path = os.path.dirname(os.path.abspath(__file__))
reqs_path = os.path.join(script_path, "..", "requirements.txt")

# Create the virtual environment in a venv folder in the project root directory
venv_dir = os.path.join(script_path, "..", venv_name)
venv.create(venv_dir, with_pip=True)

# Activate the virtual environment
activate_script = os.path.join(script_path[:-8], venv_name, "Scripts", "activate") if sys.platform == "win32" else os.path.join(script_path[:-8], venv_name, "bin", "activate")
subprocess.run(f"source {activate_script}", shell=True)

if in_virtualenv():
    subprocess.run(f"pip install -r {reqs_path} && pip freeze", shell=True)
else:
    print(f"venv not activated with: {activate_script}")
