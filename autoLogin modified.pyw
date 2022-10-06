from pickle import FALSE
import time
from unittest import result
import pyautogui
import win32gui as win
import win32con
import tkinter as tk
from tkinter import ttk
import json
from selenium import webdriver
from selenium.webdriver.common.by import By


class AutoLogin:
    white = "#ffffff"
    username = ""
    password = ""
    dropdown_index = None
    git_bash_window_index = None
    git_bash_window_ssh = None
    username_content_label = None
    password_content_label = None
    cred_data = None
    login_btn = None
    window_list = None
    selected_window = None
    git_bash_window_dropdown = None
    aws_destination = None
    aws_source = None
    commit = None

    def __init__(self):
        root = tk.Tk()
        AutoLogin.dropdown_index = tk.StringVar()
        AutoLogin.git_bash_window_index = tk.StringVar()
        AutoLogin.aws_destination = tk.StringVar()
        AutoLogin.aws_source = tk.StringVar()
        AutoLogin.commit = tk.StringVar()
        self.root = root
        root.title("Auto Login")
        white = AutoLogin.white

        # main frame
        main_frame = tk.Frame(root, bg=white, height=300,
                              width=400, padx=10, pady=20)
        main_frame.pack()
        # main_frame.pack_propagate(0)
        # main_frame.grid_propagate(0)

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

        # Git bash window selection frame
        git_bash_window_selection_frame = tk.Frame(
            main_frame, background=white)
        git_bash_window_selection_frame.pack(side="top")

        git_bash_window_label = tk.Label(
            git_bash_window_selection_frame, text="Select window:", padx=10, background=white)
        git_bash_window_label.grid(row=0, column=0)

        git_bash_window_dropdown = ttk.Combobox(git_bash_window_selection_frame, width=27,
                                                textvariable=AutoLogin.git_bash_window_index)
        AutoLogin.git_bash_window_dropdown = git_bash_window_dropdown
        git_bash_window_dropdown['values'] = AutoLogin.populate_git_bash_list()
        git_bash_window_dropdown.bind(
            '<<ComboboxSelected>>', AutoLogin.git_bash_window_selection_handler)
        git_bash_window_dropdown.grid(row=0, column=1, pady=10, padx=5)
        git_bash_window_dropdown.current()

        git_bash_window_list_refresh_btn = tk.Button(
            git_bash_window_selection_frame, text="⟳", command=lambda: AutoLogin.refresh_git_bash_dropdown_list())
        git_bash_window_list_refresh_btn.grid(row=0, column=2, padx=5)

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

        username_label.grid(column=0, row=0)
        username_content.grid(column=1, row=0)
        password_label.grid(column=0, row=1)
        password_content.grid(column=1, row=1)

        # login button frame
        login_btn_frame = tk.Frame(main_frame, background=white, pady=20)
        login_btn_frame.pack(side="top")
        login_btn = tk.Button(login_btn_frame, text="Login",
                              command=AutoLogin.wait_and_login)
        login_btn.pack(side="top")

        # AWS console frame
        aws_console_frame = tk.Frame(main_frame, background=white, pady=10)
        aws_console_frame.pack(side="top")

        branches = AutoLogin.cred_data["branches"]

        destination_label = tk.Label(
            aws_console_frame, text="Destination", bg=white, font=("", 12))
        destination_label.grid(row=0, column=0, padx=10, pady=5)

        destination_dropdown = tk.OptionMenu(
            aws_console_frame, AutoLogin.aws_destination, *branches)
        destination_dropdown.grid(row=0, column=1, padx=10, pady=5)

        source_label = tk.Label(
            aws_console_frame, text="Source", bg=white, font=("", 12))
        source_label.grid(row=0, column=2, padx=10, pady=5)

        source_dropdown = tk.OptionMenu(
            aws_console_frame, AutoLogin.aws_source, *branches)
        source_dropdown.grid(row=0, column=3, padx=10, pady=5)

        commit_text = tk.Entry(
            aws_console_frame, textvariable=AutoLogin.commit, highlightthickness=1, highlightbackground="black")
        commit_text.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        commit_and_merge_btn = tk.Button(
            aws_console_frame, text="Commit and Merge", command=lambda: AutoLogin.commit_and_merge_aws_console())
        commit_and_merge_btn.grid(
            row=1, column=2, columnspan=2, padx=10, pady=5)

        # git commands buttons frame
        git_commands_btns_frame = tk.Frame(
            main_frame, background=white, pady=0)
        git_commands_btns_frame.pack(side="top")

        # getting list of commands from file
        rowColData = {
            "other": {
                "row": 0,
                "column": 0
            }
        }
        for index, item in enumerate(self.cred_data["sortInColumn"]):
            rowColData[item] = {
                "row": 0,
                "column": index+1
            }

        if(len(self.cred_data["gitCommands"]) > 0):
            for git_command in self.cred_data["gitCommands"]:
                checker = [element for element in rowColData.keys() if(
                    element in git_command["command"])]
                checkResult = "".join(checker)
                name = AutoLogin.get_name(git_command["command"])
                btn = tk.Button(git_commands_btns_frame, text=name, command=lambda command=git_command["command"], login=git_command["login"]: AutoLogin.git_bash_command_function(
                    command, login))
                if(checkResult != ""):
                    row = rowColData[checkResult]["row"]
                    column = rowColData[checkResult]["column"]
                    btn.grid(row=row, column=column, padx=5, pady=5)
                    rowColData[checkResult]["row"] += 1
                else:
                    row = rowColData["other"]["row"]
                    column = rowColData["other"]["column"]
                    btn.grid(row=row, column=column, padx=5, pady=5)
                    rowColData["other"]["row"] += 1

                print(checkResult, git_command["command"])

        root.mainloop()

    def get_name(name):
        name_length = 20
        final_name = ""
        name_array = name.split()
        for index, item in enumerate(name_array):
            if(index == 0):
                final_name += item
            else:
                last_word = final_name.splitlines()[-1]
                if(len(last_word) + len(item) + 1 <= name_length):
                    final_name += " " + item
                else:
                    final_name += "\n" + item
        return final_name

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
        window_name = AutoLogin.cred_data["loginWindowName"]
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

    def git_bash_command_function(command, login=False):
        ssh = AutoLogin.git_bash_window_ssh
        AutoLogin.find_window_and_type(ssh, command)
        if login:
            AutoLogin.wait_and_login()

    def get_git_bash_window_handler(hwnd, ctx):
        git_window_name = AutoLogin.cred_data["gitBashWindowName"]
        if git_window_name in win.GetWindowText(hwnd):
            ctx(hwnd)

    def git_bash_window_selection_handler(event):
        window_name = AutoLogin.git_bash_window_index.get()
        ssh = ''
        for i in AutoLogin.window_list:
            if(window_name == i["title"]):
                ssh = i["ssh"]
                break
        AutoLogin.git_bash_window_ssh = ssh

    def populate_git_bash_list():
        ssh = []

        def callback(hwnd):
            nonlocal ssh
            ssh.append({
                "ssh": hwnd,
                "title": win.GetWindowText(hwnd)
            })
        win.EnumWindows(AutoLogin.get_git_bash_window_handler, callback)
        text_list = []
        AutoLogin.window_list = ssh
        for i in ssh:
            text_list.append(i["title"])

        return text_list

    def refresh_git_bash_dropdown_list():
        AutoLogin.git_bash_window_dropdown["values"] = AutoLogin.populate_git_bash_list(
        )

    def commit_and_merge_aws_console():
        commit_message = AutoLogin.commit.get()
        commit_command = 'git commit -m "'+ commit_message + '"'
        AutoLogin.git_bash_command_function("git pull origin development", True)
        AutoLogin.git_bash_command_function(commit_command, False)
        AutoLogin.git_bash_command_function("git push", True)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")

        url = "https://ap-south-1.console.aws.amazon.com/codesuite/codecommit/repositories/AICOE_FE/browse?region=ap-south-1"

        driver = webdriver.Chrome(
            "C:\\Users\\agour\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)

        driver.maximize_window()
        driver.implicitly_wait(10)
        # Loading URL
        driver.get(url)

        # General User login IAM
        driver.find_element(
            by=By.ID, value="aws-signin-general-user-selection-iam").click()
        driver.find_element(
            by=By.ID, value="resolving_input").send_keys("622055726692")
        driver.find_element(by=By.ID, value="next_button").click()
        # time.sleep(5)
        # Credential Login
        driver.find_element(by=By.ID, value="username").send_keys("aayushG")
        driver.find_element(by=By.ID, value="password").send_keys(
            "jRyG'|(x^Xg0puc")
        driver.find_element(by=By.ID, value="signin_button").click()
        time.sleep(5)

        # Create Pull Request
        driver.find_element(
            by=By.XPATH, value="//*[@id='app']/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[1]/div/div[2]/awsui-button/a").click()
        time.sleep(3)

        # Select Development in Destination
        select1 = driver.find_element(
            by=By.XPATH, value="//*[@id='awsui-select-1']")
        select1.click()
        # select1.send_keys("development")
        select1.find_element(
            by=By.XPATH, value='//*[@id="awsui-select-1-dropdown"]/div/ul/li/ul/li/div[@title="'+AutoLogin.aws_destination.get()+'"]').click()

        # Select feat/aayush in source
        select2 = driver.find_element(
            by=By.XPATH, value="//*[@id='awsui-select-2']")
        select2.click()
        # select2.send_keys("feat/aayush")
        select2.find_element(
            by=By.XPATH, value='//*[@id="awsui-select-2-dropdown"]/div/ul/li/ul/li/div[@title="'+AutoLogin.aws_source.get()+'"]').click()

        # Click Compare
        driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div/form/div/div[4]/awsui-button[1]/button').click()

        # Type in input
        driver.find_element(
            by=By.ID, value="awsui-input-5").send_keys(commit_message)
        time.sleep(3)
        # Submit Pull Request
        driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div/div[3]/form/awsui-form/div/div[2]/span/span/awsui-form-section/div/div[1]/div/div/span/div/div/div[2]/awsui-button/button').click()

        # Merge Pull request
        driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[1]/div/div[2]/awsui-button[2]/a').click()

        time.sleep(3)

        # Uncheck delete Source branch
        driver.find_element(
            by=By.XPATH, value='//*[@id="awsui-checkbox-2"]').click()
        # Merge request
        driver.find_element(
            by=By.XPATH, value='//*[@id="app"]/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/form/awsui-form/div/div[4]/span/div/div[1]/awsui-button/button').click()

        time.sleep(5)
        driver.quit()


AutoLogin()
