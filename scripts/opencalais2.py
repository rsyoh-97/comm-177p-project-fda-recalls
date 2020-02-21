import os
import json
import requests
import bs4 
import re
data_dir = os.environ['DATA_DIR']


CALAIS_URL = 'https://api-eit.refinitiv.com/permid/calais'
# BELOW VARIABLE MUST BE SET IN ~/.bash_profile
API_KEY = os.environ['OPENCALAIS_API_KEY']

def main():
    reason_par = parse_html()
    results = opencalais(reason_par)

def parse_html(): 
    html_path = os.path.join(data_dir, 'raw')
    dirs = os.listdir(html_path)
    for html_file in dirs:
        full_name = os.path.join(data_dir, 'raw', html_file)
        with open(full_name, 'rb') as source_file:
            html_file_read = source_file.read()
            soup = bs4.BeautifulSoup(html_file_read, "html.parser") 
            for item in soup.find_all('h2', string=re.compile("Reason for Recall")):    
                reason_par = item.find_next_sibling()

def opencalais(reason_par):
    headers = {
        'X-AG-Access-Token' : API_KEY,
        'Content-Type' : 'text/raw',
        'outputformat' : 'application/json',
        'x-calais-selectiveTags': 'company,industry,socialtags'
    }
    # Construst a POST request, as required by the OpenCalais API
    response = requests.post(
        CALAIS_URL,
        data=reason_par,
        headers=headers,
        timeout=80
    )

    outfile = '../data/raw/1.json'
    with open(outfile,'w') as out:
        if response.status_code == 200:
            print("Writing response to {}".format(outfile))
            json.dump(response.json(), out, indent=4) 
    
# def save_json():
#     dirs_2 = os.listdir(json_path)
#     for json_file in dirs_2:
#         json_path = os.path.join(data_dir, 'raw')



# def parse_html_new():
#     link_last_portion= link.attrs['href'].split('/')[-1]
#     # link_last_portion = short_link.split('/')[-1]
#     file_name = "{}.html".format(link_last_portion)
#     html_file = os.path.join(data_dir, 'raw', file_name)
#     with open(html_file, 'r') as source_file:
#         html_file_read = source_file.read()
#     soup = bs4.BeautifulSoup(html_file_read, "html.parser") 
#     soup_h2 = soup.find_all('h2')[6]
#     soup_p = soup.find_all('p')[4]
#     return parsed_par 


if __name__ == '__main__':
    parse_html()