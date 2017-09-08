import cPickle as pickle
import pandas as pd
import csv
import random


def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

print "Loading Interactions M0"
with open('interactions_m0.pkl', 'rb') as input:
    interactions_m0 = pickle.load(input)
print "Loading Interactions M1"
with open('interactions_m1.pkl', 'rb') as input:
    interactions_m1 = pickle.load(input)
print "Loading Interactions M2"
with open('interactions_m2.pkl', 'rb') as input:
    interactions_m2 = pickle.load(input)
print "Loading Round 0 Opinions (of M0)"
with open('m0_round0Opinions.pkl', 'rb') as input:
    m0_round0Opinions = pickle.load(input)
df = pd.Series(m0_round0Opinions, index=range(len(m0_round0Opinions)))
df_sorted = df.sort_values()
extremistIds_low = df_sorted[:50].index
extremistIds_high = df_sorted[-50:].index
normalos = random.sample(df_sorted[50:-50].index, 100)



####################################
# Model 0 ##########################
####################################


# Analysis of extremists with low opinion
lowdict = {}
highdict = {}
normalodict = {}
# Initializing
for identifier in extremistIds_low:
    lowdict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions
for identifier in extremistIds_high:
    highdict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions
for identifier in normalos:
    normalodict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions

for entry in interactions_m0:
    if (entry[1] in extremistIds_low) and (entry[4] != "Media"):# and (entry[0] % 100 == 0)):
        lowdict["agent"+str(entry[1])][1].append(entry[3])
    if (entry[1] in extremistIds_high) and (entry[4] != "Media"):# and (entry[0] % 100 == 0)):
        highdict["agent"+str(entry[1])][1].append(entry[3])
    if (entry[1] in normalos) and (entry[4] != "Media"):
        normalodict["agent" + str(entry[1])][1].append(entry[3])

headerrow = ["id", "medianOpinion"]
for i in range(0, 9000, 1):
    headerrow.append("round" + str(i) + "VocOp")
# Saving object:
w = csv.writer(open("m0_extremists_low.csv", "w"))
w.writerow(headerrow)
for identifier in extremistIds_low:
    list = [identifier, lowdict["agent"+str(identifier)][0]]
    for item in lowdict["agent"+str(identifier)][1]:
        list.append(item)
    w.writerow(list)

# Saving object:
w = csv.writer(open("m0_extremists_high.csv", "w"))
w.writerow(headerrow)
for identifier in extremistIds_high:
    list = [identifier, highdict["agent"+str(identifier)][0]]
    for item in highdict["agent"+str(identifier)][1]:
        list.append(item)
    w.writerow(list)

# Saving object:
w = csv.writer(open("m0_normalos.csv", "w"))
w.writerow(headerrow)
for identifier in normalos:
    list = [identifier, normalodict["agent"+str(identifier)][0]]
    for item in normalodict["agent"+str(identifier)][1]:
        list.append(item)
    w.writerow(list)



####################################
# Model 1 ##########################
####################################


# Analysis of extremists with low opinion
lowdict = {}
highdict = {}
normalodict = {}
# Initializing
for identifier in extremistIds_low:
    lowdict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions
for identifier in extremistIds_high:
    highdict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions
for identifier in normalos:
    normalodict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions

for entry in interactions_m1:
    if (entry[1] in extremistIds_low) and (entry[4] != "Media"):# and (entry[0] % 100 == 0)):
        lowdict["agent"+str(entry[1])][1].append(entry[3])
    if (entry[1] in extremistIds_high) and (entry[4] != "Media"):# and (entry[0] % 100 == 0)):
        highdict["agent"+str(entry[1])][1].append(entry[3])
    if (entry[1] in normalos) and (entry[4] != "Media"):
        normalodict["agent" + str(entry[1])][1].append(entry[3])

headerrow = ["id", "medianOpinion"]
for i in range(0, 9000, 1):
    headerrow.append("round" + str(i) + "VocOp")
# Saving object:
w = csv.writer(open("m1_extremists_low.csv", "w"))
w.writerow(headerrow)
for identifier in extremistIds_low:
    list = [identifier, lowdict["agent"+str(identifier)][0]]
    for item in lowdict["agent"+str(identifier)][1]:
        list.append(item)
    w.writerow(list)

# Saving object:
w = csv.writer(open("m1_extremists_high.csv", "w"))
w.writerow(headerrow)
for identifier in extremistIds_high:
    list = [identifier, highdict["agent"+str(identifier)][0]]
    for item in highdict["agent"+str(identifier)][1]:
        list.append(item)
    w.writerow(list)

# Saving object:
w = csv.writer(open("m1_normalos.csv", "w"))
w.writerow(headerrow)
for identifier in normalos:
    list = [identifier, normalodict["agent"+str(identifier)][0]]
    for item in normalodict["agent"+str(identifier)][1]:
        list.append(item)
    w.writerow(list)


####################################
# Model 2 ##########################
####################################


# Analysis of extremists with low opinion
lowdict = {}
highdict = {}
normalodict = {}
# Initializing
for identifier in extremistIds_low:
    lowdict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions
for identifier in extremistIds_high:
    highdict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions
for identifier in normalos:
    normalodict["agent" + str(identifier)] = [df[identifier], []] # second empty list is for vocalized opinions

for entry in interactions_m2:
    if (entry[1] in extremistIds_low) and (entry[4] != "Media"):# and (entry[0] % 100 == 0)):
        lowdict["agent"+str(entry[1])][1].append(entry[3])
    if (entry[1] in extremistIds_high) and (entry[4] != "Media"):# and (entry[0] % 100 == 0)):
        highdict["agent"+str(entry[1])][1].append(entry[3])
    if (entry[1] in normalos) and (entry[4] != "Media"):
        normalodict["agent" + str(entry[1])][1].append(entry[3])

headerrow = ["id", "medianOpinion"]
for i in range(0, 9000, 1):
    headerrow.append("round" + str(i) + "VocOp")
# Saving object:
w = csv.writer(open("m2_extremists_low.csv", "w"))
w.writerow(headerrow)
for identifier in extremistIds_low:
    list = [identifier, lowdict["agent"+str(identifier)][0]]
    for item in lowdict["agent"+str(identifier)][1]:
        list.append(item)
    w.writerow(list)

# Saving object:
w = csv.writer(open("m2_extremists_high.csv", "w"))
w.writerow(headerrow)
for identifier in extremistIds_high:
    list = [identifier, highdict["agent"+str(identifier)][0]]
    for item in highdict["agent"+str(identifier)][1]:
        list.append(item)
    w.writerow(list)

# Saving object:
w = csv.writer(open("m2_normalos.csv", "w"))
w.writerow(headerrow)
for identifier in normalos:
    list = [identifier, normalodict["agent"+str(identifier)][0]]
    for item in normalodict["agent"+str(identifier)][1]:
        list.append(item)
    w.writerow(list)