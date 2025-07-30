# MinePi - Minecraft Server on Raspberry Pi (*minepi*)

> *A modular Raspberry Pi Minecraft server powered by Docker, playful automation, and magical parenting scripts.*

![Python version][python-version]
![Latest version][latest-version]
[![GitHub issues][issues-image]][issues-url]
[![GitHub forks][fork-image]][fork-url]
[![GitHub Stars][stars-image]][stars-url]
[![License][license-image]][license-url]

NOTE: This project was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with [@clamytoe's](https://github.com/clamytoe) [toepack](https://github.com/clamytoe/toepack) project template.

## Initial setup

```zsh
cd Projects
git clone https://github.com/clamytoe/minepi.git
cd minepi
```

### Anaconda setup

If you are an Anaconda user, this command will get you up to speed with the base installation.

```zsh
conda env create
conda activate minepi
```

### Regular Python setup

If you are just using normal Python, this will get you ready, but I highly recommend that you do this in a virtual environment.
There are many ways to do this, the simplest using *venv*.

```zsh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Final setup

```zsh
pip install -e .
```

## Usage

```zsh
minepi
```

The output should be: `Successfully installed your project file: minepi`

## Contributing

Contributions are welcomed.
Tests can be run with with `pytest -v`, please ensure that all tests are passing and that you've checked your code with the following packages before submitting a pull request:

* black
* flake8
* isort
* mypy
* pytest-cov

I am not adhering to them strictly, but try to clean up what's reasonable.

## License

Distributed under the terms of the [MIT](https://opensource.org/licenses/MIT) license, "minepi" is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://github.com/clamytoe/toepack/issues) along with a detailed description.

[python-version]:https://img.shields.io/badge/python-3.13.3-brightgreen.svg
[latest-version]:https://img.shields.io/badge/version-0.1.0-blue.svg
[issues-image]:https://img.shields.io/github/issues/clamytoe/minepi.svg
[issues-url]:https://github.com/clamytoe/minepi/issues
[fork-image]:https://img.shields.io/github/forks/clamytoe/minepi.svg
[fork-url]:https://github.com/clamytoe/minepi/network
[stars-image]:https://img.shields.io/github/stars/clamytoe/minepi.svg
[stars-url]:https://github.com/clamytoe/minepi/stargazers
[license-image]:https://img.shields.io/github/license/clamytoe/minepi.svg
[license-url]:https://github.com/clamytoe/minepi/blob/main/LICENSE
