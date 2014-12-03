#!/usr/bin/env python
"""
    autocount -> tw_count.py
    gets and interprets tw updates and such for rightwingiit
    requires login credentials from rw_logins.py
"""
"""
-=-=-=-=-=-=-program overview-=-=-=-=-=-=-
for every "friend" this account has
    for currrent_day in dates (of the experiment)
        fetch 200 updates starting with current_tweet
        for each tweet
            if falls within current_day range (=current_date+24h)
                daily_total++
                word_count_get & save
                sort_by_content & save
            else
                record daily_total
                set new start tweet to current_tweet's id
                break out of loop
write results to file??
"""

import rw_logins
# tw api. pip install twitter
import twitter
from datetime import datetime,date,time,timedelta
import time

api = twitter.Api(rw_logins.tw_consumer_key,
                  rw_logins.tw_consumer_secret,
                  rw_logins.tw_access_token_key,
                  rw_logins.tw_access_token_secret)

# test if working & get useful info
# print api.VerifyCredentials()

users = api.GetFriends()
# get wait time and kick back for a bit
print "resting so we don't exhaust twitter..."
time.sleep(api.GetAverageSleepTime("/statuses/home_timeline"))

for u in users:
    # so we know who we're dealing with
    print "user id: " + str(u.id) + "\n"

    # first_day is first date of expiriment 11/16/2014
    # we'll be counting back from present to first_day, so this might be a little confusing
    first_day = date(2014,11,16)
    last_day = date.today()
    current_day = last_day

    # metrics
    daily_total = 0
    # keep track of final tweet each day so we can get the ones older than that
    last_id = 0

    # we don't know where to start for first call, so just get the most recent 200 tweets
    statuses = api.GetUserTimeline(u.id)
    for s in statuses:
        # status time format: dow m dom t tz y
        # substring removes the timezone, +0000, because %z wouldn't cooperate
        substr1 = s.created_at[0:20]
        substr2 = s.created_at[25:]
        creation_str = substr1 + substr2
        # create date based on modified time string
        creation_time = datetime.strptime(creation_str,"%a %b %d %H:%M:%S %Y")
       
       # if tweet happened on day we're looking for, record metrics
        if creation_time.date() == current_day:
            # get info
            daily_total+= 1
        # otherwise, it's time to move on
        else:
            # record last id and jump to next 
            last_id = s.id
            break

    # print metrics and go back one day
    print " counted: " + str(daily_total) + " statuses day " + str(current_day)
    current_day -= timedelta(days=1)

    # go backwards in time from latest tweets to earliest
    while(current_day != first_day):

        # waiting so we don't get limited
        print "resting so we don't exhaust twitter..."
        time.sleep(api.GetAverageSleepTime("/statuses/home_timeline"))

        # get tweets older than last_id
        statuses = api.GetUserTimeline(user_id = u.id, max_id = last_id) 
        # reset metrics so we get fresh numbers
        daily_total = 0

        for s in statuses:
            # do the substring dance again
            substr1 = s.created_at[0:20]
            substr2 = s.created_at[25:]
            creation_str = substr1 + substr2
            creation_time = datetime.strptime(creation_str,"%a %b %d %H:%M:%S %Y")
        
            if creation_time.date() == current_day:
                # get info
                daily_total += 1
            else:
                # record last id and jump to next 
                last_id = s.id
                break

        print " counted: " + str(daily_total) + " statuses day " + str(current_day)
        current_day -= timedelta(days=1)

    print "next user\n"
