# install.py

import os

packages_to_install = ["rsa", "pyfiglet", "rich", "termcolor", "pyopenssl"]

for package in packages_to_install:
    exit_code = os.system(f"pip show {package} > nul 2>&1")
    if exit_code != 0:
        os.system(f"pip install {package}")
        print(f"Installed {package} successfully.")
    else:
        print(f"{package} is already installed.")

print("All required packages are installed.")

