import sys
import requests
import json
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python get_glicko.py <date-in-yyyy-mm-dd>")
        sys.exit(1)

    input_date = sys.argv[1]
    try:
        yyyy, mm, dd = input_date.split('-')
        date = f"{dd}-{mm}-{yyyy}"
    except ValueError:
        print("Date must be in yyyy-mm-dd format.")
        sys.exit(1)

    output_filename = f"ratings_{sys.argv[1]}.json"
    output_path = f"data/ratings/{output_filename}"

    if os.path.exists(output_path):
        print(f"File {output_filename} already exists. Skipping API request.")
        return

    url = f"https://datdota.com/api/ratings?date={date}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    # Extract only required fields
    filtered = []
    for entry in data.get("data", []):
        filtered.append({
            "teamName": entry.get("teamName"),
            "valveId": entry.get("valveId"),
            "glicko2_rating": entry.get("glicko2", {}).get("rating")
        })


    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    print(f"Data saved to {output_filename}")

if __name__ == "__main__":
    main()