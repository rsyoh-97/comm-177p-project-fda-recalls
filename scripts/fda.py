import requests, bs4
import os
from urllib.parse import urljoin, urlparse
data_dir = os.environ['DATA_DIR']

def scrape():
    table_data = scrape_page_find_table()
    detailed_pages = get_detailed_page(table_data)

def scrape_page_find_table():
    url = "https://www.fda.gov/medical-devices/medical-device-recalls/2020-medical-device-recalls"
    response = requests.get(url).text
    soup = bs4.BeautifulSoup(response, "html.parser") 
    table = soup.find("table")
    table_data = table.find_all("a", href=True)
    return table_data

def get_detailed_page (table_data):
    for link in table_data:
        short_link = link.attrs['href']
        link_last_portion = short_link.split('/')[-1]
        full_link = urljoin('https://www.fda.gov', short_link)
        html_file = "{}.html".format(link_last_portion)
        detailed_page = requests.get(full_link).text
        outfile = os.path.join(data_dir, 'raw', html_file)
        with open(outfile, 'w') as source_file:
            source_file.write(detailed_page)

if __name__ == '__main__':
    scrape()