import pandas as pd
import numpy as np
import datetime as dt
import timeit
import matplotlib.pyplot as plt
from numpy.random import choice
from stryk_functions import *

# Function that grabs the teams for week / round specified
def get_teams(df, round):
    home_teams = []
    away_teams = []
    for i in range(teamData.shape[0] - 1, -1, -1):
        if teamData.loc[i].loc["omg"] == round:
            home_teams.append(teamData.loc[i].loc["hemmalag"])
            away_teams.append(teamData.loc[i].loc["bortalag"])
    return home_teams, away_teams

# Function for checking teams and modifying tips
def modify_tips(gen_tips, hisTable, round, home_teams, away_teams):
    # get round and reduce to last year
    round = str(round)
    r = str(int(round[0:4]) - 1)
    # loop through all teams in round
    for i in range(13):
        # loop through all teams in table
        for j in range(hisTable.shape[0] - 1):
            # check if home team occured in table
            if home_teams[i] == hisTable.loc[j].loc["Team"]:
                # get home team placement last year
                home_team_place_last_year = hisTable.loc[j].loc[r]
                # loop through all teams in table
                for k in range(hisTable.shape[0] - 1):
                    # check if away team occured in table
                    if away_teams[i] == hisTable.loc[k].loc["Team"]:
                        # get away team placement last year
                        away_team_place_last_year = hisTable.loc[k].loc[r]
                        # check if home team and away team had a placement last year
                        if away_team_place_last_year > 0 and home_team_place_last_year > 0:
                            # if home team placed 7 places higher than away last year => win
                            if home_team_place_last_year < away_team_place_last_year - 7:
                                print("MODIFIED!")
                                print("Setting hometeam %s as winner vs awayteam %s" %
                                (str(home_teams[i]), str(away_teams[i])))
                                gen_tips[0][i] = "1"
                            # if away team placed 7 places higher than home last year => win
                            elif away_team_place_last_year < home_team_place_last_year - 7:
                                print("MODIFIED!")
                                print("Setting awayteam %s as winner vs hometeam %s" %
                                (str(away_teams[i]), str(home_teams[i])))
                                gen_tips[0][i] = "2"

    return gen_tips

# imports
teamData = pd.read_csv('./data/teamDataStryktips.csv')
profit = pd.read_csv('./data/onlystryktips.csv')
hisTable = pd.read_csv('./data/HistoricTable9919.csv')


# setup
# Probability data to base tipping of
stat = np.array([1585, 864, 1087])
# Create probability distribution
s = np.sum(stat)
prob_distr = [stat[0]/s, stat[1]/s, stat[2]/s]

# main program
# num people
num_ppl = 5
# initialize
balance = []
time = []
nmbr_correct = []
# Start timer
start = timeit.default_timer()
# run
for j in range(num_ppl):
    for i in range(1, profit.shape[0]): #, profit.shape[0]):
        # Get current round
        round = profit.loc[profit.shape[0] - i].loc["omg"]

        # Get home teams and away teams for round
        home_teams, away_teams = get_teams(teamData, round)

        # Generate tips
        gen_tips = generate_tips(1, prob_distr)

        # Modify tips based on team historic table
        gen_tips = modify_tips(gen_tips, hisTable, round, home_teams, away_teams)

        # Check tips result
        balance, time, nmbr_correct = check_result_new(gen_tips, profit, round, balance, time, nmbr_correct)

        # Compute elapsed time
        run = timeit.default_timer()
        t = run - start
        print("Current runtime: %.2f s" % t)
        #print("Current round: ", round)
        #print("Balance: ", balance[len(balance) - 1])
        #print("Number correct: ", nmbr_correct)

    # Plot outcome
    fig, ax = plt.subplots(2)
    ax[0].hist(nmbr_correct, density = True, bins = 14)
    ax[0].set(xlabel = "Number of correct rows in tip", ylabel = "Number of time occured")

    ax[1].plot(time, balance)
    ax[1].set(xlabel = "iteration", ylabel = "Account Balance (SEK)")

plt.show()

# TO DO
# REPLACE OLD CHECK RESULT WITH NEW
# DO NOT MAKE GEN TIPS MULTI DIMENSIONAL WHICH IT IS NOW
# TO PLOT HISTOGRAM CHANGE SO THAT NUM CORRECT ARE GIVEN IN A LIST WITH
# NUMBER OF CORRECT IN EACH ELEMENT








'''

# Import data to backtest on
df = pd.read_csv('./data/newData.csv')

# Probability data to base tipping of
stat = np.array([1585, 864, 1087])
# Create probability distribution
s = np.sum(stat)
prob_distr = [stat[0]/s, stat[1]/s, stat[2]/s]

# Print probabilites that generated data is based of
print("These are the probabilites based on STRYKTIPSET data 2015-2020")
print("1) %.2f%% || X) %.2f%% || 2) %.2f%%" %
(prob_distr[0]*100, prob_distr[1]*100, prob_distr[2]*100))
print(" ")

nmbr_ppl = 1
# For best probabilities
winners = 0
winners_balance = 0
losers = 0
losers_balance = 0
tot_nmbr_correct = [0] * 14



for i in range(nmbr_ppl):
    # FOR BEST PROBABILITY
    # Generate tips
    gen_tips = generate_tips(df.shape[0] - 1, prob_distr)

    # Check tips result
    balance, time, nmbr_correct = check_result(gen_tips, df)

    # Total number correct
    for i in range(len(nmbr_correct)-1):
        tot_nmbr_correct[i] = tot_nmbr_correct[i] + nmbr_correct[i]

    # Check balance
    if balance[len(balance)-1] > 0:
        winners = winners + 1
        winners_balance = winners_balance + balance[len(balance)-1]
    else:
        losers = losers + 1
        losers_balance = losers_balance + balance[len(balance)-1]

    # Print result
    plt.plot(time, balance)
    run = timeit.default_timer()
    t = run - start
    print("Current runtime: %.2f s" % t)


plt.title("Result after %d people betting 1kr at %d Stryktips and Europatips" %
(nmbr_ppl, int(df.shape[0])))
plt.xlabel("Iteration")
plt.ylabel("Account Balance")
plt.show()

# For best probs
if winners > 0:
    avg_win = winners_balance / winners
else:
    avg_win = 0
if losers > 0:
    avg_loss = losers_balance / losers
else:
    avg_loss = 0


print("Final Result for probability: [%.2f%%, %.2f%% ,%.2f%%]" %
(prob_distr[0] * 100, prob_distr[1] * 100, prob_distr[2] * 100))
print("Number of losers: %d" % losers)
print("Average loss: %.2f" % avg_loss)
print("-----------------------")
print("Number of winners: %d" % winners)
print("Average win: %.2f" % avg_win)
print("-----------------------")
print("Time each number of correct rows occured")
for i in range(len(tot_nmbr_correct)):
    print("Number of times %d correct occured: %d (%.4f%%)" %
    (i, tot_nmbr_correct[i], (tot_nmbr_correct[i]/(df.shape[0]*nmbr_ppl)) * 100))

stop = timeit.default_timer()
t = stop - start
print("Total runtime: %.2f s" % t)
'''
