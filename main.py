#!/usr/bin/env python
"""
    autocount -> main.py
    runs get_metrics on several twitter accounts
    set credentials in user_logins.py
"""

from user_logins import logins
from count_tw import get_metrics 
import twitter # tw api. pip install twitter

for creds in logins:
    handle = creds[0]
    api = twitter.Api(creds[1], creds[2], creds[3], creds[4])
    out_file = creds[5]
    get_metrics(api, out_file, handle)

