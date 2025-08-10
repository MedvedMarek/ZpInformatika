
library(conics)
library(ggplot2)
library(gridExtra)
library(corpcor)
library(grid)
library(Rfast)
library(ggrepel)
library(latex2exp)

# Test na zestenie, kolko je potrebnych iteracii na 
# akceptovatelne parametre modlu.
# 

rm(list= ls())

# nacitane funkcie su identicke s funkciami v diplomovej praci, len v tomto subore su
# doplnene nejake funkcie ktore su pouzivane v testovani
# 
source("~/../Desktop/Kod,testy a data pre model/Kapitola 4.3 - pocet iteracii/funkcie test pocet iteracii.R")





# dataframe pre ulozenie odhadnutych dat z testu  
# 
vystupTest = data.frame(matrix(NA, nrow = 0, ncol = 9))
par    = paramElipsa(3,-2,-5,-4,10, 0.8, 0.005, 0.001)
parApr = c(0,1,0)


for (i in c(1:25)) {
  set.seed(i)
  cat("iteracia: ",i)
  apr = aproxDataTesty(par, parApr, velkost = 100, iter = 30, plot = F, vypis = F)
  vystupTest = rbind(vystupTest,apr[[2]])
}


vystupTest = cbind(vystupTest, rep(1:25, each = 30))
colnames(vystupTest) = c("oB","oC","oD","oF","oG","oRo","oSigma","oDelta","odhad")

# write.csv(vystupTest, file = "testPocetIteracii.csv", row.names = T)
# save(vystupTest,file = "testPocetIteracii.Rda")


setwd("~/../Desktop/Kod,testy a data pre model/Data/PocetIteracii")
load("testPocetIteracii.Rda")
data = vystupTest
rm(vystupTest)


matPlot = data[2:750,]
matPlot = rbind(matPlot,rep(0,10))


dataRozdiel = data - matPlot
dataRozdiel[seq(30,750,30),] = dataRozdiel[seq(29,750,30),]
dataRozdiel[,9] = rep(1:25, each = 30)
dataRozdiel = cbind(dataRozdiel,rep(c(1:30),25))
colnames(dataRozdiel)[10] = c("iteracia")


dataPlot = rbind(matrix(dataRozdiel[,1],ncol = 1),
                 matrix(dataRozdiel[,2],ncol = 1),
                 matrix(dataRozdiel[,3],ncol = 1),
                 matrix(dataRozdiel[,4],ncol = 1),
                 matrix(dataRozdiel[,5],ncol = 1))

dataPlot = cbind(dataPlot, rep(dataRozdiel[,9],by = 5),
                           rep(dataRozdiel[,10],by = 5),
                           rep(c(3,-2,-5,-4,10), each = 750))

dataPlot = as.data.frame(dataPlot)
colnames(dataPlot) = c("data", "odhad", "iteracia","parametre")
dataPlot$parametre = factor(dataPlot$parametre,
                            levels = c(3,-2,-5,-4,10),
                            labels = c("B","C","D","F","G"))


std = matrix(data = NA, nrow = 30, ncol = 5)

for (i in 1:5) {
  for (j in 1:30) {
    std[j,i] = mean(dataRozdiel[dataRozdiel$iteracia == j,i])
  }
}

dataPlot1 = as.data.frame(std)
dataPlot1 = rbind(matrix(dataPlot1[,1], ncol = 1),
                  matrix(dataPlot1[,2], ncol = 1),
                  matrix(dataPlot1[,3], ncol = 1),
                  matrix(dataPlot1[,4], ncol = 1),
                  matrix(dataPlot1[,5], ncol = 1))
dataPlot1 = cbind(dataPlot1, 
                  rep(c(3,-2,-5,-4,10), each = 30),
                  rep(c(1:30), 5))
dataPlot1 = as.data.frame(dataPlot1)
colnames(dataPlot1) = c("std" , "parametre", "iteracia")
dataPlot1$parametre = factor(dataPlot1$parametre,
                             levels = c(3,-2,-5,-4,10),
                             labels = c("B","C","D","F","G"))


plot = ggplot(data = dataPlot1, aes(x = iteracia, y = std, color = parametre)) +
  geom_line(size = 0.5) +
  geom_point(data = dataPlot1[dataPlot1$iteracia == 6,],aes(x = iteracia, y = std), 
             size = 3) +
  facet_grid(parametre ~., scales = "free") +
  labs(y="parametre elispy", x="poèet iterácií") +
  labs(colour = "parametre\nelipsy") +
  geom_label_repel(data = dataPlot1[dataPlot1$iteracia == 6,],
                   aes(fill = parametre, label = std),
                   box.padding = unit(1, "lines"),
                   point.padding = unit(2, 'lines'),
                   colour = "black",
                   fontface = "bold",
                   size = 2.9) +
  theme(legend.position="right") +
  labs(colour = "parametre\nelipsy", fill = "parametre\nodhad") +
  guides(colour = guide_legend(nrow = 5, override.aes = list(size = 1)),
         fill = guide_legend(nrow = 5, override.aes = list(size = 1)))
  
  
plot








