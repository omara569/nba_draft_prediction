import csv 
import sqlite3
from draft_config.config_params import get_config
from typing import List, Tuple
import os



def connect_to_db(db_name: str) -> sqlite3.Connection:
    return sqlite3.connect(db_name)


def close_connection(connection: sqlite3.Connection) -> None:
    connection.close()


def open_channel(db_connection: sqlite3.Connection) -> sqlite3.Cursor:
    return db_connection.cursor()


def create_draft(channel: sqlite3.Cursor) -> None:
    # Create tables if they don't exist
    channel.execute("CREATE TABLE IF NOT EXISTS draft_data_raw (player, team, affiliation, year, round_number, round_pick, overall_pick);")


def create_ncaa(channel: sqlite3.Cursor) -> None:
    channel.execute("CREATE TABLE IF NOT EXISTS ncaa_data_raw ('rank','name','university', 'position', 'games_played', 'minutes_per_game', 'points_per_game', 'average_field_goals_made', 'average_field_goals_attempted','field_goal_percentage', 'average_three_point_field_goals_made', 'average_three_point_field_goals_attempted', 'three_point_field_goal_percentage', 'average_free_throws_made', 'average_free_throws_attempted', 'free_throws_percentage', 'rebounds_per_game', 'assists_per_game', 'steals_per_game', 'blocks_per_game', 'turnovers_per_game', 'draft_year');")


def get_draft_write_rows(draft_path: str) -> List[Tuple]:
    with open(draft_path,'r', encoding='utf-8') as file: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(file, delimiter='|') # comma is default delimiter
        to_db = [(i['Player'],
                i['Team'],
                i['Affiliation'],
                i['Year'],
                i['RoundNumber'],
                i['RoundPick'],
                i['OverallPick']) for i in dr]
    return to_db


def get_ncaa_write_rows(ncaa_path: str) -> List[Tuple]:
    with open(ncaa_path,'r', encoding='utf-8') as file: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(file, delimiter='|') # comma is default delimiter
        to_db = [(i['Rank'],
                i['Name'],
                i['University'],
                i['Position'],
                i['Games Played'],
                i['Minutes Per Game'],
                i['Points Per Game'],
                i['Average Field Goals Made'],
                i['Average Field Goals Attempted'],
                i['Field Goal Percentage'],
                i['Average 3-Point Field Goals Made'],
                i['Average 3-Point Field Goals Attempted'],
                i['3-Point Field Goal Percentage'],
                i['Field Goal Percentage'],
                i['Average Free Throws Attmpted'],
                i['Free Throw Percentage'],
                i['Rebounds Per Game'],
                i['Assists Per Game'],
                i['Steals Per Game'],
                i['Blocks Per Game'],
                i['Turnovers Per Game'],
                i['draft_year']) for i in dr]
    return to_db


def insert_draft_data(connection: sqlite3.Connection, channel: sqlite3.Cursor, data: List[Tuple]) -> None:
    # We only write in the instances where the given row doesn't already exist in the table!
    for row in data:
        channel.execute('''SELECT * FROM draft_data_raw 
                        WHERE player=? AND team=? AND affiliation=? AND year=? AND round_number=? AND round_pick=? AND overall_pick=?''', row)
        if channel.fetchone() is None:
            channel.execute("INSERT INTO draft_data_raw (player, team, affiliation, year, round_number, round_pick, overall_pick) VALUES (?, ?, ?, ?, ?, ?, ?);", row)
    connection.commit()


def insert_ncaa_data(connection: sqlite3.Connection, channel: sqlite3.Cursor, data: List[Tuple]) -> None:
    # We only write in the instances where the given row doesn't already exist in the table!
    for row in data:
        channel.execute('''SELECT * FROM ncaa_data_raw 
                        WHERE rank=? AND name=? AND university=? AND position=? AND games_played=? AND minutes_per_game=? AND points_per_game=? AND average_field_goals_made=? AND average_field_goals_attempted=? AND field_goal_percentage=? AND average_three_point_field_goals_made=? AND average_three_point_field_goals_attempted=? AND three_point_field_goal_percentage=? AND average_free_throws_made=? AND average_free_throws_attempted=? AND free_throws_percentage=? AND rebounds_per_game=? AND assists_per_game=? AND steals_per_game=? AND blocks_per_game=? AND turnovers_per_game=? AND draft_year=?''', row)
        if channel.fetchone() is None:
            channel.execute("INSERT INTO ncaa_data_raw ('rank', 'name', 'university', 'position', 'games_played', 'minutes_per_game', 'points_per_game', 'average_field_goals_made', 'average_field_goals_attempted', 'field_goal_percentage', 'average_three_point_field_goals_made', 'average_three_point_field_goals_attempted', 'three_point_field_goal_percentage', 'average_free_throws_made', 'average_free_throws_attempted', 'free_throws_percentage', 'rebounds_per_game', 'assists_per_game', 'steals_per_game', 'blocks_per_game','turnovers_per_game', 'draft_year') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", row)
    connection.commit()


def load():
    root = os.getcwd() + '/'
    local_dir = os.path.dirname(__file__) + '/'
    params = get_config()

    print('Creating Database')
    connection_obj = connect_to_db(f'{local_dir}/nba.db')
    channel = open_channel(connection_obj)

    # Draft Data
    print('Creating Draft Data Table')
    create_draft(channel)
    print('Writing Draft Data Table')
    write_info = get_draft_write_rows(f'{root}{params.transformed_draft_dir}/{params.transformed_draft_name}')
    insert_draft_data(connection_obj, channel, write_info)
    print('Done writing Draft Data')

    # NCAA Stats
    print('Creating NCAA Data Table')
    create_ncaa(channel)
    print('Writing NCAA Data Table')
    write_info = get_ncaa_write_rows(f'{root}{params.transformed_ncaa_dir}/{params.transformed_ncaa_name}')
    insert_ncaa_data(connection_obj, channel, write_info)
    print('Done writing NCAA Data')


    close_connection(connection_obj)

    print('Done')

load()