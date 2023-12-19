import pandas as pd 
import sqlite3 
import os 
import numpy as np
from draft_config.config_params import get_config



def clean_ncaa(df: pd.DataFrame):
    # Remove the single-character names from the data, as these are not valid instances of NBA draftees since the name data is missing!
    numerical_columns = ['minutes_per_game', 'points_per_game', 'average_field_goals_made',
       'average_field_goals_attempted', 'field_goal_percentage',
       'average_three_point_field_goals_made',
       'average_three_point_field_goals_attempted',
       'three_point_field_goal_percentage', 'average_free_throws_made',
       'average_free_throws_attempted', 'free_throws_percentage',
       'rebounds_per_game', 'assists_per_game', 'steals_per_game',
       'blocks_per_game', 'turnovers_per_game']
    for column in numerical_columns:
        df[column] = df[column].fillna(df[column].median(skipna=True))
    df['games_played'] = df['games_played'].fillna(np.int32(df['games_played'].median(skipna=True)))


def clean_draft(df: pd.DataFrame):
    pass # Nothing to clean

def clean_data(params = get_config()):
    root = os.getcwd() + '/'
    connection = sqlite3.Connection(f'{root}{params.db_path}')

    print('Starting Cleaning')    
    ncaa_stat_data = pd.read_sql_query('SELECT * FROM ncaa_data_raw;', con=connection)
    ncaa_stat_data[['minutes_per_game', 'points_per_game', 'average_field_goals_made',
       'average_field_goals_attempted', 'field_goal_percentage',
       'average_three_point_field_goals_made',
       'average_three_point_field_goals_attempted',
       'three_point_field_goal_percentage', 'average_free_throws_made',
       'average_free_throws_attempted', 'free_throws_percentage',
       'rebounds_per_game', 'assists_per_game', 'steals_per_game',
       'blocks_per_game', 'turnovers_per_game']] = ncaa_stat_data[['minutes_per_game', 'points_per_game', 'average_field_goals_made',
       'average_field_goals_attempted', 'field_goal_percentage',
       'average_three_point_field_goals_made',
       'average_three_point_field_goals_attempted',
       'three_point_field_goal_percentage', 'average_free_throws_made',
       'average_free_throws_attempted', 'free_throws_percentage',
       'rebounds_per_game', 'assists_per_game', 'steals_per_game',
       'blocks_per_game', 'turnovers_per_game']].astype(dtype=np.float64)
    ncaa_stat_data['games_played'] = ncaa_stat_data['games_played'].astype(np.int32)
    draft_data = pd.read_sql_query('SELECT * FROM draft_data_raw', con=connection)

    clean_ncaa(ncaa_stat_data)
    clean_draft(draft_data)

    ncaa_stat_data.to_sql(name='ncaa_cleaned', con=connection, if_exists='replace')
    draft_data.to_sql(name='draft_cleaned', con=connection, if_exists='replace')

    print('Done')

clean_data()