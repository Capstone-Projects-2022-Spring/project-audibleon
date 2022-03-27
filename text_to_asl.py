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
    videoDict = getVideosFromTokens(tokenized)

    # create new video file from list of videos
    # return where to access the video file as a single name
    videoPath = createVideoFromDict(videoDict)

    return videoPath

def getTokensFromString(s):
    translator = str.maketrans('', '', string.punctuation)

    s = s.lower()
    s = s.translate(translator)
    tokenized = word_tokenize(s)

    # should remove articles / useless words from list first
    return tokenized

def List2Dic(List):
    return dict(map(lambda x: [ x.split("\\")[-1][:-4], x], List))

def getVideosFromTokens(tokens):
    filename = "video_list.txt"
    with open(filename) as f:
        videoFiles = f.read().splitlines()

    videoFiles = List2Dic(videoFiles)

    for key in tokens:
        if key not in videoFiles:
            tokens.remove(key)

    filesToReturn = { key: videoFiles[key] for key in tokens}
    return filesToReturn

def createVideoFromDict(dict):
    listClips = []
    print(dict)

    for key, value in dict.items():
        print("KEY: ", key)
        clip = VideoFileClip(value)
        # text_clip = TextClip(key, fontsize = 60, color = 'red')
        # text_clip = text_clip.set_position('bottom')
        #
        # clip = CompositeVideoClip([clip, text_clip])
        listClips.append(clip)

    path = "C:\\Users\\rlazz\\Documents\\GitHub\\project-audibleon\\website\\static\\testing.mp4"

    if os.path.exists(path):
        print("deleting!")
        os.remove(path)

    final_clip = concatenate_videoclips(listClips)
    final_clip.write_videofile(path)

    return path