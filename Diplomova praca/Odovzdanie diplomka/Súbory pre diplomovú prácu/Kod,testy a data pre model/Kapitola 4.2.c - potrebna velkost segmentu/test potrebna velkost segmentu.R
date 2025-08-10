library(conics)
library(ggplot2)
library(gridExtra)
library(corpcor)
library(latex2exp)
library(grid)
library(Rfast)


rm(list= ls())

# nacitane funkcie su identicke ako v zakladnej sade. Ale v tomto subore su doplnene pomecne funkcie
# ktore su pouzivane v testovani. 
# 
source("~/../Desktop/Kod,testy a data pre model/Kapitola 4.2.c - potrebna velkost segmentu/funkcie potrebna velkost segmentu.R")


# generovanie dat pre testovane velkosti segmentu potrebneho na odhad parametrov
# modelu. Je vygenerovanych 4 sady dat. A to v rozmedzi 500,700,1000,1500.
# Parametre pre generovanie su identicke ako v diplomovej praci
# 
par  = paramElipsa(3,-2,-5,-4,10, 0.01,0.002,0.0001)
data = genDataOnElipse(3,-2,-5,-4,10,500)


path = setwd("~/../Desktop/Kod,testy a data pre model/Data/Data na odhad velkosti segmentov/Data_na_elipse_a_zasumene")
# write.csv(data, file = "dat_500_elipsa.csv", row.names = T)
# save(data,file = "dat_500_elipsa.Rda")
# write.csv(data, file = "dat_500_0.01_0.002_0.0001.csv", row.names = T)
# save(data,file = "dat_500_0.01_0.002_0.0001.Rda")




# odhady pre data 500 700 1000 1500
# 

# odhad pre 500 dat
# 
load("dat_500_0.01_0.002_0.0001.Rda")
odhad = data.frame(matrix(data = NA, nrow = 28, ncol = 18))
colnames(odhad) = c("B","C","D","F","G",
                    "ro","sigma","delta",
                    "min1","min2","min3",
                    "Q1","Q2","Q3","Q4","Q5",
                    "od","do")
k = 1
l = 1
v = c(71,142,213,284,355,426,500)
m = 1

for (i in c(1:7)) {
  for (j in c(i:7)) {
    # cat(l,"",v[j],"")
    odhad[m,1:16] = odhadZRealDat(data[l:v[j],],8,vypis = T)
    odhad[m,17:18] = c(l,v[j])
    l = v[k]+1
    k = k+1
    m = m+1
  }
  k = 1
  l = 1
  # cat("\n")
}

# write.csv(odhad, file = "odhad_500_dat.csv", row.names = T)
# save(odhad,file = "odhad_500_dat.Rda")




# odhad pre 700 dat
# 
load("dat_700_0.01_0.002_0.0001.Rda")
odhad = data.frame(matrix(data = NA, nrow = 28, ncol = 18))
colnames(odhad) = c("B","C","D","F","G",
                    "ro","sigma","delta",
                    "min1","min2","min3",
                    "Q1","Q2","Q3","Q4","Q5",
                    "od","do")
k = 1
l = 1
v = c(100,200,300,400,500,600,700)
m = 1

for (i in c(1:7)) {
  for (j in c(i:7)) {
    # cat(l,"",v[j],"")
    odhad[m,1:16] = odhadZRealDat(data[l:v[j],],8,vypis = T)
    odhad[m,17:18] = c(l,v[j])
    l = v[k]+1
    k = k+1
    m = m+1
  }
  k = 1
  l = 1
  # cat("\n")
}

# write.csv(odhad, file = "odhad_700_dat.csv", row.names = T)
# save(odhad,file = "odhad_700_dat.Rda")





# odhad pre 1000 dat
# 
load("dat_1000_0.01_0.002_0.0001.Rda")
odhad = data.frame(matrix(data = NA, nrow = 28, ncol = 18))
colnames(odhad) = c("B","C","D","F","G",
                    "ro","sigma","delta",
                    "min1","min2","min3",
                    "Q1","Q2","Q3","Q4","Q5",
                    "od","do")
k = 1
l = 1
v = c(143,286,429,572,715,858,1000)
m = 1

for (i in c(1:7)) {
  for (j in c(i:7)) {
    # cat(l,"",v[j],"")
    odhad[m,1:16] = odhadZRealDat(data[l:v[j],],8,vypis = T)
    odhad[m,17:18] = c(l,v[j])
    l = v[k]+1
    k = k+1
    m = m+1
  }
  k = 1
  l = 1
  # cat("\n")
}

# write.csv(odhad, file = "odhad_1000_dat.csv", row.names = T)
# save(odhad,file = "odhad_1000_dat.Rda")





# odhad pre 1500 dat
# 
load("dat_1500_0.01_0.002_0.0001.Rda")
data = data3
rm(data3)
odhad = data.frame(matrix(data = NA, nrow = 28, ncol = 18))
colnames(odhad) = c("B","C","D","F","G",
                    "ro","sigma","delta",
                    "min1","min2","min3",
                    "Q1","Q2","Q3","Q4","Q5",
                    "od","do")
k = 1
l = 1
v = c(214,428,642,856,1070,1284,1500)
m = 1

for (i in c(1:7)) {
  for (j in c(i:7)) {
    # cat(l,"",v[j],"")
    odhad[m,1:16] = odhadZRealDat(data[l:v[j],],8,vypis = T)
    odhad[m,17:18] = c(l,v[j])
    l = v[k]+1
    k = k+1
    m = m+1
  }
  k = 1
  l = 1
  # cat("\n")
}

# write.csv(odhad, file = "odhad_1500_dat.csv", row.names = T)
# save(odhad,file = "odhad_1500_dat.Rda")



################################# Kruznica ############################
#######################################################################


par  = paramElipsa(1,-1/4,-14,-12,60, 0.1, 0.01, 0.0001)
data = genDataOnElipse(1,-1/4,-14,-12,60,500)


# write.csv(data, file = "dat_1000_kruznica.csv", row.names = T)
# save(data,file = "dat_1000_kruznica.Rda")
# write.csv(data, file = "dat_1000_0.1_0.01_0.0001.csv", row.names = T)
# save(data,file = "dat_1000_0.1_0.01_0.0001.Rda")
# 
# 
path = setwd("~/../Desktop/Kod,testy a data pre model/Data/Data na odhad velkosti segmentov/Data_na_elipse_a_zasumene_kruznica")



# odhady pre data 500 700 1000 1500

# odhad pre 500 dat
# 
load("dat_500_0.1_0.01_0.0001.Rda")
odhad = data.frame(matrix(data = NA, nrow = 28, ncol = 18))
colnames(odhad) = c("B","C","D","F","G",
                    "ro","sigma","delta",
                    "min1","min2","min3",
                    "Q1","Q2","Q3","Q4","Q5",
                    "od","do")
k = 1
l = 1
v = c(71,142,213,284,355,426,500)
m = 1

for (i in c(1:7)) {
  for (j in c(i:7)) {
    # cat(l,"",v[j],"")
    odhad[m,1:16] = odhadZRealDat(data[l:v[j],],8,vypis = T)
    odhad[m,17:18] = c(l,v[j])
    l = v[k]+1
    k = k+1
    m = m+1
  }
  k = 1
  l = 1
  # cat("\n")
}
# write.csv(odhad, file = "odhad_500_dat.csv", row.names = T)
# save(odhad,file = "odhad_500_dat.Rda")




# odhad pre 700 dat
# 
load("dat_700_0.1_0.01_0.0001.Rda")
odhad = data.frame(matrix(data = NA, nrow = 28, ncol = 18))
colnames(odhad) = c("B","C","D","F","G",
                    "ro","sigma","delta",
                    "min1","min2","min3",
                    "Q1","Q2","Q3","Q4","Q5",
                    "od","do")
k = 1
l = 1
v = c(100,200,300,400,500,600,700)
m = 1

for (i in c(1:7)) {
  for (j in c(i:7)) {
    # cat(l,"",v[j],"")
    odhad[m,1:16] = odhadZRealDat(data[l:v[j],],8,vypis = T)
    odhad[m,17:18] = c(l,v[j])
    l = v[k]+1
    k = k+1
    m = m+1
  }
  k = 1
  l = 1
  # cat("\n")
}
# write.csv(odhad, file = "odhad_700_dat.csv", row.names = T)
# save(odhad,file = "odhad_700_dat.Rda")





# odhad pre 1000 dat
# 
load("dat_1000_0.1_0.01_0.0001.Rda")
odhad = data.frame(matrix(data = NA, nrow = 28, ncol = 18))
colnames(odhad) = c("B","C","D","F","G",
                    "ro","sigma","delta",
                    "min1","min2","min3",
                    "Q1","Q2","Q3","Q4","Q5",
                    "od","do")
k = 1
l = 1
v = c(143,286,429,572,715,858,1000)
m = 1

for (i in c(1:7)) {
  for (j in c(i:7)) {
    # cat(l,"",v[j],"")
    odhad[m,1:16] = odhadZRealDat(data[l:v[j],],8,vypis = T)
    odhad[m,17:18] = c(l,v[j])
    l = v[k]+1
    k = k+1
    m = m+1
  }
  k = 1
  l = 1
  # cat("\n")
}
# write.csv(odhad, file = "odhad_1000_dat.csv", row.names = T)
# save(odhad,file = "odhad_1000_dat.Rda")





# odhad pre 1500 dat
# 
load("dat_1500_0.1_0.01_0.0001.Rda")
odhad = data.frame(matrix(data = NA, nrow = 28, ncol = 18))
colnames(odhad) = c("B","C","D","F","G",
                    "ro","sigma","delta",
                    "min1","min2","min3",
                    "Q1","Q2","Q3","Q4","Q5",
                    "od","do")
k = 1
l = 1
v = c(214,428,642,856,1070,1284,1500)
m = 1

for (i in c(1:7)) {
  for (j in c(i:7)) {
    # cat(l,"",v[j],"")
    odhad[m,1:16] = odhadZRealDat(data[l:v[j],],8,vypis = T)
    odhad[m,17:18] = c(l,v[j])
    l = v[k]+1
    k = k+1
    m = m+1
  }
  k = 1
  l = 1
  # cat("\n")
}
# write.csv(odhad, file = "odhad_1500_dat.csv", row.names = T)
# save(odhad,file = "odhad_1500_dat.Rda")








