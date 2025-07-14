import sys
import requests
import json

def main():
    if len(sys.argv) != 2:
        print("Usage: python get_glicko.py <date-in-dd-mm-yyyy>")
        sys.exit(1)

    date = sys.argv[1]
    url = f"https://datdota.com/api/ratings?date={date}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    output_filename = f"ratings_{date}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Data saved to {output_filename}")

if __name__ == "__main__":
    main()