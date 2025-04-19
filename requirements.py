import sys
import subprocess

def install_packages():
    # List of required packages
    packages = [
        'customtkinter',
        'Pillow',
        'mysql-connector-python',
        'matplotlib',
        'fpdf'
    ]

    print("Installing required packages...")
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"{package} installed successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}. Please try installing manually.")
        except Exception as e:
            print(f"An error occurred while installing {package}: {e}")

    print("\nRequired Package installation complete.")

if __name__ == "__main__":
    install_packages()