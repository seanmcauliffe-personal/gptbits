import requests
from bs4 import BeautifulSoup
from functools import reduce

def get_league_averages():
    # Scrape the league averages from Basketball-Reference.com
    url = 'https://www.basketball-reference.com/leagues/NBA_2022_totals.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    league_averages = {}
    table = soup.find('table', id='totals_stats')
    header_row = table.find('thead').find('tr')
    stat_columns = header_row.find_all('th')[6:-1]  # Exclude non-stat columns

    for col in stat_columns:
        stat_name = col['data-stat']
        league_avg = float(col.text)
        league_averages[stat_name] = league_avg

    return league_averages

def collect_player_stats(player_name):
    # Scrape the player's stats from Basketball-Reference.com
    url = f'https://www.basketball-reference.com/search/search.fcgi?search={player_name}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    player_stats = {}
    search_results = soup.find_all('div', class_='search-item-name')
    if search_results:
        player_url = search_results[0].find('a')['href']
        player_stats_url = f'https://www.basketball-reference.com{player_url}'
        player_stats_response = requests.get(player_stats_url)
        player_stats_soup = BeautifulSoup(player_stats_response.content, 'html.parser')

        table = player_stats_soup.find('table', id='per_game')
        header_row = table.find('thead').find('tr')
        stat_columns = header_row.find_all('th')[1:]  # Exclude non-stat columns

        for col in stat_columns:
            stat_name = col['data-stat']
            stat_value = float(col.text)
            player_stats[stat_name] = stat_value

    return player_stats

def normalize_stat(stat_name, stat_value, league_averages):
    if stat_name in league_averages:
        league_avg = league_averages[stat_name]
        normalized_value = stat_value / league_avg
        return normalized_value
    else:
        return stat_value

def normalize_stats(player_stats, league_averages):
    normalized_stats = {}
    normalize_fn = lambda stat_name, stat_value: normalize_stat(stat_name, stat_value, league_averages)

    for stat_name, stat_value in player_stats.items():
        normalized_value = normalize_fn(stat_name, stat_value)
        normalized_stats[stat_name] = normalized_value

    return normalized_stats

# Usage example
player_name = "LeBron James"
league_averages = get_league_averages()
player_stats = collect_player_stats(player_name)
normalized_stats = normalize_stats(player_stats, league_averages)
print(f"Normalized stats for {player_name}: {normalized_stats}")
