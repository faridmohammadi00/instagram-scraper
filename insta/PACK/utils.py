"""
Author: Farid Mohammadi
Date: 2024-08-15 09:04:53
LastEditors: 
LastEditTime: 2024-08-15 09:21:21
FilePath: utils.py
Description: Function for utility purposes
"""
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import wget


def check_load_page(driver):
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Reload page')]")
        return False
    except NoSuchElementException:
        return True
    

def allow_all_cookies(driver):
    try:
        allow_cookies_element = driver.find_element(By.XPATH, "//button[contains(text(), 'Allow all cookies')]")
        print("Allowing all cookies: ", allow_cookies_element.text)
        allow_cookies_element.click()
    except NoSuchElementException:
        return 0
    

def create_directory(username):
    if os.path.isdir("data/" + username) is not True:
        print('Creating user directory...')
        os.mkdir("./data/" + username)
        os.mkdir("./data/" + username + "/profile")
        os.mkdir("./data/" + username + "/posts")
        os.mkdir("./data/" + username + "/reels")
        os.mkdir("./data/" + username + "/highlights")

    return True


def download(url_list, username, state):
    create_directory(username)
    current_dir = os.getcwd()
    for url in url_list:
        try:
            print(f'Downloading {url}...')
            wget.download(url, f'{current_dir}/data/{username}/{state}')

        except Exception as e:
            print(f'Error downloading {url}: {e}')

    return True
    