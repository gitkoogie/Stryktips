import pandas as pd
import numpy as np
import datetime as dt
import timeit
import matplotlib.pyplot as plt
from numpy.random import choice

# Functions
# Function for generating stryktips
def generate_tips(numbr_stryktips, p = [0.33, 0.33, 0.33], games_per_tip = 13):
    # Initial parameters for tip generating
    choices = [0, 1, 2]
    result = np.array([0, 0, 0])
    gen_tips = []
    #print("Generating %d tips based on the probabilities [1 X 2] = [%.2f, %.2f, %.2f]" % (numbr_stryktips, p[0], p[1], p[2]))
    for i in range(numbr_stryktips):
        draw = choice(choices, games_per_tip, p)
        list = convert_result(draw)
        gen_tips.append(list)

    return gen_tips

# Converting result
def convert_result(draw):
    tip_list = []
    for i in range(len(draw)):
        if draw[i] == 0:
            tip_list.append("1")
        elif draw[i] == 1:
            tip_list.append("X")
        else:
            tip_list.append("2")
    return tip_list
# Check if profit
def check_profit(num_corr, df):
    profit = -1

    if num_corr == 13:
        return df.loc["utd13"]
    elif num_corr == 12:
        return df.loc["utd12"]
    elif num_corr == 11:
        return df.loc["utd11"]
    elif num_corr == 10:
        return df.loc["utd10"]
    else:
        return profit

# Check row result
def check_row(gen, corr):
    num_correct = 0
    for i in range(len(gen)):
        if gen[i] == corr[i]:
            num_correct = num_correct + 1
    return num_correct

# Convert time to datetime object
def convert_time(newTime):
    if len(newTime) == 6:
        return dt.date(int(newTime[0:4]), int(newTime[4]), int(newTime[5]))
    elif len(newTime) == 7:
        if newTime[4:5] > 12:
            return dt.date(int(newTime[0:4]), int(newTime[4]), int(newTime[5:7]))
        else:
            return dt.date(int(newTime[0:4]), int(newTime[4:6]), int(newTime[6]))
    else:
        return dt.date(int(newTime[0:4]), int(newTime[4:6]), int(newTime[6:8]))

# Check result of tipping
def check_result(gen_tips, df, time_setting = False):
    # Initialize account balance
    balance = []
    balance.append(0)
    # Initialize time list
    time = []
    # Initialize list for number of correct answers
    nmbr_correct = [0] * 14

    if time_setting == True:
        newTime = str(df.loc[df.shape[0] - 1, "omg"])
        date = convert_time(newTime)
        time.append(date)
    else:
        time.append(0)

    for i in range(1, len(gen_tips)):
        result = df.loc[df.shape[0] - i, "correctRow"]
        # Check number of correct rows
        num_correct = check_row(gen_tips[i - 1], result)
        # Add one to number of correct rows
        nmbr_correct[num_correct] = nmbr_correct[num_correct] + 1
        # Check profit
        profit = check_profit(num_correct, df.loc[df.shape[0] - i])

        # Set new balance and time
        newBal = balance[i - 1] + profit
        balance.append(newBal)
        if time_setting == True:
            newTime = str(df.loc[df.shape[0] - i, "omg"])
            date = convert_time(newTime)
            time.append(date)
        else:
            time.append(i)

    return balance, time, nmbr_correct

# Check result of tipping
def check_result_new(gen_tips, df, round, balance = [], time = [], nmbr_correct = [], time_setting = False):

    # Initialize list for number of correct answers
    result = []
    # Initialize account balance
    if len(balance) == 0:
        balance.append(0)

    # Initialize time list
    if len(time) == 0:
        if time_setting == True:
            newTime = str(df.loc[df.shape[0] - 1, "omg"])
            date = convert_time(newTime)
            time.append(date)
        else:
            time.append(0)

    # get correct row
    for i in range(df.shape[0] - 1, -1, -1):
        if df.loc[i].loc["omg"] == round:
            result = df.loc[i].loc["correctRow"]
            break

    # Check number of correct rows
    num_correct = check_row(gen_tips[0], result)
    # Add num_correct to list nmbr_correct
    nmbr_correct.append(num_correct)
    # Check profit
    profit = check_profit(num_correct, df.loc[df.shape[0] - i])

    # Set new balance and time
    newBal = balance[len(balance) - 1] + profit
    balance.append(newBal)
    if time_setting == True:
        newTime = str(df.loc[df.shape[0] - i, "omg"])
        date = convert_time(newTime)
        time.append(date)
    else:
            time.append(len(balance) - 1)

    return balance, time, nmbr_correct

# Check team performance from last year
# HOW?
# Check if stryktips or europatips
# if stryktips check date
# check for each pair which team performed better last year
# if difference in placement last year is +10 spots return winner directly
# return date
def check_team_performance(hisTable, teamData):
    print("hello")
