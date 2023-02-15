import datetime
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver 
from utilits import *
from bs4 import BeautifulSoup
import platform

class BasketScraper(object):
    '''Need doc'''
    def __init__(self) -> None: 
        service = Service(executable_path="chromedriver.exe")
        if platform.system() == "Linux":
            service = Service(executable_path="./chromedriver")
        options = get_browser_options()     
        options.headless = False
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-certificate-errors')
        self.browser = webdriver.Chrome(service=service, chrome_options = options)   
    def __del__(self) -> None:
        pass
    
    def all_results_id(self):
        all_matches = []
        url = "https://www.flashscorekz.com/basketball/usa/nba/results/"
        self.browser.get(url)
        self.browser.set_page_load_timeout(11) 
        time.sleep(4) 
        generated_html = self.browser.page_source
        soup = BeautifulSoup(generated_html, 'lxml')    
        matches = soup.find_all('div', title="Подробности матча!")
        prev_count = len(matches)
        current_count = len(matches)
        while prev_count == current_count:
            try:
                show_more = self.browser.find_element(by=By.CLASS_NAME, value='event__more--static')
                self.browser.execute_script("arguments[0].scrollIntoView();",show_more)
                time.sleep(1)
                self.browser.execute_script('arguments[0].click();', show_more)
                time.sleep(1)
            except NoSuchElementException as ex:
                print(ex.msg)
                
            soup = BeautifulSoup(self.browser.page_source, 'lxml')    
            matches = soup.find_all('div', title="Подробности матча!")
            current_count = len(matches)
            if current_count == prev_count:
                for m in matches:
                    all_matches.append(m.get('id')[4:] )
                return all_matches                   
            else:
                prev_count = current_count
    def match_info(self, m_id) -> dict:
        self.url = f"https://www.flashscorekz.com/match/{m_id}"
        self.browser.get(self.url)
        self.browser.set_page_load_timeout(3) 
        time.sleep(3) 
        generated_html = self.browser.page_source
        soup = BeautifulSoup(generated_html, 'lxml') 
        self.verbose = False 
        self.date = ""
        self.home = ""
        self.away = ""
        self.score = ""
        self.quater = { 1 : "", 2 : "", 3 : "", 4 : "", 5 : "" }
        self.all_odds = {            
            "home" : "",
            "away" : "",            
            "total" : [],
            "gandicap" : []
        }

        self.__get_duel( soup.find('div', class_ = "duelParticipant"))
        self.__get_score(soup.find('div', class_ = "smh__template" ))
        self.__get_odds(soup.find('div', class_ = "tabs__detail"))
        
        result = {
            "id" : m_id,
            "date" : self.date,
            "home" : self.home,
            "away" : self.away,
            "score" : self.score,
            "quarters" : self.quater,
            "odds" : self.all_odds,
        }
        return result

    def fixture_matches(self):
        all_matches = []
        self.url = f"https://www.flashscorekz.com/basketball/usa/nba/fixtures/"
        self.browser.get(self.url)
        self.browser.set_page_load_timeout(3) 
        time.sleep(5) 
        generated_html = self.browser.page_source
        soup = BeautifulSoup(generated_html, 'lxml') 
        matches = soup.find_all('div', title="Подробности матча!")
        for m in matches:
            all_matches.append(m.get('id')[4:] )
        return all_matches
    def today_match_info(self, m_id) ->dict:
        self.url = f"https://www.flashscorekz.com/match/{m_id}"
        self.browser.get(self.url)
        self.browser.set_page_load_timeout(3) 
        time.sleep(3) 
        generated_html = self.browser.page_source
        soup = BeautifulSoup(generated_html, 'lxml') 
        self.verbose = False              
        self.all_odds = {            
            "home" : "",
            "away" : "",            
            "total" : [],
            "gandicap" : []
        }

        names_div = soup.find('div', class_ = "duelParticipant")
        if names_div is None:
            return
        date_el = names_div.find('div', class_ = "duelParticipant__startTime")
        date = date_el.find('div').get_text()
        date =  str( pd.to_datetime(date,dayfirst=True) )
        # date = datetime.datetime.strptime(date, '%d.%m.%Y')
        

        pl1_el = names_div.find('div', class_ = "duelParticipant__home")
        pl1_div = pl1_el.find('div', class_='participant__participantName')
        pl1_name = pl1_div.find('a').get_text()

        pl2_el = names_div.find('div', class_ = "duelParticipant__away")
        pl2_div = pl2_el.find('div', class_='participant__participantName')
        pl2_name = pl2_div.find('a').get_text()

        self.__get_odds(soup.find('div', class_ = "tabs__detail"))
        
        result = {
            "id" : m_id,
            "date" : date,
            "home" : pl1_name,
            "away" : pl2_name,
            "odds" : self.all_odds,
        }
        return result

    def __get_duel(self, duel_div : BeautifulSoup):
        if duel_div is None:
            return
        date_el = duel_div.find('div', class_ = "duelParticipant__startTime")
        date = date_el.find('div').get_text()
        date = str( pd.to_datetime(date,dayfirst=True) )

        pl1_el = duel_div.find('div', class_ = "duelParticipant__home")
        pl1_div = pl1_el.find('div', class_='participant__participantName')
        pl1_link = pl1_div.find('a').get('href')
        pl1_name = pl1_div.find('a').get_text()

        pl2_el = duel_div.find('div', class_ = "duelParticipant__away")
        pl2_div = pl2_el.find('div', class_='participant__participantName')
        pl2_link = pl2_div.find('a').get('href')
        pl2_name = pl2_div.find('a').get_text()
        match_status = ""

        match_status_el = duel_div.find("span", class_ = "fixedHeaderDuel__detailStatus")
        if match_status_el is not None:
            match_status = match_status_el.get_text()

        if self.verbose:
            print(f"{date} {match_status}")
            print(f"1: {pl1_name} {pl1_link}")
            print(f"2: {pl2_name} {pl2_link}")

        self.date = date
        self.status = match_status
        # self.home = {
        #     "name" : pl1_name,
        #     "url"  : pl1_link,
        #     "id"   : pl1_link.split("/")[-1]
        # }
        # self.away = {
        #     "name" : pl2_name,
        #     "url"  : pl2_link,
        #     "id"   : pl2_link.split("/")[-1]
        # }
        self.home = pl1_name
        self.away = pl2_name
    def __get_score(self, score_div : BeautifulSoup):
        if score_div is None:
            return
        score = score_div.find_all('div', class_ ="smh__score")
        self.quater = { 1 : "", 2 : "", 3 : "", 4 : "", 5 : "" }
        if len(score) == 2: 
            if not score[0].get_text().isnumeric() or  not score[1].get_text().isnumeric():
                return       
            score_h = int(score[0].get_text())
            score_a = int(score[1].get_text())            
            if self.verbose:
                print(f"Score {score_h}:{score_a}")
            self.score = f"{score_h}:{score_a}"
            
            for set_ in range(1, 6):
                curr_set = score_div.find_all('div', class_ =f"smh__part--{set_}")
                if len(curr_set) == 2:                    
                    if not curr_set[0].get_text().isnumeric() or not curr_set[1].get_text().isnumeric():
                        continue
                    score_h = int(curr_set[0].get_text())
                    score_a = int(curr_set[1].get_text())
                    self.quater[set_] = f"{score_h}:{score_a}"  
                    if self.verbose:
                        print(f"{set_} {self.quater[set_]}")                    
                else:
                    if self.verbose:
                        print( f"Not find current {set_} set score" )
        else:
            if self.verbose:
                print(f"Not find match score")
    def __get_odds(self, get_stats_div : BeautifulSoup):
        self.all_odds = {            
            "home" : "",
            "away" : "",            
            "total" : [],
            "gandicap" : []
        }
        if get_stats_div is None:
            return
        tt = get_stats_div.find_all('a')
        for t in tt:
            if t.get_text() == "Коэфф.":
                self.haveStat = True                
                url_team_odds = self.url + "#/odds-comparison/home-away/ft-including-ot"
                self.browser.get(url_team_odds)
                time.sleep(0.5)
                generated_html = self.browser.page_source
                stat_soup = BeautifulSoup(generated_html, 'lxml')
                team_odds = stat_soup.find_all('a', class_ ="oddsCell__odd")
                home = team_odds[0].get_text()
                away = team_odds[1].get_text()
                self.all_odds["home"] = home
                self.all_odds["away"] = away
                
                if self.verbose:
                    print(f"Team odds {home} : {away}")

                url_total_odds = self.url + "#/odds-comparison/over-under/ft-including-ot"
                self.browser.get(url_total_odds)
                time.sleep(0.5)
                generated_html = self.browser.page_source
                stat_soup = BeautifulSoup(generated_html, 'lxml')
                total_rows = stat_soup.find_all( 'div', class_ = "ui-table__row" )                              
                for r in total_rows:
                    ttl = r.find( 'span', class_ =  "oddsCell__noOddsCell" ).get_text()
                    over_under = r.find_all('a', class_ = "oddsCell__odd")
                    over = over_under[0].get_text()
                    under = over_under[1].get_text()
                    if self.verbose:
                        print(f"Total odd: {ttl} : {over} {under}")
                    if float( over ) < 1.97  and float( under ) < 2.0 :
                        self.all_odds["total"] = [ttl, over, under]
                        break
                    else:
                        self.all_odds["total"].append([ttl, over, under])
                    

                url_total_odds = self.url + "#/odds-comparison/asian-handicap/full-time"
                self.browser.get(url_total_odds)
                time.sleep(0.5)
                generated_html = self.browser.page_source
                stat_soup = BeautifulSoup(generated_html, 'lxml')
                total_rows = stat_soup.find_all( 'div', class_ = "ui-table__row" )                              
                for r in total_rows:
                    ttl = r.find( 'span', class_ =  "oddsCell__noOddsCell" ).get_text()
                    over_under = r.find_all('a', class_ = "oddsCell__odd")
                    over = over_under[0].get_text()
                    under = over_under[1].get_text()
                    if self.verbose:
                        print(f"Gandicap odd: {ttl} : {over} {under}")
                    if float( over ) < 1.97  and float( under ) < 2.0 :
                        self.all_odds["gandicap"] = [ttl, over, under]
                        break
                    else:
                        self.all_odds["gandicap"].append([ttl, over, under])
                    

if __name__ == "__main__":
    pass