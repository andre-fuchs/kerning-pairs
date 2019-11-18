""" 
Fetch texts from Wikipedia by category.
I used the categories "Featured Articles" and/or "Quality Articles" to get longer 
and well approved articles only. This does not work for every language. 
You can add more categories to the dictionary and more entries to the list of languages 
to try it yourself. Depending on the number of articles and your internet connection speed
this may take up to an hour.
"""


import os
import timeit
import wikipediaapi  # https://github.com/martin-majlis/Wikipedia-API/
import wikipedia
from slugify import slugify
from tqdm import tqdm


start = timeit.default_timer()


LANGUAGES = [
    'sk',
]

CATEGORY = {
    # 'sk': 'Wikipédia:Dobré články',
    'sk': 'Wikipédia:Najlepšie články'
    # 'ro': 'Wikipedia articole de calitate',
    # 'lv': 'Vērtīgi raksti',
    # 'lt': 'Vertingi straipsniai',
    # 'hr': 'Izabrani članci',
    # 'da': 'Ugens artikel',
    # 'de': 'Wikipedia:Lesenswert',
    # 'en': 'Featured articles',
    # 'fr': 'Article de qualité',
    # 'es': 'Wikipedia:Artículos_destacados',   
    # 'pt': '!Artigos bons',
    # 'it': 'Wikipedia:Voci_di_qualità',
    # 'nl': 'Wikipedia:Uitgelicht'
    # 'pl': 'Artykuły na medal',
}


def make_directory(language):
    if not os.path.exists(language):
        os.makedirs(language)


def fetch_categorymembers(categorymembers, level=0, max_level=1):
    for page in tqdm(categorymembers.values()):
        file = open('text/' + LANGUAGE + '/' + slugify(page.title) + '.txt', 'w')
        file.write(page.text)
        ### TEMPORARY
        # title = page.title.replace('Diskussion:', '')
        # try:
        #     text = wikipedia.WikipediaPage(title).content
        #     file = open('text/' + LANGUAGE + '/' + slugify(title) + '.txt', 'w')
        #     file.write(text)
        # except wikipedia.exceptions.DisambiguationError as e:
        #     print('exception.DisambiguationError')
        ### TEMPORARY


for LANGUAGE in tqdm(LANGUAGES):
    wiki_wiki = wikipediaapi.Wikipedia(
        language=LANGUAGE,
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    ### TEMPORARY
    # wikipedia.set_lang(LANGUAGE)
    ### TEMPORARY
    category = wiki_wiki.page('Category:' + CATEGORY.get(LANGUAGE))
    # print(category.categorymembers)
    make_directory('text/' + LANGUAGE)
    fetch_categorymembers(category.categorymembers)


stop = timeit.default_timer()
print('Execution Time: ', stop - start)
