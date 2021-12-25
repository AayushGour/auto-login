import pyautogui
import win32gui as win
import win32con
import time
import tkinter as tk
from tkinter import ttk
import json


class AutoLogin:
    white = "#ffffff"
    username = ""
    password = ""
    dropdown_index = None
    username_content_label = None
    password_content_label = None
    cred_data = None
    login_btn = None

    def __init__(self):
        root = tk.Tk()
        AutoLogin.dropdown_index = tk.StringVar()
        self.root = root
        root.title("Auto Login")
        white = AutoLogin.white

        # main frame
        main_frame = tk.Frame(root, bg=white, height=250, width=400)
        main_frame.pack()
        main_frame.pack_propagate(0)
        main_frame.grid_propagate(0)

        # header frame
        header_frame = tk.Frame(
            main_frame, background=white, padx=10, pady=10)
        header_frame.pack(side="top")
        header_label = tk.Label(
            header_frame, text="Auto Login", bg=white,  font=("", 20))
        header_label.pack(side="top")

        # content frame
        content_frame = tk.Frame(
            main_frame, background=white, padx=10, pady=10)
        content_frame.pack(side="top")

        help_label = tk.Label(
            content_frame, text="Select an account:", bg=white, font=("", 12))
        help_label.pack(side="left", pady=10, padx=5)

        # Drop down
        dropdown = ttk.Combobox(content_frame, width=27,
                                textvariable=AutoLogin.dropdown_index)
        # Getting file
        file = open("credentials.json")
        allData = json.load(file)
        AutoLogin.cred_data = allData
        dropdown_values = []
        for detail in allData["userDetails"]:
            dropdown_values.append(detail["accountName"])

        file.close()
        # Adding combobox drop down list
        dropdown['values'] = dropdown_values
        dropdown.bind('<<ComboboxSelected>>', AutoLogin.combobox_handler)
        dropdown.pack(side="right", pady=10, padx=5)
        dropdown.current()

        # credentials frame
        credentials_frame = tk.Frame(main_frame, background=white)
        credentials_frame.pack(side="top")

        username_label = tk.Label(
            credentials_frame, text="Username:", padx=10, background=white)
        username_content = tk.Label(
            credentials_frame, text="-", padx=10, background=white)

        password_label = tk.Label(
            credentials_frame, text="Password:", padx=10, background=white)
        password_content = tk.Label(
            credentials_frame, text="-", padx=10, background=white)

        AutoLogin.username_content_label = username_content
        AutoLogin.password_content_label = password_content

        # login button frame
        login_btn_frame = tk.Frame(main_frame, background=white, pady=20)
        login_btn_frame.pack(side="top")
        login_btn = tk.Button(login_btn_frame, text="Login",
                              command=AutoLogin.wait_and_login)
        login_btn.pack(side="top")

        username_label.grid(column=0, row=0)
        username_content.grid(column=1, row=0)
        password_label.grid(column=0, row=1)
        password_content.grid(column=1, row=1)

        root.geometry("400x250")
        root.mainloop()

    def find_window_and_type(window_handle, credential):
        win.ShowWindow(window_handle, win32con.SW_SHOW)
        win.BringWindowToTop(window_handle)
        win.SetActiveWindow(window_handle)
        win.SetForegroundWindow(window_handle)
        pyautogui.typewrite(credential)
        pyautogui.hotkey("enter")

    def wait_and_login():
        counter = 0
        timeout = AutoLogin.cred_data["timeout"]
        window_name = AutoLogin.cred_data["windowName"]
        ssh = win.FindWindow(None, window_name)
        while ssh == 0:
            if counter < timeout:
                time.sleep(1)
                ssh = win.FindWindow(None, window_name)
                counter = counter + 1
            else:
                pyautogui.alert(text="Wait Timed Out: " +
                                str(timeout)+" seconds", title="Wait Timed Out")
                return False

        AutoLogin.find_window_and_type(ssh, AutoLogin.username)
        time.sleep(1)
        ssh = win.FindWindow(None, window_name)
        while ssh == 0:
            time.sleep(1)
            ssh = win.FindWindow(None, window_name)

        AutoLogin.find_window_and_type(
            ssh, AutoLogin.password)

    def combobox_handler(event):
        selected_key = AutoLogin.dropdown_index.get()
        userDetails = AutoLogin.cred_data["userDetails"]
        for detail in userDetails:
            if detail["accountName"] == selected_key:
                AutoLogin.username_content_label.config(
                    text=detail["username"])
                AutoLogin.password_content_label.config(
                    text=detail["password"])
                AutoLogin.username = detail["username"]
                AutoLogin.password = detail["password"]
                break


AutoLogin()
