from multiprocessing.pool import ThreadPool
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dagster import asset
from typing import List, Tuple
from tqdm import tqdm

from constants import *


@asset
def scrape_all_genres(number_titles: int = 250) -> List[Tuple[str, pd.DataFrame]]:
    print('Downloading all genres...')
    dataframes = []
    for genre in GENRES:
        dataframes.append(scrape_genre(genre, number_titles))
    print('Finished downloading genres')
    return dataframes


def scrape_genre(genre: str, number_titles: int = 250) -> Tuple[str, pd.DataFrame]:
    if genre not in GENRES:
        raise ValueError('Unknown genre. Please enter a valid genre.')
    print(f'Scraping {genre}:')
    start = -49

    # Downloading urls
    thread_num = number_titles // 50
    url_list = [IMDB_URL.format(genre=genre, start=(start := start + 50)) for __ in range(thread_num)]
    pool = ThreadPool(thread_num)
    dataframes = pool.starmap(scrape_url, zip(url_list, genre.upper(), list(range(thread_num))))
    dataframe = pd.concat(dataframes).fillna("NaN")
    print()
    return genre, dataframe


def scrape_url(url: str, genre: str, number: int = 0) -> pd.DataFrame:
    # lists
    titles, years, ratings, genres, runtimes, imdb_ratings, metascores, votes = [], [], [], [], [], [], [], []
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, 'lxml')
    containers = soup.find_all('div', class_='lister-item mode-advanced')

    # extract info from soup
    with tqdm(total=len(containers), desc=f'\tScraping url {number + 1}...',
              bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}') as pbar:
        for container in containers:
            # title
            title = container.h3.a.text
            titles.append(title)

            if container.h3.find('span', class_='lister-item-year text-muted unbold') is not None:
                # year
                year = container.h3.find('span', class_='lister-item-year text-muted unbold').text
                years.append(year)
            else:
                years.append(None)

            if container.p.find('span', class_='certificate') is not None:
                # rating
                rating = container.p.find('span', class_='certificate').text
                ratings.append(rating)

            else:
                ratings.append("")

            genre_container = []
            if container.p.find('span', class_='genre') is not None:
                # genre
                genre_container = container.p.find('span', class_='genre').text.replace("\n", "").rstrip().split(',')
            if genre not in (genre_container := list(map(lambda x: x.replace(" ", "").upper(), genre_container))):
                genre_container.append(genre)
            genres.append(genre_container)

            if container.p.find('span', class_='runtime') is not None:
                # runtime
                time = int(container.p.find('span', class_='runtime').text.replace(" min", ""))
                runtimes.append(time)

            else:
                runtimes.append(None)

            if container.strong is not None and float(container.strong.text) is not None:
                # IMDB ratings
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

            else:
                imdb_ratings.append(None)

            if container.find('span', class_='metascore') is not None and container.find('span', class_='metascore'
                                                                                         ).text is not None:
                # Metascore
                m_score = int(container.find('span', class_='metascore').text)
                metascores.append(m_score)

            else:
                metascores.append(None)

            if container.find('span', attrs={'name': 'nv'}) is not None and container.find('span', attrs={'name': 'nv'})[
                                                                            'data-value'] is not None:
                # Number of votes
                vote = int(container.find('span', attrs={'name': 'nv'})['data-value'])
                votes.append(vote)

            else:
                votes.append(None)
            pbar.update(1)

    # create dataframe
    dataframe = pd.DataFrame({'MOVIE': titles,
                              'YEAR': years,
                              'RATING': ratings,
                              'GENRE': genres,
                              'RUNTIME (min)': runtimes,
                              'IMDB': imdb_ratings,
                              'METASCORE': metascores,
                              'VOTES': votes}
                             )
    return dataframe


@asset
def genres_to_binary(dataframes: List[Tuple[str, pd.DataFrame]]) -> List[Tuple[str, pd.DataFrame]]:
    new_dataframes = []
    for genre, dataframe in dataframes:
        dataframe = dataframe.explode("GENRE").pivot_table(index=['MOVIE', 'YEAR', 'RATING',
                                                                  'RUNTIME (min)', 'IMDB',
                                                                  'METASCORE', 'VOTES'],
                                                           columns="GENRE", aggfunc="size",
                                                           fill_value=0).reset_index()
        new_dataframes.append((genre, dataframe))
    return new_dataframes


def create_csv(dataframes: List[Tuple[str, pd.DataFrame]]) -> None:
    for genre, dataframe in dataframes:
        dataframe.to_csv(SAVE_PATH + genre + '.csv')
    return None
