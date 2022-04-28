import json, os, requests, string
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from collections import defaultdict
from bs4 import BeautifulSoup

tag_map = defaultdict(lambda: wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

def getVideoPath(s):

    # split input string into tokens
    tokenized = getTokensFromString(s)

    # check to see if tokens are found in list of videos
    # return list of videos matching tokens
    videoJSON = getVideosFromTokens(tokenized)

    return videoJSON

def getTokensFromString(s):
    translator = str.maketrans('', '', string.punctuation)

    s = s.lower()
    s = s.translate(translator)
    tokenized = word_tokenize(s)

    lemmatized = []

    lemma_function = WordNetLemmatizer()
    for token, tag in pos_tag(tokenized):
        lemma = lemma_function.lemmatize(token, tag_map[tag[0]])
        lemmatized.append(lemma)

    # should remove articles / useless words from list first
    return lemmatized

def getVideosFromTokens(tokens):
    URL = "https://www.signasl.org/sign/"
    listClips = []

    for token in tokens:
        found = False
        src = ''

        sign = token
        page = requests.get(URL+sign)

        soup = BeautifulSoup(page.content, "lxml")
        results = soup.find(class_="col-md-12")

        if results is not None:
            video_elements = results.find_all("div", itemprop="video")
            for vid in video_elements:
                if not found:
                    source = vid.find("source")

                    if source is not None:
                        src = source["src"]
                        found = True
                else:
                    break
            if src != '':
                listClips.append(src)

    return json.dumps(listClips)