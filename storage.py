import json
from utilits import *
from scraper import BasketScraper
import datetime, json
import pandas as pd

class Storage():
    def __init__(self) -> None:
        self.scrap = BasketScraper()

    def update_fixtures(self):        
        matches = self.scrap.fixture_matches()
        self.__save_file( "fixtures", matches )
    def get_today(self):
        matches = self.__load_file("fixtures")        
        today_matches = []
        index = 0
        for m in matches:
            try:
                next_match = self.scrap.today_match_info(m)
                # match_date =  pd.to_datetime(next_match['date'],dayfirst=True)
                match_date = pd.to_datetime(next_match['date'],dayfirst=True)
                search_date =  datetime.datetime.now() + datetime.timedelta(days=1)
                past_date =  datetime.datetime.now() 
                if match_date > search_date :
                    break
                print(f"{index+1}")
                index += 1  
                if match_date < past_date: 
                    continue
                today_matches.append( self.__prepare_info(next_match) )
            except Exception as e:
                print(f"{warn}{warn}{warn}{warn}{warn}{warn}\nError {m} id")
                print(e)
        
        self.__save_file( "today", today_matches )
        self.__save_file( "fixtures", matches[index:] )
    def update_today(self):
        today_matches = self.__load_file("today")
        for ind, t in enumerate(today_matches, start=1):
            try:
                next_match = self.scrap.today_match_info( t["id"])                
                current = self.__prepare_info(next_match) 
                t['odd_h'] = current['odd_h']
                t['odd_a'] = current['odd_a']
                t['total'] = current['total']
                t['gandicap'] = current['gandicap']
                print(f"{ind} / {len(today_matches)}")
            except Exception as e:
                print(f"{warn}{warn}{warn}{warn}{warn}{warn}\nError {m} id")
                print(e)        
        self.__save_file( "today", today_matches )
    def transit_to_results(self):
        results = self.__load_file("results")
        today = self.__load_file("today")
        error_matches = []
        for ind, m in enumerate( today, start=1 ):
            try:
                curr = self.scrap.match_info(m["id"])
                print(f"{ind} / {len(today)}")
                results.append(self.__prepare_info(curr) )
            except Exception as e:
                print(f"{warn}{warn}{warn}{warn}{warn}{warn}\nError {m['id']} id")
                error_matches.append(m["id"])
                print(e)

        self.__save_file("results", results)
        self.__save_file("../matches_id", error_matches)
        self.__clear_file("today")

    def __save_file( self, name, col ):
        with open(f"storage/{name}.json", "w", newline='', encoding='utf-8') as fp:
            json.dump(col , fp,  indent=4, ensure_ascii=False)         
        print(f"{ok} Save {name} {len(col)} matches.")
    def __load_file( self, name ):
        col = []
        with open(f"storage/{name}.json", "r", newline='', encoding='utf-8') as fp:
            col = json.load(fp)
        print(f"{ok} Load {name} {len(col)} matches.")
        return col
    def __prepare_info(self, m):
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
    def __clear_file( self, name ):
        with open(f"storage/{name}.json", "w", newline='', encoding='utf-8') as fp:
            print(f"Clear {name} file")

if __name__ == "__main__":
    pass
