# Auto Login GUI for git bash
Auto Login for git bash using Python 

## Requirements
```
Python 3.x.x
```

### Libraries Required
```
pyautogui
win32gui
win32con
time
tkinter (tk, ttk)
json
```
## Installation
Download the libraries and the files.

## Usage

You can run the `autoLogin.py` file or `autoLogin.pyw` file if you don't want the console to display

Make sure to edit the credentials in the credentials.json file.

You can add multiple accounts with usernames and passwords, but make sure to keep the account names unique.

After selecting the acccount you can click on login.

The program will listen wait till the window with the title "OpenSSH" pops up. 

It will then enter the username, and then the password.
