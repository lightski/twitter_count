#!/usr/bin/env python
"""
    autocount -> tw_count.py
    gets and interprets tw updates and such for rightwingiit
    requires login credentials from rw_logins.py
"""

import rw_logins
# tw api. pip install twitter
import twitter

api = twitter.Api(rw_logins.tw_consumer_key,
                  rw_logins.tw_consumer_secret,
                  rw_logins.tw_access_token_key,
                  rw_logins.tw_access_token_secret)

# test if working & get useful info
# print api.VerifyCredentials()


#-=-=-=-=-=-=-program overview-=-=-=-=-=-=-
# current_tweet = tweet0, oldest tweet per expiriment's definition <--need to calculate this
# for every "friend" this account has
    # for currrent_day in dates (of the experiment)
        # fetch 200 updates starting with current_tweet
        # for each tweet
            # if falls within current_day range (=current_date+24h)
                # daily_total++
                # word_count_get & save
                # sort_by_content & save
            # else
                # record daily_total
                # set new start tweet to current_tweet's id
                # break out of loop
                   
"""
for u in users:
    statuses = api.GetUserTimeline(u.id)
    print [s.created_at for s in statuses]
"""

# first, calculate tweet0
# tweet0 is the final tweet of the last day prior to expiriment starting
# in this case, that's last tweet on 11/15/14

users = api.GetFriends()
# eg: print [u.screen_name for u in users]
statuses = api.GetUserTimeline(users[0].id) # --need to add options here to get more accurate in time


