import numpy as np

from load_data import load_filtered_data


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


def group_data_by_keyword(data, keyword='developer'):
    grouped_data = dict()

    for app_id in data:

        text = simplify_string(data[app_id][keyword])

        for keyword_value in [value.strip() for value in text.split(', ')]:
            try:
                grouped_data[keyword_value].append(app_id)
            except KeyError:
                grouped_data[keyword_value] = []

    return grouped_data


def simplify_string(text):
    # Strings with commas
    text = text.replace(', LLC', ' LLC')
    text = text.replace('o.,', 'o.')
    text = text.replace('O.,', 'O.')
    text = text.replace(', Ltd', ' Ltd')
    text = text.replace(', Inc', ' Inc')
    text = text.replace(', s.r.o.', ' s.r.o.')
    text = text.replace('Oh, ', 'Oh ')

    # Strings with unnecessary information
    text = text.replace('(Mac, Linux)', '')
    text = text.replace('(Mac &amp; Linux)', '')
    text = text.replace('(Mac / Linux)', '')
    text = text.replace('(Mac and Linux)', '')
    text = text.replace('(Mac/Linux)', '')
    text = text.replace('(Mac, Linux, &amp; Windows Update)', '')
    text = text.replace('(original release)', '')
    text = text.replace('(creator)', '')
    text = text.replace('(co-designer)', '')
    text = text.replace('(Some Models)', '')
    text = text.replace('(Developments)', '')
    text = text.replace('(Mac)', '')
    text = text.replace('(Linux)', '')
    text = text.replace(' (dev)', '')
    text = text.replace(' (art)', '')

    return text


def main():
    filtered_data = load_filtered_data()

    print('[SteamSpy ; filtered] number of games = ' + str(len(filtered_data)))

    enhanced_data, game_prior = compute_bayesian_average_for_every_game(filtered_data)

    print(game_prior)

    keyword = 'developers'

    for app_id in enhanced_data:
        l = enhanced_data[app_id][keyword]

        l = simplify_string(l)

        if ', ' in l:
            print(l)

    grouped_data_by_developer = group_data_by_keyword(enhanced_data, 'developers')

    grouped_data_by_publisher = group_data_by_keyword(enhanced_data, 'publishers')

    return True


if __name__ == '__main__':
    main()
