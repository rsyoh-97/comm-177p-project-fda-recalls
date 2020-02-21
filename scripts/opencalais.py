import os
import json
import requests
import bs4 
import re
from urllib.parse import urlsplit
data_dir = os.environ['DATA_DIR']

CALAIS_URL = 'https://api-eit.refinitiv.com/permid/calais'
# BELOW VARIABLE MUST BE SET IN ~/.bash_profile
API_KEY = os.environ['OPENCALAIS_API_KEY']

def main():
    html_path = os.path.join(data_dir, 'raw')
    dirs = os.listdir(html_path)
    for html_file in dirs:
        full_name = os.path.join(data_dir, 'raw', html_file)
        with open(full_name, 'rb') as source_file:
            html_file_read = source_file.read()
            soup = bs4.BeautifulSoup(html_file_read, "html.parser") 
            for item in soup.find_all('h2', string=re.compile("Reason for Recall")):    
                reason_par = str(item.find_next_sibling())
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
                page_name = full_name.split('/')[-1]
                json_path = str(page_name).replace('html', 'json')
                outfile = os.path.join(data_dir, 'raw', json_path)
                with open(outfile,'w') as out:
                    if response.status_code == 200:
                        print("Writing response to {}".format(outfile))
                        json.dump(response.json(), out, indent=4)

if __name__ == '__main__':
    main()