import requests
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from credentials import key
def add_movies(movies):
    try:
        API_KEY = key
        movs=[]
        for movie in movies:
            k=[]
            k.append(movie.strip().upper())
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options = options)
            query = "https://www.google.com/search?q="+movie+"+site%3Aimdb.com"
            driver.get(query)
            current_url = driver.current_url
            elem = driver.find_element_by_css_selector("div.tF2Cxc:nth-child(2) > div:nth-child(1) > a:nth-child(1) > h3:nth-child(2) > span:nth-child(1)")
            elem.click()
            WebDriverWait(driver, 15).until(EC.url_changes(current_url))
            url = driver.current_url
            payload = {'api_key': API_KEY, 'url': url}
            r = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
            soup = BeautifulSoup(r.content, 'html.parser')
            year = soup.select('#titleYear a')[0].get_text()
            k.append(year)
            star = soup.select('span[itemprop="ratingValue"]')[0].get_text().strip()
            k.append(star)
            ratings = soup.select("span.small")[0].get_text()
            k.append(ratings)
            watchtime = soup.select("time")[0].get_text().strip()
            k.append(watchtime)
            release_date_year = soup.select('a[title="See more release dates"]')[0].get_text().strip()
            k.append(release_date_year)
            f = soup.select("div.subtext a")
            genre = []
            for i in range(0,len(f)-1):
                genre.append(f[i].get_text())
            k.append(",".join(genre))
            summary = soup.select(".summary_text")[0].get_text().strip()
            k.append(summary)
            movs.append(k)
        conn = sqlite3.connect('movies.db')
        c = conn.cursor()
        for i in movs:
            c.execute(r"INSERT INTO movies VALUES(:name, :year, :star, :ratings, :watchtime, :release_date_year, :genre, :summary)",
                        {
                            'name': i[0],
                            'year': i[1],
                            'star': i[2],
                            'ratings': i[3],
                            'watchtime': i[4],
                            'release_date_year': i[5],
                            'genre': i[6],
                            'summary': i[7]
                        })
        conn.commit()
        conn.close()
    except:
        pass

def delete_movies(movies):
    try:
        conn = sqlite3.connect('movies.db')
        c = conn.cursor()
        for movie in movies:
            movie = movie.strip().upper()
            c.execute(r"DELETE FROM MOVIES WHERE NAME= :name",{
                'name':movie
            })
        conn.commit()
        conn.close()
    except:
        pass


def show_details(query):
    try:
        conn = sqlite3.connect('movies.db')
        c = conn.cursor()
        c.execute(r"SELECT * FROM MOVIES WHERE NAME= :name",{
            'name': query
        })
        k=c.fetchone()
        conn.commit()
        conn.close
        return list(k)
    except:
        return 0

