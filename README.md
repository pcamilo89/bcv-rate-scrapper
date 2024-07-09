# BCV Rate scraper

This README is also available in [Spanish/Español](README.es.md).

This project has a set of scripts to scrape currency values from the Banco Central de Venezuela (BCV) website.

The scripts are:

- `web_scrap.py`: This script scrapes the USD and EUR values from the BCV website and saves them to a file. It also logs the scraping operations to a log file and shows a desktop notification when the values are successfully scraped.

- `excel_scrap.py`: This script scrapes USD and EUR values from the xls files in the BCV website and saves them to a file. It also renames the files in the directory.

## Motivation

Currently on the website, the historical values are stored in excel xls files, separated by trimesters, and on each file each day is a different tab, the name of the tab is the date of publication, and each tab has a list of currency values for a the next day. For the current day value you have to visit the website at around 03:30pm or later to get the latest value.

This project goal is to make it easier to search past and current currency values from the data on the website converting it into a simple local text file where each line has the date and the currency values, and eliminating the need to visit the website. For this you will have to download the xls files from the website the first time to get past values to a desired point in time, and after this you can set a cron job to update daily values automatically and optionally get a notification when new values are obtained.

This project also integrates well with any other application that needs to use historical currency values.

## Installation

### Installation Instructions

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

### Required Packages

- `beautifulsoup4`
- `xlrd`

## Configuration

To configure the scripts with different settings, edit the `config.py` file, the default values are:

```python
BCV_URL = "https://www.bcv.org.ve/"
OUTPUT_DIR = "./output/"
XLS_DIR = "./xls_files/"
XLS_FILE = OUTPUT_DIR + "excel.txt"
LOG_FILE = OUTPUT_DIR + "log.txt"
HISTORY_FILE = OUTPUT_DIR + "history.txt"
NOTIFICATION_ENABLED = True
RENAME_FILES_ENABLED = True
```

Note: currently notifications of new currency values found with `web_scrap.py` are done with notify-send, you can use any other notification CLI by modifying the `show_notification` function in the script.

## Usage

### Standalone use

To run the scripts standalone from the root directory, use the following commands:

```bash
python python -m bcv_scraper.web_scrap
```

```bash
python python -m bcv_scraper.excel_scrap
```

**Note:** the `web_scrap.py` can have an optional argument to run the script, which will add a value to the log file, this can be used to differentiate between runs from different contexts. for example :

```bash
python -m bcv_scraper.web_scrap auto
```

Will generate this entry in the log:

```text
2024-07-03 15:30:00 auto
```

### Running with cron

To run the scripts with cron, using the provided `script.sh` bash script, you can add the following lines to your crontab file

```text
*/30 15-16 * * 1-5 /absolute/path/to/project/script.sh
```

**Note:** You have to change this line on the bash script with the absolute path to the project.

```bash
fullpath="/absolute/path/to/project"
```

## License

This project is licensed under the [MIT License](LICENSE). This means you can use, modify, and distribute this project for free as long as you include the original copyright and license notice in all copies or substantial portions of the software.
