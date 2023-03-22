import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

#  product title
def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": 'productTitle'})

        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string
#  product description
def get_description(soup):
    try:
         description = soup.find('div', {'id': 'productDescription'}).text.strip()
    except AttributeError:
        try:
            description = soup.find('div', {'id': 'productDescription'}).text.strip()
        except:
            description=""
    return description

# Extract the ASIN (Amazon Standard Identification Number)
def get_asin(soup):
    try:
         asin = soup.find('th', string='ASIN').find_next_sibling('td').text.strip()
    except AttributeError:
        asin=""
    return asin
# Extract the manufacturer
def get_manufacturer(soup):
    try:
         manufacturer = soup.find('th', string='Manufacturer').find_next_sibling('td').text.strip()
    except AttributeError:
        manufacturer =""
    return manufacturer

if __name__ == '__main__':
    HEADERS = ({'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'})

    product_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
    response = requests.get(product_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    links_list = []
    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[], "description":[], "asin":[],"manufacturer":[]}

    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        d['title'].append(get_title(new_soup))
        d['description'].append(get_description(new_soup))
        d['asin'].append(get_asin(new_soup))
        d['manufacturer'].append(get_manufacturer(new_soup))

    # Write the extracted data to a CSV file
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('',np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)

amazon_df