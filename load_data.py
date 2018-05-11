import json
import pathlib
import time
from urllib.request import urlopen


def get_data_path():
    data_path = 'data/'

    pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)

    return data_path


def get_steamdb_filename():
    data_filename = get_data_path() + 'steamdb.txt'

    return data_filename


def get_steamspy_filename():
    # Get current date as yyyymmdd format
    current_date = time.strftime('%Y%m%d')

    data_filename = get_data_path() + current_date + '_steamspy.json'

    return data_filename


def load_steamdb_data(verbose=False):
    steamdb_filename = get_steamdb_filename()

    with open(steamdb_filename, 'r', encoding='utf8') as f:
        d = f.readlines()

    if verbose:
        # Print the first line, which should contain column headers
        print(d[0])

    # Skip column headers
    d = d[1:]

    data = dict()

    for line in d:
        tokens = line.split()

        app_id = int(tokens[0])
        game_name = ' '.join(tokens[1:-3])
        num_positive_reviews = int(tokens[-3].replace(',', ''))
        num_negative_reviews = int(tokens[-2].replace(',', ''))
        steamdb_rating_as_percentage = float(tokens[-1].replace('%', ''))

        data[app_id] = dict()
        data[app_id]['name'] = game_name
        data[app_id]['positive'] = num_positive_reviews
        data[app_id]['negative'] = num_negative_reviews
        data[app_id]['rating'] = steamdb_rating_as_percentage

    return data


def load_steamspy_data():
    steamspy_filename = get_steamspy_filename()

    # Attempt to load cached data. If it fails, then download data from SteamSpy URL.
    try:
        with open(steamspy_filename, 'r', encoding='utf8') as f:
            data = json.load(f)

    except FileNotFoundError:
        print('Downloading and caching data from SteamSpy.')

        steamspy_url = 'http://steamspy.com/api.php?request=all'

        with urlopen(steamspy_url) as response:
            # Download JSON. Reference: https://stackoverflow.com/a/32169442
            raw_data = response.read()
            encoding = response.info().get_content_charset('utf8')

        data = json.loads(raw_data.decode(encoding))

        # Enforce double-quotes instead of single-quotes. Reference: https://stackoverflow.com/a/8710579/
        data_str = json.dumps(data)

        # Cache the json data to a local file
        with open(steamspy_filename, 'w', encoding='utf8') as f:
            print(data_str, file=f)

    return data


def load_filtered_data(verbose=False):
    steamspy_data = load_steamspy_data()

    data = dict()
    for app_id_str in steamspy_data:
        app_id = int(app_id_str)

        num_reviews = steamspy_data[app_id_str]['positive'] + steamspy_data[app_id_str]['negative']

        if num_reviews > 0:
            data[app_id] = dict()
            # noinspection SpellCheckingInspection
            data[app_id]['appid'] = app_id
            data[app_id]['name'] = steamspy_data[app_id_str]['name']
            data[app_id]['developers'] = steamspy_data[app_id_str]['developer']  # list
            data[app_id]['publishers'] = steamspy_data[app_id_str]['publisher']  # list
            # noinspection SpellCheckingInspection
            data[app_id]['base_price'] = steamspy_data[app_id_str]['initialprice']
            data[app_id]['positive'] = steamspy_data[app_id_str]['positive']
            data[app_id]['negative'] = steamspy_data[app_id_str]['negative']
        else:
            if verbose:
                print('No review could be found for appID={:7}'.format(app_id) + '\t'
                      + steamspy_data[app_id_str]['name'])

    return data


def compare_data(verbose=False):
    steamdb_data = load_steamdb_data()
    steamdb_app_ids = set(steamdb_data.keys())

    steamspy_data = load_steamspy_data()
    steamspy_app_ids = set(int(app_id_str) for app_id_str in steamspy_data.keys())

    common_app_ids = steamdb_app_ids.intersection(steamspy_app_ids)

    steamdb_unique_app_ids = steamdb_app_ids.difference(common_app_ids)

    steamspy_unique_app_ids = steamspy_app_ids.difference(common_app_ids)

    print('[SteamDB] number of games not on SteamSpy = ' + str(len(steamdb_unique_app_ids)))

    if verbose:
        for app_id in steamdb_unique_app_ids:
            print('SteamDB appID={:7}'.format(app_id) + '\t' + steamdb_data[app_id]['name'])
        print()

    print('[SteamSpy] number of games not on SteamDB = ' + str(len(steamspy_unique_app_ids)))

    if verbose:
        for app_id in steamspy_unique_app_ids:
            print('SteamSpy appID={:7}'.format(app_id) + '\t' + steamspy_data[str(app_id)]['name'])
        print()

    print('Number of games listed on both SteamDB and SteamSpy = ' + str(len(common_app_ids)))

    num_name_mismatches = 0

    for app_id in common_app_ids:
        app_id_str = str(app_id)

        steamdb_name = steamdb_data[app_id]['name']
        steamspy_name = steamspy_data[app_id_str]['name']

        if steamdb_name != steamspy_name:
            num_name_mismatches += 1
            if verbose:
                print('SteamDB appID={:7}'.format(app_id) + '\t' + steamdb_name)
                print('SteamSpy appID={:7}'.format(app_id) + '\t' + steamspy_name)

    print('Number of games listed on both SteamDB and SteamSpy, yet names mismatch = ' + str(num_name_mismatches))

    return True


def main():
    steamdb_data = load_steamdb_data()

    print('[SteamDB] number of games = ' + str(len(steamdb_data)))

    steamspy_data = load_steamspy_data()

    print('[SteamSpy] number of games = ' + str(len(steamspy_data)))

    filtered_data = load_filtered_data(verbose=False)

    print('[SteamSpy ; filtered] number of games = ' + str(len(filtered_data)))

    return True


if __name__ == '__main__':
    main()
