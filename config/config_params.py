from dataclasses import dataclass



@dataclass
class Params:
    players_list_url: str
    draft_history_url: str 


config_vals = {
    'players_list_url':'https://www.nba.com/players',
    'draft_history_url':'https://www.nba.com/stats/draft/history?'
}


def config_params():
    return Params(**config_vals)