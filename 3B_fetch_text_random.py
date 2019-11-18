""" 
Scrape random Wikipedia articles.
This is probably the most simple way to get a large number of articles from Wikipedia in every language. 
Most of these articles are very short and lower quality. 
"""

import os
import timeit
from slugify import slugify
import wikipedia


LANGUAGES = ['it', 'nl', 'cz', 'se', 'no', 'fi', ]


start = timeit.default_timer()


def make_directory(language):
    if not os.path.exists(language):
        os.makedirs(language)


# def write_file(title):
#     text = wikipedia.WikipediaPage(title).content
#     file = open('text/' + LANGUAGE + '/' + slugify(title) + '.txt', 'w')
#     file.write(text)


for LANGUAGE in LANGUAGES:
    make_directory('text/' + LANGUAGE)
    wikipedia.set_lang(LANGUAGE)
    print(LANGUAGE)
    for _ in range(100):
        for title in wikipedia.random(pages=10):
            try:
                text = wikipedia.WikipediaPage(title).content
                file = open('text/' + LANGUAGE + '/' + slugify(title) + '.txt', 'w')
                file.write(text)
            except wikipedia.exceptions.DisambiguationError as e:
                # for title in e.options:
                #     text = wikipedia.WikipediaPage(title).content
                #     file = open('text/' + LANGUAGE + '/' + slugify(title) + '.txt', 'w')
                #     file.write(text)
                print('exception.DisambiguationError')


stop = timeit.default_timer()
print('Execution Time: ', stop - start)