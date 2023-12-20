import os 
from draft_config.config_params import get_config
import pandas as pd 
import sqlite3 
from sklearn.preprocessing import MinMaxScaler
import numpy as np



def overall_shooting_percentage(df: pd.DataFrame):
    df['shooting_percentage'] = (df['field_goal_percentage'] + df['three_point_field_goal_percentage'] + df['free_throws_percentage']) / 3


def offensive_value(df: pd.DataFrame):
    df['offensive_interaction'] = df['points_per_game'] * df['assists_per_game'] * df['steals_per_game']


def defensive_value(df: pd.DataFrame):
    df['defensive_interaction'] = df['blocks_per_game'] * df['rebounds_per_game']


def normalize_values(df: pd.DataFrame):
    normalization_cols = ['games_played', 'minutes_per_game', 'points_per_game',
       'average_field_goals_made', 'average_field_goals_attempted',
       'field_goal_percentage', 'average_three_point_field_goals_made',
       'average_three_point_field_goals_attempted',
       'three_point_field_goal_percentage', 'average_free_throws_made',
       'average_free_throws_attempted', 'free_throws_percentage',
       'rebounds_per_game', 'assists_per_game', 'steals_per_game',
       'blocks_per_game', 'turnovers_per_game']
    scaler = MinMaxScaler()
    df[normalization_cols] = scaler.fit_transform(df[normalization_cols])


def standardize_positions(df: pd.DataFrame):
    # We won't differentiate between point guards and shooting guards or small-forwards or power-forwards
    df['position'] = df['position'].map(lambda x: 'G' if x in ['PG', 'SG'] else 'F' if x in ['PF', 'SF'] else '' if x=='ATH' else x)

def adjust_positions(df: pd.DataFrame) -> pd.DataFrame:
    multi_positional_cols = [col for col in df.columns if 'position_' in col and '-' in col] # All the multi positional columns in the dataframe
    for col in multi_positional_cols:
        tmp = col.lstrip('position_').split('-')
        for pos in tmp:
            df['position_'+pos].iloc[df[col]!=0] = 1

    multi_positional_cols.append('position_')
    df = df[[keep for keep in df.columns if (keep not in multi_positional_cols)]] # Remove the multi-positional columns
    return df


def engineer_features(params = get_config()):
    root = os.getcwd() + '/'
    connection = sqlite3.Connection(f'{root}{params.db_path}')
    print('Engineering Features')

    ncaa_df = pd.read_sql_query(sql="""SELECT * FROM ncaa_cleaned;""", con=connection)
    draft_df = pd.read_sql_query(sql="""SELECT * FROM draft_cleaned""", con=connection)

    # First we'll merge the tables as a feature engineering requirement. This is so that we can ensure everything is orderly
    # Prior to merging the tables, we'll remove the multiple instances of players in the NCAA over multiple years and only take the last one
    ncaa_df = ncaa_df.sort_values(by=['name', 'ncaa_year'], ascending=False) # Start by sorting the dataframe
    ncaa_df = ncaa_df[~ncaa_df.duplicated(subset='name', keep='first')] # True labels are for the duplicates. We want to remove those so we filter as shown
    
    # Now we merge the dataframes (Essentially an SQL join). Remove the columns without any meaningful information
    new_df = pd.merge(left=draft_df, right=ncaa_df, how='right', left_on='player', right_on='name', left_index=False, right_index=False)
    new_df = new_df[new_df['year']>='2010'] # We'll start with data from 2010 and beyond for the sake of keeping the data more recent
    new_df = new_df[['name', 'player', 'team', 'affiliation', 'university', 'year', 'ncaa_year', 'position',
       'games_played', 'minutes_per_game', 'points_per_game',
       'average_field_goals_made', 'average_field_goals_attempted',
       'field_goal_percentage', 'average_three_point_field_goals_made',
       'average_three_point_field_goals_attempted',
       'three_point_field_goal_percentage', 'average_free_throws_made',
       'average_free_throws_attempted', 'free_throws_percentage',
       'rebounds_per_game', 'assists_per_game', 'steals_per_game',
       'blocks_per_game', 'turnovers_per_game']]

    normalize_values(new_df)
    overall_shooting_percentage(new_df)
    offensive_value(new_df)
    defensive_value(new_df)
    standardize_positions(new_df)
    # One-hot encoding on the position of the player
    new_df = pd.get_dummies(new_df, columns=['position'], dtype=np.int32)
    new_df = adjust_positions(new_df)

    new_df.to_sql('features_engineered_table', con=connection, if_exists='replace')
    print('Done')

engineer_features()