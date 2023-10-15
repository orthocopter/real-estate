import requests
from bs4 import BeautifulSoup

class HttpStatusError (Exception) :
    pass

class ParseError (Exception) :
    pass

def url_to_soup (url) :
    # Identify as a normal browserer
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200 :
        raise HttpStatusError(f'Failed to retrieve page with status code: {response.status_code}')

    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def soup_to_number_of_baths (soup) :
    baths_section = soup.find(class_='baths-section')
    if not baths_section :
        raise ParseError
    stats_value = baths_section.find(class_='statsValue')
    if not stats_value :
        raise ParseError
    result = stats_value.text
    return result

def soup_to_estimated_value (soup) :
    div = soup.find(attrs={'data-rf-test-id': 'abp-price'})
    div = div.find(class_='statsValue')
    div = div.find('span')
    return div.text

def url_to_listing (url) :
    soup = url_to_soup(url)
    listing = {}
    listing['estimated_value'] = soup_to_estimated_value(soup)
    listing['number_of_baths'] = soup_to_number_of_baths(soup)
    return listing