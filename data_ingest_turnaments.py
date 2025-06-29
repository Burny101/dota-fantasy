import json
import pandas as pd
import os
import requests
from tqdm import tqdm
import time


def read_tournament_ids_from_csv(file_path: str):
	# Reads a CSV file containing tournament data and extracts tournament IDs.
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"The file {file_path} does not exist.")
	df = pd.read_csv(file_path, delimiter=';')
	if 'ID' not in df.columns:
		raise ValueError("The CSV file must contain a 'ID' column.")

	return df


def read_match_ids_from_json(file_path: str): # Redunant due to changed workflow
	# Reads a JSON file containing match data and extracts match IDs.
	with open(file_path, 'r') as file:
		data = json.load(file)
	# Extract only the 'match_id' entries
	match_ids = [entry['match_id'] for entry in data]
	# Create a pandas DataFrame
	df = pd.DataFrame(match_ids, columns=['match_id'])
	return df


def get_match_info(match_ids: list):
	# Fetches match information from the OpenDota API for a list of match IDs.
	api_base_url = 'https://api.opendota.com/api/matches/'
	df_matches = pd.DataFrame()
	with tqdm(total=len(match_ids)) as pbar:
		for match_id in match_ids:
			response = requests.get(api_base_url + str(match_id))
			time.sleep(1)
			if response.status_code == 200:
				match_data = json.loads(response.text)
				df_row = pd.DataFrame([match_data])
				df_matches = pd.concat([df_matches, df_row], ignore_index=True)
			pbar.update(1)
	return df_matches


def save_df_to_json(df_to_save: pd.DataFrame, filepath: str, filename: str):
# Saves a DataFrame to a JSON file in the specified directory. Creates the directory if it does not exist.
	if not os.path.exists(filepath):
		os.makedirs(filepath)
	df_to_save.to_json(filepath+filename+".json", orient='records', lines=True)


def get_all_matches_from_tournaments(tournaments: pd.DataFrame):
	# create a JSON file with all the matches played in all the tournaments
	
	all_match_ids = []
	for index, row in tqdm(tournaments.iterrows(), total=tournaments.shape[0]):
		tournament_id = row['ID']
		api_url = f'https://api.opendota.com/api/leagues/{tournament_id}/matches'
		response = requests.get(api_url)
		time.sleep(1)
		if response.status_code == 200:
			matches = json.loads(response.text)
			match_ids = [match['match_id'] for match in matches]
			all_match_ids.extend(match_ids)
	return all_match_ids
	

tournaments = read_tournament_ids_from_csv(file_path='data/turniere.csv')
match_ids = get_all_matches_from_tournaments(tournaments)
print(match_ids)
big_df = get_match_info(match_ids)

# Save all matches to a JSON file
matches_path = "data/matches/"
save_df_to_json(matches_path, big_df, "all_matches_from_tournaments")

print("Script ran successfully")