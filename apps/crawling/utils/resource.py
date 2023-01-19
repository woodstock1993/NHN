import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

chromedriver_path = os.getcwd() + '/chromedriver'
driver = webdriver.Chrome(service=Service(chromedriver_path), options=webdriver.ChromeOptions())