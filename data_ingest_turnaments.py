import json
import pandas as pd
import os
import requests
from tqdm import tqdm
import time

def read_match_ids_from_json(file_path: str):
	with open(file_path, 'r') as file:
		data = json.load(file)
	# Extract only the 'match_id' entries
	match_ids = [entry['match_id'] for entry in data]
	# Create a pandas DataFrame
	df = pd.DataFrame(match_ids, columns=['match_id'])
	return df

def get_match_info(df_tournament: pd.DataFrame):
	api_base_url = 'https://api.opendota.com/api/matches/'
	df_matches = pd.DataFrame()
	with tqdm(total=len(df_tournament)) as pbar:
		for _, row in df_tournament.iterrows():
			match_api_url = row['match_id']
			response = requests.get(api_base_url + str(match_api_url))
			time.sleep(1)
			if response.status_code == 200:
				match_data = json.loads(response.text)
				df_row = pd.DataFrame([match_data])
				df_matches = pd.concat([df_matches, df_row], ignore_index=True)
			pbar.update(1)
	return df_matches

def save_df_to_json(df_to_save: pd.DataFrame, filename: str):
	df_to_save.to_json("data/json_saves_"+filename+".json", orient='records', lines=True)


df = read_match_ids_from_json('data/tournaments/matches_17795.json')

df2 = get_match_info(df)
print(df2.head())

# save_df_to_json(df2, "match_info_17795")



print("Script ran successfully")