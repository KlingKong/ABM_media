import cPickle as pickle
import csv

# load baseline model parts
print "loading baseline model parts"
with open('m0_round0Opinions.pkl', 'rb') as input:
    m0_round0Opinions = pickle.load(input)
with open('m0_roundOpinions.pkl', 'rb') as input:
    m0_roundOpinions = pickle.load(input)
with open('m0_roundOWNMEDIANS.pkl', 'rb') as input:
    m0_roundOWNMEDIANS = pickle.load(input)
with open('m0_roundSILENCES.pkl', 'rb') as input:
    m0_roundSILENCES = pickle.load(input)
with open('m0_roundTRADEOFFS.pkl', 'rb') as input:
    m0_roundTRADEOFFS = pickle.load(input)

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


# RoundOpinions
w = csv.writer(open("m0_round0Opinions.csv", "w"))
for entry in m0_round0Opinions:
    w.writerow([entry])
w = csv.writer(open("m1_round0Opinions.csv", "w"))
for entry in m1_round0Opinions:
    w.writerow([entry])
w = csv.writer(open("m2_round0Opinions.csv", "w"))
for entry in m2_round0Opinions:
    w.writerow([entry])
w = csv.writer(open("m3a_round0Opinions.csv", "w"))
for entry in m3a_round0Opinions:
    w.writerow([entry])
w = csv.writer(open("m3b_round0Opinions.csv", "w"))
for entry in m3b_round0Opinions:
    w.writerow([entry])


# RoundOpinions
w = csv.writer(open("m0_roundOpinions.csv", "w"))
for entry in m0_roundOpinions:
    w.writerow([entry])
w = csv.writer(open("m1_roundOpinions.csv", "w"))
for entry in m1_roundOpinions:
    w.writerow([entry])
w = csv.writer(open("m2_roundOpinions.csv", "w"))
for entry in m2_roundOpinions:
    w.writerow([entry])
w = csv.writer(open("m3a_roundOpinions.csv", "w"))
for entry in m3a_roundOpinions:
    w.writerow([entry])
w = csv.writer(open("m3b_roundOpinions.csv", "w"))
for entry in m3b_roundOpinions:
    w.writerow([entry])

# RoundOwnMedians:
w = csv.writer(open("m0_roundOWNMEDIANS.csv", "w"))
for entry in m0_roundOWNMEDIANS:
    w.writerow([entry])
w = csv.writer(open("m1_roundOWNMEDIANS.csv", "w"))
for entry in m1_roundOWNMEDIANS:
    w.writerow([entry])
w = csv.writer(open("m2_roundOWNMEDIANS.csv", "w"))
for entry in m2_roundOWNMEDIANS:
    w.writerow([entry])
w = csv.writer(open("m3a_roundOWNMEDIANS.csv", "w"))
for entry in m3a_roundOWNMEDIANS:
    w.writerow([entry])
w = csv.writer(open("m3b_roundOWNMEDIANS.csv", "w"))
for entry in m3b_roundOWNMEDIANS:
    w.writerow([entry])

# RoundSilences:
w = csv.writer(open("m0_roundSILENCES.csv", "w"))
for entry in m0_roundSILENCES:
    w.writerow([entry])
w = csv.writer(open("m1_roundSILENCES.csv", "w"))
for entry in m1_roundSILENCES:
    w.writerow([entry])
w = csv.writer(open("m2_roundSILENCES.csv", "w"))
for entry in m2_roundSILENCES:
    w.writerow([entry])
w = csv.writer(open("m3a_roundSILENCES.csv", "w"))
for entry in m3a_roundSILENCES:
    w.writerow([entry])
w = csv.writer(open("m3b_roundSILENCES.csv", "w"))
for entry in m3b_roundSILENCES:
    w.writerow([entry])


# RoundSilences:
w = csv.writer(open("m0_roundTRADEOFFS.csv", "w"))
for entry in m0_roundTRADEOFFS:
    w.writerow([entry])
w = csv.writer(open("m1_roundTRADEOFFS.csv", "w"))
for entry in m1_roundTRADEOFFS:
    w.writerow([entry])
w = csv.writer(open("m2_roundTRADEOFFS.csv", "w"))
for entry in m2_roundTRADEOFFS:
    w.writerow([entry])
w = csv.writer(open("m3a_roundTRADEOFFS.csv", "w"))
for entry in m3a_roundTRADEOFFS:
    w.writerow([entry])
w = csv.writer(open("m3b_roundTRADEOFFS.csv", "w"))
for entry in m3b_roundTRADEOFFS:
    w.writerow([entry])

