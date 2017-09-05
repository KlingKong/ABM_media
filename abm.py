import numpy as np
from scipy.stats import beta
import random
from scipy.optimize import minimize
import math
import cPickle as pickle
import copy
import sys

sys.setrecursionlimit(100000)
random.seed(8)


def getNegativeUtility(x, aOwn, bOwn, aPeer, bPeer, ld, ownWeight):
    """Function to determine absolute deviation (combined area under curves)
    """
    # fbeta =(gamma(a+b) * x**(a-1) * (1-x)**(b-1))/(gamma(a)*gamma(b))
    utility = 1 - (ownWeight * math.exp(-ld * beta.cdf(x, aPeer, bPeer)) + (1 - ownWeight) * math.exp(
        -ld * (1 - beta.cdf(x, aOwn, bOwn))))
    return -1 * utility


def findNearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def findFarthest(array, value):
    idx = (np.abs(array - value)).argmax()
    return array[idx]

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


class Agent(object):
    """An Agent which represents a person.

    Attributes:
        id: identifier
        model: the model the agent is assigned to.
        opinionBetaA: beta distribution parameter which represents opinion and first beta parameter
        opinionBetaB: beta distribution parameter which represents opinion and second beta parameter
        medianOpinion: median of opinion
        vocalizedOpinion: tradeoff between own Opinion and Peergroup and Media Influence
        precision: double which represents confidence in own opinion
        friends: list of friends
        abos: list of followed media content
        group: possibility to assign agent to a subgroup (initial value: 0)
        weight: weight used to determine threshold for extremeness aversion and authenticity preference
        ld: lambda for the calculation of the utility
    """

    def __init__(self, unique_id, ABModel, group = 0):
        self.id = unique_id
        self.model = ABModel
        self.opinionBetaA = round(np.random.uniform(low=2, high=10))
        self.opinionBetaB = round(np.random.uniform(low=2, high=10))
        self.medianOpinion = beta.median(self.opinionBetaA, self.opinionBetaB)
        self.precision = 1 / beta.stats(self.opinionBetaA, self.opinionBetaB, moments='v')
        self.friends = []
        self.abos = []
        self.favorites = [] # used to store favorite articles.
        self.group = group
        self.weight = 0.5  # Weight for social extremeness / authenticity preference
        self.threshold = round(np.random.uniform(0.1, 0.2), 3)
        self.ld = 20  # Lambda parameter
        self.vocalizedOpinions = {}
        self.perceptions = list(np.random.beta(self.opinionBetaA, self.opinionBetaB,
                                          100))  # Start with 100 random samples of own opinion as perception of the world
        self.perceptionMean = self.medianOpinion


    def formLink(self, friend):
        self.friends.append(friend)

    def makeAbo(self, object):
        self.abos.append(object)

    def interact(self, object):
        friend = object
        silence = False
        # Goal: vocalize opinion and process it to other agent.
        # 1) Try to process own "authentic" median opinion:
        vocOpinion = self.medianOpinion

        if np.abs(vocOpinion - self.perceptionMean) < self.threshold:
            # Is the deviation of own "true" opinion not deviating too much? process it!
            self.processOpinion(target=friend, opinion=vocOpinion, status="OwnMedian")
        else:  # True opinion deviates too much from perceived mean: do the trade-off formulated by Brown between social extremeness aversion and authenticity preference:
            otherA = friend.opinionBetaA
            otherB = friend.opinionBetaB
            optim = minimize(getNegativeUtility, x0=0.5,
                             args=(self.opinionBetaA, self.opinionBetaB, otherA, otherB, self.ld, self.weight))
            if optim.success:
                vocOpinion = min(0.99, max(0.01, optim.x[0]))
                if np.abs(vocOpinion - self.perceptionMean) < self.threshold:
                    # Test if the trade-off opinion deviates too much from the perceived mean? No? Process it!
                    self.processOpinion(target=friend, opinion=vocOpinion, status="TradeOff")
                else:
                    silence = True
                    # Even the trade-off opinion was too far away from the perceived mean: fall silent and only process what majority thinks:
                    vocOpinion = self.perceptionMean
                    self.processOpinion(target=friend, opinion=vocOpinion, status="Silence")
                    # Additionally: entry in the log File of the model
                    if "round" + str(self.model.currentRound) in self.model.log:
                        silentPeople = self.model.log["round" + str(self.model.currentRound)]
                    else:
                        silentPeople = 0
                    self.model.log["silenceRound" + str(self.model.currentRound)] = silentPeople + 1
            else:
                silence = True
                print "No solution found: remaining silent"
                vocOpinion = self.perceptionMean
                self.processOpinion(target=friend, opinion=vocOpinion, status="Silence")
                # Additionally: entry in the log File of the model
                silentPeople = self.model.log["round" + str(self.model.currentRound)]
                self.model.log["silenceRound" + str(self.model.currentRound)] = silentPeople + 1
        return silence

    def refreshPerception(self):
        self.perceptionMean = np.mean(self.perceptions)

    def processOpinion(self, target, opinion, status):
        target.perceptions.append(opinion)
        del (target.perceptions[0])
        if target is not self:
            self.model.interactions.append([self.model.currentRound, self.id, target.id, opinion, status])
        if self.model.opinionUpdate:
            if target.medianOpinion - opinion >= 0: # evidence to the left --> increase b
                target.opinionBetaB += 1
                target.medianOpinion = beta.median(target.opinionBetaA, target.opinionBetaB)
                target.precision = 1 / beta.stats(target.opinionBetaA, target.opinionBetaB, moments='v')
            else: # evidence to the left --> increase a
                target.opinionBetaA += 1
                target.medianOpinion = beta.median(target.opinionBetaA, target.opinionBetaB)
                target.precision = 1 / beta.stats(target.opinionBetaA, target.opinionBetaB, moments='v')

    def updateFriends(self, friendToRemove):
        # Finds another friend and replaces the old friend
        ownIndex = self.model.agOpSort.index(self)
        maxPos = int(min(len(self.model.agents), ownIndex + 2 * self.model.maxFriends))
        minPos = int(max(0, ownIndex - 2 * self.model.maxFriends))

        candidate = self.friends[0]
        while candidate in self.friends:
            candidate = self.model.agOpSort[random.sample(range(minPos, maxPos), 1)[0]]
        self.friends.append(candidate)
        self.friends.remove(friendToRemove)
        # print "Agent "+str(self.id)+" changed his friend (Agent "+str(friendToRemove.id)+") to Agent "+str(candidate.id)

    def updateAbos(self, aboToRemove):
        # Finds another abo and replaces the old abo
        candidate = self.abos[0]
        while candidate in self.abos:
            candidate = random.sample(self.model.outlets, 1)[0]
        self.abos.append(candidate)
        self.abos.remove(aboToRemove)

    def consume(self, abo):
        upset = False
        if self.model.recommenderAlgorithms:
            listOfAvailableArticles = []
            for abo in self.abos:
                for article in abo.articles:
                    listOfAvailableArticles.append(article)
            randomFavorite = random.sample(self.favorites, 1)[0]
            articleOpinion = findNearest(np.array(listOfAvailableArticles), randomFavorite)
            if np.abs(articleOpinion - self.medianOpinion) > self.threshold:
                upset = True
            self.processOpinion(target=self, opinion=articleOpinion, status="Media")
            # Add to favorites if its close enough (closer than last added favorite)
            if np.abs(articleOpinion - self.medianOpinion) < np.abs(self.favorites[-1] - self.medianOpinion):
                self.favorites.append(articleOpinion)
        else:
            articleOpinion = random.sample(abo.articles, 1)[0]
            if np.abs(articleOpinion - self.medianOpinion) > self.threshold:
                upset = True
            self.processOpinion(target=self, opinion=articleOpinion, status="Media")
        return upset

    def step(self):
        # print "Current Round: "+str(self.model.currentRound)
        # print "ID "+str(self.id)
        # print "A Parameter: "+str(self.opinionBetaA)
        # print "B Parameter: "+str(self.opinionBetaB)
        # Documentation of status to analyze later
        friendOpinions = []
        aboOpinions = []
        friendIds = []
        aboIds = []
        for friend in self.friends:
            friendOpinions.append(friend.medianOpinion)
            friendIds.append(friend.id)
        for abo in self.abos:
            aboOpinions.append(abo.medianOpinion)
            aboIds.append(abo.id)
        if self.model.currentRound == 0:
            self.model.statuses.append([self.model.currentRound, self.id, self.medianOpinion, friendIds, friendOpinions, aboIds, aboOpinions])
        # print "Own Medianopinion: "+str(self.medianOpinion)

        # The steps
        # a) Refresh perception of the world:
        self.refreshPerception()
        # b) Interact with a random friend:
        friend = random.sample(self.friends, 1)[0]
        # print "Friend Opinion: "+str(friend.medianOpinion)
        silence = self.interact(friend)
        if silence:
            # If agent was silent: update friends
            self.updateFriends(friendToRemove=friend)
        # c) Consume media
        abo = random.sample(self.abos, 1)[0]
        # print "Abo Opinion: "+str(abo.medianOpinion)
        upset = self.consume(abo)
        if upset:
            # If the agent is upset about the abo: change the outlet
            self.updateAbos(abo)



class MediaOutlet(object):
    """A Media object which represents a type of media which can be consumed.

       Attributes:
           id: identifier
           model: the model, the outlet is assigned to.
           opinionBetaA: beta distribution parameter which represents opinion and first beta parameter
           opinionBetaB: beta distribution parameter which represents opinion and second beta parameter
           medianOpinion: median of opinion
           internetSources: Dummy for whether Outlets are created with a wide opinion range or with more specified opinions.

           - Note - By default, the parameters are estimated between 2 and 4 (low numbers) to guarantee
           a wide distribution of opinion. In case, outlets will be modelled by a higher number and more
           diverse opinions, the numbers should be adjusted to combinations of e.g. (2.5.|10) or (10|2.5) or also (10|10).
       """

    def __init__(self, uniqueId, Model, internetSources = False):
        self.id = uniqueId
        self.model = Model
        self.internetSources = internetSources
        if internetSources:
            randomNumber = np.random.uniform(0, 1)
            if randomNumber >= 0.5:
                self.opinionBetaA = 10
                self.opinionBetaB = np.random.uniform(low=2, high=10)
                self.medianOpinion = beta.median(self.opinionBetaA, self.opinionBetaB)
            else:
                self.opinionBetaA = np.random.uniform(low=2, high=10)
                self.opinionBetaB = 10
                self.medianOpinion = beta.median(self.opinionBetaA, self.opinionBetaB)
        else:
            self.opinionBetaA = np.random.uniform(low=2, high=4)
            self.opinionBetaB = np.random.uniform(low=2, high=4)
            self.medianOpinion = beta.median(self.opinionBetaA, self.opinionBetaB)
        self.articles = np.random.beta(self.opinionBetaA, self.opinionBetaB, 5)

    def step(self):
        self.articles = np.random.beta(self.opinionBetaA, self.opinionBetaB, 5)


class Model(object):
    """A model that wraps both agents and media outlets together and lets them proceed step by step.

    Attributes:

        ### ### ###
        id: unique Identifier of the model
        currentRound: current round/ step of the model
        agents: List of Agents
        agOpSort: List of Agents sorted by medianOpinion
        outlets: List of MediaOutlets
        outOpSort: List of MediaOutlets sorted by medianOpinion
        noAgents: Number of Agents to populate the world.
        noOutlets: Number of Media Outlets to populate the world.
        minFriends: Minimum Number of Friends a Person must have.
        maxFriends: Maximum Number of Friends a Person can have.
        opinionUpdate: Dummy for whether opinions should be updated or not

        ### Treatment variables ###
        internetSources: Is it in the new age? Influences Outlets
        recommenderAlgorithms: used to activate recommender algorithms
        timePlaceIndependence: used to de-activate the deletion of past perceptions

        ### These are used to store reports ###
        self.interactions = []
        self.log = {}
        self.statuses = []
    """

    def __init__(self, uniqueId, noAgents=1000, noOutlets=5, minFriends=1, maxFriends=10, internetSources=False, recommenderAlgorithms=False, timePlaceIndependence=False, opinionUpdate=False):

        self.id = uniqueId
        self.currentRound = 0
        self.agents = []
        self.agOpSort = self.agents
        self.outlets = []
        self.outOpSort = self.outlets
        self.noAgents = noAgents
        self.noOutlets = noOutlets
        self.minFriends = minFriends
        self.maxFriends = maxFriends
        self.opinionUpdate = opinionUpdate
        self.internetSources = internetSources
        self.interactions = []
        self.log = {}
        self.statuses = []
        self.recommenderAlgorithms = recommenderAlgorithms # used to activate recommender algorithms
        self.timePlaceIndependence = timePlaceIndependence

        for i in range(0, self.noAgents):
            self.agents.append(Agent(i, ABModel=self))
        for j in range(0, self.noOutlets):
            self.outlets.append(MediaOutlet(j, internetSources=self.internetSources, Model=self))
        self.agOpSort = sorted(self.agents, key=lambda x: x.medianOpinion, reverse=False)
        self.outOpSort = sorted(self.outlets, key=lambda x: x.medianOpinion, reverse=False)

        outletOpinions = []
        for index, outlet in enumerate(self.outOpSort):
             outletOpinions.append(outlet.medianOpinion)
        for index, agent in enumerate(self.agOpSort):
            # Friends
            # Randomly determine how many friends one agent has
            numberOfFriends = int(round(np.random.uniform(self.minFriends, self.maxFriends)))
            maxPos = int(min(self.noAgents, index + 4 * self.maxFriends))  # Minimum ID
            minPos = int(max(0, index - 4 * self.maxFriends))  # Maximum ID
            idSample = random.sample(range(minPos, maxPos), numberOfFriends)  # draw friends ID randomly
            for agentID in idSample:
                # One Way Connection: works like an abonnement of friends/influences
                agent.formLink(self.agOpSort[agentID])
            # Outlets: make abo to the nearest Outlet based on the medianOpinion.
            agent.makeAbo(
                self.outlets[outletOpinions.index(findNearest(np.array(outletOpinions), agent.medianOpinion))])

    def step(self, numberOfSteps=1):
        for step in range(0, numberOfSteps):
            for agent in self.agents:
                agent.step()
            for outlet in self.outlets:
                outlet.step()
            self.currentRound += 1

    def enterNewMediaAge(self):
        print "Entering new media age..."
        self.internetSources = True
        for j in range(0, 2 * self.noOutlets):  # Create new outlets (represent internet forums etc.)
            self.outlets.append(MediaOutlet(j, internetSources=self.internetSources, Model=self))
        numbers = [1, 2, 3]
        for agent in self.agents:
            numberOfNewAbos = random.sample(numbers, 1)[0]
            for i in range(0, numberOfNewAbos):
                candidateAbo = agent.abos[0]
                while candidateAbo in agent.abos:
                    candidateAbo = random.sample(self.outlets, 1)[0]
                agent.makeAbo(candidateAbo)
        self.outOpSort = sorted(self.outlets, key=lambda x: x.medianOpinion, reverse=False)

    def activateRecommenderAlgorithms(self):
        print "Activating Recommender Algorithms..."
        self.recommenderAlgorithms = True
        # Give every agent a favorite to work with:
        for agent in self.agents:
            availableArticles = []
            for abo in agent.abos:
                for articleOpinion in abo.articles:
                    availableArticles.append(articleOpinion)
            agent.favorites.append(findNearest(np.array(availableArticles), agent.medianOpinion))


# Baseline Model
print "Basic run"
basem = Model(1, noAgents=1000, maxFriends=10, minFriends=5)
for i in range(0, 3000):
    print "Step "+str(i)+" of Baseline Model"
    basem.step()
# save_object(basem.interactions, 'interactions_bm.pkl')
# save_object(basem.statuses, 'statuses_bm.pkl')
basem0 = copy.deepcopy(basem)
basem1 = copy.deepcopy(basem)
basem2 = copy.deepcopy(basem)
basem3a = copy.deepcopy(basem)
basem3b = copy.deepcopy(basem)

print "Basic run further"
for i in range(0, 6000):
    print "Step "+str(i)+" of Model 0"
    basem0.step()
save_object(basem0.interactions, 'interactions_m0.pkl')
save_object(basem0.statuses, 'statuses_m0.pkl')

# M1
basem1.enterNewMediaAge()
for i in range(0, 6000):
    print "Step " + str(i) + " of Model 1"
    basem1.step()
save_object(basem1.interactions, 'interactions_m1.pkl')
save_object(basem1.statuses, 'statuses_m1.pkl')

# M2
basem2.activateRecommenderAlgorithms()
for i in range(0, 6000):
    print "Step " + str(i) + " of Model 2"
    basem2.step()
save_object(basem2.interactions, 'interactions_m2.pkl')
save_object(basem2.statuses, 'statuses_m2.pkl')


# M3a
basem3a.enterNewMediaAge()
for i in range(0, 6000):
    print "Step " + str(i) + " of Model 3a"
    if basem3a.currentRound == 6000:
        basem3a.activateRecommenderAlgorithms()
    basem3a.step()
save_object(basem3a.interactions, 'interactions_m3a.pkl')
save_object(basem3a.statuses, 'statuses_m3a.pkl')

# M3b
basem3b.activateRecommenderAlgorithms()
for i in range(0, 6000):
    print "Step " + str(i) + " of Model 3b"
    if basem3b.currentRound == 6000:
        basem3b.enterNewMediaAge()
    basem3b.step()
save_object(basem3b.interactions, 'interactions_m3b.pkl')
save_object(basem3b.statuses, 'statuses_m3b.pkl')


print "Loading M0"
interactions_m0 = basem0.interactions
statuses_m0 = basem0.statuses
print "Loading M1"
interactions_m1 = basem1.interactions
statuses_m1 = basem1.statuses
print "Loading M2"
interactions_m2 = basem2.interactions
statuses_m2 = basem2.statuses
print "Loading M3a"
interactions_m3a = basem3a.interactions
statuses_m3a = basem3a.statuses
print "Loading M3b"
interactions_m3b = basem3b.interactions
statuses_m3b = basem3b.statuses



print "Processing M0"
## Zero Model - Baseline
m0_roundOpinions = []
m0_roundOWNMEDIANS = []
m0_roundSILENCES = []
m0_roundTRADEOFFS = []

for currentRound in range(0, 9000):
    roundOpinion = []
    roundOWNMEDIAN = 0
    roundSILENCE = 0
    roundTRADEOFF = 0
    for entry in interactions_m0:
        if entry[0] == currentRound:
            roundOpinion.append(entry[3])
            if entry[4] == "OwnMedian":
                roundOWNMEDIAN += 1
            if entry[4] == "Silence":
                roundSILENCE += 1
            if entry[4] == "TradeOff":
                roundTRADEOFF += 1
    m0_roundOpinions.append(np.mean(roundOpinion))
    m0_roundOWNMEDIANS.append(roundOWNMEDIAN)
    m0_roundSILENCES.append(roundSILENCE)
    m0_roundTRADEOFFS.append(roundTRADEOFF)
m0_round0Opinions = []
for entry in statuses_m0:
    if entry[0] == 0:
        m0_round0Opinions.append(entry[2])
print "Saving M0 preparations"
save_object(m0_roundOpinions, 'm0_roundOpinions.pkl')
save_object(m0_roundOWNMEDIANS, 'm0_roundOWNMEDIANS.pkl')
save_object(m0_roundSILENCES, 'm0_roundSILENCES.pkl')
save_object(m0_roundTRADEOFFS, 'm0_roundTRADEOFFS.pkl')
save_object(m0_round0Opinions, 'm0_round0Opinions.pkl')


print "Processing M1"
## First Model
m1_roundOpinions = []
m1_roundOWNMEDIANS = []
m1_roundSILENCES = []
m1_roundTRADEOFFS = []

for currentRound in range(0, 9000):
    roundOpinion = []
    roundOWNMEDIAN = 0
    roundSILENCE = 0
    roundTRADEOFF = 0
    for entry in interactions_m1:
        if entry[0] == currentRound:
            roundOpinion.append(entry[3])
            if entry[4] == "OwnMedian":
                roundOWNMEDIAN += 1
            if entry[4] == "Silence":
                roundSILENCE += 1
            if entry[4] == "TradeOff":
                roundTRADEOFF += 1
    m1_roundOpinions.append(np.mean(roundOpinion))
    m1_roundOWNMEDIANS.append(roundOWNMEDIAN)
    m1_roundSILENCES.append(roundSILENCE)
    m1_roundTRADEOFFS.append(roundTRADEOFF)

m1_round0Opinions = []
for entry in statuses_m1:
    if entry[0] == 0:
        m1_round0Opinions.append(entry[2])
print "Saving Model 1 preparations"
save_object(m1_roundOpinions, 'm1_roundOpinions.pkl')
save_object(m1_roundOWNMEDIANS, 'm1_roundOWNMEDIANS.pkl')
save_object(m1_roundSILENCES, 'm1_roundSILENCES.pkl')
save_object(m1_roundTRADEOFFS, 'm1_roundTRADEOFFS.pkl')
save_object(m1_round0Opinions, 'm1_round0Opinions.pkl')


print "Processing M2"
## Second Model
m2_roundOpinions = []
m2_roundOWNMEDIANS = []
m2_roundSILENCES = []
m2_roundTRADEOFFS = []

for currentRound in range(0, 9000):
    roundOpinion = []
    roundOWNMEDIAN = 0
    roundSILENCE = 0
    roundTRADEOFF = 0
    for entry in interactions_m2:
        if entry[0] == currentRound:
            roundOpinion.append(entry[3])
            if entry[4] == "OwnMedian":
                roundOWNMEDIAN += 1
            if entry[4] == "Silence":
                roundSILENCE += 1
            if entry[4] == "TradeOff":
                roundTRADEOFF += 1
    m2_roundOpinions.append(np.mean(roundOpinion))
    m2_roundOWNMEDIANS.append(roundOWNMEDIAN)
    m2_roundSILENCES.append(roundSILENCE)
    m2_roundTRADEOFFS.append(roundTRADEOFF)

m2_round0Opinions = []
for entry in statuses_m2:
    if entry[0] == 0:
        m2_round0Opinions.append(entry[2])

print "Saving Model 2 preparations"
save_object(m2_roundOpinions, 'm2_roundOpinions.pkl')
save_object(m2_roundOWNMEDIANS, 'm2_roundOWNMEDIANS.pkl')
save_object(m2_roundSILENCES, 'm2_roundSILENCES.pkl')
save_object(m2_roundTRADEOFFS, 'm2_roundTRADEOFFS.pkl')
save_object(m2_round0Opinions, 'm2_round0Opinions.pkl')

print "Processing M3a"
## Third Model (a)
m3a_roundOpinions = []
m3a_roundOWNMEDIANS = []
m3a_roundSILENCES = []
m3a_roundTRADEOFFS = []

for currentRound in range(0, 9000):
    roundOpinion = []
    roundOWNMEDIAN = 0
    roundSILENCE = 0
    roundTRADEOFF = 0
    for entry in interactions_m3a:
        if entry[0] == currentRound:
            roundOpinion.append(entry[3])
            if entry[4] == "OwnMedian":
                roundOWNMEDIAN += 1
            if entry[4] == "Silence":
                roundSILENCE += 1
            if entry[4] == "TradeOff":
                roundTRADEOFF += 1
    m3a_roundOpinions.append(np.mean(roundOpinion))
    m3a_roundOWNMEDIANS.append(roundOWNMEDIAN)
    m3a_roundSILENCES.append(roundSILENCE)
    m3a_roundTRADEOFFS.append(roundTRADEOFF)

m3a_round0Opinions = []
for entry in statuses_m3a:
    if entry[0] == 0:
        m3a_round0Opinions.append(entry[2])
print "Saving Model 3a preparations"
save_object(m3a_roundOpinions, 'm3a_roundOpinions.pkl')
save_object(m3a_roundOWNMEDIANS, 'm3a_roundOWNMEDIANS.pkl')
save_object(m3a_roundSILENCES, 'm3a_roundSILENCES.pkl')
save_object(m3a_roundTRADEOFFS, 'm3a_roundTRADEOFFS.pkl')
save_object(m3a_round0Opinions, 'm3a_round0Opinions.pkl')

print "Processing M3b"
## Third Model (b)
m3b_roundOpinions = []
m3b_roundOWNMEDIANS = []
m3b_roundSILENCES = []
m3b_roundTRADEOFFS = []

for currentRound in range(0, 9000):
    roundOpinion = []
    roundOWNMEDIAN = 0
    roundSILENCE = 0
    roundTRADEOFF = 0
    for entry in interactions_m3b:
        if entry[0] == currentRound:
            roundOpinion.append(entry[3])
            if entry[4] == "OwnMedian":
                roundOWNMEDIAN += 1
            if entry[4] == "Silence":
                roundSILENCE += 1
            if entry[4] == "TradeOff":
                roundTRADEOFF += 1
    m3b_roundOpinions.append(np.mean(roundOpinion))
    m3b_roundOWNMEDIANS.append(roundOWNMEDIAN)
    m3b_roundSILENCES.append(roundSILENCE)
    m3b_roundTRADEOFFS.append(roundTRADEOFF)

m3b_round0Opinions = []
for entry in statuses_m3b:
    if entry[0] == 0:
        m3b_round0Opinions.append(entry[2])
print "Saving Model 3b preparations"
save_object(m3b_roundOpinions, 'm3b_roundOpinions.pkl')
save_object(m3b_roundOWNMEDIANS, 'm3b_roundOWNMEDIANS.pkl')
save_object(m3b_roundSILENCES, 'm3b_roundSILENCES.pkl')
save_object(m3b_roundTRADEOFFS, 'm3b_roundTRADEOFFS.pkl')
save_object(m3b_round0Opinions, 'm3b_round0Opinions.pkl')

## _______________________________________________

# # First run: only news outlets
# print "First run"
# basem1 = Model(0, noAgents=1000, maxFriends=10, minFriends=5)
# for i in range(0, 6000):
#     print "Step "+str(i)+" of Model 1"
#     if i == 3000:
#         basem1.enterNewMediaAge()
#     basem1.step()
# save_object(basem1.interactions, 'interactions_m1.pkl')
# save_object(basem1.statuses, 'statuses_m1.pkl')
#
#
# # Second run: only recommender algorithms
# print "Second model"
# basem2 = Model(0, noAgents=1000, maxFriends=10, minFriends=5)
# for i in range(0, 6000):
#     print "Step "+str(i)+" of Model 2"
#     if i == 3000:
#         basem2.activateRecommenderAlgorithms()
#     basem2.step()
# save_object(basem2.interactions, 'interactions_m2.pkl')
# save_object(basem2.statuses, 'statuses_m2.pkl')
#
# # Third run: both - but new media age first
# print "Model 3a"
# basem3a = Model(3, noAgents=1000, maxFriends=10, minFriends=5)
# for i in range(0, 6000):
#     print "Step "+str(i)+" of Model 3a"
#     if i == 3000:
#         basem3a.enterNewMediaAge()
#     if i == 4500:
#         basem3a.activateRecommenderAlgorithms()
#     basem3a.step()
# save_object(basem3a.interactions, 'interactions_m3a.pkl')
# save_object(basem3a.statuses, 'statuses_m3a.pkl')
#
#
# # Fourth run: both - but recommender algorithms first
# print "Model 3b"
# basem3b = Model(4, noAgents=1000, maxFriends=10, minFriends=5)
# for i in range(0, 6000):
#     print "Step "+str(i)+" of Model 3b"
#     if i == 3000:
#         basem3b.activateRecommenderAlgorithms()
#     if i == 4500:
#         basem3b.enterNewMediaAge()
#     basem3b.step()
# save_object(basem3b.interactions, 'interactions_m3b.pkl')
# save_object(basem3b.statuses, 'statuses_m3b.pkl')


#
#
# with open('interactions_m0.pkl', 'rb') as input:
#     interactions_m0 = pickle.load(input)
# with open('statuses_m0.pkl', 'rb') as input:
#     statuses_m0 = pickle.load(input)
# with open('interactions_m1.pkl', 'rb') as input:
#     interactions_m1 = pickle.load(input)
# with open('statuses_m1.pkl', 'rb') as input:
#     statuses_m1 = pickle.load(input)
# with open('interactions_m2.pkl', 'rb') as input:
#     interactions_m2 = pickle.load(input)
# with open('statuses_m2.pkl', 'rb') as input:
#     statuses_m2 = pickle.load(input)
# with open('interactions_m3a.pkl', 'rb') as input:
#     interactions_m3a = pickle.load(input)
# with open('statuses_m3a.pkl', 'rb') as input:
#     statuses_m3a = pickle.load(input)
# with open('interactions_m3b.pkl', 'rb') as input:
#     interactions_m3b = pickle.load(input)
# with open('statuses_m3b.pkl', 'rb') as input:
#     statuses_m3b = pickle.load(input)
#
#
#
#
# ## Zero Model - Baseline
# m0_roundOpinions = []
# m0_roundOWNMEDIANS = []
# m0_roundSILENCES = []
# m0_roundTRADEOFFS = []
#
# for currentRound in range(0, 6000):
#     roundOpinion = []
#     roundOWNMEDIAN = 0
#     roundSILENCE = 0
#     roundTRADEOFF = 0
#     for entry in interactions_m1:
#         if entry[0] == currentRound:
#             roundOpinion.append(entry[3])
#             if entry[4] == "OwnMedian":
#                 roundOWNMEDIAN += 1
#             if entry[4] == "Silence":
#                 roundSILENCE += 1
#             if entry[4] == "TradeOff":
#                 roundTRADEOFF += 1
#     m0_roundOpinions.append(np.mean(roundOpinion))
#     m0_roundOWNMEDIANS.append(roundOWNMEDIAN)
#     m0_roundSILENCES.append(roundSILENCE)
#     m0_roundTRADEOFFS.append(roundTRADEOFF)
# m0_round0Opinions = []
# for entry in statuses_m1:
#     if entry[0] == 0:
#         m0_round0Opinions.append(entry[2])
# save_object(m0_roundOpinions, 'm0_roundOpinions.pkl')
# save_object(m0_roundOWNMEDIANS, 'm0_roundOWNMEDIANS.pkl')
# save_object(m0_roundSILENCES, 'm0_roundSILENCES.pkl')
# save_object(m0_roundTRADEOFFS, 'm0_roundTRADEOFFS.pkl')
# save_object(m0_round0Opinions, 'm0_round0Opinions.pkl')
#
#
#
# ## First Model
# m1_roundOpinions = []
# m1_roundOWNMEDIANS = []
# m1_roundSILENCES = []
# m1_roundTRADEOFFS = []
#
# for currentRound in range(0, 6000):
#     roundOpinion = []
#     roundOWNMEDIAN = 0
#     roundSILENCE = 0
#     roundTRADEOFF = 0
#     for entry in interactions_m1:
#         if entry[0] == currentRound:
#             roundOpinion.append(entry[3])
#             if entry[4] == "OwnMedian":
#                 roundOWNMEDIAN += 1
#             if entry[4] == "Silence":
#                 roundSILENCE += 1
#             if entry[4] == "TradeOff":
#                 roundTRADEOFF += 1
#     m1_roundOpinions.append(np.mean(roundOpinion))
#     m1_roundOWNMEDIANS.append(roundOWNMEDIAN)
#     m1_roundSILENCES.append(roundSILENCE)
#     m1_roundTRADEOFFS.append(roundTRADEOFF)
#
# m1_round0Opinions = []
# for entry in statuses_m1:
#     if entry[0] == 0:
#         m1_round0Opinions.append(entry[2])
#
# save_object(m1_roundOpinions, 'm1_roundOpinions.pkl')
# save_object(m1_roundOWNMEDIANS, 'm1_roundOWNMEDIANS.pkl')
# save_object(m1_roundSILENCES, 'm1_roundSILENCES.pkl')
# save_object(m1_roundTRADEOFFS, 'm1_roundTRADEOFFS.pkl')
# save_object(m1_round0Opinions, 'm1_round0Opinions.pkl')
#
#
#
#
#
# ## Second Model
# m2_roundOpinions = []
# m2_roundOWNMEDIANS = []
# m2_roundSILENCES = []
# m2_roundTRADEOFFS = []
#
# for currentRound in range(0, 6000):
#     roundOpinion = []
#     roundOWNMEDIAN = 0
#     roundSILENCE = 0
#     roundTRADEOFF = 0
#     for entry in interactions_m2:
#         if entry[0] == currentRound:
#             roundOpinion.append(entry[3])
#             if entry[4] == "OwnMedian":
#                 roundOWNMEDIAN += 1
#             if entry[4] == "Silence":
#                 roundSILENCE += 1
#             if entry[4] == "TradeOff":
#                 roundTRADEOFF += 1
#     m2_roundOpinions.append(np.mean(roundOpinion))
#     m2_roundOWNMEDIANS.append(roundOWNMEDIAN)
#     m2_roundSILENCES.append(roundSILENCE)
#     m2_roundTRADEOFFS.append(roundTRADEOFF)
#
# m2_round0Opinions = []
# for entry in statuses_m2:
#     if entry[0] == 0:
#         m2_round0Opinions.append(entry[2])
#
# print "Saving Model 2 preparations"
# save_object(m2_roundOpinions, 'm2_roundOpinions.pkl')
# save_object(m2_roundOWNMEDIANS, 'm2_roundOWNMEDIANS.pkl')
# save_object(m2_roundSILENCES, 'm2_roundSILENCES.pkl')
# save_object(m2_roundTRADEOFFS, 'm2_roundTRADEOFFS.pkl')
# save_object(m2_round0Opinions, 'm2_round0Opinions.pkl')
#
# ## Third Model (a)
# m3a_roundOpinions = []
# m3a_roundOWNMEDIANS = []
# m3a_roundSILENCES = []
# m3a_roundTRADEOFFS = []
#
# for currentRound in range(0, 6000):
#     roundOpinion = []
#     roundOWNMEDIAN = 0
#     roundSILENCE = 0
#     roundTRADEOFF = 0
#     for entry in interactions_m3a:
#         if entry[0] == currentRound:
#             roundOpinion.append(entry[3])
#             if entry[4] == "OwnMedian":
#                 roundOWNMEDIAN += 1
#             if entry[4] == "Silence":
#                 roundSILENCE += 1
#             if entry[4] == "TradeOff":
#                 roundTRADEOFF += 1
#     m3a_roundOpinions.append(np.mean(roundOpinion))
#     m3a_roundOWNMEDIANS.append(roundOWNMEDIAN)
#     m3a_roundSILENCES.append(roundSILENCE)
#     m3a_roundTRADEOFFS.append(roundTRADEOFF)
#
# m3a_round0Opinions = []
# for entry in statuses_m3a:
#     if entry[0] == 0:
#         m3a_round0Opinions.append(entry[2])
#
# save_object(m3a_roundOpinions, 'm3a_roundOpinions.pkl')
# save_object(m3a_roundOWNMEDIANS, 'm3a_roundOWNMEDIANS.pkl')
# save_object(m3a_roundSILENCES, 'm3a_roundSILENCES.pkl')
# save_object(m3a_roundTRADEOFFS, 'm3a_roundTRADEOFFS.pkl')
# save_object(m3a_round0Opinions, 'm3a_round0Opinions.pkl')
#
#
# ## Third Model (b)
# m3b_roundOpinions = []
# m3b_roundOWNMEDIANS = []
# m3b_roundSILENCES = []
# m3b_roundTRADEOFFS = []
#
# for currentRound in range(0, 6000):
#     roundOpinion = []
#     roundOWNMEDIAN = 0
#     roundSILENCE = 0
#     roundTRADEOFF = 0
#     for entry in interactions_m3b:
#         if entry[0] == currentRound:
#             roundOpinion.append(entry[3])
#             if entry[4] == "OwnMedian":
#                 roundOWNMEDIAN += 1
#             if entry[4] == "Silence":
#                 roundSILENCE += 1
#             if entry[4] == "TradeOff":
#                 roundTRADEOFF += 1
#     m3b_roundOpinions.append(np.mean(roundOpinion))
#     m3b_roundOWNMEDIANS.append(roundOWNMEDIAN)
#     m3b_roundSILENCES.append(roundSILENCE)
#     m3b_roundTRADEOFFS.append(roundTRADEOFF)
#
# m3b_round0Opinions = []
# for entry in statuses_m3b:
#     if entry[0] == 0:
#         m3b_round0Opinions.append(entry[2])
#
# save_object(m3b_roundOpinions, 'm3b_roundOpinions.pkl')
# save_object(m3b_roundOWNMEDIANS, 'm3b_roundOWNMEDIANS.pkl')
# save_object(m3b_roundSILENCES, 'm3b_roundSILENCES.pkl')
# save_object(m3b_roundTRADEOFFS, 'm3b_roundTRADEOFFS.pkl')
# save_object(m3b_round0Opinions, 'm3b_round0Opinions.pkl')