from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime


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
        print(f'Archiving: {url}')
    driver.close()


def activity_log(action: str, url: str) -> None:
    with open('./Auto_Wayback_Docs/wayback_log.txt', 'a') as log_file:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        log_file.write(f'{current_time} --- {action} --- {url}\n')


def archive_from_list() -> None:
    with open('./Auto_Wayback_Docs/archive_requests.txt') as f:
        archive_list = f.readlines()

    for url in archive_list:
        url = url.strip()
        activity_log('Saving Webpage', url)
        try:
            save_webpage(url)
            activity_log('Save Completed', url)
        except:
            activity_log('Save Failed', url)


def auto_archive(frequency: int, stop: datetime) -> None:
    if frequency < 10:
        frequency = 10

    while datetime.now() < stop:
        archive_from_list()
        print(f'Archiving Complete at {datetime.now()}. Next Archive in {frequency} minutes')
        time.sleep(frequency * 60)


if __name__ == "__main__":
    auto_archive(15, datetime(2020, 4, 27, 12))
