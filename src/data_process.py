
# coding: utf-8

# In[1]:

import json

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


# In[2]:

print "\n".join(sorted(good[0][0].keys()))
    


# In[3]:

print "\n".join(sorted(good[0][0]['user'].keys()))


# In[4]:

import datetime
from collections import Counter

def get_date(date_str):
    return datetime.datetime.strptime(date_str.strip('"'), "%a %b %d %H:%M:%S +0000 %Y")

# datetime.strptime((r.json()[x]["created_at"]).strip('"'), "%a %b %d %H:%M:%S +0000 %Y")
def count_dates(users):
    dates = Counter()
    min_dt = get_date(users[0][0]['created_at'])
    for user in users:
        d = get_date(user[0]['created_at'])
        min_dt = min(min_dt, d)
        dates.update([d])
    return dates, min_dt

good_counts, min_good = count_dates(good)
print "Most common: %s" % good_counts.most_common(3)
print "Latest: %s" % min_good
        
bots_counts, min_bots = count_dates(bots)
print "Most common: %s" % bots_counts.most_common(3)
print "Latest: %s" % min_bots

    


# In[5]:

## Number of users that have old tweets in good users
## with tweets not in 2014
print "Old good users %s" %  len([d for d in good_counts.keys() if d.year < 2014])
print "Old bot users %s" %  len([d for d in bots_counts.keys() if d.year < 2014])


# In[8]:

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import matplotlib as mpl 

mpl.style.use('fivethirtyeight')

years    = mdates.YearLocator()   # every year
months   = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')
monthsFmt = mdates.DateFormatter('%Y-%m')
fig = plt.figure()
ax = plt.axes()

gds =[(d,c) for d,c in good_counts.iteritems() if d.year > 2013]
bts =[(d,c) for d,c in bots_counts.iteritems() if d.year > 2013]


kg = [d.toordinal() for d,_ in gds]
kb = [d.toordinal() for d,_ in bts]
wg = [c for _,c in gds]
wb = [c for _,c in bts]
plt.hist([kg,kb], weights=[wg,wb], bins=20, stacked=False, alpha=.7, label=['real', 'bots'])

ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
# ax.xaxis.set_minor_locator(months)
plt.legend(loc='best', frameon=False, numpoints=1)
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
# minx, maxx = min(np.min(kg), np.min(kb)), max(np.max(kg), np.max(kb))
fig.autofmt_xdate()
# labels = range(minx, maxx, (maxx-minx)/20)
# labels = [datetime.date.fromordinal(d).isoformat() for d in labels]
# print labels
# plt.xticks(labels)


# In[9]:

## convert the tweet into a data format of text documents
from sklearn.datasets.base import Bunch
def timeline_to_doc(user):
    tweets = []
    for tw in user:
        tweets.append(tw['text'])
    return tweets

def user_to_doc(users):
    timeline = []
    user_names = []
    user_id = []
    
    for user in users:
        timeline.append(timeline_to_doc(user))
        user_names.append(user[0]['user']['name'])
        user_id.append(user[0]['user']['screen_name'])
    return user_id, user_names, timeline

def bunch_users(class1, class2, labels=None):
    
    if labels is None:
        labels = [0,1]

    user_id, user_names, timeline = user_to_doc(good)
    user_id2, user_names2, timeline2 = user_to_doc(bots)
    target = [labels[0]] * len(user_id)
    user_id.append(user_id2)
    user_names.append(user_names2)
    timeline.append(timeline2)
    target.append([labels[1]]* len(user_id2))
    user_text = [" ".join(t) for  t in timeline]

    data = Bunch(data=timeline, target=target, user_id=user_id, user_name=user_names, user_text=user_text)
    return data

data = bunch_users(good, bots)

from sklearn.learning_curve import learning_curve
from sklearn import linear_model
from sklearn.naive_bayes import MultinomialNB
from experiment.experiment_utils import split_data_sentences
from datautil.load_data import *
import sklearn.metrics as metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import brewer2mpl
from sklearn.cross_validation import StratifiedKFold, cross_val_score, KFold, ShuffleSplit
from collections import itertools

def learning_curve_tweet(data):

    vct = TfidfVectorizer(encoding='latin1', min_df=5, max_df=1.0, binary=False, ngram_range=(1, 1),
                          token_pattern='\\b\\w+\\b')  #, tokenizer=StemTokenizer())

    data['bow'] = vct.fit_transform(data['user_text'])

    col = brewer2mpl.get_map('Set1', 'qualitative', 7).mpl_colors
    colors_n = itertools.cycle(col)

    random_state = np.random.RandomState(5612)        
    
    kcv = KFold(len(data['target']), n_folds=5, random_state=random_state,shuffle=True)

    classifier = 'lr'
    if classifier == "mnb":
        clf = MultinomialNB(alpha=1)
    else:
        clf = linear_model.LogisticRegression(penalty='l1', C=1)

    scoring_fn = 'accuracy'
    print("Classifier name:", clf.__class__.__name__, "C=", clf.C)
    print("CV data:", data['bow'])
    train_sizes, train_scores, test_scores = learning_curve(
        clf, data['bow'], data['target'], train_sizes=sizes, cv=kcv, scoring=scoring_fn, n_jobs=20)
    
    current_color = colors_n.next()

    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = 1.0 * np.std(test_scores, axis=1) / np.sqrt(5.0)

    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color=current_color)
    plt.plot(train_sizes, test_scores_mean, 'o-', mfc='white', linewidth=2, mew=2, markersize=10, mec=current_color, color=current_color,
             # label="Cross-validation score")
             label="C={}".format(clf.C))

    print ("-"*40)
    print ("\nCOST\tMEAN\tSTDEV")
    print ("\n".join(["{0}\t{1:.3f}\t{2:.4f}".format(c,m,s) for c,m,s in zip(train_sizes, test_scores_mean, test_scores_std)]))
    plt.legend(loc="best")
    # plt.savefig('lr-{0}.png'.format(vct.__class__.__name__), bbox_inches="tight", dpi=200, transparent=True)
    plt.savefig('lradapt-sent-sent.png', bbox_inches="tight", dpi=200, transparent=True)
    plt.show()

learning_curve_tweet(data)

