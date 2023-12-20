from bs4 import BeautifulSoup
from draft_config.config_params import get_config
from data_collection.scrape import make_dir, driver_instance, open_url
from selenium.webdriver.common.by import By
import pandas as pd
import os



def parse_draft_data(scrape_path: str, local_path: str):
    """ Parses the NBA draft data collected by the scraper """
    print('Parsing the Draft Pick Web Scrapes')
    save_path = f'{local_path}draft_dir_parsed'
    make_dir(save_path)
    scraped_pages = os.listdir(scrape_path)
    for page in scraped_pages:
        save_name = f"{page.split('.')[0]}.csv"
        current_html_path = f'{scrape_path}/{page}'
        parsed_html_path = f'{save_path}/{save_name}'
        with open(current_html_path, mode='r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        get_table(soup, parsed_html_path)
    print('Completed Draft Data Parsing')


def get_table(soup: BeautifulSoup, save_path: str):
    """ Used to create a table from the NBA draft pick data"""
    table_headers = soup.find('thead').find_all('th')
    table_headers = [header.text for header in table_headers]
    tr_elems = soup.find('tbody').find_all('tr')
    list_of_tables = []
    for tr_elem in tr_elems:
        entries = list(map(lambda x: x.text, tr_elem.find_all('td')))
        list_of_tables.append( pd.DataFrame(dict(zip(table_headers, entries)), index=[0]) )
    df = pd.concat(list_of_tables, ignore_index=True)
    df.to_csv(save_path, '|', index=False)


def parse_ncaa_stats(scrape_path: str, local_path: str):
    """ Parses the stats of the NCAA players from the scrape"""
    print('Parsing NCAA Data')
    save_path = f'{local_path}ncaa_dir_parsed'
    make_dir(save_path)
    scraped_pages = os.listdir(scrape_path)
    for page in scraped_pages:
        save_name = f"{page.split('.')[0]}.csv"
        current_html_path = f'{scrape_path}/{page}'
        parsed_html_path = f'{save_path}/{save_name}'
        
        with open(current_html_path, mode='r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Block for decoding the part with the player names, rankings, and University
        table_full = []
        try:
            headers = [th.text for th in soup.find('table').find_all('th')]
        except AttributeError:
            continue
        for tr in soup.find('table').find('tbody').find_all('tr'):
            attrs = [td.text for td in tr.find_all('td')]
            table_full.append(pd.DataFrame(dict(zip(headers, attrs)), index=[0]))
        
        table_full = pd.concat(table_full, ignore_index=True)
        uni_df = table_full['Name'].str.extract(r"(?P<University>[A-Z&-]+)$")
        name_df = table_full['Name'].str.extract(r"(?P<Name>[,'A-Za-z\s().-]+?)(?:[A-Z&-]+$|$)")
        table_full['Name'] = name_df['Name']
        table_full['University'] = uni_df['University']
        table_part2 = pd.read_html(current_html_path)[1] 
        overall_table = pd.merge(table_full, table_part2, left_index=True, right_index=True)
        overall_table.to_csv(parsed_html_path, sep='|', encoding='utf-8', index=False)

    print('Done Parsing')


def parse_data(params = get_config()):
    """ Parses the data from the HTML """
    root = os.getcwd() + '/'
    local_path = os.path.dirname(os.path.realpath(__file__)) + '/'

    parse_draft_data(f'{root}{params.scraped_draft_dir}', local_path)
    parse_ncaa_stats(f'{root}{params.scraped_ncaa_dir}', local_path)


parse_data()