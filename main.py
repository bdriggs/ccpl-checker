from utilities import ccpl

csv_url = 'https://discover.cuyahogalibrary.org/Search/Results?lookfor=PS5&searchIndex=Keyword&filter[]=format%3A%22Video+Game%22&filter[]=availability_toggle%3A%22available%22&sort=relevance&view=excel&searchSource=local'
available_games_path = './files/available_games.json'
new_games_path = './files/new_games.json'
csv_path = './files/SearchResults.csv'

def main():
    ccpl.download_csv_from_url(csv_url, csv_path)
    games_csv = ccpl.read_csv_file(csv_path)

    available_games = ccpl.get_available_games(games_csv)
    previous_available_games = ccpl.read_previous_available_games(
        available_games_path)
    new_games = ccpl.compare_games(previous_available_games, available_games)

    ccpl.remove_file(csv_path)
    ccpl.write_json(available_games_path, available_games)
    ccpl.write_json(new_games_path, new_games)


if __name__ == "__main__":
    main()
