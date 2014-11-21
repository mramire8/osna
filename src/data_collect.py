import ConfigParser
import sys
import time
import json
from TwitterAPI import TwitterAPI

USER_DB = "../../data/social_honeypot_icwsm_2011/"
USERS_GOOD = "legitimate_users.txt"
USERS_BOTS = "content_polluters.txt"


def get_twitter(config_file):
    """ Read the config_file and construct an instance of TwitterAPI.
    Args:
      config_file ... A config file in ConfigParser format with Twitter credentials
    Returns:
      An instance of TwitterAPI.
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    twitter = TwitterAPI(
        config.get('twitter', 'consumer_key'),
        config.get('twitter', 'consumer_secret'),
        config.get('twitter', 'access_token'),
        config.get('twitter', 'access_token_secret'))
    return twitter


twitter = get_twitter('../../twitter.cfg')
print 'Established Twitter connection.'


def read_file_names(filename):
    """ Read a list of usernames for U.S. senators.
    Args:
      filename: The name of the text file containing one senator username per file.
    Returns:
      A list of usernames
    """
    # Complete this method.
    f = open(filename)
    users = f.read().splitlines()
    users = [u.strip().split()[0] for u in users]
    return users


def read_users():
    good = read_file_names(USER_DB + USERS_GOOD)
    bots = read_file_names(USER_DB + USERS_BOTS)
    return good, bots


good, bots = read_users()
print 'Read', len(good), 'good. \nRead', len(bots), "bots."


def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request.
      params ..... A parameter dictionary for the request.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
<<<<<<< HEAD
        elif request.status_code == 404 or request.status_code == 34 or "Not authorized" in request.text:
=======
        elif request.status_code == 404 or request.status_code == 34:
>>>>>>> 71e2a44cf6520b04c570ae543f10f5891449b578
            return None
        else:
            print >> sys.stderr, 'Got error:', request.text, '\nsleeping for 15 minutes.'
            sys.stderr.flush()
            time.sleep(60 * 15)


def get_user_timeline(user_id, twitter):
    """ Return Twitter screen names for all accounts followed by screen_name. Returns the first 200 users.
    See docs at: https://dev.twitter.com/docs/api/1.1/get/friends/list
    Args:
      user_id ... The query account.
      twitter ....... The TwitterAPI object.
    Returns:
      A list of Twitter screen names.
    """
    # get list of friends aka following accounts. 
    request = robust_request(twitter, 'statuses/user_timeline',
                             {'user_id': user_id, 'count': 200, 'contributor_details': True}, max_tries=5)


    timeline = []
    if validate_request(request):

        for r in request.get_iterator():
            if 'user' in r:
                timeline.append(r)
    return timeline


def validate_request(request):
    if request is None:
        return False
    elif 'errors' in request:
        return False
    else:
        return True


def get_all_timelines(list_users, twitter, output):
    file_output = open(output, "a")
<<<<<<< HEAD
    for i, user in enumerate(list_users):
        print "user", i
=======
    for user in list_users:
>>>>>>> 71e2a44cf6520b04c570ae543f10f5891449b578
        timeline = get_user_timeline(user, twitter)
        if len(timeline) > 0:
            strs = [json.dumps(timeline)]
            s = "[%s]" % ",\n".join(strs)
            file_output.write(s)
    file_output.close()

import random
random.seed(52234)
<<<<<<< HEAD
# good1k= random.sample(good, 1000)
# bots1k = random.sample(bots, 1000)
print "good ones\n"+"-"*40
# get_all_timelines(good[:1000], twitter, './good.json')
print "bad ones\n"+"-"*40
get_all_timelines(bots[:1000], twitter, './bots.json')
=======
good1k= random.sample(good, 1000)
bots1k = random.sample(bots, 1000)
get_all_timelines(good1k, twitter, './good.json')
get_all_timelines(bots1k, twitter, './bots.json')
>>>>>>> 71e2a44cf6520b04c570ae543f10f5891449b578
