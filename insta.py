import sys
import time
import random

import click
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as sl_exceptions


def do_login(driver, username, password, posturl):
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


@click.command()
@click.argument('username', required=True)
@click.argument('password', required=True)
@click.argument('posturl', required=True)
@click.argument('inputfile', type=click.File('r'), default='input.txt')
def run(username, password, posturl, inputfile):
    inputs = inputfile.read().split('\n')
    # random.shuffle(arrobas)

    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com")
    do_login(driver, username, password, posturl)

    tam = len(inputs)
    i = 0
    ok = 0
    while i<(tam):
        try:
            time.sleep(1)
            comment_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@aria-label="Adicione um comentário..."]')
                )
            )
            comment_input.send_keys(inputs[i])
            time.sleep(1)
            button = driver.find_element(
                By.XPATH, '//button[text()="Publicar"]'
            )
            button.click()
            try:
                error = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[text()="Tentar novamente"]')
                    )
                )
            except:
                ok = ok+1
                i = i+1
                print('posted: {}'.format(inputs[i]))

        except sl_exceptions.InvalidElementStateException as err:
            print(err)
            print('{}/{}'.format(i, tam))
            driver.get(posturl)
        except sl_exceptions.WebDriverException as err:
            print(err)
            print('{}/{}'.format(i, tam))
            continue

if __name__ == '__main__':
    run()
