from load_data import load_filtered_data


def main():
    filtered_data = load_filtered_data()

    print('[SteamSpy ; filtered] number of games = ' + str(len(filtered_data)))

    return True


if __name__ == '__main__':
    main()
