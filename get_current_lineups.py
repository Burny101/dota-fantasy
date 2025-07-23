import sys
import requests
import json
import os


def main():
    if len(sys.argv) != 2:
        print("Usage: python get_team_lineup.py <team_id>")
        sys.exit(1)

    team_id = sys.argv[1]
    output_filename = f"team_lineup_{team_id}.json"
    output_path = f"data/lineups/{output_filename}"

    if os.path.exists(output_path):
        print(f"File {output_filename} already exists. Skipping API request.")
        return

    url = f"https://api.opendota.com/api/teams/{team_id}/players"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Data saved to {output_filename}")


if __name__ == "__main__":
    main()
