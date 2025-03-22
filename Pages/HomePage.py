from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class HomePage:

    """ GAASHWD home page """

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def input_tracking_number(self, tracking_num: str):
        self.driver.find_element(By.ID, "trackingNumber").send_keys(tracking_num)

    def submit_track_number(self):
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Track Your Parcel')]").click()

    def wait_for_status_results(self):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//th[contains(text(), 'Status')]")))

    def scoll_to_track_status(self):
        table = self.driver.find_element(By.CSS_SELECTOR, "table.gww-w-full.gww-caption-bottom")
        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const scrollOffset = rect.bottom - window.innerHeight;
            if (scrollOffset > 0) {
                window.scrollBy({ top: scrollOffset, behavior: 'smooth' });
            } """, table)
        time.sleep(1) # -- make change visible
    
    def get_status_table(self):
        table = self.driver.find_element(By.CSS_SELECTOR, "table.gww-w-full.gww-caption-bottom")
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # get rows without header
        rows_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                data = {
                    'time': cells[0].text.strip(),
                    'status': cells[1].text.strip()
                }
                rows_data.append(data)

        return rows_data
