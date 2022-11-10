import difflib
import re
import pandas as pd
from IPython.display import display

from scraper import *

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 3)


class Recommender(object):
    DATA_PATH = '../data/'

    def __init__(self, amount: int = 10):
        self.amount = amount

    def config(self, amount: int = 10):
        self.amount = amount

    def recommend_film(self, genre, movie: str = None):
        try:
            dataframe = pd.read_csv(self.DATA_PATH + genre + '.csv')
        except FileNotFoundError:
            print("Genre not found. Trying to download from source...")
            create_csv(genres_to_binary([scrape_genre(genre)]))
            dataframe = pd.read_csv(self.DATA_PATH + genre + '.csv')
            print()

        if not movie:
            print(f"Here are some of the best rated {genre} movies/series")
            display(dataframe.sort_values(by='IMDB', ascending=False, ignore_index=True).loc[:,
                    'MOVIE':"IMDB"].head(self.amount))
            return

        movie_choices = difflib.get_close_matches(movie, dataframe['MOVIE'])

        if len(movie_choices) == 0:
            print(f"We couldn't find {movie} in our data source. However, here are the best rated {genre}"
                  f"movies/series")
            display(dataframe.sort_values(by='IMDB', ascending=False, ignore_index=True).loc[:,
                    'MOVIE':"IMDB"].head(self.amount))
            return

        index = 0
        if len(movie_choices) > 1 and movie.upper() != str(movie_choices[0]).upper():
            print('These where the closest matches we could find:', movie_choices)
            index = int(input('Select the index of the movie/serie you meant (0, 1, ...): '))

        print(f'These are the best rated movies similar to {movie_choices[index]}')
        movie_row = dataframe[dataframe['MOVIE'] == movie_choices[index]]
        dataframe = dataframe[dataframe['MOVIE'].apply(self.regex_filter, args=[movie_choices[index], True])]

        dataframe['SIMILARITY'] = (abs(dataframe.iloc[:, 8:].sub(movie_row.iloc[:, 8:].values))).sum(axis=1)
        display(dataframe.sort_values(by=['SIMILARITY', 'IMDB'], ignore_index=True,
                                      ascending=[True, False]).loc[:, 'MOVIE':"IMDB"].head(self.amount))
        return

    @staticmethod
    def regex_filter(name, my_regex: str, exclude: bool = False):
        if name:
            result = re.search(my_regex, name)
            if result:
                return True if not exclude else False
            else:
                return False if not exclude else True
        else:
            return False


recommender = Recommender()
recommender.recommend_film("action", "Avatar")
