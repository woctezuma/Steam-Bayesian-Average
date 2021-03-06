def simplify_comma_separated_string(text):
    # The issue is SteamSpy provides the list of developers and publishers as a string, in which commas are separators.

    # One attempt to deal with this issue is simplify_string(), but it is not satisfactory.
    # This leads to wrong hyperlinks when displaying the ranking:
    # - correct link: https://store.steampowered.com/search/?developer=CAPCOM%20CO.%2C%20LTD.
    # - wrong link: https://store.steampowered.com/search/?developer=CAPCOM%20Co.
    # - trade-off: https://store.steampowered.com/search/?term=CAPCOM%20Co.

    # TODO deal with developers and publishers whose names contain a comma,
    # e.g. 'CAPCOM CO., LTD.' should not become 'CAPCOM CO.'

    return text


def simplify_string(text):
    # Strings with commas which are not used as separators
    text = text.replace(', INC', ' INC')
    text = text.replace(', Inc', ' Inc')
    text = text.replace(', LLC', ' LLC')
    text = text.replace(', Ltd', ' Ltd')
    text = text.replace(', S.L.', ' S.L.')
    text = text.replace(', a.s.', ' a.s.')
    text = text.replace(', inc', ' inc')
    text = text.replace(', s.r.o.', ' s.r.o.')
    text = text.replace('CO.,', 'CO.')
    text = text.replace('Co.,', 'Co.')
    text = text.replace('Oh, ', 'Oh ')
    text = text.replace('co.,', 'co.')

    # Strings with unnecessary information, which would lead to the same dev appearing under different names
    text = text.replace(' - ', ' ')
    text = text.replace(' and ', ' ')
    text = text.replace('&', '')
    text = text.replace('/', ' ')
    text = text.replace('amp;', '')

    text = text.replace('(Mac', '')
    text = text.replace('Linux)', '')
    text = text.replace('Linux, ', ' ')
    text = text.replace('Mac, ', ' ')
    text = text.replace('PC Port', '')
    text = text.replace('Windows Update', '')

    text = text.replace('(Developments)', '')
    text = text.replace('(Linux)', '')
    text = text.replace('(Mac)', '')
    text = text.replace('(Some Models)', '')
    text = text.replace('(art)', '')
    text = text.replace('(co-designer)', '')
    text = text.replace('(creator)', '')
    text = text.replace('(dev)', '')
    text = text.replace('(original release)', '')

    text = text.replace('(', '')
    text = text.replace(')', '')
    while '  ' in text:
        text = text.replace('  ', ' ')

    return text


def main():
    # noinspection SpellCheckingInspection
    input_text = 'Konami Digital Entertainment  Co., Ltd'

    simplified_text = simplify_string(input_text)

    print(simplified_text)

    return True


if __name__ == '__main__':
    main()
