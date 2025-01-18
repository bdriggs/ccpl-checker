from datetime import datetime
import pandas as pd
import requests
import json

url = "https://discover.cuyahogalibrary.org/Search/Results?lookfor=&searchIndex=Keyword&filter[]=format%3A%22PlayStation+5%22&filter[]=availability_toggle%3A%22global%22&sort=relevance&view=excel&searchSource=local"


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
    csv_file = "SearchResults.csv"
    download_csv(url, csv_file)

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

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New PS5 Games</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin: 10px 0;
            }}
            a {{
                text-decoration: none;
                color: #007bff;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>New PS5 Games</h1>
        <p>These are the new PS5 games found since the last run:</p>
        <ul>
    """

    for title, link in new_games.items():
        html_content += f"""
            <li><a href="{link}" target="_blank">{title}</a></li>
        """

    html_content += """
        </ul>
    </body>
    </html>
    """

    output_html = "new_titles.html"
    with open(output_html, "w") as file:
        file.write(html_content)

    print(f"New games saved to: {output_json_file} and {output_html}")


if __name__ == "__main__":
    main()
