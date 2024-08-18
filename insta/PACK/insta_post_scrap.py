"""
Author: Farid Mohammadi
Date: 2024-08-15 09:00:27
LastEditors: 
LastEditTime: 2024-08-15 09:21:21
FilePath: insta_post_scrap.py
Description: Scraping posts from Instagram using Selenium
"""
import os
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from urllib.parse import urlparse
from utils import check_load_page
from url_proxy_set import set_proxy


def create_post_driver(post_url, try_count=3):
    is_loaded = False
    if try_count <= 0:
        print("The number try-count must be greater than 0.")
        return None, False
    print("Trying to create driver...")
    while try_count > 0:
        try_count -= 1
        driver = set_proxy()
        driver.get(post_url)
        time.sleep(15)
        if check_load_page(driver):
            is_loaded = True
            break
        else:
            continue

    if is_loaded:
        print("Driver created successfully.")
        return driver, True
    else:
        print("Failed to create driver after multiple attempts.")
        return None, False
    

def go_to_post(pid):
    """
    Go to a specific post by its id.

    Parameters:
    pid (str): The id of the post.

    Returns:
    bool: All information we need about the post
    """
    post_url = f"https://www.instagram.com/p/{pid}"
    post_driver, is_loaded = create_post_driver(post_url)
    if not is_loaded:
        print("Exiting program.")
        exit(1)
        
    try:
        p_driver = set_proxy()
        p_driver.get(post_url)
        if check_load_page(post_driver):
            print("Insight Post loaded successfully.")
            post_info = {}

            return post_info
        else:
            print("Failed to load insight post.")
            return None
    except Exception as e:
        print(f"Error loading insight post: {e}")
        return None
