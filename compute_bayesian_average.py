def load_steamdb_data(verbose=True):
    steamdb_filename = 'data/steamdb.txt'

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


def main():
    steamdb_data = load_steamdb_data()

    return


if __name__ == '__main__':
    main()
