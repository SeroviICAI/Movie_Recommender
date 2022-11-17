import argparse
import os
import sys

import pickle
from recommender import *
from scraper import *

WORKING_DIR = os.getcwd()
os.chdir(WORKING_DIR)


def create_parser():
    parser = argparse.ArgumentParser(
        prog='main.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="This is a movie recommendation engine. Try it out!")

    subparsers = parser.add_subparsers(dest='command')
    recommend = subparsers.add_parser("recommend", help="command used to recommend movies.")
    recommend.add_argument('genre', nargs=1, type=str, help="enter a genre to optimize the search.")
    recommend.add_argument('liked-movie', nargs='?', type=str, help="you can enter a movie you liked, to filter"
                                                                    " the recommender's searches to movies which"
                                                                    " resemble this film.")

    config = subparsers.add_parser("config", help="config recommender manually.")
    config.add_argument('amount', nargs='?', type=int, help="number of movies to be recommended.")

    update = subparsers.add_parser("update", help="update data sources manually.")
    update.add_argument('genre', nargs="?", type=str, help="enter a genre whose source you want to update manually."
                                                           ' Enter "-a" or nothing to update all genres.',
                        default="-a")
    update.add_argument('length', nargs="?", type=int, help="enter the amount of movies you want in your new data"
                                                            " source.",
                        default=250)
    return parser


def main():
    try:
        recommender = Recommender()
        try:
            with open('recommender.dat', 'rb') as file:
                recommender = pickle.load(file)
        except (FileNotFoundError, OSError, IOError):
            print("WARNING: Recommender configurations not found. Recommender has default config.")
        except EOFError:
            pass

        parser = create_parser()
        args = parser.parse_args()

        if args.command == 'recommend':
            recommender.recommend_film(args.genre[0], args.__dict__['liked-movie'])
        elif args.command == 'config':
            recommender.config(args.amount)
        elif args.command == 'update':
            if args.genre == "-a":
                containers = genres_to_binary(scrape_all_genres(args.length))
                create_csv(containers)
            else:
                container = genres_to_binary([scrape_genre(args.genre, args.length)])
                create_csv(container)

    except ValueError as e:
        print('ValueError:', e)

    except KeyboardInterrupt:
        print('Closing tasks...')

    finally:
        try:
            with open('recommender.dat', "wb") as file:
                pickle.dump(recommender, file)
        except (FileNotFoundError, OSError, IOError, EOFError):
            print("WARNING: Recommender configurations couldn't be saved.")
    return


if __name__ == '__main__':
    sys.exit(main())
