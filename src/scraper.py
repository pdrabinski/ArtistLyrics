from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import csv
from selenium import webdriver
from dateutil.parser import parse
import time
import os

class Artist_Lyrics:

    def __init__(self,artist_name,base_url):
        self.artist = artist_name
        self.base_url = base_url

    def get_lyrics(self,url,csv_location):
        self.url = url
        self.csv_location = csv_location 
        self.song_list = []

        driver = webdriver.Firefox()
        driver.get(url)
        response = driver.page_source
        driver.quit()

        soup = BeautifulSoup(response, 'html.parser')

        soup = soup.find('div', attrs={'id': 'listAlbum'})
        for row in soup:
            if row.name == 'div' and row.attrs['class'] == ['album']:
                try:
                    album = row.find('b').contents[0].strip('"')
                except:
                    album = 'Single'
            elif row.name == 'a':
                song_url = self.base_url + row['href'][2:]
                song_name = row.contents[0]
                self.song_list.append([album,song_name, song_url])
        self.get_song_lyrics()
        return True

    def get_song_lyrics(self):
        for song in self.song_list:
            album = song[0]
            song_name = song[1]
            url = song[2]

            driver = webdriver.Firefox()
            driver.get(url)
            response = driver.page_source
            driver.quit()

            soup = BeautifulSoup(response, 'html.parser')
            song_to_find = '"' + song_name + '"'
            # lyrics = soup.find('b',string=song_to_find).next_element.next_element.next_element.next_element.next_element.next_element.text
            lyrics = soup.find('b',string=song_to_find)
            while lyrics.name != 'div':
                lyrics = lyrics.next_element
            # print(type(lyrics))
            lyrics = lyrics.text
            self.parse_lyrics(lyrics,album,song_name)
        return True

    def parse_lyrics(self,lyrics,album,song_name):
        lyrics = lyrics.strip('\n')
        lyrics = lyrics.split('\n\n')
        lyrics = [lyric.replace('\n',', ') for lyric in lyrics]  
        for lyric in lyrics:
            print("album: " + album)
            print("song: " + song_name)
            print("lyric: " + lyric)
            self.print_to_csv(lyric,album,song_name)
        return True
    
    def print_to_csv(self,lyric,album,song_name):
        with open(self.csv_location,'a', newline='') as pf:
            writer = csv.writer(pf, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow([album, song_name, lyric])
        return True

if __name__ == '__main__':
    start = time.time()
    data_file = '../data/lyrics.csv'
    base_url = 'https://www.azlyrics.com'
    artist_url = 'https://www.azlyrics.com/k/kinggizzardthelizardwizard.html'
    artist_name = 'King Gizzard and the Lizard Wizard'
    # os.remove(data_file)
    lyrics = Artist_Lyrics(artist_name,base_url)
    lyrics.get_lyrics(artist_url, data_file)
    total_time = time.time() - start
    print(total_time, "sec")
