import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as sl_exceptions

driver = webdriver.Chrome()
driver.get("https://www.instagram.com")

username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@name="username"]'))
)
username.send_keys(usrn)

password = driver.find_element(By.XPATH, '//*[@name="password"]')
password.send_keys(pswd)
password.send_keys(Keys.RETURN)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Página inicial"]'))
)
button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//button[text()="Agora não"]'))
)
button.click()

POST_URL = 'https://www.instagram.com/p/B2Mey3SHywTK3oLJNzAnjm13RajzfKvOK0BA8k0/'
driver.get(POST_URL)

inputs = 'M A N A - M A R I A'.split()
i = 0
while i<(len(inputs)):
    try:
        comment_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@aria-label="Adicione um comentário..."]')
            )
        )
        button = driver.find_element(By.XPATH, '//button[text()="Publicar"]')
        time.sleep(2)
        comment_input.send_keys(inputs[i])
        button.click()
        print('OK')
        i = i+1
    except sl_exceptions.InvalidElementStateException as err:
        print('ERRO: '+ str(err))
        driver.get(POST_URL)
    except Exception as err:
        print('ERRO: '+ str(err))
