# Wiktionary Migaku Dictionary

_Parses a Wiktionary database dump into a [Migaku Dictionary](https://github.com/migaku-official/Migaku-Dictionary-Addon) (Anki add-on)._

## Build

Before running the application, you need to setup the environment. We recommend using pyenv as part of that setup.

```shell
pyenv virtualenv 3.8.3 migaku_wiktionary
pyenv activate migaku_wiktionary
pip install -r requirements-dev.txt
pip install -r requirements.txt
```

# Testing

The project is backed by a test suite. Run it with the following command:

```shell
pytest -vv --cov=migaku_wiktionary
```

To convert an XML already downloaded, run the following snippet:

```shell
time python cli.py --xml data/dewiktionary-latest-pages-meta-current.xml convert
export DICTIONARY_PATH=~/Library/Application\ Support/Anki2/addons21/Migaku\ Dictionary/user_files/dictionaries/German/DeutschWiktionary
mkdir -p $DICTIONARY_PATH
cp /tmp/dewiktionary-latest-pages-meta-current.json $DICTIONARY_PATH/DeutschWiktionary.json
```
