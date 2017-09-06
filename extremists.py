import cPickle as pickle
import pandas as pd
import csv


def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

# print "Loading Interactions M1"
# with open('interactions_m1.pkl', 'rb') as input:
#     interactions_m1 = pickle.load(input)
with open("statuses_m1.pkl", "rb") as input:
    statuses_m1 = pickle.load(input)
for entry in statuses_m1:
    if entry[1] in entry[3]:
        print entry
# print "Loading Interactions M2"
# with open('interactions_m2.pkl', 'rb') as input:
#     interactions_m2 = pickle.load(input)
print "Loading Round 0 Opinions (of M0)"
with open('m0_round0Opinions.pkl', 'rb') as input:
    m0_round0Opinions = pickle.load(input)
df = pd.Series(m0_round0Opinions, index = range(len(m0_round0Opinions)))
df_sorted = df.sort_values()
extremistIds_low = df_sorted[:50].index
extremistIds_high = df_sorted[-50:].index


# Analysis of extremists with low opinion
# print df[:50]
# print df[-50:]
lowdict = {}
highdict = {}
# Initializing
for identifier in extremistIds_low:
    lowdict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions
for identifier in extremistIds_high:
    highdict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions

for entry in interactions_m1:
    if ((entry[1] in extremistIds_low) and (entry[4] != "Media")):# and (entry[0] % 100 == 0)):
        #print entry
        lowdict["agent"+str(entry[1])][1].append(entry[3])
    if ((entry[1] in extremistIds_high) and (entry[4] != "Media")):# and (entry[0] % 100 == 0)):
        highdict["agent"+str(entry[1])][1].append(entry[3])

# Saving object:
w = csv.writer(open("extremists_low.csv", "w"))
roundLabels = []
headerrow = ["id", "medianOpinion"]
for i in range(0, 9001, 1):
    headerrow.append("round"+str(i)+"VocOp")
w.writerow(headerrow)
print len(headerrow)
for identifier in extremistIds_low:
    list = [identifier, lowdict["agent"+str(identifier)][0]]
    for item in lowdict["agent"+str(identifier)][1]:
        list.append(item)
    print len(list)
    w.writerow(list)


# # Saving object:
# w = csv.writer(open("extremists_high.csv", "w"))
# roundLabels = []
# for i in range(len(interactions_m1)):
#     roundLabels.append("round"+str(i+1)+"VocOp")
# w.writerow(headerrow)
# for identifier in extremistIds_high:
#     w.writerow([identifier, lowdict["agent"+str(identifier)][0], lowdict["agent"+str(identifier)][1]])
