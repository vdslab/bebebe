import datetime
import requests
from bs4 import BeautifulSoup
import json
import serch_spotify
import time

def create_json_data(year,month,day):
  url = 'https://www.billboard-japan.com/charts/detail?a=tiktok&year=' + str(year) + '&month=' + str(month) +'&day=' + str(day)
  response = requests.get(url)
  text_html = response.text
  soup = BeautifulSoup(text_html, 'html.parser')
  ranking = soup.select('td.rank_td.pc_obj')
  music_title = soup.select('p.musuc_title')
  artists = soup.select('p.artist_name')
  ranking_data = []
  for r,title,artist in zip(ranking,music_title,artists):
    r = r.select_one('span')
    ranking_info = {}
    ranking_info['ranking'] = r.text
    ranking_info['title'] = title.text
    ranking_info['artist'] = artist.text
    ranking_info['url'] = serch_spotify.serch_spotify_url(title.text)
    ranking_info['date'] = str(year) + '/' + str(month) + '/' + str(day)
    ranking_data.append(ranking_info)
    # time.sleep(1)
  return ranking_data

def main():
  tiktok_ranking_data = []
  date = datetime.date(2021,12,13)
  end = datetime.date(2022,5,16)
  while date <= end:
    print(date)
    year = date.year
    month = date.month
    day = date.day
    ranking_data = create_json_data(year,month,day)
    tiktok_ranking_data.extend(ranking_data)
    date += datetime.timedelta(days=7)
  path = './data/tiktok_ranking_data.json'
  with open(path,'w',encoding='utf-8') as f:
    json.dump({'tiktok_ranking_data':tiktok_ranking_data},f,indent=2,ensure_ascii=False)

if __name__ == '__main__':
  main()