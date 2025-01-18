import pandas as pd
import requests
import json
from datetime import datetime

csv_url = "https://discover.cuyahogalibrary.org/Search/Results?lookfor=&searchIndex=Keyword&filter[]=format%3A%22PlayStation+5%22&filter[]=availability_toggle%3A%22global%22&sort=relevance&view=excel&searchSource=local"
csv_file = "SearchResults.csv"


def download_csv(url, output_filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_filename, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download CSV. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error downloading CSV: {e}")


def main():
    download_csv(csv_url, csv_file)

    previous_json_file = "previous_titles.json"
    output_json_file = f'new_titles_{datetime.now().strftime("%Y%m%d")}.json'

    current_data = pd.read_csv(csv_file)
    current_games = {
        row["Title"]: row["Link"]
        for _, row in current_data[["Title", "Link"]].dropna().iterrows()
    }

    try:
        with open(previous_json_file, "r") as file:
            previous_games = json.load(file)
    except FileNotFoundError:
        previous_games = {}

    new_games = {
        title: link
        for title, link in current_games.items()
        if title not in previous_games
    }

    with open(output_json_file, "w") as file:
        json.dump(new_games, file, indent=4)

    with open(previous_json_file, "w") as file:
        json.dump(current_games, file, indent=4)

    print(f"New games saved to: {output_json_file}")


if __name__ == "__main__":
    main()
