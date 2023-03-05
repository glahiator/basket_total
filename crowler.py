import argparse, json
from utilits import *
from scraper import BasketScraper
from storage import Storage

def scrap_all_matches_id_from_results( ) -> None:
    scrap = BasketScraper()
    matches = scrap.all_results_id()
    with open(f"matches_id.json", "w", newline='', encoding='utf-8') as fp:
        json.dump(matches , fp, sort_keys=True, indent=4, ensure_ascii=False) 
    print(f"{ok} Save to file: matches.json {len(matches)} items")

def scrap_match_info_from_file(  ) -> None:
    def __prepare_info( m):
        m_new = {}
        for k,v in m.items():
            if k in ["home", "away", "id"]:
                m_new[k] = v
            elif k == "odds":
                m_new["odd_h"] = v["home"]
                m_new["odd_a"] = v["away"]
                m_new['total'] = v['total'][0]
                m_new['gandicap'] = v['gandicap'][0]
            elif k in ["quarters", "score", "date"]:
                m_new[k] = v
        return m_new

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
            mm = __prepare_info(mm)
            match_scrap.append(mm)
        except Exception as e:
            print(f"{warn}{warn}{warn}{warn}{warn}{warn}\nError {m} id")
            print(e)
        
    with open(f"matches.json", "w", newline='', encoding='utf-8') as fp:
        json.dump(match_scrap , fp,  indent=4, ensure_ascii=False) 
    print(f"{ok} Scraped {len(match_scrap)} matches.")

def scrap_shedule_matches( ):
    scrap = BasketScraper()
    matches = scrap.fixture_matches()
    print(f"{ok} Load {len(matches)} matches.\nStart parsing...")
    match_scrap = []
    index = 1
    for m in matches:
        try:
            mm = scrap.today_match_info(m)
            print(f"{index} / {len(matches)}")
            index += 1
            match_scrap.append(mm)
        except Exception as e:
            print(f"{warn}{warn}{warn}{warn}{warn}{warn}\nError {m} id")
            print(e)
        
    with open(f"matches_sched.json", "w", newline='', encoding='utf-8') as fp:
        json.dump(match_scrap , fp,  indent=4, ensure_ascii=False) 
    print(f"{ok} Scraped {len(match_scrap)} matches.")

def get_lifecycle():
    keeper = Storage()
    keeper.transit_to_results()
    keeper.get_today()
        

def convert():
    old_matches = []
    with open(f"matches_new.json", "r", newline='', encoding='utf-8') as fp:
        old_matches = json.load(fp)
    print(f"{ok} Load {len(old_matches)} matches.")
    new_matches = []
    for ind, m in enumerate( old_matches, start=1 ):
        m_new = {}
        for k,v in m.items():
            
            if k in ["home", "away"]:
                m_new[k] = v
            if k in [ "id", "date"]:
                m_new[k] = v
            elif k == "odds":
                m_new["odd_h"] = v["home"]
                m_new["odd_a"] = v["away"]
                m_new['total'] = v["total"][0]
                m_new['gandicap'] = v['gandicap'][0] 
            elif k in ["score", "quarters"]:
                m_new[k] = v
        print( f"{ind}/{len(old_matches)} {m['id']}")
        new_matches.append(m_new)
    with open(f"results.json", "w", newline='', encoding='utf-8') as fp:
        json.dump(new_matches , fp,  indent=4, ensure_ascii=False)         
    print(f"{ok} Save {len(new_matches)} matches.")



def main(args):    
    if args.mode == "matches":
        scrap_match_info_from_file( )
    elif args.mode == "results" :
        scrap_all_matches_id_from_results()  
    elif args.mode == "shedule":
        get_lifecycle()
    elif args.mode == "update":
        keeper = Storage()
        keeper.update_fixtures()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrapper modes select.')
    parser.add_argument('mode', choices=['matches', "results", "shedule", "update"])
    args = parser.parse_args()       
    main(args)
    print("Finish")

