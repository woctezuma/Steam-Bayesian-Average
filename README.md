# Steam Bayesian Average [![Build status][Build image]][Build] [![Updates][Dependency image]][PyUp] [![Python 3][Python3 image]][PyUp]

  [Build]: https://travis-ci.org/woctezuma/Steam-Bayesian-Average
  [Build image]: https://travis-ci.org/woctezuma/Steam-Bayesian-Average.svg?branch=master

  [PyUp]: https://pyup.io/repos/github/woctezuma/Steam-Bayesian-Average/
  [Dependency image]: https://pyup.io/repos/github/woctezuma/Steam-Bayesian-Average/shield.svg
  [Python3 image]: https://pyup.io/repos/github/woctezuma/Steam-Bayesian-Average/python-3-shield.svg

This repository contains Python code to compute the Bayesian average of Steam games, developers, and publishers.

## Requirements

- Install the latest version of [Python 3.X](https://www.python.org/downloads/).

- Install the required packages:

```
pip install -r requirements.txt
```

## Usage

- Download data from [SteamDB](https://steamdb.info/stats/gameratings/?all). You will need to be signed in with a Steam account.

![SteamDB login](https://i.imgur.com/cPO5t8v.png)

Once you are signed-in, make sure to view all games, then copy and paste the whole table as text into `data/steamdb.txt`.

![SteamDB start](https://i.imgur.com/PzwJXA3.png)

![SteamDB end](https://i.imgur.com/Mf8k1nY.png)


- Call the Python script. SteamSpy data will be automatically downloaded through [an API](https://steamspy.com/api.php).

```
python compute_bayesian_average.py
```

## References

[Wikipedia: Bayesian Average](https://en.wikipedia.org/wiki/Bayesian_average)

