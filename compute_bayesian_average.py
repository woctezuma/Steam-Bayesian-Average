import json

import numpy as np

from load_data import load_filtered_data
from remove_noise import simplify_comma_separated_string


def compute_game_increment_value(game):
    increment_value = game['positive']

    return increment_value


def compute_game_raw_score(game):
    raw_score = game['positive'] / (game['positive'] + game['negative'])

    return raw_score


def compute_game_num_votes(game):
    num_votes = game['positive'] + game['negative']

    return num_votes


def compute_dev_increment_value(dev):
    increment_value = np.sum(dev['scores'])

    return increment_value


def compute_dev_raw_score(dev):
    raw_score = np.mean(dev['scores'])

    return raw_score


def compute_dev_num_votes(dev):
    num_votes = len(dev['scores'])

    return num_votes


def choose_prior(data, keyword=None):
    if keyword is None:
        list_increment_values = [
            compute_game_increment_value(game) for game in data.values()
        ]
        list_raw_scores = [compute_game_raw_score(game) for game in data.values()]
        list_num_votes = [compute_game_num_votes(game) for game in data.values()]
    else:
        list_increment_values = [
            compute_dev_increment_value(dev) for dev in data.values()
        ]
        list_raw_scores = [compute_dev_raw_score(dev) for dev in data.values()]
        list_num_votes = [compute_dev_num_votes(dev) for dev in data.values()]

    prior = {}
    prior['raw_score'] = np.sum(list_increment_values) / np.sum(list_num_votes)
    prior['num_votes'] = np.mean(list_num_votes)

    return prior


def compute_bayesian_average_for_an_element(element, prior, keyword=None):
    if keyword is None:
        raw_score = compute_game_raw_score(element)
        num_votes = compute_game_num_votes(element)
    else:
        raw_score = compute_dev_raw_score(element)
        num_votes = compute_dev_num_votes(element)

    bayesian_average = (
        prior['num_votes'] * prior['raw_score'] + num_votes * raw_score
    ) / (prior['num_votes'] + num_votes)

    return bayesian_average


def compute_bayesian_average_for_every_element(data, keyword=None):
    prior = choose_prior(data, keyword)

    for app_id in data:
        data[app_id]['bayesian_average'] = compute_bayesian_average_for_an_element(
            data[app_id],
            prior,
            keyword,
        )

    return data, prior


def get_separator():
    separator = ', '
    return separator


def match_data_by_keyword(data, keyword='developers'):
    # Objective: create a dictionary which maps developers (or publishers) to a list of appIDs

    matched_data = {}

    for app_id in data:
        text = simplify_comma_separated_string(data[app_id][keyword])

        for keyword_value in {value.strip() for value in text.split(get_separator())}:
            try:
                matched_data[keyword_value].append(app_id)
            except KeyError:
                matched_data[keyword_value] = [app_id]

    return matched_data


def normalize_game_weights(game_weights):
    # Objective: scale the weights so that the sum of weights is equal to the number of weights,
    #            which is here equal to the number of games.
    #
    # NB 1: The value of the sum of SCALED weights MATCHES the value of the sum of weights in the UNWEIGHTED situation,
    # i.e. in the case that all the terms of the sum have identical weight, equal to 1.
    #
    # NB 2: This scale value is important because these weights will appear in a weighted sum, not a weighted average.

    num_games = len(game_weights)

    game_weights = np.multiply(game_weights, num_games / np.sum(game_weights))

    return game_weights


def group_data_by_keyword(data, keyword='developers'):
    # Objective: aggregate game reviews for each developer (or publisher)

    matched_data = match_data_by_keyword(data, keyword)

    grouped_data = {}

    for keyword_value in matched_data:
        grouped_data[keyword_value] = {}
        grouped_data[keyword_value]['name'] = keyword_value
        grouped_data[keyword_value]['positive'] = 0
        grouped_data[keyword_value]['negative'] = 0

        game_weights = []
        for app_id in matched_data[keyword_value]:
            grouped_data[keyword_value]['positive'] += data[app_id]['positive']
            grouped_data[keyword_value]['negative'] += data[app_id]['negative']

            game_score = data[app_id]['bayesian_average']
            try:
                grouped_data[keyword_value]['scores'].append(game_score)
            except KeyError:
                grouped_data[keyword_value]['scores'] = [game_score]

            game_weights.append(compute_game_num_votes(data[app_id]))

        # Once the iteration over app_ids is over, scale the weights:
        grouped_data[keyword_value]['weights'] = normalize_game_weights(game_weights)

    return grouped_data


def check_string(data, keyword='developers'):
    # Objective: check what remains after calls to simplify_string(), so that one could try to improve simplify_string()

    for app_id in data:
        text = data[app_id][keyword]

        text = simplify_comma_separated_string(text)

        if get_separator() in text:
            print(f'appID={app_id:7}' + '\t' + text)

    return


def get_ranking(data):
    ranking = sorted(
        data.keys(),
        key=lambda element: data[element]['bayesian_average'],
        reverse=True,
    )

    return ranking


def simplify_url_item(url_item):
    simplified_url_item = url_item.replace(' ', '%20').replace(',', '%2C')

    return simplified_url_item


def print_ranking(data, ranking, keyword=None, num_elements=250, markdown_format=True):
    steam_store_url = 'https://store.steampowered.com/app/'

    if keyword == 'developers':
        steam_search_url = 'https://store.steampowered.com/search/?developer='
    elif keyword == 'publishers':
        steam_search_url = 'https://store.steampowered.com/search/?publisher='
    else:
        steam_search_url = 'https://store.steampowered.com/search/?term='

    for i, element in enumerate(ranking[:num_elements]):
        element_name = data[element]['name']

        if markdown_format:
            if keyword == 'games':
                # noinspection SpellCheckingInspection
                app_id = data[element]['appid']
                hyperlink = (
                    '[' + element_name + '](' + steam_store_url + str(app_id) + ')'
                )
            else:
                hyperlink = (
                    '['
                    + element_name
                    + ']('
                    + steam_search_url
                    + simplify_url_item(element_name)
                    + ')'
                )
        else:
            hyperlink = element_name

        print(
            f'{1 + i:4}.\t'
            + hyperlink
            + ' ({:1.3f})'.format(data[element]['bayesian_average']),
        )

    return True


def print_prior(prior):
    hyperlink_to_github = (
        ' ; [reference](https://github.com/woctezuma/Steam-Bayesian-Average)'
    )
    print(
        'Prior: score={:1.3f} ; size={:3.0f}'.format(
            prior['raw_score'],
            prior['num_votes'],
        )
        + hyperlink_to_github,
    )

    return


def merge_game_scores_and_weights(grouped_data):
    # Caveat: this is experimental! Weights are a hack to avoid disrupting devs with each new game release.

    for keyword_value in grouped_data:
        grouped_data[keyword_value]['scores'] = np.multiply(
            grouped_data[keyword_value]['scores'],
            grouped_data[keyword_value]['weights'],
        )

    return grouped_data


def run_bayesian_average_workflow(data, keyword=None, criterion='the most reliable'):
    # Bayesian Average for games
    enhanced_game_data, game_prior = compute_bayesian_average_for_every_element(
        data,
        keyword=None,
    )

    if keyword is None:
        keyword = 'games'
        criterion = 'the most acclaimed'
        enhanced_data = enhanced_game_data
        prior = game_prior
    else:
        grouped_data = group_data_by_keyword(enhanced_game_data, keyword)

        if criterion.endswith('established'):
            # Bayesian Averages of games are weighted for each developer (or publisher).
            grouped_data = merge_game_scores_and_weights(grouped_data)

        # Bayesian Average for developers (or publishers)
        if criterion.endswith('reliable') or criterion.endswith('established'):
            # Bayesian Averages of games are aggregated for each developer (or publisher).
            enhanced_data, prior = compute_bayesian_average_for_every_element(
                grouped_data,
                keyword=keyword,
            )
        else:
            # Positive and negative reviews of games are aggregated for each developer (or publisher).
            enhanced_data, prior = compute_bayesian_average_for_every_element(
                grouped_data,
            )

    print('\n# Ranking of ' + criterion + ' ' + keyword + '\n')
    print_prior(prior)

    ranking = get_ranking(enhanced_data)

    print_ranking(enhanced_data, ranking, keyword)

    return enhanced_data, prior, ranking


def main(verbose=False):
    filtered_data = load_filtered_data()

    print('[SteamSpy ; filtered] number of games = ' + str(len(filtered_data)))

    # Game data including Bayesian average.
    # NB: An unused variable is the ranking for the most acclaimed games.
    enhanced_data, _, _ = run_bayesian_average_workflow(filtered_data)

    # Optionally, for uses in other projects, export the database including Bayesian averages:
    temp_filename = 'data/game_data.json'
    with open(temp_filename, 'w', encoding='utf8') as f:
        json.dump(enhanced_data, f)

    if verbose:
        for keyword in ['developers', 'publishers']:
            check_string(enhanced_data, keyword)

    # Rankings for developers and publishers
    for criterion in [
        'the most acclaimed',
        'the most reliable',
        'the most established',
    ]:
        for keyword in ['developers', 'publishers']:
            run_bayesian_average_workflow(enhanced_data, keyword, criterion)

    return True


if __name__ == '__main__':
    main()
