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


def get_match_info(match_ids: pd.DataFrame):
	# Fetches match information from the OpenDota API for a DataFrame of match IDs and start_dates.
	api_base_url = 'https://api.opendota.com/api/matches/'
	df_matches = pd.DataFrame()
	with tqdm(total=len(match_ids)) as pbar:
		for idx, row in match_ids.iterrows():
			match_id = row['match_id']
			start_date = row['tournament_start_date']
			response = requests.get(api_base_url + str(match_id))
			time.sleep(1)
			if response.status_code == 200:
				match_data = json.loads(response.text)
				match_data['tournament_start_date'] = start_date
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
	# Create a DataFrame with all the matches played in all the tournaments, including start_date
	all_matches = []
	for index, row in tqdm(tournaments.iterrows(), total=tournaments.shape[0]):
		tournament_id = row['ID']
		start_date = row['Date First Game']
		api_url = f'https://api.opendota.com/api/leagues/{tournament_id}/matches'
		response = requests.get(api_url)
		while True:
			time.sleep(1)
			response = requests.get(api_url)
			if response.status_code == 200:
				matches = json.loads(response.text)
				for match in matches:
					all_matches.append({
						'match_id': match['match_id'],
						'tournament_start_date': start_date
					})
				break
			else:
				print(f"API returned status code {response.status_code} for tournament {tournament_id}. Retrying in 5 seconds...")
				time.sleep(5)
	df_all_matches = pd.DataFrame(all_matches)
	return df_all_matches
	

tournaments = read_tournament_ids_from_csv(file_path='data/turniere.csv')
print(tournaments)
match_ids = get_all_matches_from_tournaments(tournaments)
#print(match_ids)
big_df = get_match_info(match_ids)

# Save all matches to a JSON file
matches_path = "data/matches/"
save_df_to_json(big_df, matches_path, "all_matches_from_tournaments")

print("Script ran successfully!")