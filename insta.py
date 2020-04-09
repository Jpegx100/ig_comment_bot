import sys
import time

import click
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as sl_exceptions


driver = webdriver.Chrome()
driver.get("https://www.instagram.com")


@click.command()
@click.argument('username', required=True)
@click.argument('password', required=True)
@click.argument('posturl', required=True)
@click.argument('inputfile', type=click.File('r'), default='input.txt')
def run(username, password, posturl, inputfile):
    inputs = inputfile.read().split('\n')

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@name="username"]'))
    )
    username_input.send_keys(username)
    password_input = driver.find_element(By.XPATH, '//*[@name="password"]')
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    # TODO: Support other languages
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@aria-label="Página inicial"]')
        )
    )

    driver.get(posturl)
    i = 0
    while i<(len(inputs)):
        try:
            comment_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@aria-label="Adicione um comentário..."]')
                )
            )
            comment_input.send_keys(inputs[i])

            button = driver.find_element(
                By.XPATH, '//button[text()="Publicar"]'
            )
            button.click()
            print('posted: {}'.format(inputs[i]))
            i = i+1

        except sl_exceptions.InvalidElementStateException as err:
            time.sleep(2)
            print(err)
            driver.get(posturl)
        except sl_exceptions.WebDriverException as err:
            print(err)
            continue

if __name__ == '__main__':
    run()
