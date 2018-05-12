import numpy as np

from load_data import load_filtered_data
from remove_noise import simplify_string


def compute_game_raw_score(game):
    raw_score = game['positive'] / (game['positive'] + game['negative'])

    return raw_score


def compute_game_num_votes(game):
    num_votes = game['positive'] + game['negative']

    return num_votes


def choose_prior_for_games(data):
    list_raw_scores = [compute_game_raw_score(game) for game in data.values()]
    list_num_votes = [compute_game_num_votes(game) for game in data.values()]

    prior = dict()
    prior['raw_score'] = np.average(list_raw_scores)
    prior['num_votes'] = np.median(list_num_votes)

    return prior


def compute_game_bayesian_average(game, prior):
    raw_score = compute_game_raw_score(game)
    num_votes = compute_game_num_votes(game)

    bayesian_average = (prior['num_votes'] * prior['raw_score'] + num_votes * raw_score) / (
            prior['num_votes'] + num_votes)

    return bayesian_average


def compute_bayesian_average_for_every_game(data):
    prior = choose_prior_for_games(data)

    for app_id in data:
        data[app_id]['bayesian_average'] = compute_game_bayesian_average(data[app_id], prior)

    return data, prior


def get_separator():
    separator = ', '
    return separator


def group_data_by_keyword(data, keyword='developers'):
    # Objective: create a dictionary which maps developers (or publishers) to a list of appIDs

    grouped_data = dict()

    for app_id in data:

        text = simplify_string(data[app_id][keyword])

        for keyword_value in set(value.strip() for value in text.split(get_separator())):
            try:
                grouped_data[keyword_value].append(app_id)
            except KeyError:
                grouped_data[keyword_value] = [app_id]

    return grouped_data


def check_string(data, keyword='developers'):
    # Objective: check what remains after calls to simplify_string(), so that one could try to improve simplify_string()

    for app_id in data:
        text = data[app_id][keyword]

        text = simplify_string(text)

        if get_separator() in text:
            print('appID={:7}'.format(app_id) + '\t' + text)

    return


def main(verbose=False):
    filtered_data = load_filtered_data()

    print('[SteamSpy ; filtered] number of games = ' + str(len(filtered_data)))

    enhanced_data, game_prior = compute_bayesian_average_for_every_game(filtered_data)

    print(game_prior)

    for keyword in ['developers', 'publishers']:
        if verbose:
            check_string(enhanced_data, keyword)

        grouped_data = group_data_by_keyword(enhanced_data, keyword)

    return True


if __name__ == '__main__':
    main()
