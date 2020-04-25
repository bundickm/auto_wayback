from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def save_webpage(url: str) -> None:
    driver = webdriver.Firefox(executable_path='./geckodriver.exe')
    driver.get('https://web.archive.org/save')

    save_text_bar = driver.find_element_by_class_name('web-save-url-input')
    save_text_bar.send_keys(url)
    save_text_bar.send_keys(Keys.RETURN)

    while True:
        time.sleep(15)
        try:
            driver.find_element_by_class_name('label.label-success')
            break
        except:
            pass
        print('Waiting...')
    driver.close()


def activity_log(action: str, url: str) -> None:
    with open('wayback_log.txt', 'a') as log_file:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        log_file.write(f'{current_time} --- {action} --- {url}\n')


def archive_from_list() -> None:
    with open('archive_requests.txt') as f:
        archive_list = f.readlines()

    for url in archive_list:
        url = url.strip()
        activity_log('Saving Webpage', url)
        try:
            save_webpage(url)
            activity_log('Save Completed', url)
        except:
            activity_log('Save Failed', url)

archive_from_list()