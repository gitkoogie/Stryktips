import numpy as np
from numpy.random import choice

# Functions
def check_result(draw, result):
    for i in range(len(draw)):
        if draw[i] == 0:
            result[0] = result[0] + 1
        elif draw[i] == 1:
            result[1] = result[1] + 1
        else:
            result[2] = result[2] + 1
    return result

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

# data to base tipping on
stat = np.array([1585, 864, 1087])
# Create probability distribution
s = np.sum(stat)
prob_distr = [stat[0]/s, stat[1]/s, stat[2]/s]

print("These are the probabilites based on STRYKTIPSET data 2015-2020")
print("1) %.2f%% || X) %.2f%% || 2) %.2f%%" % (prob_distr[0]*100, prob_distr[1]*100, prob_distr[2]*100))
print(" ")


# initial parameters
choices = [0, 1, 2]
num_of_tips = 13
result = np.array([0, 0, 0])
numbr_stryktips = 4160

for i in range(1, numbr_stryktips):
    draw = choice(choices, num_of_tips, p=prob_distr)
    result = check_result(draw, result)
s_new = np.sum(result)
prob_distr_new = [result[0]*100/s_new, result[1]*100/s_new, result[2]*100/s_new]

print("|--------------------------------------------------|")
print("| Total number of occurences and probabilities     |" )
print("| after simulating %d stryktips                  |" % numbr_stryktips)
print("|--------------------------------------------------|")
print("| 1) %d                    Probability: %.2f%%  |" % (result[0], prob_distr_new[0]))
print("| X) %d                    Probability: %.2f%%  |" % (result[1], prob_distr_new[1]))
print("| 2) %d                    Probability: %.2f%%  |" % (result[2], prob_distr_new[2]))
print("|--------------------------------------------------|")

nmbrTips = input("Input the number of tips to generate: ")

print("Here are your tips:")
for i in range(int(nmbrTips)):
    draw = choice(choices, num_of_tips, p=prob_distr)
    draw = convert_result(draw)
    print("Tip number %d:" % int(i+1))
    for j in range(len(draw)):
        print("Game %d: %s" % (j+1, draw[j]))
