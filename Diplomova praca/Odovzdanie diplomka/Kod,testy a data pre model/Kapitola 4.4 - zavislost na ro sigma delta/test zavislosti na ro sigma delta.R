
library(conics)
library(ggplot2)
library(gridExtra)
library(corpcor)
library(grid)
library(Rfast)
library(ggrepel)
library(latex2exp)
library(ggpubr)
library(qqplotr)


rm(list= ls())
source("~/../Desktop/Kod,testy a data pre model/Kapitola 4.4 - zavislost na ro sigma delta/funkcie pre test zavislosti na ro sigma delta.R")


# test ako sa skrati doba odhadu, ak dame ako vstupny parameter vektor
# v ktorom su priblizne hodnot ro, sigma, delta
# 
param = paramElipsa(3,-2,-5,-4,10,0.8,0.05,0.001)
parApr1 = c(0.8, 0.05, 0.001)
parApr2 = c(0.3, 0.95, 0)

vystupTest1 = data.frame(matrix(data = NA, nrow = 0, ncol = 8))
vystupTest2 = data.frame(matrix(data = NA, nrow = 0, ncol = 8))
mat = data.frame(matrix(data = 0,nrow = 30, ncol = 8))
colnames(vystupTest1) = c("B","C","D","F","G","ro","sigma","delta")
colnames(vystupTest2) = c("B","C","D","F","G","ro","sigma","delta")
colnames(mat) = c("B","C","D","F","G","ro","sigma","delta")


for (i in c(1:300)) {
  cat("iteracia: ",i,"\n")
  set.seed(i)
  apr1 = aproxDataTesty(param, parApr1, velkost = 100, iter = 30)
  set.seed(i)
  apr2 = aproxDataTesty(param, parApr2, velkost = 100, iter = 30)
  
  if(isFALSE(apr1)){vystupTest1 = rbind(vystupTest1, mat)}
  else{
    vystupTest1 = rbind(vystupTest1,apr1[[2]])
  }
  
  if(isFALSE(apr2)){vystupTest2 = rbind(vystupTest2, mat)}
  else{
    vystupTest2 = rbind(vystupTest2,apr2[[2]])
  }
}

# write.csv(vystupTest1, file = "testZavislostNaRoSigmaDelta1.csv", row.names = T)
# save(vystupTest1,file = "testZavislostNaRoSigmaDelta1.Rda")
# write.csv(vystupTest2, file = "testZavislostNaRoSigmaDelta2.csv", row.names = T)
# save(vystupTest2,file = "testZavislostNaRoSigmaDelta2.Rda")


####################### druha elipsa ##################################

param2   = paramElipsa(1,-1/4,-14,-12,60, 0.4, 0.05, 0.001)
parApr3 = c(0.4, 0.05, 0.001)
parApr4 = c(0.1, 0.95, 0)

vystupTest3 = data.frame(matrix(data = NA, nrow = 0, ncol = 8))
vystupTest4 = data.frame(matrix(data = NA, nrow = 0, ncol = 8))
mat = data.frame(matrix(data = 0,nrow = 30, ncol = 8))
colnames(vystupTest3) = c("B","C","D","F","G","ro","sigma","delta")
colnames(vystupTest4) = c("B","C","D","F","G","ro","sigma","delta")
colnames(mat) = c("B","C","D","F","G","ro","sigma","delta")


for (i in c(1:300)) {
  cat("iteracia: ",i,"\n")
  set.seed(i)
  apr3 = aproxDataTesty(param2, parApr3, velkost = 100, iter = 30)
  set.seed(i)
  apr4 = aproxDataTesty(param2, parApr4, velkost = 100, iter = 30)
  
  if(isFALSE(apr3)){vystupTest3 = rbind(vystupTest3, mat)}
  else{
    vystupTest3 = rbind(vystupTest3,apr3[[2]])
  }
  
  if(isFALSE(apr4)){vystupTest4 = rbind(vystupTest4, mat)}
  else{
    vystupTest4 = rbind(vystupTest4,apr4[[2]])
  }
}

# path = setwd("C:/Users/marek/Dropbox/Skola/Diplomovka/R/Testy data/ZavislostNaRoSigmaDelta")
# write.csv(vystupTest3, file = "testZavislostNaRoSigmaDelta3.csv", row.names = T)
# save(vystupTest3,file = "testZavislostNaRoSigmaDelta3.Rda")
# write.csv(vystupTest4, file = "testZavislostNaRoSigmaDelta4.csv", row.names = T)
# save(vystupTest4,file = "testZavislostNaRoSigmaDelta4.Rda")






#################### testy ######################################

path = setwd("~/../Desktop/Kod,testy a data pre model/Data/ZavislostNaRoSigmaDelta")
# 
load("testZavislostNaRoSigmaDelta1.Rda")
data1 = vystupTest1[,1:5]
rm(vystupTest1)
load("testZavislostNaRoSigmaDelta2.Rda")
data2 = vystupTest2[,1:5]
rm(vystupTest2)
load("testZavislostNaRoSigmaDelta3.Rda")
data3 = vystupTest3[,1:5]
rm(vystupTest3)
load("testZavislostNaRoSigmaDelta4.Rda")
data4 = vystupTest4[,1:5]
rm(vystupTest4)


dt1 = cbind(data1, rep(c(1:300), each = 30))
colnames(dt1)[6] = "odhad"
dt2 = cbind(data2, rep(c(1:300), each = 30))
colnames(dt2)[6] = "odhad"

vec = as.numeric(dt1$B != 0 & dt2$B !=0)

d1 = dt1[vec == 1,]
d2 = dt2[vec == 1,]


data_1 = data.frame.to_matrix(d1)[,1:5]
data_2 = data.frame.to_matrix(d2)[,1:5]


data_1 = as.data.frame(data_1)
data_1 = cbind(data_1,rep(c(1:30),228))
colnames(data_1) = c("B","C","D","F","G","iter")


data_2 = as.data.frame(data_2)
data_2 = cbind(data_2,rep(c(1:30),228))
colnames(data_2) = c("B","C","D","F","G","iter")


matDt1 = matrix(data = NA, nrow = 30, ncol = 5)
matDt2 = matrix(data = NA, nrow = 30, ncol = 5)



for (j in 1:5) {
  for (i in 1:30) {
    matDt1[i,j] = mean(data_1[data_1$iter == i,j], na.rm = TRUE)
    matDt2[i,j] = mean(data_2[data_2$iter == i,j], na.rm = TRUE)
  }
}




data_1 = data.frame(matDt1)
data_2 = data.frame(matDt2)
colnames(data_1) = c("B","C","D","F","G")
colnames(data_2) = c("B","C","D","F","G")



data = rbind(as.matrix(data_1[,1],ncol = 1),
             as.matrix(data_2[,1],ncol = 1),
             as.matrix(data_1[,2],ncol = 1),
             as.matrix(data_2[,2],ncol = 1),
             as.matrix(data_1[,3],ncol = 1),
             as.matrix(data_2[,3],ncol = 1),
             as.matrix(data_1[,4],ncol = 1),
             as.matrix(data_2[,4],ncol = 1),
             as.matrix(data_1[,5],ncol = 1),
             as.matrix(data_2[,5],ncol = 1))


data = cbind(data,
             rep(c(1:30),10),
             rep(c(1:5),each = 60),
             rep(rep(c(1,2), each = 30),5))
data = data.frame(data)
colnames(data) = c("data", "iter","parametre", "vstup")
data$parametre = factor(data$parametre,
                        levels = c(1,2,3,4,5),
                        labels = c("B","C","D","F","G"))
data$vstup = factor(data$vstup,
                    levels = c(1,2),
                    labels = c("užívate¾", "default"))

p1 = ggplot(data = data) + 
  geom_line(aes(x = iter, y = data, color = vstup), size = 0.7) +
  facet_grid(parametre ~., scales = "free") +
  labs(y="parametre elispy", x="poèet iterácií") +
  labs(colour = TeX("$vstup: \\rho, \\sigma^2, \\delta$")) +
  theme(legend.position="right") +
  scale_color_manual(values = c("#2196F3", "#B71C1C"))
p1





############################## druha elipsa #################################

dt3 = cbind(data3, rep(c(1:300), each = 30))
colnames(dt3)[6] = "iter1"
dt4 = cbind(data4, rep(c(1:300), each = 30))
colnames(dt4)[6] = "iter2"

vec = as.numeric(dt3$B != 0 & dt4$B !=0)

d3 = dt3[vec == 1,]
d4 = dt4[vec == 1,]

data_3 = data.frame.to_matrix(d3)[,1:5]
data_4 = data.frame.to_matrix(d4)[,1:5]



data_3 = as.data.frame(data_3)
data_3 = cbind(data_3,rep(c(1:30),299))
colnames(data_3) = c("B","C","D","F","G","iter")


data_4 = as.data.frame(data_4)
data_4 = cbind(data_4,rep(c(1:30),299))
colnames(data_4) = c("B","C","D","F","G","iter")


matDt3 = matrix(data = NA, nrow = 30, ncol = 5)
matDt4 = matrix(data = NA, nrow = 30, ncol = 5)



for (j in 1:5) {
  for (i in 1:30) {
    matDt3[i,j] = mean(data_3[data_3$iter == i,j], na.rm = TRUE)
    matDt4[i,j] = mean(data_4[data_4$iter == i,j], na.rm = TRUE)
  }
}


data_3 = data.frame(matDt3)
data_4 = data.frame(matDt4)
colnames(data_3) = c("B","C","D","F","G")
colnames(data_4) = c("B","C","D","F","G")


dataB = rbind(as.matrix(data_3[,1],ncol = 1),
              as.matrix(data_4[,1],ncol = 1),
              as.matrix(data_3[,2],ncol = 1),
              as.matrix(data_4[,2],ncol = 1),
              as.matrix(data_3[,3],ncol = 1),
              as.matrix(data_4[,3],ncol = 1),
              as.matrix(data_3[,4],ncol = 1),
              as.matrix(data_4[,4],ncol = 1),
              as.matrix(data_3[,5],ncol = 1),
              as.matrix(data_4[,5],ncol = 1))


dataB = cbind(dataB,
             rep(c(1:30),10),
             rep(c(1:5),each = 60),
             rep(rep(c(1,2), each = 30),5))
dataB = data.frame(dataB)
colnames(dataB) = c("data", "iter","parametre", "vstup")
dataB$parametre = factor(dataB$parametre,
                         levels = c(1,2,3,4,5),
                         labels = c("B","C","D","F","G"))
dataB$vstup = factor(dataB$vstup,
                     levels = c(1,2),
                     labels = c("užívate¾", "default"))

p2 = ggplot(data = dataB) + 
        geom_line(aes(x = iter, y = data, color = vstup), size = 0.7) +
        facet_grid(parametre ~., scales = "free") +
        labs(y="parametre elispy", x="poèet iterácií") +
        labs(colour = TeX("$vstup: \\rho, \\sigma^2, \\delta$")) +
        theme(legend.position="right") +
        scale_color_manual(values = c("#2196F3", "#B71C1C"))
p2



