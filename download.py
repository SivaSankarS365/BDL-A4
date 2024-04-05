import requests
import os
from bs4 import BeautifulSoup


def scrape_data(year, locs=[], n_locs=None):
    """
    Downloads csv files for a given year and locations from NOAA.
    
    Args:
        year (int): The year to download data for.
        locs (list, optional): List of locations to download data for. 
            Defaults to an empty list.
        n_locs (int, optional): Number of locations to download data for. 
            Defaults to None.
    """
    # Construct the base url for the given year
    base_url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}'
    os.makedirs(f'./data/{year}', exist_ok=True)
    
    # Construct the url for the index file
    url = base_url.format(year=year)
    
    # Print the url of the index file being fetched
    print('Fetching index file...')
    
    # Fetch the index file
    res = requests.get(url)
    
    # Parse the index file
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Find all the anchor tags in the index file
    table = soup.find('table')
    anchors = table.find_all('a')
    
    # Filter the anchor tags to only include those with 'csv' in their text
    anchors = [a for a in anchors if 'csv' in a.text]
    
    # Filter the anchor tags to only include those with text in locs
    if locs:
        locs = [str(file) + '.csv' for file in locs if not str(file).endswith('.csv')]
        anchors = [a for a in anchors if a.text in locs]
    
    # Limit the number of anchor tags to n_locs
    if n_locs:
        anchors = anchors[:n_locs]
    
    # Download each anchor tag
    for anchor in anchors:
        file = anchor.text
        file_url = f'{url}/{file}'
        print(file_url)
        res = requests.get(file_url)
        csv = res.text
        
        # Write the csv file to disk
        with open(f'./data/{year}/{file}', 'w') as f:
            f.write(csv)
            f.write(csv)

if __name__ == '__main__':
    import yaml
    with open('params.yaml') as f:
        params = yaml.safe_load(f)
    scrape_data(**params['download'])
    print('Done!')