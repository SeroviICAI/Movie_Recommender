# Movie Recommender:
This program recommends you a movie for any genre. This program uses argparse, so just running the program with no arguments won't execute anything.

## Code:
The code is inside the src directory.
- main.py - is in charge of orchestring the other modules.
- recommender.py - contains the recommendation engine.
- scraper.py - this is a IMDB web scraper, where it downloads all necessary data for any given genre and creates .csv files with them.
- constants.py - contains the few constants of the program.

The program recommends movies from a specific genre (that must be given by the user). The first movies/series to be recommended are those that share the most similar
genres, and have the best IMDB rating. Movies with a higher rating but less similar genres will have less priority than movies that share more similar genres.

## Running the program:
In order to run the recommender, on a command prompt type "python "path-to-main"/main.py -h". This will give you the basic instructions on how to run the program.

### Example:
If you have cloned this repository on your desktop, enter the command prompt in your computer (cmd in case you have windows) and type:
<p align="center">
    <strong>python C:\Users\<fill with username>\Desktop\movie_recomender\src\main.py -h</strong>
</p>
This program does not have a graphical interface, so all commands and functions are executed via command prompt.

### More use examples:
This command recommends the user some **action** films, similar to **Black Adam**.
<p align="center">
    <strong>python C:\Users\<fill with username>\Desktop\movie_recomender\src\main.py recommend action "Black Adam"</strong>
</p>
If you don't specify a movie:
<p align="center">
    <strong>python C:\Users\<fill with username>\Desktop\movie_recomender\src\main.py recommend action</strong>
</p>
The recommender will recommend the user the **best rated** movies of such genre, in this case **action**.

This command updates the program's "database" for a specific genre. If you don't specify any genre or write *, it will update all genres.
<p align="center">
    <strong>python C:\Users\<fill with username>\Desktop\movie_recomender\src\main.py update <optional: fill with genre></strong>
</p>
This command takes some time, and needs internet connection.

With the config command you can alter the amount of films/series to be recommended.

### Dockerfile:
Make sure, when running on dockerfile, go on terminal mode, in order to play with its functions.

### Some issues found:
1. The autocomplete function for movie titles does not work perfect.
2. The recommender is yet not very customable.
3. Some exception handling is missing.
