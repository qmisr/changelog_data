# changelog_data
data collection scripts that matches changelog.com data to GitHub project data

# How to use
1. rename local_settings.py.template to local_settings.py
2. Open local_settings.py and replace your GitHub credentials with appropriate values
3. import the functions from utils.py and fetch the data

# Requirements
Install the following packages using pip:
- requests-html
- python-dateutil
- pytz
- pandas

# Sample
See the [changelog_notebook](./changelog_notebook.ipynb) for example on how functions were used to collect data then store as CSV

**Note:** you can view jupyter notebooks on GitHub!
