import requests, bs4
import os
import json
import nested_lookup
import csv
data_dir = os.environ['DATA_DIR']
dir_path = os.path.join(data_dir, 'raw')
dirs = os.listdir(dir_path)
csv_path = os.path.join(data_dir, 'processed','fda_tags.csv')

def create_csv_social_tag():
    with open(csv_path, 'w') as newfile:
        col_headers = ['entity', 'source_file']
        writer = csv.DictWriter(newfile, fieldnames=col_headers)
        writer.writeheader()
        for json_file in dirs:
            if json_file.endswith(".json"): 
                full_name = os.path.join(data_dir, 'raw', json_file)
                with open(full_name) as source_file:
                    read_json = json.load(source_file)     
                    for key, val in read_json.items():
                        try:
                            if val['_typeGroup'] == "socialTag":
                                writer.writerow({
                                    'entity': val["name"],
                                    'source_file': full_name
                                })    
                        except KeyError:
                            continue
                       
if __name__ == '__main__':
    create_csv_social_tag()