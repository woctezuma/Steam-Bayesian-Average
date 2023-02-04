# Steam Bayesian Average

 [![Build status][Build image]][Build]
 [![Code coverage][Codecov image]][Codecov]
 [![Code Quality][codacy image]][codacy]

This repository contains Python code to compute the Bayesian average of Steam games, developers, and publishers.

![The most reliable publishers at Steam250](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/img/2019_04_07_banner_publishers.png)

## Requirements

- Install the latest version of [Python 3.X](https://www.python.org/downloads/).

- Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

- Call the Python script. SteamSpy data will be automatically downloaded through [an API](https://steamspy.com/api.php).

```bash
python compute_bayesian_average.py
```

## Vocabulary

Formulas are shown [on the Wiki](https://github.com/woctezuma/Steam-Bayesian-Average/wiki#vocabulary).

### Acclaimed

The higher the ratio of positive reviews, and the more reviews, the more likely a game, a developer or a publisher is *acclaimed*.

### Reliable

The higher the game scores, and the more released games, the more likely a developer or a publisher is *reliable*.

### Established

The most acclaimed its most reviewed games, and the more reliable, the more likely a developer or a publisher is *established*.

## Results

Results are shown in the Wiki for:
 - [the most acclaimed games](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Acclaimed-Games),
 - [the most acclaimed](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Acclaimed-Developers), [the most reliable](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Reliable-Developers), and [the most established](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Established-Developers) developers,
 - [the most acclaimed](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Acclaimed-Publishers), [the most reliable](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Reliable-Publishers), and [the most established](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Established-Publishers) publishers.

## References

* [Wikipedia: Bayesian Average](https://en.wikipedia.org/wiki/Bayesian_average)
* [the Steam250 website](https://steam250.com/contributors) which updates rankings every day.

## Appendix: data

The current algorithm relies solely on SteamSpy data. In case SteamSpy API stops providing the numbers of positive and
negative reviews, data from SteamDB could be merged with SteamSpy data.

- To download data from [SteamDB](https://steamdb.info/stats/gameratings/?all), first sign-in with your Steam account.

![SteamDB login](https://i.imgur.com/cPO5t8v.png)

Once you are signed-in, make sure to view all games, then copy and paste the whole table as text into `data/steamdb.txt`.

![SteamDB start](https://i.imgur.com/PzwJXA3.png)

![SteamDB end](https://i.imgur.com/Mf8k1nY.png)

<!-- Definitions -->

  [Build]: <https://github.com/woctezuma/Steam-Bayesian-Average/actions>
  [Build image]: <https://github.com/woctezuma/Steam-Bayesian-Average/workflows/Python application/badge.svg?branch=master>

  [PyUp]: https://pyup.io/repos/github/woctezuma/Steam-Bayesian-Average/
  [Dependency image]: https://pyup.io/repos/github/woctezuma/Steam-Bayesian-Average/shield.svg
  [Python3 image]: https://pyup.io/repos/github/woctezuma/Steam-Bayesian-Average/python-3-shield.svg

  [Codecov]: https://codecov.io/gh/woctezuma/Steam-Bayesian-Average
  [Codecov image]: https://codecov.io/gh/woctezuma/Steam-Bayesian-Average/branch/master/graph/badge.svg

  [codacy]: https://www.codacy.com/app/woctezuma/Steam-Bayesian-Average
  [codacy image]: https://api.codacy.com/project/badge/Grade/82a9d45f5c2d443daf525e7a1a2ee65d 

