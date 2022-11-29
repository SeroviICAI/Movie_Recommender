from dagster import job, op
from scraper import *


@op
def update_genre(genre, length):
    try:
        if genre == '-a' or not genre:
            if length:
                containers = genres_to_binary(scrape_all_genres(length))
            else:
                containers = genres_to_binary(scrape_all_genres())
        else:
            if length:
                containers = genres_to_binary([scrape_genre(genre, length)])
            else:
                containers = genres_to_binary([scrape_genre(genre)])
        create_csv(containers)
    except ConnectionError as e:
        print("ConnectionError:", e)


@op
def create_csv(dataframes: List[Tuple[str, pd.DataFrame]]) -> None:
    for genre, dataframe in dataframes:
        dataframe.to_csv(SAVE_PATH + genre + '.csv')


@job
def update_all_genres():
    update_genre()
