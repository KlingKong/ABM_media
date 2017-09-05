import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cPickle as pickle

# load baseline model parts
print "loading baseline model parts"
with open('m0_round0Opinions.pkl', 'rb') as input:
    m0_round0Opinions = pickle.load(input)
with open('m0_roundOpinions.pkl', 'rb') as input:
    m0_roundOpinions = pickle.load(input)
m0_roundOpinions_truncated = m0_roundOpinions[:6000]
with open('m0_roundOWNMEDIANS.pkl', 'rb') as input:
    m0_roundOWNMEDIANS = pickle.load(input)
m0_roundOWNMEDIANS_truncated = m0_roundOWNMEDIANS[:6000]
with open('m0_roundSILENCES.pkl', 'rb') as input:
    m0_roundSILENCES = pickle.load(input)
m0_roundSILENCES_truncated = m0_roundSILENCES[:6000]
with open('m0_roundTRADEOFFS.pkl', 'rb') as input:
    m0_roundTRADEOFFS = pickle.load(input)
m0_roundTRADEOFFS_truncated = m0_roundTRADEOFFS[:6000]

print "loading model 1 parts"
with open('m1_round0Opinions.pkl', 'rb') as input:
    m1_round0Opinions = pickle.load(input)
with open('m1_roundOpinions.pkl', 'rb') as input:
    m1_roundOpinions = pickle.load(input)
with open('m1_roundOWNMEDIANS.pkl', 'rb') as input:
    m1_roundOWNMEDIANS = pickle.load(input)
with open('m1_roundSILENCES.pkl', 'rb') as input:
    m1_roundSILENCES = pickle.load(input)
with open('m1_roundTRADEOFFS.pkl', 'rb') as input:
    m1_roundTRADEOFFS = pickle.load(input)


print "loading model 2 parts"
with open('m2_round0Opinions.pkl', 'rb') as input:
    m2_round0Opinions = pickle.load(input)
with open('m2_roundOpinions.pkl', 'rb') as input:
    m2_roundOpinions = pickle.load(input)
with open('m2_roundOWNMEDIANS.pkl', 'rb') as input:
    m2_roundOWNMEDIANS = pickle.load(input)
with open('m2_roundSILENCES.pkl', 'rb') as input:
    m2_roundSILENCES = pickle.load(input)
with open('m2_roundTRADEOFFS.pkl', 'rb') as input:
    m2_roundTRADEOFFS = pickle.load(input)


print "loading model 3a parts"
with open('m3a_round0Opinions.pkl', 'rb') as input:
    m3a_round0Opinions = pickle.load(input)
with open('m3a_roundOpinions.pkl', 'rb') as input:
    m3a_roundOpinions = pickle.load(input)
with open('m3a_roundOWNMEDIANS.pkl', 'rb') as input:
    m3a_roundOWNMEDIANS = pickle.load(input)
with open('m3a_roundSILENCES.pkl', 'rb') as input:
    m3a_roundSILENCES = pickle.load(input)
with open('m3a_roundTRADEOFFS.pkl', 'rb') as input:
    m3a_roundTRADEOFFS = pickle.load(input)


print "loading model 3b parts"
with open('m3b_round0Opinions.pkl', 'rb') as input:
    m3b_round0Opinions = pickle.load(input)
with open('m3b_roundOpinions.pkl', 'rb') as input:
    m3b_roundOpinions = pickle.load(input)
with open('m3b_roundOWNMEDIANS.pkl', 'rb') as input:
    m3b_roundOWNMEDIANS = pickle.load(input)
with open('m3b_roundSILENCES.pkl', 'rb') as input:
    m3b_roundSILENCES = pickle.load(input)
with open('m3b_roundTRADEOFFS.pkl', 'rb') as input:
    m3b_roundTRADEOFFS = pickle.load(input)


# Baseline Plot:
# First plot: Comparison between vocalized opinions and own opinion
line2 = plt.plot(m0_roundOpinions, color = "#b30000") # red
line4 = plt.plot((0, 9000), (np.mean(m0_round0Opinions), np.mean(m0_round0Opinions)), '#ff6666') # lightred
red_patch = mpatches.Patch(color='#b30000', label='Vocalized Opinions (M0)') # red
lightred_patch = mpatches.Patch(color='#ff6666', label='Average overall opinion (M0)') # lightred
plt.legend(handles=[ red_patch, lightred_patch])
plt.suptitle("Model 0: Average overall vocalized opinion")
plt.ylabel("Vocalized Opinion")
plt.xlabel("Round")
plt.show()
# Second Plot: Comparison for the type of vocalized opinions
line1_5 = plt.plot(m0_roundOWNMEDIANS, color = "#8080ff") # lightblue
line2_5 = plt.plot(m0_roundTRADEOFFS, color = "#5c0099") #violet
line3_5 = plt.plot(m0_roundSILENCES, color = "#ff6666") #lightred

lightblue_patch = mpatches.Patch(color='#8080ff', label='Vocalization of Own Median (M0)') # lightblue
lightred_patch = mpatches.Patch(color='#ff6666', label='Silenced (M0)') # lightred
violet_patch = mpatches.Patch(color='#5c0099', label='Vocalization of Trade-Off Opinion (M0)') # violet

plt.legend(handles=[lightblue_patch, lightred_patch, violet_patch])
plt.suptitle("Model 0: Types of vocalized opinions")
plt.ylabel("Frequency")
plt.xlabel("Round")
plt.show()

# MODEL 1
# First Plot: Comparison between vocalized opinions, own opinion and introduction of new media age
line1 = plt.plot(m1_roundOpinions, color = "#000080") # blue
line2 = plt.plot(m0_roundOpinions, color = "#b30000") # red
line3 = plt.plot((0, 9000), (np.mean(m1_round0Opinions), np.mean(m1_round0Opinions)), '#8080ff') # lightblue
line4 = plt.plot((0, 9000), (np.mean(m0_round0Opinions), np.mean(m1_round0Opinions)), '#ff6666') # lightred
line5 = plt.plot((3000, 3000), (0.505, 0.465), 'green') # green - new types of outlets

blue_patch = mpatches.Patch(color='#000080', label='Vocalized Opinions (M1)') # blue
red_patch = mpatches.Patch(color='#b30000', label='Vocalized Opinions (M0)') # red
lightred_patch = mpatches.Patch(color='#ff6666', label='Average overall opinion (M0 and M1)') # lightred
green_patch = mpatches.Patch(color='green', label='Introduction: New Media Outlets') # green - new types of outlets

plt.legend(handles=[blue_patch, red_patch, lightred_patch, green_patch])
plt.suptitle("Model 1: Average overall vocalized opinion")
plt.ylabel("Vocalized Opinion")
plt.xlabel("Round")
plt.show()

# Second Plot: Comparison for the type of vocalized opinions
line1 = plt.plot(m1_roundOWNMEDIANS, color = "#000080") # blue
line1_5 = plt.plot(m0_roundOWNMEDIANS, color = "#8080ff") # lightblue
line2 = plt.plot(m1_roundTRADEOFFS, color = "black") # black
line2_5 = plt.plot(m0_roundTRADEOFFS, color = "#5c0099") #violet
line3 = plt.plot(m1_roundSILENCES, color = "#b30000") # red
line3_5 = plt.plot(m0_roundSILENCES, color = "#ff6666") #lightred
line4 = plt.plot((3000, 3000), (0, 500), 'green') # green - new types of outlets

blue_patch = mpatches.Patch(color='#000080', label='Vocalization of Own Median (M1)') # blue
lightblue_patch = mpatches.Patch(color='#8080ff', label='Vocalization of Own Median (M0)') # lightblue
red_patch = mpatches.Patch(color='#b30000', label='Silenced (M1)') # red
lightred_patch = mpatches.Patch(color='#ff6666', label='Silenced (M0)') # lightred
black_patch = mpatches.Patch(color='black', label='Vocalization of Trade-Off Opinion (M1)') #black
violet_patch = mpatches.Patch(color='#5c0099', label='Vocalization of Trade-Off Opinion (M0)') # violet
green_patch = mpatches.Patch(color='green', label='Introduction: New Media Outlets')  # green - new types of outlets

plt.legend(handles=[blue_patch, lightblue_patch, red_patch, lightred_patch, black_patch, violet_patch, green_patch])
plt.suptitle("Model 1: Types of vocalized opinions")
plt.ylabel("Frequency")
plt.xlabel("Round")
plt.show()



## MODEL 2
# First Plot: Comparison between vocalized opinions, own opinion and introduction of new media age
line1 = plt.plot(m2_roundOpinions, color = "#000080") # blue
line2 = plt.plot(m0_roundOpinions, color = "#b30000") # red
line3 = plt.plot((0, 9000), (np.mean(m2_round0Opinions), np.mean(m2_round0Opinions)), '#8080ff') # lightblue
line4 = plt.plot((0, 9000), (np.mean(m0_round0Opinions), np.mean(m0_round0Opinions)), '#ff6666') # lightred
line5 = plt.plot((3000, 3000), (0.5005, 0.48), 'orange') # orange - recommender algorithms

blue_patch = mpatches.Patch(color='#000080', label='Vocalized Opinions (M2)') # blue
red_patch = mpatches.Patch(color='#b30000', label='Vocalized Opinions (M0)') # red
lightred_patch = mpatches.Patch(color='#ff6666', label='Average overall opinion (M0 and M2)') # lightred
orange_patch = mpatches.Patch(color='orange', label='Introduction: Recommender Algorithm') # orange - recommender alg

plt.legend(handles=[blue_patch, red_patch, lightred_patch, orange_patch])
plt.suptitle("Model 2: Average overall vocalized opinion")
plt.ylabel("Vocalized Opinion")
plt.xlabel("Round")
plt.show()

# Second Plot: Comparison for the type of vocalized opinions
line1 = plt.plot(m2_roundOWNMEDIANS, color = "#000080") # blue
line1_5 = plt.plot(m0_roundOWNMEDIANS, color = "#8080ff") # lightblue
line2 = plt.plot(m2_roundTRADEOFFS, color = "black") # black
line2_5 = plt.plot(m0_roundTRADEOFFS, color = "#5c0099") #violet
line3 = plt.plot(m2_roundSILENCES, color = "#b30000") # red
line3_5 = plt.plot(m0_roundSILENCES, color = "#ff6666") #lightred
line4 = plt.plot((3000, 3000), (0, 500), 'orange') # orange - recommender algo

blue_patch = mpatches.Patch(color='#000080', label='Vocalization of Own Median (M2)') # blue
lightblue_patch = mpatches.Patch(color='#8080ff', label='Vocalization of Own Median (M0)') # lightblue
red_patch = mpatches.Patch(color='#b30000', label='Silenced (M2)') # red
lightred_patch = mpatches.Patch(color='#ff6666', label='Silenced (M0)') # lightred
black_patch = mpatches.Patch(color='black', label='Vocalization of Trade-Off Opinion (M2)') #black
violet_patch = mpatches.Patch(color='#5c0099', label='Vocalization of Trade-Off Opinion (M0)') # violet
orange_patch = mpatches.Patch(color='orange', label='Introduction: Recommender Algorithm')  # orange - recommender algo

plt.legend(handles=[blue_patch, lightblue_patch, red_patch, lightred_patch, black_patch, violet_patch, orange_patch])
plt.suptitle("Model 2: Types of vocalized Opinions")
plt.ylabel("Frequency")
plt.xlabel("Round")
plt.show()


## MODEL 3a
# First Plot: Comparison between vocalized opinions, own opinion and introduction of new media age
line1 = plt.plot(m3a_roundOpinions, color = "#000080") # blue
line2 = plt.plot(m0_roundOpinions, color = "#b30000") # red
line3 = plt.plot((0, 9000), (np.mean(m3a_round0Opinions), np.mean(m3a_round0Opinions)), '#8080ff') # lightblue
line4 = plt.plot((0, 9000), (np.mean(m0_round0Opinions), np.mean(m0_round0Opinions)), '#ff6666') # lightred
line5 = plt.plot((3000, 3000), (0.505, 0.475), 'green') # green - new media outlets
line6 = plt.plot((6000, 6000), (0.505, 0.475), 'orange') # orange - recommender algorithms

blue_patch = mpatches.Patch(color='#000080', label='Vocalized Opinions (M3a)') # blue
red_patch = mpatches.Patch(color='#b30000', label='Vocalized Opinions (M0)') # red
lightred_patch = mpatches.Patch(color='#ff6666', label='Average overall opinion (M0 and M3a)') # lightred
green_patch = mpatches.Patch(color='green', label='Introduction: New Media Outlets') # green - new media outlets
orange_patch = mpatches.Patch(color='orange', label='Introduction: Recommender Algorithm') # orange - recommender algo

plt.legend(handles=[blue_patch, red_patch, lightred_patch, green_patch, orange_patch])
plt.suptitle("Model 3a: Average overall vocalized opinion")
plt.ylabel("Vocalized Opinion")
plt.xlabel("Round")
plt.show()

# Second Plot: Comparison for the type of vocalized opinions
line1 = plt.plot(m3a_roundOWNMEDIANS, color = "#000080") # blue
line1_5 = plt.plot(m0_roundOWNMEDIANS, color = "#8080ff") # lightblue
line2 = plt.plot(m3a_roundTRADEOFFS, color = "black") # black
line2_5 = plt.plot(m0_roundTRADEOFFS, color = "#5c0099") #violet
line3 = plt.plot(m3a_roundSILENCES, color = "#b30000") # red
line3_5 = plt.plot(m0_roundSILENCES, color = "#ff6666") #lightred
line4 = plt.plot((3000, 3000), (0, 500), 'green') # green - new media outlets
line5 = plt.plot((6000, 6000), (0, 500), 'orange') # orange - recommender algo

blue_patch = mpatches.Patch(color='#000080', label='Vocalization of Own Median (M3a)') # blue
lightblue_patch = mpatches.Patch(color='#8080ff', label='Vocalization of Own Median (M0)') # lightblue
red_patch = mpatches.Patch(color='#b30000', label='Silenced (M3a)') # red
lightred_patch = mpatches.Patch(color='#ff6666', label='Silenced (M0)') # lightred
black_patch = mpatches.Patch(color='black', label='Vocalization of Trade-Off Opinion (M3a)') #black
violet_patch = mpatches.Patch(color='#5c0099', label='Vocalization of Trade-Off Opinion (M0)') # violet
green_patch = mpatches.Patch(color='green', label='Introduction: New Media Outlets') # green - new media outlets
orange_patch = mpatches.Patch(color='orange', label='Introduction: Recommender Algorithm') # orange - recommender algo

plt.legend(handles=[blue_patch, lightblue_patch, red_patch, lightred_patch, black_patch, violet_patch, green_patch, orange_patch])
plt.suptitle("Model 3a: Types of vocalized opinions")
plt.ylabel("Frequency")
plt.xlabel("Round")
plt.show()


## MODEL 3b
# First Plot: Comparison between vocalized opinions, own opinion and introduction of new media age
line1 = plt.plot(m3b_roundOpinions, color = "#000080") # blue
line2 = plt.plot(m0_roundOpinions, color = "#b30000") # red
line3 = plt.plot((0, 9000), (np.mean(m3b_round0Opinions), np.mean(m3b_round0Opinions)), '#8080ff') # lightblue
line4 = plt.plot((0, 9000), (np.mean(m0_round0Opinions), np.mean(m0_round0Opinions)), '#ff6666') # lightred
line5 = plt.plot((3000, 3000), (0.505, 0.48), 'orange') # orange - recommender algorithms
line6 = plt.plot((6000, 6000), (0.505, 0.48), 'green') # green - new media outlets

blue_patch = mpatches.Patch(color='#000080', label='Vocalized Opinions (M3b)') # blue
red_patch = mpatches.Patch(color='#b30000', label='Vocalized Opinions (M0)') # red
lightred_patch = mpatches.Patch(color='#ff6666', label='Average overall opinion (M0 and M3b)') # lightred
orange_patch = mpatches.Patch(color='orange', label='Introduction: Recommender Algorithm') # orange - recommender algo
green_patch = mpatches.Patch(color='green', label='Introduction: New Media Outlets') # green - new media outlets


plt.legend(handles=[blue_patch, red_patch, lightred_patch, orange_patch, green_patch])
plt.suptitle("Model 3b: Average overall vocalized opinion")
plt.ylabel("Vocalized Opinion")
plt.xlabel("Round")
plt.show()

# Second Plot: Comparison for the type of vocalized opinions
line1 = plt.plot(m3b_roundOWNMEDIANS, color = "#000080") # blue
line1_5 = plt.plot(m0_roundOWNMEDIANS, color = "#8080ff") # lightblue
line2 = plt.plot(m3b_roundTRADEOFFS, color = "black") # black
line2_5 = plt.plot(m0_roundTRADEOFFS, color = "#5c0099") #violet
line3 = plt.plot(m3b_roundSILENCES, color = "#b30000") # red
line3_5 = plt.plot(m0_roundSILENCES, color = "#ff6666") #lightred
line4 = plt.plot((3000, 3000), (0, 500), 'orange') # orange - recommender algo
line5 = plt.plot((6000, 6000), (0, 500), 'green') # green - new media outlets

blue_patch = mpatches.Patch(color='#000080', label='Vocalization of Own Median (M3b)') # blue
lightblue_patch = mpatches.Patch(color='#8080ff', label='Vocalization of Own Median (M0)') # lightblue
red_patch = mpatches.Patch(color='#b30000', label='Silenced (M3b)') # red
lightred_patch = mpatches.Patch(color='#ff6666', label='Silenced (M0)') # lightred
black_patch = mpatches.Patch(color='black', label='Vocalization of Trade-Off Opinion (M3b)') #black
violet_patch = mpatches.Patch(color='#5c0099', label='Vocalization of Trade-Off Opinion (M0)') # violet
orange_patch = mpatches.Patch(color='orange', label='Introduction: Recommender Algorithm') # orange - recommender algo
green_patch = mpatches.Patch(color='green', label='Introduction: New Media Outlets') # green - new media outlets


plt.legend(handles=[blue_patch, lightblue_patch, red_patch, lightred_patch, black_patch, violet_patch, orange_patch, green_patch])
plt.suptitle("Model 3b: Types of vocalized opinions")
plt.ylabel("Frequency")
plt.xlabel("Round")
plt.show()