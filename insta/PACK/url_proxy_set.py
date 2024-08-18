"""
Author: Farid Mohammadi 
Date: 2024-08-13 12:36:58
LastEditors: 
LastEditTime: 2024-08-17 14:53:01
FilePath: insta/PACK/url_proxy_set.py
Description: Set url proxy for selenium webdriver.
"""
import os
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random


def set_proxy():
    proxies_list = []
    current_dir = os.getcwd()
    with open(current_dir + "/insta/PACK/proxy/up-proxies.txt", "r") as f:
        for line in f:
            proxies_list.append(line.strip("\n"))
    
    proxy_url = random.choice(proxies_list)
    seleniumwire_options = {
        "proxy": {
            "http": proxy_url
        }
    }
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("enable-automation")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-javascript")
    options.add_argument("--disable-image-loading")
    options.add_argument('--blink-settings=imagesEnabled=false')
    
    options.page_load_strategy = 'eager'
    # options.platform_name = 'any'
    options.accept_insecure_certs = True
    
    options.add_experimental_option(
        "prefs", {
            "profile.managed_default_content_settings.images": 2,
            'profile.managed_default_content_settings.javascript': 2
        }
    )
    options.add_argument("--disk-cache-dir=C:\mhmdi\dj-scrap\instascrap\insta\PACK\cache")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        seleniumwire_options=seleniumwire_options,
        options=options,
    )
    
    return driver
    