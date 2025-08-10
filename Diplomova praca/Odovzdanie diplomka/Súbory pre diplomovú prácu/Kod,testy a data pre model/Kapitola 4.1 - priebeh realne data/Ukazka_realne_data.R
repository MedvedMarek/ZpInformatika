library(conics)
library(ggplot2)
library(gridExtra)
library(corpcor)
library(latex2exp)
library(grid)
library(Rfast)
library(readr)


rm(list= ls())

path = setwd("~/../Desktop/Kod,testy a data pre model/Data/Realne data")
data = read_tsv("Heydemann_data4.txt")


# Nahlad na sutocne meranie. Ako sa sprava na elipse a ako sa 
# spravaju sinusoidy
# 
data = as.data.frame(data)
data = data[,1:4]
colnames(data) = c("x", "y", "ox", "oy")

vzorka1 = 2500
vzorka2 = 4500
vzorka3 = 6500

p1 = ggplot(data = data[1:vzorka1,]) +
  geom_point(aes(x = x, y = y), color = "#311B92", size = 1) +
  xlab("reálne dáta x") +
  ylab("reálne dáta y") +
  ggtitle(sprintf("poèet vzoriek - %d",vzorka1)) +
  theme(plot.title = element_text(size = 11))

p2 = ggplot(data = data[1:vzorka2,]) +
  geom_point(aes(x = x, y = y), color = "#311B92", size = 1) +
  xlab("reálne dáta x") +
  ylab("reálne dáta y") +
  ggtitle(sprintf("poèet vzoriek - %d",vzorka2)) +
  theme(plot.title = element_text(size = 11))

p3 = ggplot(data = data[1:vzorka3,]) +
  geom_point(aes(x = x, y = y), color = "#311B92", size = 1) +
  xlab("reálne dáta x") +
  ylab("reálne dáta y") +
  ggtitle(sprintf("poèet vzoriek - %d",vzorka3)) +
  theme(plot.title = element_text(size = 11))

g = grid.arrange(p1, p2, p3,ncol = 3)



dataSin = rbind(matrix(data[,1], ncol = 1), matrix(data[,2], ncol = 1))
dataSin = cbind(dataSin, rep(c(1,2), each = 10000), rep(c(1:10000),2))
dataSin = data.frame(dataSin)
colnames(dataSin) = c("data", "xy", "pocet")
dataSin$xy = factor(dataSin$xy, levels = c(1,2), labels = c("x", "y"))


plot = ggplot(data = dataSin) +
  geom_point(aes(x = pocet, y = data, colour = xy), size = 1) +
  labs(x = "poèet meraní",
       y = "nameraná hodnota",
       colour = "signál") +
  scale_color_manual(values=c("#2196F3", "#B71C1C"))


graf = grid.arrange(plot, g, ncol = 1)


























