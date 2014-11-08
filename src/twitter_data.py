
import json

data_path = 'C:/Users/mramire8/Documents/Datasets/twitter'

f = open(data_path + "/good.json")

i = 0
tot = 0
for line in f:
    user = line.split("]][[")
    print user[0]
    last = len(user)
    print "Total %s users" % last
 

good = []
for i,tweets in enumerate(user):
#         if i == 165:
#             print tweets[544928-5:544928+5]
        if i == 0:
            t = json.loads(tweets[1:] + "]")
        elif i == (last-1):
            t = json.loads("["+tweets[:-1])
        else:
            t = json.loads("["+tweets+"]")
        good.append(t)
        print "User %s, tweets %s" % (i, len(t))

import pickle    

# <codecell>

f2 = open(data_path + "/bots.json")
for line2 in f2:
    bots = line2.split("]][[")
#     print bots[0]
    last = len(bots)

print "Total %s users" % last
 

# <codecell>

from collections import Counter

bts = Counter()
for i,tweets in enumerate(bots):
    if i == 0:
        t = json.loads(tweets[1:] + "]")
    elif i == (last-1):
        t = json.loads("["+tweets[:-1])
    else:
        t = json.loads("["+tweets+"]")
    bts.update([len(t)])

# <codecell>

import numpy as np
print bts.most_common(4)

print sum(bts)
print sum(bts.values())
print 1. * np.multiply(np.array(bts.values()),np.array(bts.keys())).sum() / sum(bts)

print np.array(bts.keys()) 

# <codecell>


