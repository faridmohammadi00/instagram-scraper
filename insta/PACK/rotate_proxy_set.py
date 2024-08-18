"""
Author: Farid Mohammadi  
Date: 2024-08-13 13:00:02
LastEditors: 
LastEditTime: 2024-08-13 16:25:38
FilePath: rotate_proxy_set.py
Description: Set rotate proxy on selenium webdriver.
"""
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import random


def set_rotate_proxy():
    proxies_list = []
    with open("proxy/proxies.txt", "r") as f:
        for line in f:
            proxies_list.append(line.strip("\n"))
    
    proxy = random.choice(proxies_list)
    seleniumwire_options = {
        "proxy": {
            "http": proxy,
            "https": proxy
        }
    }
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        seleniumwire_options=seleniumwire_options,
        options=options
    )
    
    return driver
            