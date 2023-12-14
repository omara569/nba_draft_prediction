# Scraping functionality unique to the NBA website
from draft_config.config_params import get_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import scrape
import os 


# Gather the draft history data
def draft_hist_collection(url: str, driver: webdriver.firefox.webdriver.WebDriver):
    """ Opens the NBA Draft URL in the selenium webdriver and begins saving webpages locally """
    print('Collecting NBA Draft History')
    local_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    save_dir = local_path + 'scraped_draft_dir' # This is where we'll save each page of draft picks
    scrape.make_dir(save_dir)
    print('Opening Browser')
    scrape.open_url(url=url, driver=driver)
    sleep(2)
    print('Navigating and Saving Pages')
    num_pages = int(driver.find_element(By.CLASS_NAME, 'Crom_cromSettings__ak6Hd').text.split('of ')[-1])
    
    close_elem_container = driver.find_element(By.ID, 'onetrust-close-btn-container')
    close_elem_container.find_element(By.TAG_NAME, 'button').click()
    sleep(5)
    
    for i in range(num_pages):
        table_element = driver.find_element(By.CLASS_NAME, 'Crom_table__p1iZz')
        table_html = table_element.get_attribute('outerHTML')
        
        with open(f"{save_dir}/page_{i+1}.html", mode='w', encoding='utf-8') as f:
            f.write(table_html)

        if (i+1) != num_pages: # We won't look for any new pages once we've gotten to the last one
            page_elem_container = driver.find_element(By.CLASS_NAME, 'Pagination_buttons__YpLUe')
            page_elem_container.find_elements(By.CLASS_NAME, 'Pagination_button__sqGoH')[-1].click()
            sleep(.5)

    print('Completed Draft History Collection')


def ncaa_hist_collection(url: str, driver: webdriver.firefox.webdriver.WebDriver):
    """ Opens the NCAA college player stats URL in the selenium webdriver and begins saving webpages locally """
    print('Starting NBA college player stats collection')
    scrape.open_url(url, driver)
    
    local_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    save_dir = local_path + 'scraped_ncaa_dir'
    scrape.make_dir(save_dir)
    # Find the list of seasonal information available on the page
    seasons_element = driver.find_element(By.CLASS_NAME, 'dropdown.dropdown--md.mr3.mt2.mb3.filters__seasonDropdown')
    seasons_element = seasons_element.find_elements(By.CLASS_NAME, 'dropdown__option')
    years = [elem.get_attribute('data-param-value') for elem in seasons_element]
    base_url = 'https://www.espn.com/mens-college-basketball/stats/player/_/season/'
    for year in years:
        scrape.open_url(f'{base_url}{year}', driver)
        saved_html_name = driver.find_element(By.CLASS_NAME, 'headline.headline__h1.dib').text.split(' ')[-1]
        perpetual_loading(driver)
        with open(f'{save_dir}/{saved_html_name}.html', mode='w', encoding='utf-8') as f:
            f.write(driver.page_source)
    print('Completed college player stats collection')


def perpetual_loading(driver: webdriver.firefox.webdriver.WebDriver):
    """ Perpetually clicks the 'Load More' button on the web page until 5 failed attempts to find the button are reached """
    counter = 0
    while counter < 5: # 5 repeated attempts and then break
        try:
            driver.find_element(By.CLASS_NAME, 'AnchorLink.loadMore__link').click()
            if driver.find_element(By.CLASS_NAME, 'AnchorLink.loadMore__link').text == 'Try Again': # If statement breaks out of perpetual looping in this case
                counter += 1
            else:
                counter = 0
        except NoSuchElementException:
            counter += 1


# Gather draft pick history for college players
def nba_data_collection():
    """ Runs the scraper """    
    params = get_config()
    root = os.getcwd()

    # driver = scrape.driver_instance(params.gecko_driver_file_name, kill_existing_bool=True)
    # draft_hist_collection(params.draft_history_url, driver)
    # driver.quit()

    driver = scrape.driver_instance(params.gecko_driver_file_name, kill_existing_bool=True)
    ncaa_hist_collection(params.ncaa_url, driver)
    driver.quit()
    

nba_data_collection()