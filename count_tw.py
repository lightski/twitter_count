#!/usr/bin/env python
"""
    autocount -> count_tw.py
    gets and interprets tw updates and such for a twitter account api
    called by main.py

-=-=-=-=-=-=-get_metrics overview-=-=-=-=-=-=-
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
write results to file
"""

import twitter # tw api. pip install twitter
from datetime import datetime, date, time, timedelta
import time

def get_metrics(api, file_name, account_name):
    '''
    '    params: 
    '     api          - active twitter connection api as defined by 'pydoc twitter.api'
    '     file_name    - name of file to save results to 
    '     account_name - @tw handle, for record keeping
    '''

    # to get an accurate tally we count back from present to first_day
    # first_day of experiment: 11/16/2014
    first_day = date(2014,11,16)

    # open file to save results
    try:
        save_file = open(file_name, mode='w')
        print "Saving results to " + file_name
        save_file.write("Twitter expiriment results.\n Gathered on " + str(date.today()) + "\n")
        save_file.write("@" + account_name + " on Twitter \n")
    except IOError:
        # quit because some later stuff requires a file to write to
        print "Error: cannot save " + file_name + " due to i/o error"
        print "Please correct the problem and try again."
        quit()
     
    users = api.GetFriends()
    for u in users:
        # so we know who we're dealing with
        id_string =  "\n\nuser id: " + str(u.id)
        print id_string
        save_file.write(id_string + "\nuser name: " + str(u.name) + "\n date \t\t csv word counts \t\t\t number of statuses\n")

        # set current_day to tomorrow, to solve accounts in different timezones who post from the future 
        #  that is, the future relative to this script's location
        current_day = date.today() + timedelta(days=1)
        # record first "current day". later, record this after changing days
        save_file.write(" " + str(current_day) + "  ") 

        first_run = True
        # keep track of final tweet each day so we can get the ones older than that
        last_id = 0
        # metrics
        daily_total = 0

        # go backwards in time from latest tweets to earliest
        while(current_day >= first_day):
 
            # get wait time and kick back for a bit
            print "resting so we don't exhaust twitter..."
            time.sleep(api.GetAverageSleepTime("/statuses/home_timeline"))

            # we don't know where to start for first call, so just get the most recent 200 tweets
            if first_run:
                statuses = api.GetUserTimeline(u.id, count = 200)
                first_run = False
            else:
                # get tweets older than last_id, the last tweet we examined last run
                statuses = api.GetUserTimeline(user_id = u.id, max_id = last_id, count = 200) 

            for s in statuses:
                # record id as though it's your last (solves rare >200 tweets/day bug)
                last_id = s.id 
                # status time format: dow m dom t tz y
                # substring removes the timezone, +0000, because %z wouldn't cooperate
                #print "  Now substringing: " + s.created_at
                substr1 = s.created_at[0:20]
                substr2 = s.created_at[25:]
                creation_str = substr1 + substr2
                # create date based on modified time string
                creation_time = datetime.strptime(creation_str,"%a %b %d %H:%M:%S %Y")

                #print "  now comparing: " + str(creation_time) + " to " + str(current_day)
                # if tweet happened on day we're looking for, record metrics
                if creation_time.date() == current_day:
                    daily_total += 1
                    #  word count calculations based on splitting update text by space and getting length of resulting list
                    save_file.write(str(len(s.GetText().split())) + ",")
                # otherwise, it's time to move on
                else:
                    # print metrics and write them to file
                    print " counted: " + str(daily_total) + " statuses on " + str(current_day)
                    save_file.write("\t total statuses: " + str(daily_total))

                    # goto the next day, end if this is the first day
                    current_day = creation_time.date() 
                    if current_day < first_day:
                        break

                    daily_total = 1
                    # record current day
                    save_file.write("\n " + str(current_day) + "\t\t") 
                    # record current status word count
                    save_file.write(str(len(s.GetText().split())) + ",")

    save_file.write("\n\nEnd of results")
    save_file.close()
# end of function def

