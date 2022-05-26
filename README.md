# Data Mining Tool

## Requirements
- Python >= 3.10
- dependencies listed in the file [requirements.txt](requirements.txt)

## Getting started

```commandline
git clone https://github.com/mhawryluk/data-mining-tool data-mining-tool
cd data-mining-tool
virtualenv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export MONGO_PASS=<password to mongo db>
cd src
python app.py
```