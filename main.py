from selenium import webdriver
import chromedriver_autoinstaller
from selenium.common.exceptions import TimeoutException

from datetime import datetime
import csv
import os

from Pages.HomePage import HomePage


def log2csv(datalist: dict, filename: str):
    """ Save data to csv file """
    log_path = f'Logs/{filename}'
    dir_path = os.path.dirname(log_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    is_file_exists = os.path.isfile(log_path)
    if is_file_exists:
        print("Overwrite existing file")

    with open(log_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["time", "status"])
        writer.writeheader()
        writer.writerows(datalist)
        print(f"data saved to {log_path}")


def track_package(tracking_num: str):

    # Auto Install Chrome Driver
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    driver.set_page_load_timeout(15)  # Set max time for page to load

    # Load the page until timeout than start testing
    print("Loading Page...")
    try:
        driver.get("https://gaashwd.com/")
    except TimeoutException:
        pass

    driver.maximize_window()
    driver.implicitly_wait(10)

    home_page = HomePage(driver)

    # remove privacy popup
    home_page.input_tracking_number(tracking_num)
    home_page.submit_track_number()
    home_page.scoll_to_track_status()
    status_table = home_page.get_status_table()

    latest_record = max(status_table, key=lambda x: datetime.strptime(x['time'], "%d/%m/%Y %H:%M"))
    log2csv(status_table, filename=f'{tracking_num}.csv')

    print(f"last record: {latest_record}")

    driver.close()


if __name__ == '__main__':
    track_package('AP28344067')
    