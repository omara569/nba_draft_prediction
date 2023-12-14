from dataclasses import dataclass



@dataclass
class Params:
    players_list_url: str
    draft_history_url: str
    gecko_driver_file_name: str 
    scraped_draft_dir: str
    ncaa_url: str
    scraped_ncaa_dir: str


config_vals = {
    'players_list_url':'https://www.nba.com/players',
    'draft_history_url':'https://www.nba.com/stats/draft/history?',
    'gecko_driver_file_name':'geckodriver.log',
    'scraped_draft_dir':'data_collection/scraped_draft_dir',
    'ncaa_url':'https://www.espn.com/mens-college-basketball/stats/player/_/season/2024',
    'scraped_ncaa_dir':'data_collection/scraped_ncaa_dir',
}


def get_config():
    return Params(**config_vals)