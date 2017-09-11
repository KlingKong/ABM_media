# Import from csv-file:
library(stargazer)
setwd("/home/philipp/Dropbox/uni_dokumente_dropbox/bitbucket/ABM_media")
setwd("/home/philipp/Dropbox/uni_dokumente_dropbox/bitbucket/ABM_media")
# Load
m0_round0Opinions <- read.csv("m0_round0Opinions.csv", header = F)
m1_round0Opinions <- read.csv("m1_round0Opinions.csv", header = F)
m2_round0Opinions <- read.csv("m2_round0Opinions.csv", header = F)
m3a_round0Opinions <- read.csv("m3a_round0Opinions.csv", header = F)
m3b_round0Opinions <- read.csv("m3b_round0Opinions.csv", header = F)

m0_roundOpinions <- read.csv("m0_roundOpinions.csv", header = F)
m1_roundOpinions <- read.csv("m1_roundOpinions.csv", header = F)
m2_roundOpinions <- read.csv("m2_roundOpinions.csv", header = F)
m3a_roundOpinions <- read.csv("m3a_roundOpinions.csv", header = F)
m3b_roundOpinions <- read.csv("m3b_roundOpinions.csv", header = F)

m0_roundOWNMEDIANS <- read.csv("m0_roundOWNMEDIANS.csv", header = F)
m1_roundOWNMEDIANS <- read.csv("m1_roundOWNMEDIANS.csv", header = F)
m2_roundOWNMEDIANS <- read.csv("m2_roundOWNMEDIANS.csv", header = F)
m3a_roundOWNMEDIANS <- read.csv("m3a_roundOWNMEDIANS.csv", header = F)
m3b_roundOWNMEDIANS <- read.csv("m3b_roundOWNMEDIANS.csv", header = F)

m0_roundSILENCES <- read.csv("m0_roundSILENCES.csv", header = F)
m1_roundSILENCES <- read.csv("m1_roundSILENCES.csv", header = F)
m2_roundSILENCES <- read.csv("m2_roundSILENCES.csv", header = F)
m3a_roundSILENCES <- read.csv("m3a_roundSILENCES.csv", header = F)
m3b_roundSILENCES <- read.csv("m3b_roundSILENCES.csv", header = F)

m0_roundTRADEOFFS <- read.csv("m0_roundTRADEOFFS.csv", header = F)
m1_roundTRADEOFFS <- read.csv("m1_roundTRADEOFFS.csv", header = F)
m2_roundTRADEOFFS <- read.csv("m2_roundTRADEOFFS.csv", header = F)
m3a_roundTRADEOFFS <- read.csv("m3a_roundTRADEOFFS.csv", header = F)
m3b_roundTRADEOFFS <- read.csv("m3b_roundTRADEOFFS.csv", header = F)

# Load 2
roundOpinions <- cbind(read.csv("m0_roundOpinions.csv", header = F),
                       read.csv("m1_roundOpinions.csv", header = F),
                       read.csv("m2_roundOpinions.csv", header = F),
                       read.csv("m3a_roundOpinions.csv", header = F),
                       read.csv("m3b_roundOpinions.csv", header = F))
roundOwnMedians <- cbind(read.csv("m0_roundOWNMEDIANS.csv", header = F),
                         read.csv("m1_roundOWNMEDIANS.csv", header = F),
                         read.csv("m2_roundOWNMEDIANS.csv", header = F),
                         read.csv("m3a_roundOWNMEDIANS.csv", header = F),
                         read.csv("m3b_roundOWNMEDIANS.csv", header = F))
roundSilences <- cbind(read.csv("m0_roundSILENCES.csv", header = F),
                       read.csv("m1_roundSILENCES.csv", header = F),
                       read.csv("m2_roundSILENCES.csv", header = F),
                       read.csv("m3a_roundSILENCES.csv", header = F),
                       read.csv("m3b_roundSILENCES.csv", header = F))
roundTradeoffs <- cbind(read.csv("m0_roundTRADEOFFS.csv", header = F),
                        read.csv("m1_roundTRADEOFFS.csv", header = F),
                        read.csv("m2_roundTRADEOFFS.csv", header = F),
                        read.csv("m3a_roundTRADEOFFS.csv", header = F),
                        read.csv("m3b_roundTRADEOFFS.csv", header = F))
round0Opinions <- cbind(read.csv("m0_round0Opinions.csv", header = F),
                        read.csv("m1_round0Opinions.csv", header = F), 
                        read.csv("m2_round0Opinions.csv", header = F),
                        read.csv("m3a_round0Opinions.csv", header = F),
                        read.csv("m3b_round0Opinions.csv", header = F))
names(roundOpinions) <-  c("m0","m1","m2","m3a","m3b")
names(roundOwnMedians) <-  c("m0","m1","m2","m3a","m3b")
names(roundSilences) <-  c("m0","m1","m2","m3a","m3b")
names(roundTradeoffs) <-  c("m0","m1","m2","m3a","m3b")
names(round0Opinions) <-  c("m0","m1","m2","m3a","m3b")



# Analysis:

# preparations
# Model 1:
df1 <-cbind(m0_roundOpinions,
            m0_roundOWNMEDIANS,
            m0_roundSILENCES,
            m0_roundTRADEOFFS,
            rep(0,9000),
            c(rep(0,3000),rep(1,6000)))
names(df1) <- c("roundOpinion","medianVoc","silenced","tradeoff","tGroup","tAssigned")
df2 <- cbind(m1_roundOpinions,
             m1_roundOWNMEDIANS,
             m1_roundSILENCES,
             m1_roundTRADEOFFS,
             rep(1,9000),
             c(rep(0,3000),rep(1,6000)))
names(df2) <- c("roundOpinion","medianVoc","silenced","tradeoff","tGroup","tAssigned")
m1 <- rbind(df1, df2)
# Model 2:
df2 <- cbind(m2_roundOpinions,
             m2_roundOWNMEDIANS,
             m2_roundSILENCES,
             m2_roundTRADEOFFS,
             rep(1,9000),
             c(rep(0,3000),rep(1,6000)))
names(df2) <- c("roundOpinion","medianVoc","silenced","tradeoff","tGroup","tAssigned")
m2 <- rbind(df1, df2)

# Descriptives:
# M1:
tapply(m1[m1$tGroup==1,]$roundOpinion, m1[m1$tGroup==1,]$tAssigned, summary)
tapply(m1[m1$tGroup==1,]$medianVoc, m1[m1$tGroup==1,]$tAssigned, summary)
tapply(m1[m1$tGroup==1,]$silenced, m1[m1$tGroup==1,]$tAssigned, summary)
tapply(m1[m1$tGroup==1,]$tradeoff, m1[m1$tGroup==1,]$tAssigned, summary)
# M2
tapply(m2[m2$tGroup==1,]$roundOpinion, m2[m2$tGroup==1,]$tAssigned, summary)
tapply(m2[m2$tGroup==1,]$medianVoc, m2[m2$tGroup==1,]$tAssigned, summary)
tapply(m2[m2$tGroup==1,]$silenced, m2[m2$tGroup==1,]$tAssigned, summary)
tapply(m2[m2$tGroup==1,]$tradeoff, m2[m2$tGroup==1,]$tAssigned, summary)
# DD models:
# Differences in levels of Opinion
lin_m1_1 <- lm(m1$roundOpinion ~ m1$tGroup*m1$tAssigned)
summary(lin_m1_1)
lin_m2_1 <- lm(m2$roundOpinion ~ m2$tGroup*m2$tAssigned)
summary(lin_m2_1)
# Differences in median vocalization
lin_m1_2 <- lm(m1$medianVoc ~ m1$tGroup*m1$tAssigned)
summary(lin_m1_2)
lin_m2_2 <- lm(m2$medianVoc ~ m2$tGroup*m2$tAssigned)
summary(lin_m2_2)
# Differences in silenced tendency:
lin_m1_3 <- lm(m1$silenced ~ m1$tGroup*m1$tAssigned)
summary(lin_m1_3)
lin_m2_3 <- lm(m2$silenced ~ m2$tGroup*m2$tAssigned)
summary(lin_m2_3) 
# Differences in tradefoff opinions
lin_m1_4 <- lm(m1$tradeoff ~ m1$tGroup*m1$tAssigned)
summary(lin_m1_4)
lin_m2_4 <- lm(m2$tradeoff ~ m2$tGroup*m2$tAssigned)
summary(lin_m2_4) 

# Latex output
stargazer(lin_m1_1, lin_m1_2, lin_m1_3, lin_m1_4)
stargazer(lin_m2_1, lin_m2_2, lin_m2_3, lin_m2_4)






# Individual analysis of extreme opinions
setwd("/home/philipp/Dropbox/uni_dokumente_dropbox/bitbucket/ABM_media")
extremists_low <- read.csv("m0_extremists_low.csv", header = T)
extremists_high <- read.csv("m0_extremists_high.csv", header = T)
normalos <- read.csv("m0_normalos.csv", header = T)
# extremists_low[c(1:4),c(1:5)] # inspection


# Low extremists:
differences_low <- extremists_low[,1]
for (i in 4:(dim(extremists_low)[2])){
  differences_low <- cbind(differences_low, abs(extremists_low[,i]-extremists_low[,2]))
}
differences_low <- differences_low[,c(2:dim(differences_low)[2])] # remove ids
means_low = vector()
for (i in 1:dim(differences_low)[2]){
  means_low <- append(means_low, mean(differences_low[,i]))
}
# High extremists:
differences_high <- extremists_high[,1]
for (i in 4:(dim(extremists_high)[2])){
  differences_high <- cbind(differences_high, abs(extremists_high[,i]-extremists_high[,2]))
}
differences_high <- differences_high[,c(2:dim(differences_high)[2])] # remove ids
means_high = vector()
for (i in 1:dim(differences_high)[2]){
  means_high <- append(means_high, mean(differences_high[,i]))
}
# Normalos:
differences_norm <- normalos[,1]
for (i in 4:(dim(normalos)[2])){
  differences_norm <- cbind(differences_norm, abs(normalos[,i]-normalos[,2]))
}
differences_norm <- differences_norm[,c(2:dim(differences_norm)[2])] # remove ids
means_norm = vector()
for (i in 1:dim(differences_norm)[2]){
  means_norm <- append(means_norm, mean(differences_norm[,i]))
}
length(means_high)
length(means_low)
x <- seq(1,length(means_low))

plot(x,means_high, type = "l",col = "black", 
     lwd = 3, 
     xlab = "Round", 
     ylab = "Mean Difference",
     main = "Mean Absolute Difference: Vocalized Opinion to Median Opinion")
lines(x, means_low, type = "l", lwd = 3, col = "red")
lines(x, means_norm, type = "l", lwd = 3, col = "blue")
legend(5500,0.2, # places a legend at the appropriate place 
       c("Left extremists","Right extremists","Random agents"), # puts text in the legend
       col = c("red","black","blue","darkgreen"),
       lty=c(1,1,1),
       lwd=c(3,3,3)) # gives the legend appropriate symbols (lines
extremist <- rep(1,length(means_high))
normie <- rep(0, length(means_norm))
treatment <- c(rep(0,3000),rep(1,6000))
df <- data.frame(rbind(cbind(means_high,extremist,treatment), 
                       cbind(means_low,extremist,treatment), 
                       cbind(means_norm,normie,treatment)))
names(df) <- c("difference","extremist","treatment")
model0 <- lm(df$difference ~ df$extremist*df$treatment)


## Model 1:
extremists_low <- read.csv("m1_extremists_low.csv", header = T)
extremists_high <- read.csv("m1_extremists_high.csv", header = T)
normalos <- read.csv("m1_normalos.csv", header = T)
# extremists_low[c(1:4),c(1:5)] # inspection


# Low extremists:
differences_low <- extremists_low[,1]
for (i in 4:(dim(extremists_low)[2])){
  differences_low <- cbind(differences_low, abs(extremists_low[,i]-extremists_low[,2]))
}
differences_low <- differences_low[,c(2:dim(differences_low)[2])] # remove ids
means_low = vector()
for (i in 1:dim(differences_low)[2]){
  means_low <- append(means_low, mean(differences_low[,i]))
}
# High extremists:
differences_high <- extremists_high[,1]
for (i in 4:(dim(extremists_high)[2])){
  differences_high <- cbind(differences_high, abs(extremists_high[,i]-extremists_high[,2]))
}
differences_high <- differences_high[,c(2:dim(differences_high)[2])] # remove ids
means_high = vector()
for (i in 1:dim(differences_high)[2]){
  means_high <- append(means_high, mean(differences_high[,i]))
}
# Normalos:
differences_norm <- normalos[,1]
for (i in 4:(dim(normalos)[2])){
  differences_norm <- cbind(differences_norm, abs(normalos[,i]-normalos[,2]))
}
differences_norm <- differences_norm[,c(2:dim(differences_norm)[2])] # remove ids
means_norm = vector()
for (i in 1:dim(differences_norm)[2]){
  means_norm <- append(means_norm, mean(differences_norm[,i]))
}
length(means_high)
length(means_low)
x <- seq(1,length(means_low))

plot(x,means_high, type = "l",col = "black", 
     lwd = 3, 
     xlab = "Round", 
     ylab = "Mean Difference",
     main = "Mean Absolute Difference: Vocalized Opinion to Median Opinion")
abline(v = 3000, col = "darkgreen", lwd = 5)
lines(x, means_low, type = "l", lwd = 3, col = "red")
lines(x, means_norm, type = "l", lwd = 3, col = "blue")
legend(5500,0.2, # places a legend at the appropriate place 
       c("Left extremists","Right extremists","Random agents","Recommender Algorithms"), # puts text in the legend
       col = c("red","black","blue","darkgreen"),
       lty=c(1,1,1,1),
       lwd=c(3,3,3,3)) # gives the legend appropriate symbols (lines
extremist <- rep(1,length(means_high))
normie <- rep(0, length(means_norm))
treatment <- c(rep(0,3000),rep(1,6000))
df <- data.frame(rbind(cbind(means_high,extremist,treatment), 
                       cbind(means_low,extremist,treatment), 
                       cbind(means_norm,normie,treatment)))
names(df) <- c("difference","extremist","treatment")
model1 <- lm(df$difference ~ df$extremist*df$treatment)


# Model 2:
extremists_low <- read.csv("m2_extremists_low.csv", header = T)
extremists_high <- read.csv("m2_extremists_high.csv", header = T)
normalos <- read.csv("m2_normalos.csv", header = T)
# extremists_low[c(1:4),c(1:5)] # inspection


# Low extremists:
differences_low <- extremists_low[,1]
for (i in 4:(dim(extremists_low)[2])){
  differences_low <- cbind(differences_low, abs(extremists_low[,i]-extremists_low[,2]))
}
differences_low <- differences_low[,c(2:dim(differences_low)[2])] # remove ids
means_low = vector()
for (i in 1:dim(differences_low)[2]){
  means_low <- append(means_low, mean(differences_low[,i]))
}
# High extremists:
differences_high <- extremists_high[,1]
for (i in 4:(dim(extremists_high)[2])){
  differences_high <- cbind(differences_high, abs(extremists_high[,i]-extremists_high[,2]))
}
differences_high <- differences_high[,c(2:dim(differences_high)[2])] # remove ids
means_high = vector()
for (i in 1:dim(differences_high)[2]){
  means_high <- append(means_high, mean(differences_high[,i]))
}
# Normalos:
differences_norm <- normalos[,1]
for (i in 4:(dim(normalos)[2])){
  differences_norm <- cbind(differences_norm, abs(normalos[,i]-normalos[,2]))
}
differences_norm <- differences_norm[,c(2:dim(differences_norm)[2])] # remove ids
means_norm = vector()
for (i in 1:dim(differences_norm)[2]){
  means_norm <- append(means_norm, mean(differences_norm[,i]))
}
length(means_high)
length(means_low)
x <- seq(1,length(means_low))

plot(x,means_high, type = "l",col = "black", 
     lwd = 3, 
     xlab = "Round", 
     ylab = "Mean Difference",
     main = "Mean Absolute Difference: Vocalized Opinion to Median Opinion")
abline(v = 3000, col = "orange", lwd = 5)
lines(x, means_low, type = "l", lwd = 3, col = "red")
lines(x, means_norm, type = "l", lwd = 3, col = "blue")
legend(5500,0.2, # places a legend at the appropriate place 
       c("Left extremists","Right extremists","Random agents","Recommender Algorithms"), # puts text in the legend
       col = c("red","black","blue","darkgreen"),
       lty=c(1,1,1,1),
       lwd=c(3,3,3,3)) # gives the legend appropriate symbols (lines
extremist <- rep(1,length(means_high))
normie <- rep(0, length(means_norm))
treatment <- c(rep(0,3000),rep(1,6000))
df <- data.frame(rbind(cbind(means_high,extremist,treatment), 
                       cbind(means_low,extremist,treatment), 
                       cbind(means_norm,normie,treatment)))
names(df) <- c("difference","extremist","treatment")
model2 <- lm(df$difference ~ df$extremist*df$treatment)

library(stargazer)
stargazer(model0, model1, model2)

# For M0: 
# -significant higher value for extremists
# - significant higher number after treatment
# - significant higher number for extremists after treatment
# For M1: 
# - significantly higher value for extremists, 
# - significant reduction through treatment, 
# - but significant higher difference for extremists after treatment introduction
# For M2:
# - significant higher difference for extremists
# - significant reduction through treatment
# - significant reduction for extremists after treatment introductions.