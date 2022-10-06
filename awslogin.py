from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

commit = "Removing unnecessary console logs"

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
driver.find_element(by=By.ID, value="password").send_keys("jRyG'|(x^Xg0puc")
driver.find_element(by=By.ID, value="signin_button").click()
time.sleep(5)

# Create Pull Request
driver.find_element(
    by=By.XPATH, value="//*[@id='app']/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[1]/div/div[2]/awsui-button/a").click()
time.sleep(3)

# Select Development in Destination
select1 = driver.find_element(by=By.XPATH, value="//*[@id='awsui-select-1']")
select1.click()
# select1.send_keys("development")
select1.find_element(
    by=By.XPATH, value='//*[@id="awsui-select-1-dropdown"]/div/ul/li/ul/li/div[@title="development"]').click()

# Select feat/aayush in source
select2 = driver.find_element(by=By.XPATH, value="//*[@id='awsui-select-2']")
select2.click()
# select2.send_keys("feat/aayush")
select2.find_element(
    by=By.XPATH, value='//*[@id="awsui-select-2-dropdown"]/div/ul/li/ul/li/div[@title="feat/aayush"]').click()

# Click Compare
driver.find_element(
    by=By.XPATH, value='//*[@id="app"]/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div/form/div/div[4]/awsui-button[1]/button').click()

# Type in input
driver.find_element(
    by=By.ID, value="awsui-input-5").send_keys(commit)
time.sleep(3)
# Submit Pull Request
driver.find_element(
    by=By.XPATH, value='//*[@id="app"]/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div/div[3]/form/awsui-form/div/div[2]/span/span/awsui-form-section/div/div[1]/div/div/span/div/div/div[2]/awsui-button/button').click()

# Merge Pull request
driver.find_element(
    by=By.XPATH, value='//*[@id="app"]/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[1]/div/div[2]/awsui-button[2]/a').click()

time.sleep(3)

# Uncheck delete Source branch
driver.find_element(by=By.XPATH, value='//*[@id="awsui-checkbox-2"]').click()
# Merge request
driver.find_element(
    by=By.XPATH, value='//*[@id="app"]/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/form/awsui-form/div/div[4]/span/div/div[1]/awsui-button/button').click()

time.sleep(3)
driver.quit()
