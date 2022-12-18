import argparse, json
from utilits import *
from scraper import BasketScraper

def scrap_all_matches_id_from_results( ) -> None:
    scrap = BasketScraper()
    matches = scrap.all_results_id()
    with open(f"matches_id.json", "w", newline='', encoding='utf-8') as fp:
        json.dump(matches , fp, sort_keys=True, indent=4, ensure_ascii=False) 
    print(f"{ok} Save to file: matches.json {len(matches)} items")

def scrap_match_info_from_file(  ) -> None:
    scrap = BasketScraper()
    with open(f"matches_id.json", "r", newline='', encoding='utf-8') as fp:
        matches = json.load(fp)
    print(f"{ok} Load {len(matches)} matches.\nStart parsing...")
    match_scrap = []
    index = 1
    for m in matches:
        try:
            mm = scrap.match_info(m)
            print(f"{index} / {len(matches)}")
            index += 1
            match_scrap.append(mm)
        except Exception as e:
            print(f"{warn}{warn}{warn}{warn}{warn}{warn}\nError {m} id")
            print(e)
        
    with open(f"matches.json", "w", newline='', encoding='utf-8') as fp:
        json.dump(match_scrap , fp,  indent=4, ensure_ascii=False) 
    print(f"{ok} Scraped {len(match_scrap)} matches.")

def main(args):    
    if args.mode == "matches":
        scrap_match_info_from_file( )
    if args.mode == "results" :
        scrap_all_matches_id_from_results()     

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrapper modes select.')
    parser.add_argument('mode', choices=['matches', "results"])
    args = parser.parse_args()       
    main(args)
    print("Finish")

