from fda import scrape
from opencalais import run_opencalais
from report import create_csv_social_tag

def main():
    scrape()
    run_opencalais()
    create_csv_social_tag()
    
if __name__ == '__main__':
    main()