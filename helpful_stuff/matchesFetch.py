import requests
import pandas as pd
import time
import os
import json
from tqdm import tqdm
import pickle

# Funktion zum Überprüfen und Erstellen der CSV-Datei match_details.csv
def create_csv_if_not_exists():
    if not os.path.exists('match_details.csv'):
        # Wenn die CSV-Datei nicht vorhanden ist, erstellen und Header generieren
        with open('match_details.csv', 'w') as f:
            api_url = f'https://api.opendota.com/api/matches/7373420473'
            response = requests.get(api_url)
            match_data = json.loads(response.text)

            # Spaltennamen aus der ersten Zeile der API-Antwort extrahieren
            header = list(match_data.keys())
            f.write(','.join(header) + '\n')

# Funktion zum Abrufen von Match-Daten und Speichern in match_details.csv
def get_and_save_match_details(match_id):
    api_url = f'https://api.opendota.com/api/matches/{match_id}'
    response = requests.get(api_url)

    time.sleep(1)

    if response.status_code == 200:
        match_data = json.loads(response.text)
        df = pd.DataFrame([match_data])  # DataFrame aus der JSON-Antwort erstellen
        df.to_csv('match_details.csv', mode='a', header=False, index=False)  # In CSV speichern

# Funktion zum Speichern und Laden des aktuellen Index
def save_current_index(index):
    with open('current_index.pkl', 'wb') as f:
        pickle.dump(index, f)

def load_current_index():
    if os.path.exists('current_index.pkl'):
        with open('current_index.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        return 0

# CSV-Datei mit Match-IDs einlesen
match_ids_df = pd.read_csv('match_ids_teil_2_Börniiii.csv')

# Lade den zuletzt bearbeiteten Index
current_index = load_current_index()

# CSV-Datei überprüfen oder erstellen und Daten speichern
create_csv_if_not_exists()

# Fortschrittsanzeige
total_match_ids = len(match_ids_df)

# Verwende tqdm für die Fortschrittsanzeige
with tqdm(total=total_match_ids, initial=current_index) as pbar:
    for index, row in match_ids_df.iterrows():
        if index < current_index:
            continue  # Überspringe bereits bearbeitete Zeilen

        match_id = row['match_id']
        get_and_save_match_details(match_id)
        current_index = index + 1

        # Speichere den aktuellen Index
        save_current_index(current_index)

        # Fortschritt anzeigen
        pbar.update(1)

print("\nFertig! Match-Daten wurden in 'match_details.csv' gespeichert.")
