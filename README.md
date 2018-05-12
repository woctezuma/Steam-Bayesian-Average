# Steam Bayesian Average [![Build status][Build image]][Build] [![Updates][Dependency image]][PyUp] [![Python 3][Python3 image]][PyUp] [![Code coverage][Codecov image]][Codecov]

  [Build]: https://travis-ci.org/woctezuma/Steam-Bayesian-Average
  [Build image]: https://travis-ci.org/woctezuma/Steam-Bayesian-Average.svg?branch=master

  [PyUp]: https://pyup.io/repos/github/woctezuma/Steam-Bayesian-Average/
  [Dependency image]: https://pyup.io/repos/github/woctezuma/Steam-Bayesian-Average/shield.svg
  [Python3 image]: https://pyup.io/repos/github/woctezuma/Steam-Bayesian-Average/python-3-shield.svg

  [Codecov]: https://codecov.io/gh/woctezuma/Steam-Bayesian-Average
  [Codecov image]: https://codecov.io/gh/woctezuma/Steam-Bayesian-Average/branch/master/graph/badge.svg

This repository contains Python code to compute the Bayesian average of Steam games, developers, and publishers.

## Requirements

- Install the latest version of [Python 3.X](https://www.python.org/downloads/).

- Install the required packages:

```
pip install -r requirements.txt
```

## Usage

- Call the Python script. SteamSpy data will be automatically downloaded through [an API](https://steamspy.com/api.php).

```
python compute_bayesian_average.py
```

## Vocabulary

### Acclaimed

The higher the ratio of positive reviews, and the more reviews, the more likely a game, a developer or a publisher is *acclaimed*.

### Reliable

The higher the game scores, and the more released games, the more likely a developer or a publisher is *reliable*.

## Results

Results are shown in the Wiki for:
 - [the most acclaimed games](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Acclaimed-Games),
 - [the most acclaimed](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Acclaimed-Developers) and [the most reliable](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Reliable-Developers) developers,
 - [the most acclaimed](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Acclaimed-Publishers) and [the most reliable](https://github.com/woctezuma/Steam-Bayesian-Average/wiki/Reliable-Publishers) publishers.

## References

[Wikipedia: Bayesian Average](https://en.wikipedia.org/wiki/Bayesian_average)

## Appendix: data

The current algorithm relies solely on SteamSpy data. In case SteamSpy API stops providing the numbers of positive and
negative reviews, data from SteamDB could be merged with SteamSpy data.

- To download data from [SteamDB](https://steamdb.info/stats/gameratings/?all), first sign-in with your Steam account.

![SteamDB login](https://i.imgur.com/cPO5t8v.png)

Once you are signed-in, make sure to view all games, then copy and paste the whole table as text into `data/steamdb.txt`.

![SteamDB start](https://i.imgur.com/PzwJXA3.png)

![SteamDB end](https://i.imgur.com/Mf8k1nY.png)
