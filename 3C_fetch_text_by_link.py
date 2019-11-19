""" 
Fetch texts from Wikipedia by hyperlinks.
Following all links on a given Wiki URL. 
Methodically not as clean as "fetch by category". Some minor articles aside get fetched as well.
I used it for one language at a time whenever I couldn't get "fetch by category" to work.
Just paste in some URLs of a "Fetaured Articles" archive (or any other Wiki page) and language
according to your needs.
"""


import os
import timeit
import wikipediaapi  # https://github.com/martin-majlis/Wikipedia-API/
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from slugify import slugify
from tqdm import tqdm


start = timeit.default_timer()


LANGUAGE = "sq"

URLS = [
    "https://sq.wikipedia.org/wiki/Wikipedia:Faqja_kryesore/Artikulli_i_jav%C3%ABs/Arkivi/2019",
    "https://sq.wikipedia.org/wiki/Wikipedia:Faqja_kryesore/Artikulli_i_jav%C3%ABs/Arkivi/2018",
    "https://sq.wikipedia.org/wiki/Wikipedia:Faqja_kryesore/Artikulli_i_jav%C3%ABs/Arkivi/2017",
    "https://sq.wikipedia.org/wiki/Wikipedia:Faqja_kryesore/Artikulli_i_jav%C3%ABs/Arkivi/2016",
    "https://sq.wikipedia.org/wiki/Wikipedia:Faqja_kryesore/Artikulli_i_jav%C3%ABs/Arkivi/2015",
    "https://sq.wikipedia.org/wiki/Wikipedia:Faqja_kryesore/Artikulli_i_jav%C3%ABs/Arkivi/2014",
    "https://sq.wikipedia.org/wiki/Wikipedia:Faqja_kryesore/Artikulli_i_jav%C3%ABs/Arkivi/2013",
    "https://sq.wikipedia.org/wiki/Wikipedia:Faqja_kryesore/Artikulli_i_jav%C3%ABs/Arkivi/2012",
]

URL_BLACKLIST = [
    ":",
    "#",
    "/w/",
]


def make_directory(language):
    if not os.path.exists(language):
        os.makedirs(language)


for URL in URLS:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("a", href=True)
    titles = []
    for link in links:
        url = link["href"]
        if not any(exception in url for exception in URL_BLACKLIST):
            title = link.get_text()
            titles.append(title)
    wiki_wiki = wikipediaapi.Wikipedia(
        language=LANGUAGE, extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    make_directory("text/" + LANGUAGE)
    for counter, title in tqdm(enumerate(titles)):
        try:
            page = wiki_wiki.page(title)
            file = open("text/" + LANGUAGE + "/" + slugify(page.title) + ".txt", "w")
            file.write(page.text)
        except:
            print(URL, counter, "Something went wrong")


stop = timeit.default_timer()
print("Execution Time:", stop - start, "Language:", LANGUAGE)
