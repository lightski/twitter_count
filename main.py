#!/usr/bin/env python
"""
    autocount -> gp_count_tw.py
    runs get_metrics on several twitter accounts
    requires login credentials from *_logins.py
     and count_tw.py for get_metrics

    no, it's not parallel at all. but it now has the potential 
     to be, some day...
"""

import gp_logins, rw_logins, lw_logins
import count_tw
# tw api. pip install twitter
import twitter

# define logins and filename then get info for each account
# @greenearthiit
gp_api = twitter.Api(gp_logins.tw_consumer_key,
                     gp_logins.tw_consumer_secret,
                     gp_logins.tw_access_token_key,
                     gp_logins.tw_access_token_secret)
gp_file = "gp_results_tw.txt"
gp_handle = "greenearthiit"
count_tw.get_metrics(gp_api, gp_file, gp_handle)

# @leftwingiit
lw_api = twitter.Api(lw_logins.tw_consumer_key,
                     lw_logins.tw_consumer_secret,
                     lw_logins.tw_access_token_key,
                     lw_logins.tw_access_token_secret)
lw_file = "lw_results_tw.txt"
lw_handle = "leftwingiit"
count_tw.get_metrics(lw_api, lw_file)

# @rightwingiit
rw_api = twitter.Api(rw_logins.tw_consumer_key,
                     rw_logins.tw_consumer_secret,
                     rw_logins.tw_access_token_key,
                     rw_logins.tw_access_token_secret)
rw_file = "rw_results_tw.txt"
rw_handle = "rightwingiit"
count_tw.get_metrics(rw_api, rw_file, rw_handle)

# test if working & get useful info
# print api.VerifyCredentials()

