import pandas as pd
import requests
import re
from typing import Optional
from operator import methodcaller

# Function to get the text content of a file
get_text = lambda url: requests.get(url).text

# Function to extract the required string from a text
extract_string = lambda pattern, text: re.search(pattern, text).group() if re.search(pattern, text) else None

# Function to build a full url for a file in the repository
build_url = lambda base_url, filename: f"{base_url}{filename}"

# Load the Excel file
df = pd.read_excel('path_to_your_excel_file.xlsx')

# Specify the column containing the GitHub filenames
github_filenames_column = 'column_name_here'

# Specify the repository URL
repo_url = 'https://raw.githubusercontent.com/user/repo/main/directory/'

# Specify the regex pattern to extract the required string
pattern = 'your_regex_pattern'

# Apply functions to each filename to get the required string and store it in a new column
df['new_column'] = df[github_filenames_column].pipe(
    methodcaller('map', partial(build_url, repo_url)),
    methodcaller('map', get_text),
    methodcaller('map', partial(extract_string, pattern))
)

# Save the modified dataframe back to an Excel file
df.to_excel('path_to_output_excel_file.xlsx', index=False)
