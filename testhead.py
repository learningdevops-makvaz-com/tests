#!/usr/bin/env python3
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os
import logging

main_url = "http://localhost"
plugin_version = "v0.10.0"
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO)


def set_chrome_options() -> None:
    """
    Sets chrome options for Selenium.
    """
    chrome_options = Options()
    # Comment out next line if you want to run tests with an opening browser.
    # GUI it's useless if you run this on containers.
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    return chrome_options


def search_media(name):
    """
    Search for media by name in searchbox
    """
    search = driver.find_element_by_id("media-search-input")
    search.send_keys(name)


def media_found(name):
    """
    Check if media found or not by name
    """
    driver.get(main_url + "/wp-admin/upload.php")
    search_media(name)
    try:
        driver.find_element_by_css_selector(
            ".attachment-preview.js--select-attachment.type-image.subtype-jpeg"
            + ".landscape")
    except:
        return False
    return True


def add_media(path):
    """
    Upload media files(pictures, music, videos)
    """
    driver.get(main_url + "/wp-admin/media-new.php?browser-uploader")
    media = driver.find_element_by_name("async-upload")
    media.clear()
    media.send_keys(os.path.abspath(path))
    driver.find_element_by_name("html-upload").click()


def publish_post():
    """
    Clicks 'Publish' button two times
    """
    driver.find_element_by_css_selector(
        ".components-button.editor-post-publish-panel__toggle.editor-post-publish-button__button.is-primary"
    ).click()
    driver.find_element_by_css_selector(
        ".components-button.editor-post-publish-button.editor-post-publish-button__button.is-primary"
    ).click()


def add_media_to_post(path):
    """
    Searchs for media in 'Media Library' and adds it to current post
    """
    driver.find_element_by_css_selector(
        ".components-placeholder__fieldset > .components-button").click()
    driver.find_element_by_id("menu-item-browse").click()
    search_media(path)
    time.sleep(2)
    driver.find_element_by_css_selector(
        ".attachment-preview.js--select-attachment.type-image.subtype-jpeg.landscape"
    ).click()
    driver.find_element_by_css_selector(
        ".button.media-button.button-primary.button-large.media-button-select"
    ).click()


def check_thank_found():
    try:
        if "Thanks for reading!" in driver.find_element_by_css_selector(
                "p[class='thank']").text:
            return True
        else:
            return False
    except:
        return False
    return True


def add_post(title, body, media=''):
    """
    Create new post with title from 'title' variable
    set body from 'body' variable.
    If media set, then it tries to find this media in 'Media Library' and
    add it to post.
    """
    driver.get(main_url + "/wp-admin/post-new.php?post_type=page")
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    post_title = driver.find_element_by_class_name("editor-post-title__input")
    post_title.clear()
    post_title.send_keys(title)

    driver.find_element_by_class_name(
        "block-editor-default-block-appender__content").click()
    webdriver.ActionChains(driver).send_keys(body).perform()
    driver.find_element_by_css_selector(
        ".components-button.edit-post-header-toolbar__inserter-toggle" +
        ".is-primary.has-icon").click()
    driver.find_element_by_css_selector(
        ".components-button.block-editor-block-types-list__item" +
        ".editor-block-list-item-image").click()
    if media:
        add_media_to_post(media)

    publish_post()
    driver.find_element_by_css_selector(
        ".components-button.components-snackbar__action.is-tertiary").click()


def check_or_fail(condition,
                  success_message="Successfully passed",
                  failure_message="Failed to pass"):
    if condition:
        logging.info(success_message)
    else:
        logging.error(failure_message)
        os._exit(1)


def check_version_found(plugin_version):
    try:
        if plugin_version in driver.find_element_by_css_selector(
                "p[class='version']").text:
            return True
        else:
            return False
    except:
        return False


def test_login():
    """
    Goes to login page, paste login and password, then hits Enter button
    """
    logging.info("Starting login check ...")
    driver.get(main_url + "/wp-admin")
    elem = driver.find_element_by_name("log")
    elem.clear()
    elem.send_keys("admin")
    elem = driver.find_element_by_name("pwd")
    elem.clear()
    elem.send_keys('password')
    elem.send_keys(Keys.RETURN)
    check_or_fail(driver.current_url == main_url + "/wp-admin/",
                  failure_message="Couldn't loging")


def test_plugin_on_text_post(plugin_version):
    """
    Create new post with only text.
    """
    logging.info("Starting test of plugin when creating text post ...")
    add_post(
        title="Simple text post",
        body="This is multiline\nText that could take a lot of space.\n" +
             "This version shouldn't be mentioned " + plugin_version + "\n" +
             "Please find it in the other place.",
    )
    check_or_fail(
        check_thank_found(),
        failure_message="Couldn't find find <p> element with class 'thank'." +
                        " Looks like plugin not working, or not installed")
    # Uncomment this lines to checkversion
    check_or_fail(
        check_version_found(plugin_version),
        failure_message="Couldn't find find <p> element with class 'version'."
        + " Looks like plugin not working, or not installed") 

def test_post_with_media():
    media_file = 'teapot.jpg'
    logging.info("Starting test. Creating text post with media ...")
    if not media_found(media_file):
        add_media(media_file)
    add_post(title="This post contains media",
             body="No need to much text here",
             media=media_file)
    for i in range(5):
        logging.info('refreshing post page ...')
        driver.refresh()
        wait = WebDriverWait(driver, 10)
        img = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "img[class^='wp-image-']")))
        for check in [{
            'condition':
                img.get_attribute("naturalWidth") != '0',
            'success_message':
                media_file + " displayed properly",
            'failure_message':
                media_file + " wasn't displayed properly"
        }, {
            'condition': media_file in img.get_attribute("src"),
            'success_message': "Proper picture displayed",
            'failure_message': "Wrong image displayed"
        }]:
            check_or_fail(check['condition'],
                          success_message=check['success_message'],
                          failure_message=check['failure_message'])


driver = webdriver.Chrome(options=set_chrome_options())
driver.accept_untrusted_certs = True
driver.implicitly_wait(10)
test_login()
test_plugin_on_text_post(plugin_version)
test_post_with_media()
driver.quit()
