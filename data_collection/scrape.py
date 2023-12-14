# General web scrapering module using selenium
import os 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from psutil import process_iter
from time import sleep


def make_dir(current_directory: str) -> bool:
    """ Create a directory and returns boolean. Boolean returned is True if the directory already exists. Returns False if a directory was created."""
    doesExist = os.path.exists(current_directory)
    if not doesExist:
        os.makedirs(current_directory)
    return doesExist


def kill_existing(): # kills existing instances of the geckodriver for firefox
    """ Kills the existing instances of the geckodriver log file for firefox. This is because we scrape using firefox, and existing instances will throw exceptions. """
    for proc in process_iter(['pid', 'name', 'open_files']):
        if proc.info['open_files'] is not None:
            for file in proc.info['open_files']:
                if 'geckodriver.log' in file.path.lower():
                    proc.kill()
    sleep(1)


# Creates an instance of the web browser
def driver_instance(driver_file_name=None, kill_existing_bool=False, headless_bool=True) -> webdriver.firefox.webdriver.WebDriver:
    """ Opens an instance of the web driver. The web driver instance runs the 'kill_existing()' function prior to opening a new instance to ensure there are no conflicts. """
    if kill_existing_bool:
        kill_existing()
    firefox_options = Options()
    if headless_bool:
        firefox_options.add_argument('-headless')
    if driver_file_name is not None: # We only perform this at the start
        if driver_file_name in os.listdir(os.getcwd()):
            os.remove(os.getcwd()+'/'+driver_file_name)
    return webdriver.Firefox(options=firefox_options)


# Opens URL
def open_url(url: str, driver: webdriver.firefox.webdriver.WebDriver) -> None:
    driver.get(url)