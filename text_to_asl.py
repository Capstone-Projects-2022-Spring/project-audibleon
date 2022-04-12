import json, os, requests, string
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

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

    # should remove articles / useless words from list first
    return tokenized

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