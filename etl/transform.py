from draft_config.config_params import get_config
from data_collection.scrape import make_dir
import pandas as pd 
import os



def transform_draft(extracted_draft_path: str, save_path: str):
    print('Transforming Draft Data')
    make_dir(save_path)
    extracted_df = pd.read_csv(extracted_draft_path, sep='|', encoding='utf-8')
    # Nothing to change at this time, so save as-is
    extracted_df.to_csv(f'{save_path}/transformed_draft.csv', sep='|', encoding='utf-8', index=False)
    print('Finished Transforming Draft Data')


def transform_ncaa(extracted_ncaa_path: str, save_path: str):
    print('Transforming NCAA Stats')
    make_dir(save_path)
    extracted_df = pd.read_csv(extracted_ncaa_path, sep='|', encoding='utf-8')
    renamed_columns = ['Rank', 'Name', 'University', 'Position', 'Games Played', 'Minutes Per Game', 'Points Per Game', 'Average Field Goals Made', 
                       'Average Field Goals Attempted', 'Field Goal Percentage', 'Average 3-Point Field Goals Made', 'Average 3-Point Field Goals Attempted',
                       '3-Point Field Goal Percentage', 'Average Free Throws Made', 'Average Free Throws Attmpted', 'Free Throw Percentage', 
                       'Rebounds Per Game', 'Assists Per Game', 'Steals Per Game', 'Blocks Per Game', 'Turnovers Per Game']
    tmp_dict = dict(zip(extracted_df.columns, renamed_columns))
    extracted_df = extracted_df.rename(columns=tmp_dict)
    extracted_df.to_csv(f'{save_path}/transformed_ncaa.csv', sep='|', encoding='utf-8', index=False)
    print('Finished Transforming NCAA Stats')


def transform(params = get_config()):
    root = os.getcwd() + '/'
    local_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    transform_draft(f'{root}{params.extracted_draft_dir}/{params.extracted_draft_name}', f'{root}/{params.transformed_draft_dir}')
    transform_ncaa(f'{root}{params.extracted_ncaa_dir}/{params.extracted_ncaa_name}', f'{root}/{params.transformed_ncaa_dir}')


transform()