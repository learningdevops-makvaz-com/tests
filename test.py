# To run this program type: "pytest test.py -vx"
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import os

main_url = ''
plugin_version = ''


def test_environment_variables():
    """
    * Make sure to set environment variable 'WP_URL' to your wordpress URL.
        For example, `export WP_URL='http://192.168.50.2'`
    * Make sure to set environment variable 'WP_PLUGIN_VERSION' to
        thank-after-post plugin that would be used.
        For example, `export WP_PLUGIN_VERSION='v0.9.0'`
    """
    assert 'WP_URL' in os.environ
    assert 'WP_PLUGIN_VERSION' in os.environ
    global main_url
    global plugin_version
    main_url = os.environ['WP_URL']
    plugin_version = os.environ['WP_PLUGIN_VERSION']


def set_chrome_options() -> None:
    """Sets chrome options for Selenium."""
    chrome_options = Options()
    # Comment out next line if you want to see how it looks in Chrome browser
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    return chrome_options


def search_media(name):
    """search for media by name in searchbox"""
    search = driver.find_element_by_id("media-search-input")
    search.send_keys(name)


def media_found(name):
    """check if media found or not by name"""
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
    """ Upload media files(pictures, music, videos)"""
    driver.get(main_url + "/wp-admin/media-new.php?browser-uploader")
    media = driver.find_element_by_name("async-upload")
    media.clear()
    media.send_keys(path)
    driver.find_element_by_name("html-upload").click()


def publish_post():
    """ Clicks 'Publish' button two times"""
    driver.find_element_by_css_selector(
        ".components-button.editor-post-publish-panel__toggle.editor-post-publish-button__button.is-primary"
    ).click()
    driver.find_element_by_css_selector(
        ".components-button.editor-post-publish-button.editor-post-publish-button__button.is-primary"
    ).click()


def add_media_to_post(path):
    """ Searchs for media in 'Media Library' and adds it to current post"""
    driver.find_element_by_css_selector(
        ".components-placeholder__fieldset > .components-button").click()
    driver.find_element_by_id("menu-item-browse").click()
    search_media('teapot.jpg')
    time.sleep(2)
    driver.find_element_by_css_selector(
        ".attachment-preview.js--select-attachment.type-image.subtype-jpeg.landscape"
    ).click()
    driver.find_element_by_css_selector(
        ".button.media-button.button-primary.button-large.media-button-select"
    ).click()


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
        add_media_to_post('path')

    publish_post()
    driver.find_element_by_css_selector(
        ".components-button.components-snackbar__action.is-tertiary").click()


def test_login():
    """
    Goes to login page, paste login and password, then hits Enter button
    """
    driver.get(main_url + "/wp-admin")
    elem = driver.find_element_by_name("log")
    elem.clear()
    elem.send_keys("admin")
    elem = driver.find_element_by_name("pwd")
    elem.clear()
    elem.send_keys('!2three45.')
    elem.send_keys(Keys.RETURN)
    assert driver.current_url == main_url + "/wp-admin/"


def test_text_post():
    """
    Create new post with only text.
    """
    add_post(
        title="Simple text post",
        body="This is multiline\nText that could take a lot of space",
    )
    assert "Thanks for reading!<br>v0.9.0" in driver.page_source


def test_post_with_media():
    if not media_found('teapot.jpg'):
        add_media('/Users/aliaksei.karneyeu/projects/' +
                  'learndevops-practice/p01t03/teapot.jpg')
    add_post(title="This post contains media",
             body="No need to much text here",
             media='teapot.jpg')
    for i in range(5):
        driver.refresh()
        img = driver.find_element_by_css_selector("img[class^='wp-image-']")
        assert img.get_attribute("naturalWidth") != '0'
        assert 'teapot.jpg' in img.get_attribute("src")


def test_quit():
    driver.quit()


driver = webdriver.Chrome(options=set_chrome_options())
driver.accept_untrusted_certs = True
driver.implicitly_wait(10)
