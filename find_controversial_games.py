import json

from compute_bayesian_average import print_ranking


def get_reddit_controversial_score(ups, downs):
    # Reference: https://github.com/reddit-archive/reddit/blob/master/r2/r2/lib/db/_sorts.pyx

    if downs <= 0 or ups <= 0:
        score = 0
    else:
        magnitude = ups + downs
        if ups > downs:
            balance = downs / ups
        else:
            balance = ups / downs
        score = magnitude ** balance

    return score


def get_bernoulli_variance(p):
    return p * (1 - p)


def get_controversial_score(data_element):
    controversial_score = get_bernoulli_variance(data_element['bayesian_average'])
    return controversial_score


def get_controversial_ranking(data):
    ranking = sorted(data.keys(),
                     key=lambda element: get_controversial_score(data[element]),
                     reverse=True)

    return ranking


def main(verbose=False):
    temp_filename = 'data/game_data.json'

    keyword = 'games'
    criterion = 'the most controversial'

    # Import game data including Bayesian average.
    with open(temp_filename, 'r', encoding='utf8') as f:
        enhanced_data = json.load(f)

    print('[SteamSpy ; enhanced] number of games = ' + str(len(enhanced_data)))

    # Print the ranking of controversial games
    print('\n# Ranking of ' + criterion + ' ' + keyword + '\n')

    ranking = get_controversial_ranking(enhanced_data)
    print_ranking(enhanced_data, ranking, keyword)

    return True


if __name__ == '__main__':
    main()
