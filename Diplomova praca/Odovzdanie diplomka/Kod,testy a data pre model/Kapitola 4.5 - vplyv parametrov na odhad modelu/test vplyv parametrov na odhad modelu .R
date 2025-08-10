
library(conics)
library(ggplot2)
library(gridExtra)
library(corpcor)
library(latex2exp)
library(grid)
library(Rfast)


rm(list= ls())
source("~/../Desktop/Kod,testy a data pre model/Kapitola 3 - funkcie model/Funkcie model.R")


# je to rozdelene do 8 casti. Bolo to spustene na 8-mich PC, kvoli dlhemu casu pre jeden
# pocitac.


# nastavenie gridu 1
# 
ro     = seq(from = 0.01, to = 0.1325, length.out = 30 )  # povodne 200
sigma  = seq(from = 0.001, to = 0.2, length.out = 30) # povodne 50
delta1 = c(0, 0.0002502, 0.0002867, 0.0003284, 0.0003798, 0.000444, 0.0005270, 0.0006349, 0.0007796)
delta2 = c(0, 0.02525,   0.02867,   0.03284,   0.03798,   0.04,     0.05270,   0.06349,   0.07796)

# dataframe pre ulozenie odhadnutych dat z gridu  
# 
vystupGrid = data.frame(matrix(NA, nrow = (length(ro)*length(sigma)*length(delta1)),
                               ncol = 24))
colnames(vystupGrid) = c("B","C","D","F","G","ro","sigma","delta",
                         "oB","oC","oD","oF","oG","oRo","oSigma","oDelta",
                         "min1","min2","min3",
                         "Q_1","Q_2","Q_3","Q_4","Q_5")

set.seed(12345)
tm = proc.time()
iteracia = 1
for (k in 1:length(ro)) {
  for (j in 1:length(sigma)) {
    if(sigma[j] <= 0.1){
      delta = delta1}
    else{delta = delta2}
    for (i in 1:length(delta)) {
      cat("iteracia: ",iteracia,"\n")
      par = paramElipsa(3,-2,-5,-4,10, ro =ro[k], sigma = sigma[j], delta = delta[i])
      parApr = c(0,1,0)
      apr = aproxData(par, parApr, 100, 10, plot = F, vypis = F)
      vystupGrid[iteracia,] = apr
      iteracia = iteracia + 1
    }
  }
}
proc.time() - tm

# write.csv(vystupGrid, file = "vystupGrid1.csv", row.names = F)
# save(vystupGrid,file = "vystupGrid1.Rda")





# nastavenie gridu 2
# 
ro     = seq(from = 0.1325, to = 0.255, length.out = 30 )  # povodne 200
sigma  = seq(from = 0.001, to = 0.2, length.out = 30) # povodne 50
delta1 = c(0, 0.0002502, 0.0002867, 0.0003284, 0.0003798, 0.000444, 0.0005270, 0.0006349)
delta2 = c(0, 0.02525,   0.02867,   0.03284,   0.03798,   0.04,     0.05270,   0.06349)

# dataframe pre ulozenie odhadnutych dat z gridu  
# 
vystupGrid = data.frame(matrix(NA, nrow = (length(ro)*length(sigma)*length(delta1)),
                               ncol = 24))
colnames(vystupGrid) = c("B","C","D","F","G","ro","sigma","delta",
                         "oB","oC","oD","oF","oG","oRo","oSigma","oDelta",
                         "min1","min2","min3",
                         "Q_1","Q_2","Q_3","Q_4","Q_5")

set.seed(12345)
tm = proc.time()
iteracia = 1
for (k in 1:length(ro)) {
  for (j in 1:length(sigma)) {
    if(sigma[j] <= 0.1){
      delta = delta1}
    else{delta = delta2}
    for (i in 1:length(delta)) {
      cat("iteracia: ",iteracia,"\n")
      par = paramElipsa(3,-2,-5,-4,10, ro =ro[k], sigma = sigma[j], delta = delta[i])
      parApr = c(0,1,0)
      apr = aproxData(par, parApr, 100, 10, plot = F, vypis = F)
      vystupGrid[iteracia,] = apr
      iteracia = iteracia + 1
    }
  }
}
proc.time() - tm

# write.csv(vystupGrid, file = "vystupGrid2.csv", row.names = F)
# save(vystupGrid,file = "vystupGrid2.Rda")





# nastavenie gridu 3
# 
ro     = seq(from = 0.255, to = 0.3775, length.out = 30 )  # povodne 200
sigma  = seq(from = 0.001, to = 0.2, length.out = 30) # povodne 50
delta1 = c(0, 0.0002502, 0.0002867, 0.0003284, 0.0003798, 0.000444, 0.0005270)
delta2 = c(0, 0.02525,   0.02867,   0.03284,   0.03798,   0.04,     0.05270)

# dataframe pre ulozenie odhadnutych dat z gridu  
# 
vystupGrid = data.frame(matrix(NA, nrow = (length(ro)*length(sigma)*length(delta1)),
                               ncol = 24))
colnames(vystupGrid) = c("B","C","D","F","G","ro","sigma","delta",
                         "oB","oC","oD","oF","oG","oRo","oSigma","oDelta",
                         "min1","min2","min3",
                         "Q_1","Q_2","Q_3","Q_4","Q_5")

set.seed(12345)
tm = proc.time()
iteracia = 1
for (k in 1:length(ro)) {
  for (j in 1:length(sigma)) {
    if(sigma[j] <= 0.1){
      delta = delta1}
    else{delta = delta2}
    for (i in 1:length(delta)) {
      cat("iteracia: ",iteracia,"\n")
      par = paramElipsa(3,-2,-5,-4,10, ro =ro[k], sigma = sigma[j], delta = delta[i])
      parApr = c(0,1,0)
      apr = aproxData(par, parApr, 100, 10, plot = F, vypis = F)
      vystupGrid[iteracia,] = apr
      iteracia = iteracia + 1
    }
  }
}
proc.time() - tm

# write.csv(vystupGrid, file = "vystupGrid3.csv", row.names = F)
# save(vystupGrid,file = "vystupGrid3.Rda")




# nastavenie gridu 4
# 
ro     = seq(from = 0.3775, to = 0.5, length.out = 30 )  # povodne 200
sigma  = seq(from = 0.001, to = 0.2, length.out = 30) # povodne 50
delta1 = c(0, 0.0002502, 0.0002867, 0.0003284, 0.0003798, 0.000444)
delta2 = c(0, 0.02525,   0.02867,   0.03284,   0.03798,   0.04)

# dataframe pre ulozenie odhadnutych dat z gridu  
# 
vystupGrid = data.frame(matrix(NA, nrow = (length(ro)*length(sigma)*length(delta1)),
                               ncol = 24))
colnames(vystupGrid) = c("B","C","D","F","G","ro","sigma","delta",
                         "oB","oC","oD","oF","oG","oRo","oSigma","oDelta",
                         "min1","min2","min3",
                         "Q_1","Q_2","Q_3","Q_4","Q_5")

set.seed(12345)
tm = proc.time()
iteracia = 1
for (k in 1:length(ro)) {
  for (j in 1:length(sigma)) {
    if(sigma[j] <= 0.1){
      delta = delta1}
    else{delta = delta2}
    for (i in 1:length(delta)) {
      cat("iteracia: ",iteracia,"\n")
      par = paramElipsa(3,-2,-5,-4,10, ro =ro[k], sigma = sigma[j], delta = delta[i])
      parApr = c(0,1,0)
      apr = aproxData(par, parApr, 100, 10, plot = F, vypis = F)
      vystupGrid[iteracia,] = apr
      iteracia = iteracia + 1
    }
  }
}
proc.time() - tm

# write.csv(vystupGrid, file = "vystupGrid4.csv", row.names = F)
# save(vystupGrid,file = "vystupGrid4.Rda")





# nastavenie gridu 5
# 
ro     = seq(from = 0.5, to = 0.6225, length.out = 30 )  # povodne 200
sigma  = seq(from = 0.001, to = 0.2, length.out = 30) # povodne 50
delta1 = c(0, 0.0002502, 0.0002867, 0.0003284, 0.0003798)
delta2 = c(0, 0.02525,   0.02867,   0.03284,   0.03798)

# dataframe pre ulozenie odhadnutych dat z gridu  
# 
vystupGrid = data.frame(matrix(NA, nrow = (length(ro)*length(sigma)*length(delta1)),
                               ncol = 24))
colnames(vystupGrid) = c("B","C","D","F","G","ro","sigma","delta",
                         "oB","oC","oD","oF","oG","oRo","oSigma","oDelta",
                         "min1","min2","min3",
                         "Q_1","Q_2","Q_3","Q_4","Q_5")

set.seed(12345)
tm = proc.time()
iteracia = 1
for (k in 1:length(ro)) {
  for (j in 1:length(sigma)) {
    if(sigma[j] <= 0.1){
      delta = delta1}
    else{delta = delta2}
    for (i in 1:length(delta)) {
      cat("iteracia: ",iteracia,"\n")
      par = paramElipsa(3,-2,-5,-4,10, ro =ro[k], sigma = sigma[j], delta = delta[i])
      parApr = c(0,1,0)
      apr = aproxData(par, parApr, 100, 10, plot = F, vypis = F)
      vystupGrid[iteracia,] = apr
      iteracia = iteracia + 1
    }
  }
}
proc.time() - tm

# write.csv(vystupGrid, file = "vystupGrid5.csv", row.names = F)
# save(vystupGrid,file = "vystupGrid5.Rda")





# nastavenie gridu 6
# 
ro     = seq(from = 0.6225, to = 0.745, length.out = 30 )  # povodne 200
sigma  = seq(from = 0.001, to = 0.2, length.out = 30) # povodne 50
delta1 = c(0, 0.0002502, 0.0002867, 0.0003284)
delta2 = c(0, 0.02525,   0.02867,   0.03284)

# dataframe pre ulozenie odhadnutych dat z gridu  
# 
vystupGrid = data.frame(matrix(NA, nrow = (length(ro)*length(sigma)*length(delta1)),
                               ncol = 24))
colnames(vystupGrid) = c("B","C","D","F","G","ro","sigma","delta",
                         "oB","oC","oD","oF","oG","oRo","oSigma","oDelta",
                         "min1","min2","min3",
                         "Q_1","Q_2","Q_3","Q_4","Q_5")

set.seed(12345)
tm = proc.time()
iteracia = 1
for (k in 1:length(ro)) {
  for (j in 1:length(sigma)) {
    if(sigma[j] <= 0.1){
      delta = delta1}
    else{delta = delta2}
    for (i in 1:length(delta)) {
      cat("iteracia: ",iteracia,"\n")
      par = paramElipsa(3,-2,-5,-4,10, ro =ro[k], sigma = sigma[j], delta = delta[i])
      parApr = c(0,1,0)
      apr = aproxData(par, parApr, 100, 10, plot = F, vypis = F)
      vystupGrid[iteracia,] = apr
      iteracia = iteracia + 1
    }
  }
}
proc.time() - tm

# write.csv(vystupGrid, file = "vystupGrid6.csv", row.names = F)
# save(vystupGrid,file = "vystupGrid6.Rda")





# nastavenie gridu 7
# 
ro     = seq(from = 0.745, to = 0.8675, length.out = 30 )  # povodne 200
sigma  = seq(from = 0.001, to = 0.2, length.out = 30) # povodne 50
delta1 = c(0, 0.0002502, 0.0002867)
delta2 = c(0, 0.02525,   0.02867)

# dataframe pre ulozenie odhadnutych dat z gridu  
# 
vystupGrid = data.frame(matrix(NA, nrow = (length(ro)*length(sigma)*length(delta1)),
                               ncol = 24))
colnames(vystupGrid) = c("B","C","D","F","G","ro","sigma","delta",
                         "oB","oC","oD","oF","oG","oRo","oSigma","oDelta",
                         "min1","min2","min3",
                         "Q_1","Q_2","Q_3","Q_4","Q_5")

set.seed(12345)
tm = proc.time()
iteracia = 1
for (k in 1:length(ro)) {
  for (j in 1:length(sigma)) {
    if(sigma[j] <= 0.1){
      delta = delta1}
    else{delta = delta2}
    for (i in 1:length(delta)) {
      cat("iteracia: ",iteracia,"\n")
      par = paramElipsa(3,-2,-5,-4,10, ro =ro[k], sigma = sigma[j], delta = delta[i])
      parApr = c(0,1,0)
      apr = aproxData(par, parApr, 100, 10, plot = F, vypis = F)
      vystupGrid[iteracia,] = apr
      iteracia = iteracia + 1
    }
  }
}
proc.time() - tm

# write.csv(vystupGrid, file = "vystupGrid7.csv", row.names = F)
# save(vystupGrid,file = "vystupGrid7.Rda")



# nastavenie gridu 8
# 
ro     = seq(from = 0.8675, to = 0.99, length.out = 30 )  # povodne 200
sigma  = seq(from = 0.001, to = 0.2, length.out = 30) # povodne 50
delta1 = c(0, 0.00025)
delta2 = c(0, 0.02525)

# dataframe pre ulozenie odhadnutych dat z gridu  
# 
vystupGrid = data.frame(matrix(NA, nrow = (length(ro)*length(sigma)*length(delta1)),
                               ncol = 24))
colnames(vystupGrid) = c("B","C","D","F","G","ro","sigma","delta",
                         "oB","oC","oD","oF","oG","oRo","oSigma","oDelta",
                         "min1","min2","min3",
                         "Q_1","Q_2","Q_3","Q_4","Q_5")

set.seed(12345)
tm = proc.time()
iteracia = 1
for (k in 1:length(ro)) {
  for (j in 1:length(sigma)) {
    if(sigma[j] <= 0.1){
      delta = delta1}
    else{delta = delta2}
    for (i in 1:length(delta)) {
      cat("iteracia: ",iteracia,"\n")
      par = paramElipsa(3,-2,-5,-4,10, ro =ro[k], sigma = sigma[j], delta = delta[i])
      parApr = c(0,1,0)
      apr = aproxData(par, parApr, 100, 10, plot = F, vypis = F)
      vystupGrid[iteracia,] = apr
      iteracia = iteracia + 1
    }
  }
}
proc.time() - tm

# write.csv(vystupGrid, file = "vystupGrid8.csv", row.names = F)
# save(vystupGrid,file = "vystupGrid8.Rda")




































