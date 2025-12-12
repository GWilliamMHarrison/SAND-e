rm(list = ls())
library(tidyverse)


path<-"directory with all the classifier Output files"
# eg path<-"G:/CH4/R/Input_Data"
setwd(path)

Filelist <- list.files(path)

samples <- read.csv(Filelist[1])
samples <- subset(samples[1:3])
samples[is.na(samples)]<-0

SamplesList <- list()
for(i in list.files(path)){
  SamplesList[[i]]<-read.csv((paste(path,i, sep="/")))
}

Votes <- data.frame()
Votes <- SamplesList[[1]][2]
for (i in 2:length(SamplesList)){
  Votes <- cbind(Votes, SamplesList[[i]][2])
}


Votes[Votes == "Gastropod"] <-"Mollusc"
Votes[Votes == "Bivalve"] <-"Mollusc"
Votes[Votes == "CCA"] <-"Algae"
Votes[Votes == "Echinoderm Spine"] <-"Echinoderm"
Votes[Votes == "Echinoderm Shell"] <-"Echinoderm"

Carbtypes<-unique(unlist(Votes))

Tally<-data.frame()
NumVotes<-data.frame()
Majority<-ncol(Votes)/2
for (i in 1:nrow(Votes)) {
  if (sort(summary(as.factor(as.character(Votes[i,]))), decreasing=T)[1][[1]]>Majority){
    Tally<-rbind(Tally,names(sort(summary(as.factor(as.character(Votes[i,])),sort(summary(as.factor(as.character(Votes[i,]))), decreasing=T)[1][[1]]), decreasing=T)[1]))
    NumVotes<-rbind(NumVotes,sort(summary(as.factor(as.character(Votes[i,]))), decreasing=T)[1][[1]])
  } else {
    Tally <-rbind(Tally, "Unidentified")
    NumVotes<-rbind(NumVotes,sort(summary(as.factor(as.character(Votes[i,]))), decreasing=T)[1][[1]])
  }
}

colnames(Tally)<-"Vote"
colnames(NumVotes)<-"VoteCount"
Tallyfinal<-cbind(samples[1],Tally,NumVotes)


Confidence <- data.frame()
Confidence <- SamplesList[[1]][3]
for (i in 2:length(SamplesList)){
  Confidence <- cbind(Confidence, SamplesList[[i]][3])
}

AVGPercentConfidence<-data.frame()
Tally<-data.frame()
NumVotes<-data.frame()
for (i in 1:nrow(Votes)) {
  if (sort(summary(as.factor(as.character(Votes[i,]))), decreasing=T)[1][[1]]>Majority){
    Tally<-rbind(Tally,names(sort(summary(as.factor(as.character(Votes[i,])),sort(summary(as.factor(as.character(Votes[i,]))), decreasing=T)[1][[1]]), decreasing=T)[1]))
    NumVotes<-rbind(NumVotes,sort(summary(as.factor(as.character(Votes[i,]))), decreasing=T)[1][[1]])
    PercentConfidence<-data.frame()
    for (j in 1:ncol(Votes)){
      if (names(sort(summary(as.factor(as.character(Votes[i,])),sort(summary(as.factor(as.character(Votes[i,]))), decreasing=T)[1][[1]]), decreasing=T)[1])==Votes[i,j]) {
        PercentConfidence<-rbind(PercentConfidence,Confidence[i,j])
      }
    }
    AVGPercentConfidence<-rbind(AVGPercentConfidence,mean(as.numeric(PercentConfidence[,1])))
  } else {
    Tally <-rbind(Tally, "Unidentified")
    NumVotes<-rbind(NumVotes,sort(summary(as.factor(as.character(Votes[i,]))), decreasing=T)[1][[1]])
    AVGPercentConfidence<-rbind(AVGPercentConfidence,"0")
  }
}

colnames(Tally)<-"Vote"
colnames(NumVotes)<-"VoteCount"
colnames(AVGPercentConfidence)<-"AverageConfidence"

TallyConfidence<-cbind(samples[1],Tally,NumVotes,AVGPercentConfidence)

#####Use this if you want to write the votes to a separate file
#write.csv(TallyConfidence,"Votes.csv", row.names = FALSE)

###I have a whole file of functions that I wrote for myself; I usually read it in at the start of a script but it doesn't make sense here since I only need one of them for this script.
ComplexConfidenceThresholds<-function(Votes,Confidences1,threshold1,Confidences2,threshold2){
  for (i in 1:length(Votes)){
    if (Confidences1[i]<=threshold1 & Confidences2[i]<=threshold2){
      Votes[i]<-"Unidentified"
    }
    i=i+1
  }
  Output<-data.frame(Votes,Confidences1,Confidences2)
  colnames(Output)<-c("Vote","AverageConfidence","AverageConfidence2")
  return(Output)
}

samplescurrent<-TallyConfidence
samplesconfidence<-ComplexConfidenceThresholds(samplescurrent$Vote,samplescurrent$AverageConfidence,0.8,samplescurrent$VoteCount,4)
samplescurrent<-cbind(samplescurrent[1],samplesconfidence)

write.csv(samplescurrent,"Data.csv", row.names = FALSE)
