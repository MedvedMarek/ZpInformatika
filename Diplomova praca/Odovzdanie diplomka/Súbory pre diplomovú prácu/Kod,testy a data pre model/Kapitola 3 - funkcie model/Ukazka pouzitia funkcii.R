# 
# install.packages("conics")
# install.packages("ggplot2")
# install.packages("gridExtra")
# install.packages("corpcor")
# install.packages("latex2exp")
# install.packages("grid")
# install.packages("Rfast")
# 
library(conics)
library(ggplot2)
library(gridExtra)
library(corpcor)
library(latex2exp)
library(grid)
library(Rfast)


rm(list= ls())
source("~/../Desktop/Kod,testy a data pre model/Kapitola 3 - funkcie model/Funkcie model.R")


# Ukazka pouzitia funkcii
# 
# elipsa 1
# odhad parametrov modelu
# 
set.seed(12345)
par = paramElipsa(3,-2,-5,-4,10, 0.5, 0.005, 0.001)
parApr = c(0,1,0)

odhad = aproxData(par, parApr, 150, 6, plot = F, vypis = T)
odhad


# elipsa 2
# odhad parametrov modelu
# 
par = paramElipsa(1,-1/4,-14,-12,60, 0.5, 0.005, 0)
parApr = c(0,1,0)

aproxData(par, parApr, 150, 6, plot = F, vypis = T)




# odhad ak su k dispozicii realne data
# 
par = paramElipsa(3,-2,-5,-4,10, 0.5, 0.005, 0.001)
data = generujData(par, 150)
data = data[[1]] # reprezentuje realne data

odhad = odhadZRealDat(data, 7, vypis = T)
odhad


































