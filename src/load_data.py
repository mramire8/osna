__author__ = 'maru'

TWEET_HOME = '../../data/tweeter'
from sklearn.feature_extraction.text import TfidfVectorizer

def load_twitter_corpus(path):
    pass


def create_corpus(path, split=.5, vct=TfidfVectorizer(), seed=454545):
    import json
    import os
    import ast
    file_names = ['good.json','bots.json']

    labels = ['good', 'bot']
    for f in file_names:
        file_data = open(path + "/" + f)
        for line in file_data:
            user = line.split("]][[")
 
            good = []
            for i,tweets in enumerate(user):

                if i == 0:
                    t = json.loads(tweets[1:] + "]")
                elif i == (last-1):
                    t = json.loads("["+tweets[:-1])
                else:
                    t = json.loads("["+tweets+"]")
                good.append(t)
                print "User %s, tweets %s" % (i, len(t))


def load_tweeter_data():
    pass


def extract_user_timeline(user_object):
    pass

def main():
    create_corpus(TWEET_HOME)


## MAIN FUNCTION
if __name__ == '__main__':
    main()


