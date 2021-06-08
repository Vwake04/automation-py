from time import sleep
from selenium import webdriver

# Initialize Chrome
driver = webdriver.Chrome()

# Navigate to url
driver.get("https://www.maersk.com/")
sleep(5)

# Accept the cookies
try:
    _cookie = '//*[@id="coiPage-1"]/div[2]/button[3]'
    el_cookie = driver.find_element_by_xpath(_cookie)
    driver.execute_script("arguments[0].click();", el_cookie)
    sleep(5)
except Exception as e:
    print("Failed to click: Allow All Cookies")

# Click Logo
try: 
    _logo = '//*[@id="ign-header"]/div[2]/div[8]/div/a'
    el_logo = driver.find_element_by_xpath(_logo)
    driver.execute_script("arguments[0].click();", el_logo)
    sleep(5)
except:
    print("Failed to click: Login logo")

try:
    _user = '//*[@id="ign-username"]'
    el_user = driver.find_element_by_xpath(_user)
    el_user.send_keys("bhavesh_global")
except:
    print("Failed to enter: Login Username")

try:
    _pass = '//*[@id="panel__login"]/form/div[1]/div[4]/input'
    el_pass = driver.find_element_by_xpath(_pass)
    el_pass.send_keys("Bhavesh2019$")
except:
    print("Failed to enter: Login Password")

try:
    _submit = '//*[@id="panel__login"]/form/div[1]/div[5]/div/button[1]'
    el_submit = driver.find_element_by_xpath(_submit)
    driver.execute_script("arguments[0].click();", el_submit)
except:
    print("Failed to click: Submit Button")

print("Logged In")


