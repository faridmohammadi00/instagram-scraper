import os
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from .url_proxy_set import set_proxy
from urllib.parse import urlparse
from .utils import check_load_page, allow_all_cookies


def get_number_of_pff(driver):
    try:
        li_wrapper = driver.find_elements(By.XPATH, "//li[@class='xl565be x1m39q7l x1uw6ca5 x2pgyrj']")
        n_posts = 0
        n_followers = 0
        n_real_followers = 0
        n_following = 0
        n_real_following = 0
        for element in li_wrapper:
            pff_spans = element.find_elements(By.TAG_NAME, "span")
            if li_wrapper.index(element) == 0:
                n_posts = pff_spans[0].text
            if li_wrapper.index(element) == 1:
                n_followers = pff_spans[0].text
                if pff_spans[0].get_attribute("title"):
                    n_real_followers = pff_spans[0].get_attribute("title")

            if li_wrapper.index(element) == 2:
                n_following = pff_spans[0].text
                if pff_spans[0].get_attribute("title"):
                    n_real_following = pff_spans[0].get_attribute("title")

        return {
            "posts": n_posts,
            "followers": n_followers,
            "real_followers": n_real_followers,
            "following": n_following,
            "real_following": n_real_following
        }
    except NoSuchElementException:
        return 0


def get_profile_picture(driver):
    try:
        profile_picture_element = driver.find_element(By.XPATH, "//img[@class='xpdipgo x972fbf xcfux6l x1qhh985 xm0m39n xk390pu x5yr21d xdj266r x11i5rnm xat24cr x1mh8g0r xl1xv1r xexx8yu x4uap5 x18d9i69 xkhd6sd x11njtxf xh8yej3']")
        profile_picture_url = profile_picture_element.get_attribute("src")

        return [profile_picture_url]
    except NoSuchElementException:
        print("Profile Picture URL: ", "None")
        return None


def try_create_driver(username, try_count):
    is_loaded = False
    if try_count <= 0:
        print("The number try-count must be greater than 0.")
        return None, False
    print("Trying to create driver...")
    while try_count > 0:
        try_count -= 1
        driver = set_proxy()
        driver.get("https://www.instagram.com/" + username + "/")
        # time.sleep(10)
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


def check_online_story(driver):
    try:
        canvas = driver.find_element(By.CLASS_NAME, "_aarh")
        if canvas:
            print("Online story found.")
            return True
    except NoSuchElementException:
        print("No online story found.")
        return False


def get_highlights(driver):
    h_infos = {}
    h_cover_urls = []
    try:
        highlights_elements = driver.find_elements(By.XPATH, "(//div[@class='x6s0dn4 x9f619 x78zum5 xdt5ytf xwzhuwn x19xppfw x1lvlso5 x1hqdklf x4js05n xm4az7 x1jo5dny x5zefxq x1u2d83q x1lvagci x11853ko'])")
        print("Number of Highlights: ", len(highlights_elements))
        for element in highlights_elements:
            h_img = element.find_element(By.TAG_NAME, "img")
            h_url = h_img.get_attribute("src")
            h_infos[element.text.strip()] = h_url
            h_cover_urls.append(h_url)

        print("Highlights: ", h_infos)

        return h_cover_urls, h_infos

    except NoSuchElementException:
        print("No highlights found.")
        return None


def get_bio(driver):
    try:
        bio_element = driver.find_element(By.XPATH, "//span[@class='_ap3a _aaco _aacu _aacx _aad7 _aade']")
        return bio_element.text.strip()

    except NoSuchElementException:
        print("No bio found.")
        return ''


def get_bio_link(driver):
    try:
        bio_element = driver.find_element(By.XPATH, "//div[@class='x3nfvp2 x193iq5w']")
        return bio_element.text.strip()

    except NoSuchElementException:
        print("No bio's link found.")
        return ''


def get_name(driver):
    try:
        name_element = driver.find_element(By.XPATH, "//div[@class='x9f619 xjbqb8w x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1oa3qoh x6s0dn4 x1amjocr x78zum5 xl56j7k']")
        return name_element.text.strip()

    except NoSuchElementException:
        print("No name found.")
        return ''


def get_posts(driver):
    try:
        posts_elements = driver.find_elements(By.XPATH, "//div[@class='x1lliihq x1n2onr6 xh8yej3 x4gyw5p x2pgyrj x56m6dy x1ntc13c xn45foy x9i3mqj']")
        print("Number of Posts: ", len(posts_elements))
        post_urls = []
        post_img_urls = []
        post_img_alts = {}
        for element in posts_elements:
            post_a = element.find_element(By.TAG_NAME, "a")
            post_url = post_a.get_attribute("href")
            post_urls.append(post_url)
            img_cover_element = post_a.find_element(By.TAG_NAME, "img")
            img_cover_src = img_cover_element.get_attribute("src")
            img_cover_src_parse = urlparse(img_cover_src)
            img_cover_name = img_cover_src_parse.path.split("/")[-1]
            post_img_urls.append(img_cover_src)
            post_img_alts[img_cover_name] = (img_cover_element.get_attribute("alt"))

        print("Posts: ", post_urls)
        print("Post Images: ", post_img_urls)
        print("Post Image Alts: ", post_img_alts)
        return post_img_urls

    except NoSuchElementException:
        print("No posts found.")


def start(username, try_count=3):

    driver, is_created = try_create_driver(username, try_count)

    if is_created is False:
        print("Exiting program.")
        exit(1)
    driver.implicitly_wait(10)
    allow_all_cookies(driver)
    pff_data = get_number_of_pff(driver)  # dictionary
    profile_pic_list = get_profile_picture(driver)  # list

    exist_story = check_online_story(driver)  # boolean
    h_cover_urls, h_infos = get_highlights(driver)  # list, dictionary

    bio = get_bio(driver)  # string
    bio_link = get_bio_link(driver)  # string
    name = get_name(driver)  # string
    # post_cover_urls = get_posts(driver)

    time.sleep(1)
    driver.quit()
    return {
        "pff_number": pff_data,
        "profile_picture": profile_pic_list,
        "exist_story": exist_story,
        "h_cover_urls": h_cover_urls,
        "h_infos": h_infos,
        "bio": bio,
        "bio_link": bio_link,
        "name": name,
    }


# if __name__ == "__main__":
#     username = "finch"
#     try_count = 3
#     driver, is_created = try_create_driver(username, try_count)
#
#     if is_created is False:
#         print("Exiting program.")
#         exit(1)
#
#     allow_all_cookies(driver)
#     pff_data = get_number_of_pff(driver)  # dictionary
#     profile_pic_list = get_profile_picture(driver)  # list
#
#     exist_story = check_online_story(driver)  # boolean
#     h_cover_urls, h_infos = get_highlights(driver)  # list, dictionary
#
#     bio = get_bio(driver)  # string
#     bio_link = get_bio_link(driver)  # string
#     name = get_name(driver)  # string
#     # post_cover_urls = get_posts(driver)
#
#     time.sleep(5)
#     driver.quit()
