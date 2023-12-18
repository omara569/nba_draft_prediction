from draft_config.config_params import get_config
from data_collection.scrape import make_dir
import pandas as pd 
import os 



def extract_ncaa(ncaa_path: str, save_path: str):
    make_dir(save_path)
    # Appending the files together
    data_list = []
    for file in os.listdir(ncaa_path):
        data = pd.read_csv(f'{ncaa_path}/{file}', sep='|', encoding='utf-8')
        data['draft_year'] = file.split('.')[0]
        data_list.append(data)
        
    aggregated = pd.concat(data_list, ignore_index=True)
    aggregated.to_csv(save_path+'ncaa_extracted.csv', sep='|', encoding='utf-8', index=False)


def extract_draft(draft_path: str, save_path: str):
    make_dir(save_path)
    data_list = []
    for file in os.listdir(draft_path):
        data = pd.read_csv(f'{draft_path}/{file}', sep='|', encoding='utf-8')
        data_list.append(data)
    aggregated = pd.concat(data_list, ignore_index=True)
    aggregated.to_csv(save_path+'draft_extracted.csv', sep='|', encoding='utf-8', index=False)


def extract(params = get_config()):
    ncaa_dir = params.parsed_ncaa_dir
    draft_dir = params.parsed_draft_dir
    root = os.getcwd()+'/'
    local_path = os.path.dirname(os.path.realpath(__file__)) + '/'

    extract_ncaa(f'{root}{ncaa_dir}', f'{local_path}extracted_ncaa/')
    extract_draft(f'{root}{draft_dir}', f'{local_path}extracted_draft/')


extract()