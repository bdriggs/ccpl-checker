import requests
import json
import csv
import re
import os


def download_csv_from_url(url, output_filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_filename, 'wb') as file:
                file.write(response.content)
        else:
            print(
                f'Failed to download CSV. Status code: {response.status_code}')
    except requests.RequestException as e:
        print(f'Error downloading CSV: {e}')


def read_csv_file(filename):
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                yield row
    except FileNotFoundError:
        print(f'File {filename} not found.')
    except Exception as e:
        print(f'Error reading CSV file: {e}')
        yield None


def read_previous_available_games(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            previous_available_games = json.load(json_file)
    else:
        previous_available_games = []

    return previous_available_games


def write_json(file_path, available_games):
    with open(file_path, 'w') as file:
        json.dump(available_games, file, indent=2)


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f'File does not exist.')


def find_available_editions(availability_string):
    pattern = r'VIDEO GAME PS5'
    edition_match = re.findall(pattern, availability_string)

    return edition_match


def get_location_and_availability(game_availability):
    game_location = re.search(r'::(.*?) -', game_availability)
    game_location = re.sub(r'[^a-zA-Z]', '', game_location.group(0))
    game_availability = re.search(r'[^-]*$', game_availability)
    game_availability = re.sub(r'[^a-zA-Z]', '', game_availability.group(0))

    return game_location, game_availability


def get_available_games(games_csv):
    available_games = []
    row_num = 1

    for row in games_csv:
        if row and row_num != 1:
            availibility = row[6].split(',')
            for raw_game_status in availibility:
                is_valid_edition = find_available_editions(raw_game_status)

                if is_valid_edition:
                    game_title = row[1].lower()
                    game_location_and_status = get_location_and_availability(
                        raw_game_status)
                    game_location = game_location_and_status[0]
                    game_availability = game_location_and_status[1].lower()
                    game_link = row[0]

                    if game_availability == 'onshelf':
                        game_and_availability = {
                            game_title: [game_location, game_link]}
                        available_games.append(game_and_availability)

        row_num += 1

    return available_games


def compare_games(previous_available_games, available_games):
    previous_game_titles = []
    new_games = []

    for game_info in previous_available_games:
        for game_title in game_info.keys():
            previous_game_titles.append(game_title)

    for game_info in available_games:
        for game_title in game_info.keys():
            if game_title not in previous_game_titles:
                new_games.append(game_info)

    return new_games
