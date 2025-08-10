library(conics)
library(ggplot2)
library(gridExtra)
library(corpcor)
library(latex2exp)
library(grid)
library(Rfast)
library(ggrepel)


rm(list= ls())
source("~/../Desktop/Kod,testy a data pre model/Kapitola 4.2.c - potrebna velkost segmentu/funkcie na grafy potrebna velkost segmentu.R")


# Vykreslenie grafov pre potrebnu velkost segmentu
# 

setwd("~/../Desktop/Kod,testy a data pre model/Data/Data na odhad velkosti segmentov/Data_na_elipse_a_zasumene")
load("odhad_500_dat.Rda")
odhad500 = odhad
load("odhad_700_dat.Rda")
odhad700 = odhad
load("odhad_1000_dat.Rda")
odhad1000 = odhad
load("odhad_1500_dat.Rda")
odhad1500 = odhad
rm(odhad)
load("dat_500_0.01_0.002_0.0001.Rda")
data500 = data
load("dat_700_0.01_0.002_0.0001.Rda")
data700 = data
load("dat_1000_0.01_0.002_0.0001.Rda")
data1000 = data
load("dat_1500_0.01_0.002_0.0001.Rda")
data1500 = data3
rm(data)
rm(data3)



p1 = plot1(data1500,odhad1500)
p2 = plot2(data1500,odhad1500)
p3 = plot3(data1500,odhad1500)
p4 = plot4(data1500,odhad1500)
p5 = plot5(data1500,odhad1500)
p6 = plot6(data1500,odhad1500)
p7 = plot7(data1500,odhad1500)







