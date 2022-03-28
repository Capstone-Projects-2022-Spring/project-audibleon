import json
import os

from moviepy.editor import *
from nltk.tokenize import word_tokenize
import string


PATH = os.getcwd()

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

def List2Dic(List):
    return dict(map(lambda x: [ x.split(".")[0], x], List))

def getVideosFromTokens(tokens):
    filename = "video_list.txt"
    with open(filename) as f:
        videoFiles = f.read().splitlines()

    videoFiles = List2Dic(videoFiles)

    for key in tokens:
        if key not in videoFiles:
            tokens.remove(key)

    keptFiles = { key: videoFiles[key] for key in tokens}

    listClips = []


    for key, value, in keptFiles.items():
        print("KEY: ", key)

        data = value
        listClips.append(data)

    return json.dumps(listClips)

# def createVideoFromDict(dict):
#     listClips = []
#     print(dict)
#
#     data = {}
#     data['type'] = 'video/mp4'
#
#     for key, value in dict.items():
#         print("KEY: ", key)
#         # text_clip = TextClip(key, fontsize = 60, color = 'red')
#         # text_clip = text_clip.set_position('bottom')
#         #
#         # clip = CompositeVideoClip([clip, text_clip])
#         data['src'] = value
#         listClips.append(data)
#
#     # path = "C:\\Users\\rlazz\\Documents\\GitHub\\project-audibleon\\website\\static\\testing.mp4"
#     #
#     # if os.path.exists(path):
#     #     print("deleting!")
#     #     os.remove(path)
#     #
#     # final_clip = concatenate_videoclips(listClips)
#     # final_clip.write_videofile(path)
#     json_data = json.dumps(listClips)
#
#     return json_data