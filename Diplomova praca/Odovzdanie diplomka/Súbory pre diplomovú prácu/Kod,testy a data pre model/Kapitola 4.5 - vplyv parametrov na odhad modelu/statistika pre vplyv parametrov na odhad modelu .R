
library(ggplot2)
library(Rcpp)
library(gridExtra)
library(latex2exp)
library(GGally)


rm(list = ls())

setwd("~/../Desktop/Kod,testy a data pre model/Data/GridPreRoSigmaDelta/GridSDeltou")

load("vystupGrid1.Rda")
vystupGrid1 = vystupGrid
rm(vystupGrid)
load("vystupGrid2.Rda")
vystupGrid2 = vystupGrid
rm(vystupGrid)
load("vystupGrid3.Rda")
vystupGrid3 = vystupGrid
rm(vystupGrid)
load("vystupGrid4.Rda")
vystupGrid4 = vystupGrid
rm(vystupGrid)
load("vystupGrid5.Rda")
vystupGrid5 = vystupGrid
rm(vystupGrid)
load("vystupGrid6.Rda")
vystupGrid6 = vystupGrid
rm(vystupGrid)
load("vystupGrid7.Rda")
vystupGrid7 = vystupGrid
rm(vystupGrid)
load("vystupGrid8.Rda")
vystupGrid8 = vystupGrid
rm(vystupGrid)

vystupGrid = rbind(vystupGrid1,
                   vystupGrid2,
                   vystupGrid3,
                   vystupGrid4,
                   vystupGrid5,
                   vystupGrid6,
                   vystupGrid7,
                   vystupGrid8)

save(vystupGrid,file = "vystupGrid.Rda")

rm(vystupGrid1)
rm(vystupGrid2)
rm(vystupGrid3)
rm(vystupGrid4)
rm(vystupGrid5)
rm(vystupGrid6)
rm(vystupGrid7)
rm(vystupGrid8)
gc()


data = vystupGrid

data = data[data$oRo>-0.3 & 
            data$oRo<1.2,]
data = data[data$oSigma>-0.01 &
            data$oSigma<0.25,]
data = data[data$oDelta>-0.25 & 
            data$oDelta<0.25,]




# 
# znazornenie rozdielu medzi ro a odhadnute ro
# 
p1 = ggplot(data = data) +
  geom_point(aes(x = ro, y = oRo, colour = ro), alpha = 0.5,
             position = position_jitter(width = 0.001, height = 0.001),
             size = 1) +
  geom_abline(slope = 1, alpha = 0.8, color = "red", size = 1) +
  xlab(TeX("$\\rho$")) +
  ylab(TeX("$\\hat{\\rho}$")) +
  theme(legend.position = "bottom")
 


# 
# znazornenie rozdielu medzi sigmaS a rSigma
# 
p2 = ggplot(data = data) +
  geom_point(aes(x = sigma, y = oSigma, colour = sigma), alpha = 0.5,
             position = position_jitter(width = 0.003, height = 0.003),
             size = 1) +
  geom_abline(slope = 1, alpha = 0.8, color = "red", size = 1) +
  xlab(TeX("$\\sigma^2$")) +
  ylab(TeX("$\\hat{\\sigma^2}$")) +
  theme(legend.position = "bottom")


# 
# znazornenie rozdielu medzi deltaS a delta
# 
p3 = ggplot(data = data) +
  geom_point(aes(x = delta, y = oDelta, colour = delta), alpha = 0.5,
             position = position_jitter(width = 0.003, height = 0.003),
             size = 1) +
  geom_abline(slope = 1, alpha = 0.8, color = "red", size = 1) +
  xlab(TeX("$\\delta$")) +
  ylab(TeX("$\\hat{\\delta}$")) +
  theme(legend.position = "bottom")



p1
p2
p3
grid.arrange(p1,p2,p3,ncol = 3)


# Histohram pre Ro
# 
rezRo1 = data[data$ro > 0.01 & data$ro < 0.05,]
rezRo2 = data[data$ro > 0.23 & data$ro < 0.27,]
rezRo3 = data[data$ro > 0.48 & data$ro < 0.52,]
rezRo4 = data[data$ro > 0.73 & data$ro < 0.77,]
rezRo5 = data[data$ro > 0.95 & data$ro < 0.99,]

h1 = ggplot(data = rezRo1) +
  geom_histogram(aes(oRo),alpha = 0.5, binwidth = 0.03, color = "grey", fill = "#4A148C") +
  geom_vline(xintercept = 0, color = "red") +
  ggtitle(TeX("rez v $\\rho = 0$")) +
  xlab(TeX("$\\rho$"))

h2 = ggplot(data = rezRo2) +
  geom_histogram(aes(oRo),alpha = 0.5, binwidth = 0.03, color = "grey", fill = "#1B5E20") +
  geom_vline(xintercept = 0.25, color = "red") +
  ggtitle(TeX("rez v $\\rho = 0.25$")) +
  xlab(TeX("$\\rho$"))

h3 = ggplot(data = rezRo3) +
  geom_histogram(aes(oRo),alpha = 0.5, binwidth = 0.03, color = "grey", fill = "#B71C1C") +
  geom_vline(xintercept = 0.5, color = "red") +
  ggtitle(TeX("rez v $\\rho = 0.5$")) +
  xlab(TeX("$\\rho$"))

h4 = ggplot(data = rezRo4) +
  geom_histogram(aes(oRo),alpha = 0.5, binwidth = 0.02, color = "grey", fill = "#E65100") +
  geom_vline(xintercept = 0.75, color = "red") +
  ggtitle(TeX("rez v $\\rho = 0.75$")) +
  xlab(TeX("$\\rho$"))

h5 = ggplot(data = rezRo5) +
  geom_histogram(aes(oRo),alpha = 0.5, binwidth = 0.01, color = "grey", fill = "#3E2723") +
  geom_vline(xintercept = 1, color = "red") +
  ggtitle(TeX("rez v $\\rho = 0.99$")) +
  xlab(TeX("$\\rho$"))

g1 = grid.arrange(h1,h2,h3, h4, h5, ncol = 1)
grid1 = grid.arrange(p1,g1, ncol = 2)





# Histohram pre Sigma
# 
rezSigma1 = data[data$sigma > 0.001 & data$sigma < 0.009,]
rezSigma2 = data[data$sigma > 0.046 & data$sigma < 0.054,]
rezSigma3 = data[data$sigma > 0.096 & data$sigma < 0.104,]
rezSigma4 = data[data$sigma > 0.140 & data$sigma < 0.158,]
rezSigma5 = data[data$sigma > 0.180 & data$sigma < 0.200,]

h6 = ggplot(data = rezSigma1) +
  geom_histogram(aes(oSigma),alpha = 0.5, binwidth = 0.0004, color = "grey", fill = "#4A148C") +
  geom_vline(xintercept = 0.005, color = "red") +
  ggtitle(TeX("rez v $\\sigma^2 = 0.005")) +
  xlab(TeX("$\\sigma^2$"))

h7 = ggplot(data = rezSigma2) +
  geom_histogram(aes(oSigma),alpha = 0.5, binwidth = 0.004, color = "grey", fill = "#1B5E20") +
  geom_vline(xintercept = 0.05, color = "red") +
  ggtitle(TeX("rez v $\\sigma^2 = 0.05")) +
  xlab(TeX("$\\sigma^2$"))

h8 = ggplot(data = rezSigma3) +
  geom_histogram(aes(oSigma),alpha = 0.5, binwidth = 0.005, color = "grey", fill = "#B71C1C") +
  geom_vline(xintercept = 0.10, color = "red") +
  ggtitle(TeX("rez v $\\sigma^2 = 0.10")) +
  xlab(TeX("$\\sigma^2$"))

h9 = ggplot(data = rezSigma4) +
  geom_histogram(aes(oSigma),alpha = 0.5, binwidth = 0.007, color = "grey", fill = "#E65100") +
  geom_vline(xintercept = 0.145, color = "red") +
  ggtitle(TeX("rez v $\\sigma^2 = 0.15")) +
  xlab(TeX("$\\sigma^2$"))

h10 = ggplot(data = rezSigma5) +
  geom_histogram(aes(oSigma),alpha = 0.5, binwidth = 0.007, color = "grey", fill = "#3E2723") +
  geom_vline(xintercept = 0.19, color = "red") +
  ggtitle(TeX("rez v $\\sigma^2 = 0.20")) +
  xlab(TeX("$\\sigma^2$"))

g2 = grid.arrange(h6,h7,h8,h9,h10, ncol = 1)
grid2 = grid.arrange(p2,g2, ncol = 2)






# Histohram pre Delta
# 
rezDelta1 = data[data$delta > 0.0002502 & data$delta < 0.0007796,]
rezDelta2 = data[data$delta > 0.02525 & data$delta < 0.04,]
rezDelta3 = data[data$delta == 0.05270,]
rezDelta4 = data[data$delta == 0.06349,]
rezDelta5 = data[data$delta == 0.07796,]

h11 = ggplot(data = rezDelta1) +
  geom_histogram(aes(oDelta),alpha = 0.5, binwidth = 0.01, color = "grey", fill = "#4A148C") +
  geom_vline(xintercept = 0.0005, color = "red") +
  ggtitle(TeX("rez v $\\delta = 0.0005")) +
  xlab(TeX("$\\delta$"))

h12 = ggplot(data = rezDelta2) +
  geom_histogram(aes(oDelta),alpha = 0.5, binwidth = 0.01, color = "grey", fill = "#1B5E20") +
  geom_vline(xintercept = 0.032, color = "red") +
  ggtitle(TeX("rez v $\\delta = 0.032")) +
  xlab(TeX("$\\delta$"))

h13 = ggplot(data = rezDelta3) +
  geom_histogram(aes(oDelta),alpha = 0.5, binwidth = 0.008, color = "grey", fill = "#B71C1C") +
  geom_vline(xintercept = 0.05270, color = "red") +
  ggtitle(TeX("rez v $\\delta = 0.05270")) +
  xlab(TeX("$\\delta$"))

h14 = ggplot(data = rezDelta4) +
  geom_histogram(aes(oDelta),alpha = 0.5, binwidth = 0.011, color = "grey", fill = "#E65100") +
  geom_vline(xintercept = 0.06349, color = "red") +
  ggtitle(TeX("rez v $\\delta = 0.06349")) +
  xlab(TeX("$\\delta$"))

h15 = ggplot(data = rezDelta5) +
  geom_histogram(aes(oDelta),alpha = 0.5, binwidth = 0.010, color = "grey", fill = "#3E2723") +
  geom_vline(xintercept = 0.07796, color = "red") +
  ggtitle(TeX("rez v $\\delta = 0.07796")) +
  xlab(TeX("$\\delta$"))

g3 = grid.arrange(h11,h12,h13,h14,h15, ncol = 1)
grid3 = grid.arrange(p3,g3, ncol = 2)









































