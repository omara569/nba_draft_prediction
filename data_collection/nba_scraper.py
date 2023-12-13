# Scraping functionality unique to the NBA website
from draft_config.config_params import get_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import scrape
import os 


# For debugging purposes
import logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Gather the draft history data
def draft_hist_collection(url: str, driver: webdriver.firefox.webdriver.WebDriver):
    """ Opens the URL in the selenium webdriver and begins saving webpages locally """
    print('Collecting NBA Draft History')
    local_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    save_dir = local_path + 'scraped_draft_dir' # This is where we'll save each page of draft picks
    scrape.make_dir(save_dir)
    print('Opening Browser')
    scrape.open_url(url=url, driver=driver)
    sleep(10)
    print('Navigating and Saving Pages')
    num_pages = int(driver.find_element(By.CLASS_NAME, 'Crom_cromSettings__ak6Hd').text.split('of ')[-1])
    for i in range(num_pages):
        table_element = driver.find_element(By.CLASS_NAME, 'Crom_table__p1iZz')
        table_html = table_element.get_attribute('outerHTML')
        
        with open(f"{save_dir}/page_{i+1}.html", mode='w', encoding='utf-8') as f:
            f.write(table_html)

        if (i+1) != num_pages:
            driver.find_element(By.CLASS_NAME, 'Pagination_button__sqGoH').click()
            sleep(1)
        if i==2:
            break

    print('Completed Draft History Collection')


# Gather draft pick history for college players
def nba_data_collection():
    params = get_config()
    root = os.getcwd()

    driver = scrape.driver_instance(params.gecko_driver_file_name, kill_existing_bool=True)
    draft_hist_collection(params.draft_history_url, driver)

    driver.quit()
    

nba_data_collection()