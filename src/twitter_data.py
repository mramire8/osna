
import json
import pickle    

data_path = 'C:/Users/mramire8/Documents/Datasets/twitter'
data_path = '../../data/twitter'


def get_tweets_file(path):
    f = open(path)

    i = 0
    users = []
    for line in f:
        data = line.split("]][[")
        last = len(data)

    for i,tweets in enumerate(data):
            if i == 0:
                t = json.loads(tweets[1:] + "]")
            elif i == (last-1):
                t = json.loads("["+tweets[:-1])
            else:
                t = json.loads("["+tweets+"]")
            users.append(t)

    return users

good = get_tweets_file(data_path + "/good.json")
print "Real users %s" % (len(good))
     
bots = get_tweets_file(data_path + "/bots.json")
print "Bot users %s" % (len(bots))


from collections import Counter

bts = Counter()

for i,tweets in enumerate(bots):
    bts.update([len(tweets)])

import numpy as np
print bts.most_common(4)

print sum(bts)
print sum(bts.values())
print 1. * np.multiply(np.array(bts.values()),np.array(bts.keys())).sum() / sum(bts)

print np.array(bts.keys()) 



