"""
Module Docstring:
A module that extracts specific string patterns from a list of GitHub files.
"""

import re
from operator import methodcaller
from functools import partial
import requests
import pandas as pd

# Function to get the text content of a file
def get_text(url):
    return requests.get(url).text

# Function to extract the required string from a text
def extract_string(pattern, text):
    return re.search(pattern, text).group() if re.search(pattern, text) else None

# Function to build a full url for a file in the repository
def build_url(base_url, filename):
    return f"{base_url}{filename}"

# Load the Excel file
df = pd.read_excel('path_to_your_excel_file.xlsx')

# Specify the column containing the GitHub filenames
GITHUB_FILENAMES_COLUMN = 'column_name_here'

# Specify the repository URL
REPO_URL = 'https://raw.githubusercontent.com/user/repo/main/directory/'

# Specify the regex pattern to extract the required string
PATTERN = 'your_regex_pattern'

# Apply functions to each filename to get the required string and store it in a new column
df['new_column'] = df[GITHUB_FILENAMES_COLUMN].pipe(
    methodcaller('map', partial(build_url, REPO_URL)),
    methodcaller('map', get_text),
    methodcaller('map', partial(extract_string, PATTERN))
)

# Save the modified dataframe back to an Excel file
df.to_excel('path_to_output_excel_file.xlsx', index=False)
