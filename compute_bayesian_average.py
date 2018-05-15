import numpy as np

from load_data import load_filtered_data
from remove_noise import simplify_comma_separated_string


def compute_game_raw_score(game):
    raw_score = game['positive'] / (game['positive'] + game['negative'])

    return raw_score


def compute_game_num_votes(game):
    num_votes = game['positive'] + game['negative']

    return num_votes


def compute_dev_raw_score(dev):
    raw_score = np.mean(dev['scores'])

    return raw_score


def compute_dev_num_votes(dev):
    num_votes = len(dev['scores'])

    return num_votes


def choose_prior(data, keyword=None):
    if keyword is None:
        list_raw_scores = [compute_game_raw_score(game) for game in data.values()]
        list_num_votes = [compute_game_num_votes(game) for game in data.values()]
    else:
        list_raw_scores = [compute_dev_raw_score(dev) for dev in data.values()]
        list_num_votes = [compute_dev_num_votes(dev) for dev in data.values()]

    prior = dict()
    prior['raw_score'] = np.average(list_raw_scores)
    prior['num_votes'] = np.median(list_num_votes)

    return prior


def compute_bayesian_average_for_an_element(element, prior, keyword=None):
    if keyword is None:
        raw_score = compute_game_raw_score(element)
        num_votes = compute_game_num_votes(element)
    else:
        raw_score = compute_dev_raw_score(element)
        num_votes = compute_dev_num_votes(element)

    bayesian_average = (prior['num_votes'] * prior['raw_score'] + num_votes * raw_score) / (
            prior['num_votes'] + num_votes)

    return bayesian_average


def compute_bayesian_average_for_every_element(data, keyword=None):
    prior = choose_prior(data, keyword)

    for app_id in data:
        data[app_id]['bayesian_average'] = compute_bayesian_average_for_an_element(data[app_id], prior, keyword)

    return data, prior


def get_separator():
    separator = ', '
    return separator


def match_data_by_keyword(data, keyword='developers'):
    # Objective: create a dictionary which maps developers (or publishers) to a list of appIDs

    matched_data = dict()

    for app_id in data:

        text = simplify_comma_separated_string(data[app_id][keyword])

        for keyword_value in set(value.strip() for value in text.split(get_separator())):
            try:
                matched_data[keyword_value].append(app_id)
            except KeyError:
                matched_data[keyword_value] = [app_id]

    return matched_data


def group_data_by_keyword(data, keyword='developers'):
    # Objective: aggregate game reviews for each developer (or publisher)

    matched_data = match_data_by_keyword(data, keyword)

    grouped_data = dict()

    for keyword_value in matched_data:
        grouped_data[keyword_value] = dict()
        grouped_data[keyword_value]['name'] = keyword_value
        grouped_data[keyword_value]['positive'] = 0
        grouped_data[keyword_value]['negative'] = 0

        for app_id in matched_data[keyword_value]:
            grouped_data[keyword_value]['positive'] += data[app_id]['positive']
            grouped_data[keyword_value]['negative'] += data[app_id]['negative']

            game_score = data[app_id]['bayesian_average']
            try:
                grouped_data[keyword_value]['scores'].append(game_score)
            except KeyError:
                grouped_data[keyword_value]['scores'] = [game_score]

            game_weight = compute_game_num_votes(data[app_id])

            try:
                grouped_data[keyword_value]['weights'].append(game_weight)
            except KeyError:
                grouped_data[keyword_value]['weights'] = [game_weight]

    return grouped_data


def check_string(data, keyword='developers'):
    # Objective: check what remains after calls to simplify_string(), so that one could try to improve simplify_string()

    for app_id in data:
        text = data[app_id][keyword]

        text = simplify_comma_separated_string(text)

        if get_separator() in text:
            print('appID={:7}'.format(app_id) + '\t' + text)

    return


def get_ranking(data):
    ranking = sorted(data.keys(), key=lambda element: data[element]['bayesian_average'], reverse=True)

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

    for (i, element) in enumerate(ranking[:num_elements]):
        element_name = data[element]['name']

        if markdown_format:
            if keyword == 'games':
                # noinspection SpellCheckingInspection
                app_id = data[element]['appid']
                hyperlink = '[' + element_name + '](' + steam_store_url + str(app_id) + ')'
            else:
                hyperlink = '[' + element_name + '](' + steam_search_url + simplify_url_item(element_name) + ')'
        else:
            hyperlink = element_name

        print('{:4}.\t'.format(1 + i) + hyperlink + ' ({:1.3f})'.format(data[element]['bayesian_average']))

    return True


def print_prior(prior):
    hyperlink_to_github = ' ; [reference](https://github.com/woctezuma/Steam-Bayesian-Average)'
    print('Prior: score={:1.3f} ; size={:3.0f}'.format(prior['raw_score'], prior['num_votes']) + hyperlink_to_github)

    return


def merge_game_scores_and_weights(grouped_data):
    for keyword_value in grouped_data:
        sum_game_weights = compute_game_num_votes(grouped_data[keyword_value])

        weighted_game_scores = []
        for (game_score, game_weight) in zip(grouped_data[keyword_value]['scores'],
                                             grouped_data[keyword_value]['weights']):
            normalized_weight = game_weight / sum_game_weights
            exponential_weight = np.exp(- 0.5 * normalized_weight ** 2)
            weighted_game_score = game_score * exponential_weight
            weighted_game_scores.append(weighted_game_score)

        grouped_data[keyword_value]['scores'] = weighted_game_scores

    return grouped_data


def run_bayesian_average_workflow(data, keyword=None, criterion='the most reliable'):
    # Bayesian Average for games
    enhanced_game_data, game_prior = compute_bayesian_average_for_every_element(data, keyword=None)

    if keyword is None:
        keyword = 'games'
        criterion = 'the most acclaimed'
        enhanced_data = enhanced_game_data
        prior = game_prior
    else:

        grouped_data = group_data_by_keyword(enhanced_game_data, keyword)

        # Bayesian Average for developers (or publishers)
        if criterion.startswith('the most reliable'):
            if criterion.endswith('(with weights)'):
                # Bayesian Averages of games are weighted for each developer (or publisher).
                # Caveat: this is experimental! Weights are a hack to avoid disrupting devs with each new game release.
                grouped_data = merge_game_scores_and_weights(grouped_data)

            # Bayesian Averages of games are aggregated for each developer (or publisher).
            enhanced_data, prior = compute_bayesian_average_for_every_element(grouped_data, keyword=keyword)
        else:
            # Positive and negative reviews of games are aggregated for each developer (or publisher).
            enhanced_data, prior = compute_bayesian_average_for_every_element(grouped_data)

    print('\nRanking of ' + criterion + ' ' + keyword)
    print_prior(prior)

    ranking = get_ranking(enhanced_data)

    print_ranking(enhanced_data, ranking, keyword)

    return enhanced_data, prior, ranking


def main(verbose=False):
    filtered_data = load_filtered_data()

    print('[SteamSpy ; filtered] number of games = ' + str(len(filtered_data)))

    enhanced_data, game_prior, game_ranking = run_bayesian_average_workflow(filtered_data)

    if verbose:
        for keyword in ['developers', 'publishers']:
            check_string(enhanced_data, keyword)

    for criterion in ['the most acclaimed', 'the most reliable', 'the most reliable (with weights)']:
        for keyword in ['developers', 'publishers']:
            run_bayesian_average_workflow(enhanced_data, keyword, criterion)

    return True


if __name__ == '__main__':
    main()
