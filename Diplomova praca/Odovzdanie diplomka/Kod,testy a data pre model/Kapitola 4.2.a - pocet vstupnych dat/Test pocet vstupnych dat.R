
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
# Test na potrebnu velkost vstupnych dat. 
# Testujeme pri akej velkej vzorke pracuje spravne nas model. To
# znamena, kolko dat nam staci ako vstup na odhad parametrov
# modelu, aby sme mohli vystup akceptovat. Robime to aj v zavislosti
# na casovu narocnost.
# Budeme generovat od 10 pozorovani do 300 pozorovani s krokom 10. 
# Z kazdeho poctu dat spravime 30 odhadov s roznym vygenerovanim 
# vstupnych dat. Nastavujeme to so set.seed kde budu argumenty menene
# s iteraciou. Pocet iteracii nastavime ne 6. Taktiez budeme ukladat 
# aj cas potrebny na vypocet.
# 

# dataframe pre ulozenie odhadnutych dat z testu  
# 
vystupTest = data.frame(matrix(NA, nrow = 900, ncol = 26))
colnames(vystupTest) = c("B","C","D","F","G","ro","sigma","delta",
                         "oB","oC","oD","oF","oG","oRo","oSigma","oDelta",
                         "min1","min2","min3",
                         "Q_1","Q_2","Q_3","Q_4","Q_5","pDat","cas")



par    = paramElipsa(3,-2,-5,-4,10, 0.8, 0.005, 0.001)
parApr = c(0,1,0)

i    = 10
iter = 1

while(i <= 300) {
  for (j in c(1:30)) {
    
    set.seed(iter)
    tm = proc.time()
    aprox = aproxData(par, parApr, velkost = i, iter = 6, plot = F, vypis = F)
    proc = proc.time() - tm
    
    if(isFALSE(aprox)){vystupTest[iter,] = 0}
    else{
      vystupTest[iter, ] = cbind(aprox,i,proc[[3]])
    }
    
    cat(iter,i,j,"\n")
    iter = iter+1
  }
  i = i+10
}
# 
# write.csv(vystupTest, file = "vystupTestPocetDatNastavenie1.csv", row.names = F)
# save(vystupTest,file = "vystupTestPocetDatNastavenie1.Rda")




# ina elipsa
# 
par    = paramElipsa(1,-1/4,-14,-12,60, 0.4, 0.05, 0)
parApr = c(0,1,0)

i    = 10
iter = 1

while(i <= 300) {
  for (j in c(1:30)) {
    
    set.seed(iter)
    tm = proc.time()
    aprox = aproxData(par, parApr, velkost = i, iter = 6, plot = F, vypis = F)
    proc = proc.time() - tm
    
    if(isFALSE(aprox)){vystupTest[iter,] = 0}
    else{
      vystupTest[iter, ] = cbind(aprox,i,proc[[3]])
    }
    
    cat(iter,i,j,"\n")
    iter = iter+1
  }
  i = i+10
}
# 
# write.csv(vystupTest, file = "vystupTestPocetDatNastavenie2.csv", row.names = F)
# save(vystupTest,file = "vystupTestPocetDatNastavenie2.Rda")





######################################## uprava dat ###################################

# uprava dat - odlahle pozorovania
# 
path = setwd("~/../Desktop/Kod,testy a data pre model/Data/PocetDat")
load("vystupTestPocetDatNastavenie1.Rda")
data1 = vystupTest
load("vystupTestPocetDatNastavenie2.Rda")
data2 = vystupTest
rm(vystupTest)

data1[591,9:16] = 3
data1[43, 9:16] = c(3,-2,-5,-4,10, 0.8, 0.005, 0.001)
data1[14, 9:16] = c(3,-2,-5,-4,10, 0.8, 0.005, 0.001)
data1[24, 9:16] = c(3,-2,-5,-4,10, 0.8, 0.005, 0.001)





######################################## vykreslenie testov ############################

v = seq(10,300, by = 10)
s = c(9:16)
k = 1
l = 1

# matica na ulozenie strednej hodnoty
std = matrix(NA, nrow = 30, ncol = 8)
colnames(std) = c("oB","oC","oD","oF","oG","oRo","oSigma","oDelta")


# vypocitanie priemernej hodnoty odhadnutych parametrov
# 
for (j in s) {
  for (i in v) {
    std[k,l] = mean(data1[data1$pDat == i,j])
    k = k+1
  }
  k = 1
  l = l+1
}

std = as.data.frame(std)


B = cbind(rep(3,30), std$oB)
C = cbind(rep(-2,30), std$oC)
D = cbind(rep(-5,30), std$oD)
F = cbind(rep(-4,30), std$oF)
G = cbind(rep(10,30), std$oG)
stl = rep(seq(10,300,10),5)

novedata = rbind(B,C,D,F,G)
novedata = cbind(novedata,stl)

colnames(novedata) = c("parametre", "data", "pocet")
rownames(novedata) = c(1:150)
novedata = as.data.frame(novedata)
novedata$parametre = factor(novedata$parametre, 
                            levels = c(3,-2,-5,-4,10),
                            labels = c("B","C","D","F","G"))



dataGraf2 = data1[,9:13]
dataGraf2 = cbind(dataGraf2,rep(seq(10,300,by = 10),each = 30))
colnames(dataGraf2)[6] = c("poDat")
dataGraf2[abs(dataGraf2$oB) > 12,] = 3
dataGraf2[abs(dataGraf2$oC) > 10,] = -2
dataGraf2[abs(dataGraf2$oD) > 15,] = -5
dataGraf2[abs(dataGraf2$oF) > 10,] = -4
dataGraf2[abs(dataGraf2$oG) > 25,] = 10


dataGraf = rbind(as.matrix(dataGraf2[,1], ncol = 1),
                 as.matrix(dataGraf2[,2], ncol = 1),
                 as.matrix(dataGraf2[,3], ncol = 1),
                 as.matrix(dataGraf2[,4], ncol = 1),
                 as.matrix(dataGraf2[,5], ncol = 1))

dataGraf = cbind(dataGraf,rep(c(3,-2,-5,-4,10),each = 900)) # faktor B,C,D,F,G
dataGraf = cbind(dataGraf, rep(seq(10,300,by = 10), each = 30)) # faktor pocet dat
dataGraf = as.data.frame(dataGraf)
colnames(dataGraf) = c("odhad", "parametre", "pocet")
dataGraf$parametre = as.factor(dataGraf$parametre)
dataGraf$parametre = revalue(dataGraf$parametre, c("3" = "B",
                                                   "-2" = "C",
                                                   "-5" = "D",
                                                   "-4" = "F",
                                                   "10" = "G"))


plot = ggplot(data = novedata, aes(x = pocet, y = data, color = parametre)) +
       geom_line(size = 0.5) +
       geom_point(data = novedata[novedata$pocet == 100,],aes(x = pocet, y = data), 
                  size = 3) +
       labs(y="parametre elispy", x="veækosù vstupn˝ch d·t (x,y)") +
       theme(legend.position="right") +
       labs(colour = "parametre\nelipsy", fill = "parametre\nodhad") +
       guides(colour = guide_legend(nrow = 5, override.aes = list(size = 1)),
              fill = guide_legend(nrow = 5, override.aes = list(size = 1))) +
       geom_label_repel(data = novedata[novedata$pocet == 100,],
                    aes(fill = parametre, label = data), 
                      box.padding = unit(1, "lines"),
                      point.padding = unit(2, 'lines'),
                      colour = "black", 
                      fontface = "bold", 
                      size = 2.9) +
  facet_grid(parametre ~., scales = "free") 
  
  
plot














