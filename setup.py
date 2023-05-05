"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_packages

# The version of this tool is based on the following steps:
# https://packaging.python.org/guides/single-sourcing-package-version/
VERSION = {}

with open("./szte_python_kotprog/__init__.py", encoding="UTF-8") as fp:
    # pylint: disable=W0122
    exec(fp.read(), VERSION)

setup(
    name="szte_python_kotprog",
    author="Südi Tamás",
    version=VERSION.get("__version__", "0.0.0"),
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "setuptools>=45.0",
        "discord.py==2.2.2",
        "fuzzywuzzy==0.18.0",
        "python-Levenshtein==0.21.0",
    ],
    classifiers=[
        "Environment :: No Input/Output (Daemon)",
        "Framework :: Pytest",
        "Intended Audience :: Education",
    ],
)
