"""
setup.py

Setup for installing the package.
"""

from pathlib import Path

from setuptools import find_packages, setup

import minepi

VERSION = minepi.__version__
AUTHOR = minepi.__author__
EMAIL = minepi.__email__

BASE_DIR = Path(__file__).resolve().parent
README = BASE_DIR.joinpath("README.md")

setup(
    name="minepi",
    version=VERSION,
    description="A modular Raspberry Pi Minecraft server powered by Docker, playful automation, and magical parenting scripts. (minepi)",
    long_description=README.read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/clamytoe/minepi",
    author=AUTHOR,
    author_email=EMAIL,
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        #   6 - Mature
        #   7 - Inactive
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.13.3",
    ],
    keywords="python utility",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["pytest"],
    license="MIT",
    entry_points={
        "console_scripts": ["minepi=minepi.app:main"],
    },
    project_urls={
        "Bug Reports": "https://github.com/clamytoe/minepi/issues",
        "Source": "https://github.com/clamytoe/minepi/",
    },
)
