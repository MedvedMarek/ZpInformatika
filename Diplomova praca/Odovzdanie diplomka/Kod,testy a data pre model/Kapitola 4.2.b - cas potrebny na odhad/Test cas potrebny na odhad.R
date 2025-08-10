
library(conics)
library(ggplot2)
library(gridExtra)
library(corpcor)
library(grid)
library(Rfast)
library(ggrepel)
library(latex2exp)
library(plyr)

rm(list= ls())
source("~/../Desktop/Kod,testy a data pre model/Kapitola 3 - funkcie model/Funkcie model.R")


# 
# Test na ukazanie casovej narocnosti modelu.
# Data su uz vygenerovane pri teste o pocte dat


######################################## vykreslenie testov ############################

# vykreslenie casu potrebneho na vypocet modelu pre urcity pocet dat na vstupe
# 
path = setwd("~/../Desktop/Kod,testy a data pre model/Data/PocetDat")
load("vystupTestCasNaOdhad.Rda")
data = cas
rm(cas)

v = seq(10,300, by = 10)
k = 1
l = 1
std = matrix(NA, nrow = 30, ncol = 2)
std[,2] = v
colnames(std) = c("std", "pocet")
colnames(data) = c("cas", "pocetDat")
data[10,] = c(0.6,20)

for (i in v) {
  std[k,1] = mean(data[data$pocetDat == i,1])
  k = k+1
}

std = as.data.frame(std)
colnames(std) = c("priemer", "pocet")

plot2 = ggplot(data = std, aes(x = pocet, y = priemer)) +
  geom_line(color = "lightsalmon3", size = 0.6) +
  geom_point(aes(x = 100, y = std[10,1]), color = "lightsalmon3", size = 2) +
  labs(y="Ëas v sekund·ch", x="veækosù vstupn˝ch d·t (x,y)", fill = "Ëas pre 100 pozorovanÌ") +
  theme(legend.position="botton") +
  geom_label_repel(data = std[10,], aes(fill = pocet, label = 3.434),
                   box.padding = unit(5, "lines"),
                   point.padding = unit(0.5, 'lines'),
                   colour = "black", 
                   fill = "lightsalmon3",
                   fontface = "bold", 
                   size = 2.8)
plot2











