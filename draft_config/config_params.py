from dataclasses import dataclass



@dataclass
class Params:
    players_list_url: str
    draft_history_url: str
    gecko_driver_file_name: str 
    scraped_draft_dir: str
    ncaa_url: str
    scraped_ncaa_dir: str
    parsed_ncaa_dir: str 
    parsed_draft_dir: str
    extracted_ncaa_dir: str
    extracted_draft_dir: str
    transformed_draft_dir: str
    transformed_ncaa_dir: str
    transformed_draft_name: str
    extracted_draft_name: str
    transformed_ncaa_name: str
    extracted_ncaa_name: str
    db_path: str


config_vals = {
    'players_list_url':'https://www.nba.com/players',
    'draft_history_url':'https://www.nba.com/stats/draft/history?',
    'gecko_driver_file_name':'geckodriver.log',
    'scraped_draft_dir':'data_collection/scraped_draft_dir',
    'ncaa_url':'https://www.espn.com/mens-college-basketball/stats/player/_/season/2024',
    'scraped_ncaa_dir':'data_collection/scraped_ncaa_dir',
    'parsed_ncaa_dir': 'data_parsing/ncaa_dir_parsed',
    'parsed_draft_dir': 'data_parsing/draft_dir_parsed',
    'extracted_ncaa_dir': 'etl/extracted_ncaa',
    'extracted_draft_dir': 'etl/extracted_draft',
    'transformed_draft_dir':'etl/transformed_draft',
    'transformed_ncaa_dir':'etl/transformed_ncaa',
    'transformed_draft_name':'transformed_draft.csv',
    'extracted_draft_name':'draft_extracted.csv',
    'transformed_ncaa_name':'transformed_ncaa.csv',
    'extracted_ncaa_name':'ncaa_extracted.csv',
    'db_path':'etl/nba.db'
}


def get_config():
    return Params(**config_vals)