
# pouzivane baliky
#
# library(conics)
# library(ggplot2)
# library(gridExtra)
# library(corpcor)
# library(latex2exp)
# library(foreach)
# library(doParallel)
# library(Rfast)
# library(gpuR)
#



############0. Vygenerovanie a vykreslenie dat na elipse  #############

# Funkcia pre krivku elipsy 
#
# Sluzi na vygenerovanie 
# vstupnych hodnot, pre pocitanie  a ako krivka do grafu.
# Je to horna a spodna cast krivky,
# preto je funkcia oznacena "p" alebo "m" - (plus, minus)
#
# parametre:
#            - x: premenna
#              B: parameter elipsy
#              C: parameter elipsy
#              D: parameter elipsy
#              F: parameter elipsy
#              G: parameter elipsy
#
#    vystup: - vystupna hodnota je len cislo. Sluzi ako klasicka
#              funkcia.
#
getElipse_p = function(x,B,C,D,F,G){
  y = (-(C*x + F) + sqrt((C*x+F)^2 - 4*B*(x^2 + D*x + G)))/(2*B) 
  return(y)
}
getElipse_m = function(x,B,C,D,F,G){
  y = (-(C*x + F) - sqrt((C*x+F)^2 - 4*B*(x^2 + D*x + G)))/(2*B)  
  return(y)
}




# Funkcia urcujuca definicny obor pre elispu
#
# vratenie hornej a dolnej hranice definicneho oboru pre
# hodnotu x. Je to potrebne pre vykreslovanie grafu a aj
# pre vygenerovanie dat. 
#
# vo vnutri je pouzita kniznica conics, je to na hladanie
# vrcholov elipsy, hlavnych os, atd...
#
# parametre:
#            - B: parameter elipsy
#              C: parameter elipsy
#              D: parameter elipsy
#              F: parameter elipsy
#              G: parameter elipsy
#
#    vystup: - dataframe s minimom a maximom definicneho 
#              oboru pre funkciu getElispe
#
getXIntervalForElipse = function(B,C,D,F,G){
  v   =  c(1,C,B,D,F,G)
  res = conicPlot(v, type = "n")
  
  # osetrovanie podmienky, ak mame kruznicu. To funkcia
  # optimize nevie rozhodnut 
  if(res$vertices$x[1] == res$vertices$x[3]){
    minimum = res$vertices$x[2]
    maximum = res$vertices$x[4]
  }  
  else{
    min = (res$vertices$x[2]) - 5
    max = (res$vertices$x[4]) + 5
    
    maximum = optimize(getElipse_m, interval = c(min, max),
                        maximum = TRUE,B=B, C=C, D=D, F=F, G=G)[[1]]
    minimum = optimize(getElipse_p, interval = c(min, max),
                        maximum = FALSE,B=B, C=C, D=D, F=F, G=G)[[1]]
    }
  data = data.frame(x = c(minimum, maximum))
  return(data)
}
# getXIntervalForElipse(3,-2,-5,-4,10)
#
# x
# 1 1.657687
# 2 7.842313
# There were 36 warnings (use warnings() to see them)




# Funkcia na vykreslenie elipsy
#
# parametre:
#           B: parameter elipsy
#           C: parameter elipsy
#           D: parameter elipsy
#           F: parameter elipsy
#           G: parameter elipsy
#    interval: definicny obor pre hodnotu x pri kresleni 
#              krivky elipsy v ggplote. JE to vystup 
#              z funkcie getIntervalForElipse
#
plotElipse = function(B,C,D,F,G, interval){
  int = interval
  
  plot = ggplot() +
    stat_function(data = int, aes(x = x), fun = getElipse_m, 
                  args = list(B=B,C=C,D=D,F=F,G=G)) + 
    stat_function(data = int, aes(x = x), fun = getElipse_p,
                  args = list(B=B,C=C,D=D,F=F,G=G))
  return(plot)
}
# interval = getXIntervalForElipse(3,-2,-5,-4,10)
# plotElipse(3,-2,-5,-4,10, interval)




# vygenerovanie dat na elipse
#
# parametre:
#           B: parameter elipsy
#           C: parameter elipsy
#           D: parameter elipsy
#           F: parameter elipsy
#           G: parameter elipsy
#     velkost: kolko sa ma vygenerovat dat na elipse
#
#    vystup: - dataframe kde su vygenerovane data na elipse
#
genDataOnElipse = function (B,C,D,F,G, velkost) {
  A  = 1
  U  = matrix(c(A, C / 2, C / 2, B), 2L)
  V  = c(-D / 2, -F / 2)
  mu = solve(U, V)
  
  # generovanie na kruznici
  r     = sqrt(A * mu[1] ^ 2 + B * mu[2] ^ 2 + C * mu[1] * mu[2] - G)
  theta = seq(0, 2 * pi, length = velkost)
  v     = rbind(r * cos(theta), r * sin(theta))
  
  ## transformovanie na bodov na elipsu
  z = backsolve(chol(U), v) + mu
  z = data.frame(t(z))
  colnames(z) = c("mi","ni")

  return(z)
}
#
# genDataOnElipse(3,-2,-5,-4,10,100)
#           mi        ni
# 1   7.274876 2.2500000
# 2   7.383027 2.3632343
# 3   7.480576 2.4760127
# 4   7.567129 2.5878811
# 5   7.642340 2.6983888





#
# vykreslenie vygenerovanych dat na elipse
#
# parametre:
#           B: parameter elipsy
#           C: parameter elipsy
#           D: parameter elipsy
#           F: parameter elipsy
#           G: parameter elipsy
#        data: vygenerovane data na elipse
#     intForX: definicny obor pre hodnotu x pri kresleni 
#              krivky elipsy v ggplote
#
plotGenDataOnElipse = function(B,C,D,F,G,data,intForX){
  
  int = intForX
  
  plot = ggplot() +
    stat_function(data = int, aes(x = x), fun = getElipse_m, 
                  args = list(B=B,C=C,D=D,F=F,G=G)) + 
    stat_function(data = int, aes(x = x), fun = getElipse_p,
                  args = list(B=B,C=C,D=D,F=F,G=G)) +
    geom_point(aes(x = data$mi, y = data$ni))
  
  return(plot)
}
# interval = getXIntervalForElipse(3,-2,-5,-4,10)
# data = genDataOnElipse(3,-2,-5,-4,10, 101, interval )
# plotGenDataOnElipse(3,-2,-5,-4,10, data, interval)




############  Vygenerovanie a vykreslenie zasumenych dat na elipse  ####
#
# vstupne parametre ro, sigma_s, delta su zadavane na vstupe 
# uzivatelom
#


#
# matica V
# 
# Vytvaranie autoregresneho modelu pre zasumenie dat
#
# parametre:
#          ro: parameter pre zasumenie
#     sigma_s: parameter pre zasumenie
#     velkost: kolko dat je vygenerovanych
#     
#      vystup: matica nxn, kde n = velkost
#
V = function(ro, sigma_s, velkost){
  skalar           = (sigma_s)/(1-ro^2)
  maticaDiagonalna = diag(x = 1, velkost, velkost)
  maticaNulova     = matrix(0,velkost,velkost)
  
  for (i in 1:velkost) {
    j = NULL
    j = i+1
    k = 1
    while (j <= velkost) {
      maticaNulova[i,j] = ro^(k)
      j = j+1
      k = k+1
    }
  }
  vystup = skalar*(maticaNulova + maticaDiagonalna + t(maticaNulova))

  return(vystup)
}
# V(0.2, 0.5, 4)
#
#             [,1]       [,2]       [,3]        [,4]
# [1,] 0.520833333 0.10416667 0.02083333 0.004166667
# [2,] 0.104166667 0.52083333 0.10416667 0.020833333
# [3,] 0.020833333 0.10416667 0.52083333 0.104166667
# [4,] 0.004166667 0.02083333 0.10416667 0.520833333




#
# matica W
#
# parametre:
#       delta: parameter pre zasumenie
#     velkost: kolko dat je vygenerovanych
#           V: vystup z matice V(ro, sigma_s, velkost)
# 
#      vystup: matica 2n,2n
# 
W = function(delta, velkost, V){
  A = V
  B = delta*diag(1,velkost,velkost)
  C = rbind(A,B)
  D = rbind(B,A)
  E = cbind(C,D)
  return(E)
}
# 
# V = V(0.2, 0.5, 4)
# W(0, 4, V)
#
#             [,1]       [,2]       [,3]        [,4]
# [1,] 0.520833333 0.10416667 0.02083333 0.004166667
# [2,] 0.104166667 0.52083333 0.10416667 0.020833333
# [3,] 0.020833333 0.10416667 0.52083333 0.104166667
# [4,] 0.004166667 0.02083333 0.10416667 0.520833333
# [5,] 0.000000000 0.00000000 0.00000000 0.000000000
# [6,] 0.000000000 0.00000000 0.00000000 0.000000000
# [7,] 0.000000000 0.00000000 0.00000000 0.000000000
# [8,] 0.000000000 0.00000000 0.00000000 0.000000000
#             [,5]       [,6]       [,7]        [,8]
# [1,] 0.000000000 0.00000000 0.00000000 0.000000000
# [2,] 0.000000000 0.00000000 0.00000000 0.000000000
# [3,] 0.000000000 0.00000000 0.00000000 0.000000000
# [4,] 0.000000000 0.00000000 0.00000000 0.000000000
# [5,] 0.520833333 0.10416667 0.02083333 0.004166667
# [6,] 0.104166667 0.52083333 0.10416667 0.020833333
# [7,] 0.020833333 0.10416667 0.52083333 0.104166667
# [8,] 0.004166667 0.02083333 0.10416667 0.520833333




#
# Funkcia B
# 
# Funkcia na rozklad matice W pomocou Choleskeho rozkadu
#
# parametre:
#           W: vystup z matice W(delta, velkost, V)
# 
#    vystup: matica 2n,2n
# 
B = function(W){
  vlCisla = {
    tryCatch(
      expr = {
        ev = eigen(W)
        P  = ev$vectors
        A  = diag(ev$values)
        A  = sqrt(A)
        PA = mat.mult(P,A)
      },
      error = function(e){
        # vypis chybovej hlasky
        print("nekonecne hodnoty pre vypocet vlastnych cisel")
        print("je to vo funkcii B pri generovani dat na elipse")
        ev = FALSE
      },
      warning = function(w){
        print(w)
      },
      finally = {
        ev = FALSE
      }
    )
  }
  return(vlCisla)
}
# V = V(0.2, 0.5, 4)
# W = W(0, 4, V)
# B(W)
#
#           [,1]       [,2]       [,3]       [,4]
# [1,]  0.0000000 -0.3339459  0.0000000  0.4620463
# [2,]  0.0000000 -0.4932491  0.0000000  0.2616062
# [3,]  0.0000000 -0.4932491  0.0000000 -0.2616062
# [4,]  0.0000000 -0.3339459  0.0000000 -0.4620463
# [5,] -0.3339459  0.0000000  0.4620463  0.0000000
# [6,] -0.4932491  0.0000000  0.2616062  0.0000000
# [7,] -0.4932491  0.0000000 -0.2616062  0.0000000
# [8,] -0.3339459  0.0000000 -0.4620463  0.0000000
#           [,5]       [,6]       [,7]       [,8]
# [1,]  0.0000000  0.3885616  0.0000000 -0.2117700
# [2,]  0.0000000 -0.2630690  0.0000000  0.3740261
# [3,]  0.0000000 -0.2630690  0.0000000 -0.3740261
# [4,]  0.0000000  0.3885616  0.0000000  0.2117700
# [5,]  0.3885616  0.0000000 -0.2117700  0.0000000
# [6,] -0.2630690  0.0000000  0.3740261  0.0000000
# [7,] -0.2630690  0.0000000 -0.3740261  0.0000000
# [8,]  0.3885616  0.0000000  0.2117700  0.0000000




#
# Funkcia na generovanie zasumenych dat
#
# Vygenerovanie zasumenych dat. Vstup su data 
# vygenerovane na elipse. Vystup je dataframe.
#
# parametre:
#        data: vygenerovane data na elipse
#           B: vystup z matice B(W)
# 
#      vystup: dataframe
#
genData = function(data, B){
  
  # vytvorenie jedneho vektora spojenim mi ni
  mi      = as.matrix(data[1])
  ni      = as.matrix(data[2])
  mini    = rbind(mi,ni)
  velkost = length(mi)
  
  # vytvorenie druheho scitanca pre hodnoty x y
  nor = as.matrix(rnorm(2*velkost,0,1))
  b   = mat.mult(B,nor)
  
  # konecne hodnoty x y
  xy = mini + b
  
  # rozdelenie xy do matice, aby sa moholi vykreslovat
  # v ggplote
  x  = xy[1:velkost]
  y  = xy[(velkost+1):(2*velkost)]
  xy = cbind(x,y)
  
  return(as.data.frame(xy))
}
#
# V = V(0.2, 0.5, 4)
# W = W(0, 4, V)
# B = B(W)
# interval = getXIntervalForElipse(3,-2,-5,-4,10)
# data     = genDataOnElipse(3,-2,-5,-4,10, 4,interval)
# genData(data, B)
#
#         x          y
# 1 5.543802 -0.3628816
# 2 4.934941  1.7297207
# 3 3.529854  3.8182488
# 4 3.101714  4.4199204




#
# Funkcia pre vykreslenie vygenerovanych zasumenzch dat
#
# Funkcia pouziva dve funkcie na vypocet elipsy. Jedna je pre
# hornu cast elipsy je to getElispe_p
# dolna cast elipsy je to getElispe_m
#
# parametre:
#     paremetre: parematre elipsy
#                 - B: parameter elipsy
#                 - C: parameter elipsy
#                 - D: parameter elipsy
#                 - F: parameter elipsy
#                 - G: parameter elipsy
#        data: vygenerovane zasumene data na elipse
#     intForX: definicny obor pre hodnotu x pri kresleni 
#              krivky elipsy v ggplote
# 
plotGenData = function(param, data, intForX){
  
  B   = param[[1]]
  C   = param[[2]]
  D   = param[[3]]
  F   = param[[4]]
  G   = param[[5]]
  int = intForX

  plot1 = ggplot() +
    stat_function(data = int, aes(x = x), fun = getElipse_m,
                  args = list(B=B,C=C,D=D,F=F,G=G)) +
    stat_function(data = int, aes(x = x), fun = getElipse_p,
                  args = list(B=B,C=C,D=D,F=F,G=G)) +
    geom_point(aes(x = data$x, y = data$y))
  
  return(plot1)
}




#
# Funkcia na zjednotenie parametrov ako vstupne hodnoty 
# pre vypocet generovanych udajov
#
# parametre:
#           B: parameter elipsy
#           C: parameter elipsy
#           D: parameter elipsy
#           F: parameter elipsy
#           G: parameter elipsy
#          ro: parameter zasumenia
#       sigma: parameter zasumenia
#       delta: parameter zasumenia
#
paramElipsa = function(B,C,D,F,G, ro, sigma, delta){
  data = data.frame("B"=B, "C"=C, "D"=D, "F"=F, "G"=G,
                    "ro"=ro, "sigma"=sigma, "delta"=delta)
  return(data)
}
# dataElipsa(1,2,3,4,5, 0,1,0)



#
# Funkcia na vypisanie udajov na konzolu. Je to vypis 
# pre prvy riadok, aby sa zobrazili hodnoty, ktore chceme
# aproximovat. Su to skutocne hodnoty, ku ktorym chceme 
# dotiahnut vypocet.
#
# parametre:
#           B: parameter elipsy
#           C: parameter elipsy
#           D: parameter elipsy
#           F: parameter elipsy
#           G: parameter elipsy
#          ro: parameter zasumenia
#       sigma: parameter zasumenia
#       delta: parameter zasumenia
#       vypis: ci cheme vypisovat na konzolu parametre
#              alebo nie. Defaultne je nastavene nie.
#
showParamElipsa = function(param, vypis = F){
  
  B       = param[[1]]
  C       = param[[2]]
  D       = param[[3]]
  F       = param[[4]]
  G       = param[[5]]
  ro      = param[[6]]
  sigma   = param[[7]]
  delta   = param[[8]]
  
  if(vypis != FALSE){
    cat("\n\n\n")
    cat(sprintf("iter  B=%.3f   C=%.3f   D=%.3f   F=%.3f   G=%.3f   r=%.3f   s=%.3f   d=%.3f",
                B,C,D,F,G, ro, sigma, delta))
    cat("\n\n")
  }
}




############  1. Generovanie dat  ######################################

#
# Jedna funkcia na generovanie a vykreslenie vstupnych dat
#
# parametre:
#         param: vstupne udaje pre elipsu a zasumenie. Je to
#                vystup z funkcie paramElipsa
#       velkost: kolko dat chceme vygenerovat
#         vypis: vykreslovanie grafov pri vypoctoch.
#                Defaultne je nastaveny na FALSE
#
#   Vystup: je list. V prvom liste su ulozene zasumene data.
#           V druhom liste su ulozene povodne data z ktorych 
#           bol generovany sum. Tieto data potrebujeme pre
#           konecne trasovanie aby sme veddeli ako sa nam 
#           priblizuju odhadovane body k pociatocnym bodom.
#
generujData = function(param, velkost, vypis = FALSE){
  
  B       = param[[1]]
  C       = param[[2]]
  D       = param[[3]]
  F       = param[[4]]
  G       = param[[5]]
  ro      = param[[6]]
  sigma   = param[[7]]
  delta   = param[[8]]
  intForX = getXIntervalForElipse(B,C,D,F,G)
  
  # generovanie dat na elipse
  dataOnElipse = genDataOnElipse(B,C,D,F,G,velkost)
  
  # v nasledujucej casti sa vykonava zasumenie vygenerovanzch
  # dat na elipse
  #
  V = V(ro, sigma, velkost)
  W = W(delta, velkost, V)
  B = B(W)
  
  # osetrenie ci je vo vystupe z funkcie Q_0 singularna matica
  # 
  if(isFALSE(B)) {return(FALSE);break} else{B}
  
  dataZasumene = genData(dataOnElipse, B)
  
  # je to skryty vystup, lebo ked pocitame vystup pre grid
  # aby sme nestracali zbytocne cas s kreslenim grafov.
  # 
  if(vypis != FALSE){
    show(plotGenData(param, dataZasumene, intForX))
  }
  return(list(dataZasumene, dataOnElipse))
}
# 
# par  = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data = generujData(par,100)
# data[[1]]
# data[[2]]





















############  2. Linearization the Measurement Model  ##################
#
# vstupne parametre ro, sigma_s, delta su zadavane na vstupe uzivatelom
# Data ako vstup pre nasledujuce matice su vygenerovane funkciou
# genData()
#


#
# Funkcia pre maticu parametrov
#
# Pri prvej iteracii zadava tieto parametre uzivatel. Pri dalsich
# iteraciach je to vystup z predchadzajuceho vypoctu
#
# parametre:
#           ro: zadava uzivatel
#       sigmas: zadava uzivatel (sigma square)
#        delta: zadava uzivatel
#        theta: pri prvej iteracii je nastaveny na NULL, lebo 
#               prva iteracia sa pocita cez matice. Druha iteracia
#               a dalsie nasledujuce su uz priradovena ako 
#               parameter. 
#
#      vystup: list parametrov ro, sigmaS, delta, theta
# 
paramVstupne = function(ro, sigmaS, delta, theta = NULL){
  
  data = list("ro" = ro, "sigmaS" = sigmaS, "delta" = delta, 
              "theta" = theta)
  # vypisujem na konzolu aky je stav parametrov pre elipsu
  return(data)
}






#
# Funkcia pre maticu W_1
#
# Rozdelena je na dve matice. Matica A je  povodna uz 
# naprograovana matica V, iba skalar je 
# derivovany. Druha matica B je derivovana a skalar je povodny.
#
# parametre:
#       param: funkcia vracajuca parametre od uzivatela
#             - ro
#             - sigmaS
#             - delta
#     velkost: sluzi na nastavenie velkosti matic
#
#      vystup: matica 2n x 2n
# 
W_1 = function(param, velkost){
  
  ro     = param[[1]]
  sigmaS = param[[2]]
  delta  = param[[3]]
  
  skalarP = (sigmaS)/(1-ro^2)
  skalarD = (2*sigmaS*ro)/(1-ro^2)^2
  
  AA = function(){
    maticaDiagonalna = diag(x = 1, velkost, velkost)
    maticaNulova     = matrix(0,velkost,velkost)
    
    for (i in 1:velkost) {
      j = NULL
      j = i+1
      k = 1
      while (j <= velkost) {
        maticaNulova[i,j] = ro^(k)
        j = j+1
        k = k+1
      }
    }
    vystup = skalarD*(maticaNulova + maticaDiagonalna + t(maticaNulova))
    return(vystup)
  }
  
  BB = function(){
    maticaNulova = matrix(0,velkost,velkost)
    
    for (i in 1:velkost) {
      j = NULL
      j = i+1
      k = 0
      while (j <= velkost) {
        maticaNulova[i,j] = (k+1)*ro^(k)
        j = j+1
        k = k+1
      }
    }
    vystup = skalarP*(maticaNulova + t(maticaNulova))
    return(vystup)
  }
  
  maticaDerivovana = AA() + BB()
  
  # spojenie matic s nulovou maticou
  W = matrix(0,velkost,velkost)
  C = cbind(maticaDerivovana, W)
  D = cbind(W, maticaDerivovana)
  E = rbind(C,D)
  
  return(E)
}
# 
# set.seed(123)
# par = paramElipsa(3,-2,-5,-4,10, 0.8, 0.005, 0.001)
# data = generujData(par,4)[[1]]
# param = paramVstupne(0.2,0.4,0)
# W_1(param, 4)
#
#           [,1]      [,2]      [,3]       [,4]
# [1,] 0.17361111 0.4513889 0.1736111 0.05138889
# [2,] 0.45138889 0.1736111 0.4513889 0.17361111
# [3,] 0.17361111 0.4513889 0.1736111 0.45138889
# [4,] 0.05138889 0.1736111 0.4513889 0.17361111
# [5,] 0.00000000 0.0000000 0.0000000 0.00000000
# [6,] 0.00000000 0.0000000 0.0000000 0.00000000
# [7,] 0.00000000 0.0000000 0.0000000 0.00000000
# [8,] 0.00000000 0.0000000 0.0000000 0.00000000
#           [,5]      [,6]      [,7]       [,8]
# [1,] 0.00000000 0.0000000 0.0000000 0.00000000
# [2,] 0.00000000 0.0000000 0.0000000 0.00000000
# [3,] 0.00000000 0.0000000 0.0000000 0.00000000
# [4,] 0.00000000 0.0000000 0.0000000 0.00000000
# [5,] 0.17361111 0.4513889 0.1736111 0.05138889
# [6,] 0.45138889 0.1736111 0.4513889 0.17361111
# [7,] 0.17361111 0.4513889 0.1736111 0.45138889
# [8,] 0.05138889 0.1736111 0.4513889 0.17361111




#
# Funkcia pre maticu W_2
#
# Toto je taka ista funkcia ako je funkcia V(), ktora už je
# naprogramovana. Je tam iba zmeneny skalar, ktory je 
# derivovany podla sigmaS.
#
# parametre:
#       param: funkcia vracajuca parametre od uzivatela
#             - ro
#             - sigmaS
#             - delta
#     velkost: sluzi na nastavenie velkosti matic
#
#      vystup: matica 2n x 2n
# 
W_2 = function(param, velkost){
  
  ro     = param[[1]]
  sigmaS = param[[2]]
  delta  = param[[3]]
  
  skalar           = 1/(1-ro^2)
  maticaDiagonalna = diag(x = 1, velkost, velkost)
  maticaNulova     = matrix(0,velkost,velkost)
  
  for (i in 1:velkost) {
    j = NULL
    j = i+1
    k = 1
    while (j <= velkost) {
      maticaNulova[i,j] = ro^(k)
      j = j+1
      k = k+1
    }
  }
  
  vystup = skalar*(maticaNulova + maticaDiagonalna + t(maticaNulova))
  
  # spojenie matic s nulovou maticou
  W = matrix(0,velkost,velkost)
  C = cbind(vystup, W)
  D = cbind(W, vystup)
  E = rbind(C,D)
  
  return(E)
}
# 
# set.seed(123)
# par  = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data = generujData(par,4)[[1]]
# param = paramVstupne(0.2,0.4,0)
# W_2(param, 4)
#
#             [,1]       [,2]       [,3]        [,4]
# [1,] 1.041666667 0.20833333 0.04166667 0.008333333
# [2,] 0.208333333 1.04166667 0.20833333 0.041666667
# [3,] 0.041666667 0.20833333 1.04166667 0.208333333
# [4,] 0.008333333 0.04166667 0.20833333 1.041666667
# [5,] 0.000000000 0.00000000 0.00000000 0.000000000
# [6,] 0.000000000 0.00000000 0.00000000 0.000000000
# [7,] 0.000000000 0.00000000 0.00000000 0.000000000
# [8,] 0.000000000 0.00000000 0.00000000 0.000000000
#             [,5]       [,6]       [,7]        [,8]
# [1,] 0.000000000 0.00000000 0.00000000 0.000000000
# [2,] 0.000000000 0.00000000 0.00000000 0.000000000
# [3,] 0.000000000 0.00000000 0.00000000 0.000000000
# [4,] 0.000000000 0.00000000 0.00000000 0.000000000
# [5,] 1.041666667 0.20833333 0.04166667 0.008333333
# [6,] 0.208333333 1.04166667 0.20833333 0.041666667
# [7,] 0.041666667 0.20833333 1.04166667 0.208333333
# [8,] 0.008333333 0.04166667 0.20833333 1.041666667
#





#
# Funkcia pre maticu W_3
#
# Je to blokova matica zlozena z nulovych matic a 
# z diagonalnych jednotkovych matic.
#
# parametre:
#    velkost: sluzi na nastavenie velkosti matic
#
#     Vystup: matica 2n x 2n
# 
W_3 = function(velkost){
  
  A = matrix(0, velkost, velkost)
  B = diag(1, velkost, velkost)
  C = cbind(A, B)
  D = cbind(B, A)
  E = rbind(C, D)
  
  return(E)
}
# 
# par  = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data = generujData(par,4)[[1]]
# param = paramVstupne(0.2,0.4,0)
# W_3(4)
#
#       [,1] [,2] [,3] [,4] [,5] [,6] [,7] [,8]
# [1,]    0    0    0    0    1    0    0    0
# [2,]    0    0    0    0    0    1    0    0
# [3,]    0    0    0    0    0    0    1    0
# [4,]    0    0    0    0    0    0    0    1
# [5,]    1    0    0    0    0    0    0    0
# [6,]    0    1    0    0    0    0    0    0
# [7,]    0    0    1    0    0    0    0    0
# [8,]    0    0    0    1    0    0    0    0
#





#
# Funkcia pre maticu V_1
#
# Je to vstupna matica pre H_0 a 0dhad_H_0
#
# parametre:
#       param: funkcia vracajuca parametre od uzivatela
#             - ro
#             - sigmas
#             - delta
#     velkost: sluzi na nastavenie velkosti matic
#     
#      vystup: matica n x n
# 
V_1 = function(param, velkost){
  
  ro      = param[[1]]
  sigma_s = param[[2]]
  
  skalar           = (sigma_s)/(1-ro^2)
  maticaDiagonalna = diag(x = 1, velkost, velkost)
  maticaNulova     = matrix(0,velkost,velkost)
  
  for (i in 1:velkost) {
    j = NULL
    j = i+1
    k = 1
    while (j <= velkost) {
      maticaNulova[i,j] = ro^(k)
      j = j+1
      k = k+1
    }
  }
  
  vystup = skalar*(maticaNulova + maticaDiagonalna + t(maticaNulova))
  
  return(vystup)
}
# 
# set.seed(123)
# par  = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data = generujData(par,5)[[1]]
# param = paramVstupne(0.2,0.4,0)
# V1 = V_1(param, 5)
# V1
# 
#             [,1]        [,2]       [,3]        [,4]         [,5]
# [1,] 0.4166666667 0.083333333 0.01666667 0.003333333 0.0006666667
# [2,] 0.0833333333 0.416666667 0.08333333 0.016666667 0.0033333333
# [3,] 0.0166666667 0.083333333 0.41666667 0.083333333 0.0166666667
# [4,] 0.0033333333 0.016666667 0.08333333 0.416666667 0.0833333333
# [5,] 0.0006666667 0.003333333 0.01666667 0.083333333 0.4166666667
# 





#
# Funkcia pre maticu H_0
#
# Je to taka ista funkcia a matica ako matica W pre
# gemerovanie dat. 
#
# parametre:
#       param: funkcia vracajuca parametre od uzivatela
#             - ro
#             - sigmas
#             - delta
#     velkost: sluzi na nastavenie velkosti matic
#          V1: je to vystup z matice V_1
#
#      vystup: matica 2n x 2n
# 
H_0 = function(param, velkost, V1){
  
  delta = param[[3]]
  
  A = V1
  B = delta*diag(1,velkost,velkost)
  C = rbind(A,B)
  D = rbind(B,A)
  E = cbind(C,D)
  
  return(E)
}
# 
# set.seed(123)
# par  = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data = generujData(par,5)[[1]]
# param = paramVstupne(0.2,0.4,0.1)
# V1 = V_1(param, 5)
# H0 = H_0(param, 5, V1)
# H0
# 
#             [,1]        [,2]       [,3]        [,4]         [,5]
# [1,] 0.4166666667 0.083333333 0.01666667 0.003333333 0.0006666667
# [2,] 0.0833333333 0.416666667 0.08333333 0.016666667 0.0033333333
# [3,] 0.0166666667 0.083333333 0.41666667 0.083333333 0.0166666667
# [4,] 0.0033333333 0.016666667 0.08333333 0.416666667 0.0833333333
# [5,] 0.0006666667 0.003333333 0.01666667 0.083333333 0.4166666667
# [6,] 0.1000000000 0.000000000 0.00000000 0.000000000 0.0000000000
# [7,] 0.0000000000 0.100000000 0.00000000 0.000000000 0.0000000000
# [8,] 0.0000000000 0.000000000 0.10000000 0.000000000 0.0000000000
# [9,] 0.0000000000 0.000000000 0.00000000 0.100000000 0.0000000000
# [10,] 0.0000000000 0.000000000 0.00000000 0.000000000 0.1000000000
#             [,6]        [,7]       [,8]        [,9]        [,10]
# [1,] 0.1000000000 0.000000000 0.00000000 0.000000000 0.0000000000
# [2,] 0.0000000000 0.100000000 0.00000000 0.000000000 0.0000000000
# [3,] 0.0000000000 0.000000000 0.10000000 0.000000000 0.0000000000
# [4,] 0.0000000000 0.000000000 0.00000000 0.100000000 0.0000000000
# [5,] 0.0000000000 0.000000000 0.00000000 0.000000000 0.1000000000
# [6,] 0.4166666667 0.083333333 0.01666667 0.003333333 0.0006666667
# [7,] 0.0833333333 0.416666667 0.08333333 0.016666667 0.0033333333
# [8,] 0.0166666667 0.083333333 0.41666667 0.083333333 0.0166666667
# [9,] 0.0033333333 0.016666667 0.08333333 0.416666667 0.0833333333
# [10,] 0.0006666667 0.003333333 0.01666667 0.083333333 0.4166666667
#




#
# Funkcia pre maticu B_0
#
# parametre:
#    data_mini: data su odhadnute hodnoty mini z vygenerovanych
#               dat x,y. Je to dataframe.
#     velkost: sluzi na nastavenie velkosti matic
#
#      vystup: matica n x 5

B_0 = function(data_mini,velkost){
  
  mi = data_mini[,1]
  ni = data_mini[,2]
  
  vystup = matrix(NA,velkost,5)
  
  vystup[,1] = ni^2
  vystup[,2] = mi*ni
  vystup[,3] = mi
  vystup[,4] = ni
  vystup[,5] = 1
  
  return(vystup)
}
# 
# set.seed(123)
# par  = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data = generujData(par,7)[[1]]
# B_0(data,7)
#
#             [,1]      [,2]     [,3]      [,4] [,5]
# [1,]  0.2392236  1.706099 3.488207 0.4891049    1
# [2,]  2.5427561 10.544583 6.612673 1.5946022    1
# [3,]  0.4154412  2.712438 4.208284 0.6445473    1
# [4,] 15.5204562 28.338444 7.193227 3.9396010    1
# [5,] 15.5229427 29.641563 7.523399 3.9399166    1
# [6,]  3.7469583  3.486584 1.801195 1.9357061    1
# [7,] 14.7473803 19.090414 4.971162 3.8402318    1
#





#
# Funkcia pre maticu theta_0
#
# Princip je nasledovny:
#               Ako vstup do funkcie je vystup z funkcie 
#               v prvej iteracii paramVstupne a v dalsich
#               iteraciach je to vystup z funkcie param_nove.
#               Testuje sa tu podmienka, ak je nulta iteracia
#               tak sa pocita theta cez matice. Ak uz prebehla
#               nejaka iteracia tak je vystup funkcie 
#               parameter z param.
#
# parametre:
#        param: je to vystup z funkcii paramVstupne, alebo
#               z funkcie param_nove
#    data_mini: data su odhadnute hodnoty mini z vygenerovanzch
#               dat x,y. Je to dataframe.
#           B0: vystup z funkcie B_0
# 
#       vystup: matica 5 x 1
#
theta_0 = function(param, data_mini, B0){
  
  paramTheta = param[[4]]
  
  # V pripade prvej iteracie pocita theta z matice B0
  # ak je v param uz zmenena theta z NULL na hodnotu
  # tak vracia iba tuto hodnotu
  # 
  if(!is.null(paramTheta)){
    return(paramTheta)
  }
  else{
    mi     = data_mini[,1]
    A      = mat.mult(t(B0),B0)
    vystup = mat.mult((-solve(A)), t(B0))%*% mi^2
    
    return(vystup)
  }
}
# 
# set.seed(123)
# par  = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data = generujData(par,100)[[1]]
# param = paramVstupne(0,1,0)
# B0   = B_0(data,100)
# theta_0(param, data, B0)
# 
#           [,1]
# [1,]  2.919024
# [2,] -1.945596
# [3,] -5.144817
# [4,] -3.860972
# [5,] 10.277728
# 





#
# Funkcia pre maticu A_0
#
# parametre:
#    data_mini: data su odhadnute hodnoty mini z vygenerovanzch
#               dat x,y. Je to dataframe.
#        theta: vystup z funkcie theta_0
#      velkost: sluzi na nastavenie velkosti matic
#
#       vystup: matica n x 2n
# 
A_0 = function(data_mini, theta, velkost){
  
  mi = data_mini[,1]
  ni = data_mini[,2]
  D  = matrix(0, velkost, 5)
  E  = D
  
  D[,2] = ni
  D[,3] = 1
  
  E[,1] = 2*ni
  E[,2] = mi
  E[,4] = 1
  
  F = mat.mult(D, theta) + 2*mi
  G = mat.mult(E, theta)
  
  vystup = cbind(diag(as.vector(F)),diag(as.vector(G)))
  
  return(vystup)
}
# 
# set.seed(123)
# par   = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data  = generujData(par,5)[[1]]
# param = paramVstupne(0,1,0)
# B0    = B_0(data,5)
# theta = theta_0(param, data, B0)
# A0    = A_0(data, theta,5)
# A0
# 
#           [,1]     [,2]     [,3]    [,4]     [,5]
# [1,]  0.719249 0.000000  0.00000 0.00000 0.000000
# [2,]  0.000000 4.391714  0.00000 0.00000 0.000000
# [3,]  0.000000 0.000000 -3.40789 0.00000 0.000000
# [4,]  0.000000 0.000000  0.00000 1.24013 0.000000
# [5,]  0.000000 0.000000  0.00000 0.00000 2.491712
#           [,6]     [,7]     [,8]     [,9]    [,10]
# [1,] -6.209012  0.00000 0.000000 0.000000 0.000000
# [2,]  0.000000 -5.50546 0.000000 0.000000 0.000000
# [3,]  0.000000  0.00000 6.799312 0.000000 0.000000
# [4,]  0.000000  0.00000 0.000000 4.324565 0.000000
# [5,]  0.000000  0.00000 0.000000 0.000000 2.513585
# 







#
# Funkcia pre maticu c_0
#
# parametre:
#    data_mini: data su odhadnute hodnoty mini z vygenerovanzch
#               dat x,y. Je to dataframe.
#           B0: je to vystup z funkcie B_0
#        theta: je to vystup z funkcie theta_0
#
#       vystup: matica n x 1
# 
c_0 = function(data_mini, B0, theta){
  
  mi = data_mini[,1] 
  A  = mat.mult(B0, theta) + mi^2
  
  return(A)
}
# 
# set.seed(123)
# par   = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data  = generujData(par,5)[[1]]
# param = paramVstupne(0,1,0)
# B0    = B_0(data,5)
# theta = theta_0(param, data, B0)
# c0 = c_0(data, B0, theta)
# c0
# 
#               [,1]
# [1,] -3.787193e-12
# [2,]  7.553069e-12
# [3,]  5.407585e-11
# [4,]  7.465673e-11
# [5,]  6.692602e-11
# 





#
# Funkcia pre maticu xy_triangle
#
# parametre:
#    data_mini: data su odhadnute hodnoty mini z vygenerovanzch
#               dat x,y. Je to dataframe.
#      data xy: data ktore mame ako vstupne data, teda namerane
#               hodnoty
#
#       vystup: matica 2n x 1
# 
xy_triangle = function(data_mini, data_xy){
  
  x  = data_xy[,1]
  y  = data_xy[,2]
  mi = data_mini[,1]
  ni = data_mini[,2]
  
  xtr = x - mi
  ytr = y - ni
  
  data = rbind(as.matrix(xtr), as.matrix(ytr))
  
  return(data)
}
# 
# set.seed(123)
# par   = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data  = generujData(par,5)[[1]]
# xyTriangle = xy_triangle(data,data)
# xyTriangle
# 
#       [,1]
# [1,]    0
# [2,]    0
# [3,]    0
# [4,]    0
# [5,]    0
# [6,]    0
# [7,]    0
# [8,]    0
# [9,]    0
# [10,]   0
# 






#
# Funkcia pre maticu Q_0
#
# parametre:
#           A0: vystup z funkcie A_0
#           H0: vystup z funkcie H_0
#           B0: vystup z funkcie B_0
#
#       vystup: matica (n+5) x (n+5)
# 
Q_0 = function(A0, H0, B0){
  
  Q11 = mat.mult(mat.mult(A0, H0), t(A0))
  Q12 = B0
  Q21 = t(B0)
  Q22 = matrix(0,5,5)
  
  Q11_12 = cbind(Q11,Q12)
  Q21_22 = cbind(Q21,Q22)
  Q      = rbind(Q11_12, Q21_22)
  
  # Poptrebujeme odchytit pseudoinverznu maticu. 
  # Princip: odchyti chybu, vypise chybovu hlasku 
  #          na konzolu a vyskoci von z funkcie.
  #          Osetrenie aby nezastal kod, je vo funkcii,
  #          ktora vola tuto funkciu.
  # 
  invQ = {
    tryCatch(
      expr = {
        inverzna = solve(Q)
      },
      error = function(e){
        # pise chybovu hlasku na konzolu
        print("singularna matica vo funkcii Q_0")
        inverzna = FALSE
      },
      warning = function(w){
        print(w)
      },
      finally = {
        inverzna = FALSE
      }
    )
  }
  
  return(invQ)
}
# 
# set.seed(123)
# par   = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data  = generujData(par,5)[[1]]
# param = paramVstupne(0.2,0.4,0.1)
# V1    = V_1(param, 5)
# H0    = H_0(param, 5, V1)
# B0    = B_0(data,5)
# theta = theta_0(param, data, B0)
# A0    = A_0(data, theta,5)
# Q0    = Q_0(A0, H0, B0)
# Q0
# 
#                [,1]          [,2]          [,3]          [,4]          [,5]
# [1,] -3.013292e-16  6.790843e-16 -3.510052e-16  1.964008e-15 -2.174488e-15
# [2,]  2.764510e-16 -7.877360e-16  4.561318e-16 -2.438456e-15  2.342477e-15
# [3,]  4.131320e-17 -1.636204e-16 -1.172796e-17 -7.897348e-16  4.593023e-16
# [4,]  2.198480e-16 -5.053828e-16  4.930862e-16 -1.386484e-15  1.161946e-15
# [5,] -3.403961e-16  8.842348e-16 -6.516701e-16  2.644418e-15 -2.160220e-15
# [6,]  2.119553e-03  2.111244e-01 -2.673701e-01  1.577809e+00 -1.523683e+00
# [7,]  1.029463e-01 -2.642454e-01  5.423706e-02 -8.025939e-01  9.096558e-01
# [8,] -3.673810e-01  9.528937e-01 -4.678976e-01  2.574404e+00 -2.692019e+00
# [9,] -7.012915e-01  1.208250e-01  1.232169e+00 -3.209423e+00  2.557721e+00
# [10,]  2.455267e+00 -3.122302e+00  1.144457e+00 -7.031290e+00  7.553869e+00
#               [,6]         [,7]         [,8]         [,9]       [,10]
# [1,]   0.002119553   0.10294633   -0.3673810   -0.7012915    2.455267
# [2,]   0.211124439  -0.26424536    0.9528937    0.1208250   -3.122302
# [3,]  -0.267370133   0.05423706   -0.4678976    1.2321686    1.144457
# [4,]   1.577808768  -0.80259385    2.5744042   -3.2094227   -7.031290
# [5,]  -1.523682627   0.90965583   -2.6920193    2.5577205    7.553869
# [6,] -33.838996867  18.60572550  -59.1487373   64.8597041  163.759142
# [7,]  18.605725504 -10.77213969   34.0382588  -32.8860580  -97.031554
# [8,] -59.148737324  34.03825882 -109.9498950  107.8094339  313.747392
# [9,]  64.859704083 -32.88605801  107.8094339 -142.1517334 -281.075699
# [10,] 163.759142329 -97.03155434  313.7473924 -281.0756987 -925.940547
# 





#
# Funkcia pre maticu Q_11
#
# parametre:
#    data_mini: data su odhadnute hodnoty mini z vygenerovanzch
#               dat x,y. Je to dataframe.
#           Q0: vystup z funkcie Q_0
#      velkost: sluzi na nastavenie velskoti matic
#
#       vystup: matica n x n
# 
Q_11 = function(data_mini, Q0, velkost){
  
  Q11 = Q0[1:velkost, 1:velkost]
  
  return(Q11)
} 
# 
# set.seed(123)
# par   = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data  = generujData(par,5)[[1]]
# param = paramVstupne(0.2,0.4,0.1)
# V1    = V_1(param, 5)
# H0    = H_0(param, 5, V1)
# B0    = B_0(data,5)
# theta = theta_0(param, data, B0)
# A0    = A_0(data, theta,5)
# Q0    = Q_0(A0, H0, B0)
# Q11   = Q_11(data, Q0,5)
# Q11
# 
#               [,1]          [,2]          [,3]          [,4]          [,5]
# [1,] -3.013292e-16  6.790843e-16 -3.510052e-16  1.964008e-15 -2.174488e-15
# [2,]  2.764510e-16 -7.877360e-16  4.561318e-16 -2.438456e-15  2.342477e-15
# [3,]  4.131320e-17 -1.636204e-16 -1.172796e-17 -7.897348e-16  4.593023e-16
# [4,]  2.198480e-16 -5.053828e-16  4.930862e-16 -1.386484e-15  1.161946e-15
# [5,] -3.403961e-16  8.842348e-16 -6.516701e-16  2.644418e-15 -2.160220e-15
# 





#
# Funkcia pre maticu S_0
#
# parametre:
#           A0: vystup z funkcie A_0
#          Q11: vystup z funkcie Q_11
#           W1: vystup z funkcie W_1
#           W2: vystup z funkcie W_2
#           W3: vystup z funkcie W_3
#
#       vystup: matica 3 x 3
# 
S_0 = function(A0, Q11, W1, W2, W3){
  
  # Zjednotenie rovnakych vypoctov do jednej matice
  
  a = (mat.mult(t(A0),Q11))
  X = mat.mult(a,A0)
  rm(a)
  
  s = matrix(0,3,3)
  
  # Zjednotenie rovnakych vypoctov do jednej matice
  
  a = mat.mult(X, W1)
  X_W1_X = mat.mult(a, X)
  rm(a)
  b = mat.mult(X, W2)
  X_W2_X = mat.mult(b, X)
  rm(b)
  c = mat.mult(X, W3)
  X_W3_X = mat.mult(c, X)
  rm(c)
  
  a = mat.mult(X_W1_X, W1)
  s[1,1] = sum(diag(mat.mult(X_W1_X, W1)))
  rm(a)
  b = mat.mult(X_W1_X, W2)
  s[1,2] = sum(diag(mat.mult(X_W1_X, W2)))
  rm(b)
  c = mat.mult(X_W1_X, W3)
  s[1,3] = sum(diag(mat.mult(X_W1_X, W3)))
  rm(c)
  
  a = mat.mult(X_W2_X, W1)
  s[2,1] = sum(diag(mat.mult(X_W2_X, W1)))
  rm(a)
  b = mat.mult(X_W2_X, W2)
  s[2,2] = sum(diag(mat.mult(X_W2_X, W2)))
  rm(b)
  c = mat.mult(X_W2_X, W3)
  s[2,3] = sum(diag(mat.mult(X_W2_X, W3)))
  rm(c)
  
  a = mat.mult(X_W3_X, W1)
  s[3,1] = sum(diag(mat.mult(X_W3_X, W1)))
  rm(a)
  b = mat.mult(X_W3_X, W2)
  s[3,2] = sum(diag(mat.mult(X_W3_X, W2)))
  rm(b)
  c = mat.mult(X_W3_X, W3)
  s[3,3] = sum(diag(mat.mult(X_W3_X, W3)))
  rm(c)
  
  return(s)
}
# set.seed(123)
# par   = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data  = generujData(par,5)[[1]]
# param = paramVstupne(0.2,0.4,0.1)
# V1    = V_1(param, 5)
# H0    = H_0(param, 5, V1)
# B0    = B_0(data,5)
# theta = theta_0(param, data, B0)
# A0    = A_0(data, theta,5)
# Q0    = Q_0(A0, H0, B0)
# Q11   = Q_11(data, Q0,5)
# W1    = W_1(param, 5) 
# W2    = W_2(param, 5)
# W3    = W_3(5)
# S0    = S_0(A0, Q11, W1, W2, W3)
# S0
# 
#               [,1]          [,2]          [,3]
# [1,]  4.480027e-28 -1.869438e-27 -1.348451e-28
# [2,] -1.869438e-27  7.874000e-27  6.799347e-28
# [3,] -1.348451e-28  6.799347e-28 -2.481293e-28
# 








#
# Funkcia pre maticu gama_0
#
# parametre:
#    data_mini: data su odhadnute hodnoty mini z vygenerovanzch
#               dat x,y. Je to dataframe.
#           H0: vystup z funkcie h_0
#           A0: vystup z funkcie A_0
#          Q11: vystup z funkcie Q_11
#           c0: vystup z funkcie c_0
#   xyTriangle: vystup z funkcie xy_triangle
#      velkost: sluzi na nastavenie velkosti matic
#
#       vystup: matica 2n x 1
# 
gama_0 = function(data_mini, H0, A0, Q11, c0, xyTriangle, velkost){
  
  velkost = 2*velkost
  I       = diag(1, velkost, velkost)
  
  # Zdruzenie rovnakych matic do jednej matice (pozri vzorec)
  X = mat.mult(mat.mult(H0, t(A0)), Q11)
  
  vystup = mat.mult((I - mat.mult(X, A0)), xyTriangle) - mat.mult(X, c0)
  
  return(vystup)
}
# # 
# set.seed(123)
# par        = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data       = generujData(par,5)[[1]]
# xyTriangle = matrix(data = 0,nrow = 10)
# param      = paramVstupne(0,1,0)
# B0         = B_0(data,5)
# theta      = theta_0(param, data, B0)
# c0         = c_0(data, B0, theta)
# V1         = V_1(param, 5)
# H0         = H_0(param, 5, V1)
# B0         = B_0(data,5)
# theta      = theta_0(param, data, B0)
# A0         = A_0(data, theta,5)
# Q0         = Q_0(A0, H0, B0)
# Q11        = Q_11(data, Q0,5)
# gama0      = gama_0(data, H0, A0, Q11, c0, xyTriangle, 5)
# gama0
# #
#               [,1]
# [1,] -1.606399e-27
# [2,]  1.014582e-26
# [3,]  5.821914e-27
# [4,] -1.915996e-26
# [5,]  3.536240e-26
# [6,]  1.386745e-26
# [7,] -1.271882e-26
# [8,] -1.161569e-26
# [9,] -6.681433e-26
# [10,]  3.567281e-26
# 









#
# Funkcia pre maticu Odhad_ro_sigma_delta
# 
#           s0: vystup z funkcie S_0
#        gama0: vystup z funkcie gama_0
#           H0: vystup z funkcie H_0
#           W1: vystup z funkcie W_1
#           W2: vystup z funkcie W_2
#           W3: vystup z funkcie W_3
#   xyTriangle: vystup z funkcie xy_triangle
# 
#       vystup: list - dva prvky
#               1 - odhad ro, sigma, delta
#               2 - minque matica
#
odhad_ro_sigma_delta = function(s0, gama0, H0, W1, W2, W3, xyTriangle){
  
  # Poptrebujeme odchytit pseudoinverznu maticu. 
  # Princip: odchyti chybu, vypise chybovu hlasku 
  #          na konzolu a vyskoci von z funkcie.
  #          Osetrenie aby nezastal kod, je vo funkcii,
  #          ktora vola tuto funkciu.
  # 
  vystup = {
    tryCatch(
      expr = {
        H_inverzna = solve(H0)
        s_inverzna = solve(s0)
        
        A = (xyTriangle - gama0)
        B = t(xyTriangle - gama0)
        
        B_H_inverzna = mat.mult(B, H_inverzna)
        H_inverzna_A = mat.mult(H_inverzna, A)
        
        a = mat.mult(mat.mult(B_H_inverzna, W1), H_inverzna_A)
        b = mat.mult(mat.mult(B_H_inverzna, W2), H_inverzna_A)
        c = mat.mult(mat.mult(B_H_inverzna, W3), H_inverzna_A)
        d = matrix(c(a,b,c), 3,1)
        
        oRSD = mat.mult(s_inverzna, d)
        
        # potrebujeme pre vypis do dataframu minque
        minque = 2*s_inverzna
        vystup = list(oRSD, minque)
      },
      error = function(e){
        # pise chybovu hlasku na konzolu
        print("singularna matica vo funkcii odhad_ro_sigma_delta pre H_0, alebo s_0")
        H_inverzna = FALSE
        s_inverzna = FALSE
        return(FALSE)
      },
      warning = function(w){
        print(w)
      },
      finally = {
        H_inverzna = FALSE
        s_inverzna = FALSE
      }
    )
  }
  return(vystup)
}







#
# Funkcia pre maticu odhad_H_0
#
# parametre:
#    odhad_RSD: vystup z funkcie odhad_ro_sigma_delta
#      velkost: sluzi na nastavenie velkosti matic
#
#       vystup: matica 2n x 2n
# 
odhad_H_0 = function(odhad_RSD, velkost){
  
  ro    = odhad_RSD[1,1]
  sigma = odhad_RSD[2,1]
  delta = odhad_RSD[3,1]
  
  param = paramVstupne(ro, sigma, delta)
  
  V2 = V_1(param, velkost)
  
  A = V2
  B = delta*diag(1,velkost,velkost)
  C = rbind(A,B)
  D = rbind(B,A)
  E = cbind(C,D)
  
  return(E)
}





#
# Funkcia pre maticu odhad_Q_0
#
# parametre:
#           A0: vystup z funkcie A_0
#     odhad_H0: vystup z funkcie odhad_H_0
#           B0: vystup z funkcie B_0
#
#       vystup: matica (n+5) x (n+5)
# 
odhad_Q_0 = function(A0, odhad_H0, B0){
  
  Q11 = mat.mult(mat.mult(A0, odhad_H0), t(A0))
  Q12 = B0
  Q21 = t(Q12)
  Q22 = matrix(0,5,5)
  
  Q11_12 = cbind(Q11,Q12)
  Q21_22 = cbind(Q21,Q22)
  Q      = rbind(Q11_12, Q21_22)
  
  # Poptrebujeme odchytit pseudoinverznu maticu. 
  # Princip: odchyti chybu, vypise chybovu hlasku 
  #          na konzolu a vyskoci von z funkcie.
  #          Osetrenie aby nezastal kod, je vo funkcii,
  #          ktora vola tuto funkciu.
  # 
  invQ = {
    tryCatch(
      expr = {
        inverzna = solve(Q)
      },
      error = function(e){
        # pise chybovu hlasku na konzolu
        print("singularna matica vo funkcii odhad Q_0")
        inverzna = FALSE
      },
      warning = function(w){
        print(w)
      },
      finally = {
        inverzna = FALSE
      }
    )
  }
  return(invQ)
}






#
# Funkcia pre maticu odhad_Q_11
#
# parametre:
#      velkost: sluzi na nastavenie velkosti matic
#     odhad_Q0: vystup z funkcie odhad_Q_0
# 
#       vystup: matica n x n
# 
odhad_Q11 = function(velkost, odhad_Q0){
  
  Q11 = odhad_Q0[1:velkost, 1:velkost]
  return(Q11)
}






#
# Funkcia pre maticu odhad_Q_21
#
# parametre:
#      velkost: sluzi na nastavenie velkosti matic
#     odhad_Q0: vystup z funkcie odhad_Q_0
# 
#       vystup: matica 5 x n
#
odhad_Q21 = function(velkost, odhad_Q0){
  
  Q21 = odhad_Q0[(1+velkost):dim(odhad_Q0)[1], 1:velkost]
  return(Q21)
}






#
# Funkcia pre maticu odhad_Q_22
#
# parametre:
#     odhad_Q0: vystup z funkcie odhad_Q_0
# 
#       vystup: matica 5 x 5
#
odhad_Q22 = function(odhad_Q0){
  
  Q22 = odhad_Q0[(dim(odhad_Q0)[1]-4):dim(odhad_Q0)[1], 
                 (dim(odhad_Q0)[1]-4):dim(odhad_Q0)[1]]
  return(Q22)
}






#
# Funkcia pre maticu odhad_mi_ni_theta
#
# parametre:
#      velkost: sluzi na nastavenie velkosti matic
#     odhad_H0: vystup z funkcie odhad_H_0
#           A0: vystup z funkcie A_0
#    odhad_Q11: vystup z funkcie odhad_Q_11
#    odhad_Q21: vystup z funkcie odhad_Q_21
#           c0: vystup z funkcie c_0
#   xyTriangle: vystup z funkcie cy_triangle
#
#    vystup: vystup je list dva prvky
#            1 - prirastky pre mi ni
#            2 - prirastky pre tetu
#
odhad_mi_ni_heta = function(velkost, odhad_H0, A0, odhad_Q11, 
                            odhad_Q21, c0, xyTriangle){
  
  I =  diag(1, (2*velkost), (2*velkost))
  
  # zlucenie matic pre lepsiu prehladnost
  #
  X = mat.mult(mat.mult(odhad_H0, t(A0)), odhad_Q11)
  B = I - mat.mult(X, A0)
  
  C = rbind(X, odhad_Q21)
  D = rbind(B, mat.mult((-odhad_Q21), A0))
  
  vystup   = mat.mult((-C), c0) + mat.mult(D, xyTriangle)
  velkost1 = dim(vystup)[1]
  theta    = vystup[(velkost1 - 4):velkost1]
  ls       = list(mini_tr = vystup, theta_tr = theta)
  
  return(ls)  
}








######## 3. aproximacia elipsy ###########################

#
# Funkcia aproximujuca data, ktore sa priblizuju datam
# leziacim na elipse
#
# Pri prvej iteracii zadava vstupne parametre ro sigma, delta, 
# uzivatel. Pri dalsich iteraciach je to vystup
# z predchadzajuceho vypoctu.
#
# parametre:
#         param:
#               - ro    : zadava uzivatel
#               - sigmas: zadava uzivatel (sigma square)
#               - delta : zadava uzivatel
#                 a pri dalsich iteraciach su to uz odhadnute
#                 hodnoty
#     data_mini: data su odhadnute hodnoty mini z vygenerovanzch
#                dat x,y. Je to dataframe.
#       data_xy: vygenerovane data xy
#       velkost: sluzi na nastavovanie velkosti matic
#
#        vystup: vystupom je list, v prvej casti su data, ktore
#                aproximuju elipsu, v duhej casti su data, 
#                odhad (ro, sigma, delta), teta0, teta_tr
#
generujPriblizenie = function(param, data_mini, data_xy, velkost){
  
  W1         = W_1(param, velkost)
  W2         = W_2(param, velkost)
  W3         = W_3(velkost)
  V1         = V_1(param, velkost)
  H0         = H_0(param, velkost, V1)
  B0         = B_0(data_mini, velkost)
  theta0     = theta_0(param, data_mini,B0)
  A0         = A_0(data_mini, theta0, velkost)
  c0         = c_0(data_mini, B0, theta0)
  xyTriangle = xy_triangle(data_mini, data_xy)
  Q0         = Q_0(A0, H0, B0)
  
  # osetrenie ci je vo vystupe z funkcie Q_0 singularna matica.
  # Ak vystupnou hodnotou funkcie Q_0 je parameter FALSE, tak
  # sa ukoncuje vykonavanie tejto funkcie.
  # 
  if(isFALSE(Q0)) {return(FALSE);break} else{Q0}
  
  Q11       = Q_11(data_mini, Q0, velkost)
  s0        = S_0(A0, Q11, W1, W2, W3)
  gama0     = gama_0(data_mini, H0, A0, Q11, c0, xyTriangle, velkost)
  odhad_RSD = odhad_ro_sigma_delta(s0, gama0, H0, W1, W2, W3, xyTriangle)
  
  # osetrenie ci je vo vystupe z funkcie odhad_RSD singularna matica.
  # Ak vystupnou hodnotou funkcie odhad_RSD je parameter FALSE, tak
  # sa ukoncuje vykonavanie tejto funkcie.
  # 
  if(isFALSE(odhad_RSD[[1]])) {return(FALSE);break} else{odhad_RSD[[1]]}
  
  odhad_H0 = odhad_H_0(odhad_RSD[[1]], velkost)
  odhad_Q0 = odhad_Q_0(A0, odhad_H0, B0)
  
  # osetrenie ci je vo vystupe z funkcie odhad_Q0 singularna matica.
  # Ak vystupnou hodnotou funkcie odhad_Q0 je parameter FALSE, tak
  # sa ukoncuje vykonavanie tejto funkcie.
  # 
  if(isFALSE(odhad_Q0)) {return(FALSE);break} else{odhad_Q0}
  
  odhad_Q11 = odhad_Q11(velkost, odhad_Q0)
  odhad_Q21 = odhad_Q21(velkost, odhad_Q0)
  odhad_Q22 = odhad_Q22(odhad_Q0)
  odhad_MNT = odhad_mi_ni_heta(velkost, odhad_H0, A0, odhad_Q11, 
                               odhad_Q21, c0, xyTriangle)
  theta_tr  = odhad_MNT[[2]]
  minque    = diag(odhad_RSD[[2]])
  
  return(list(odhad_MNT[[1]], odhad_RSD[[1]], theta0, theta_tr, 
              minque, odhad_Q22))
}





#
# Funkcia pre maticu odhadnutych dat mi ni
#
# parametre:
#         data_mini: toto su vstupne data mini do iteracii
#                    ktore su v kazdej iteracii odhadovane
#         dataOdhad: je to vystup z funkcie generuj priblizenie
# 
#            vystup: dataframe - hodnoty odhadnutych mi ni
# 
odhadnute_mini = function(data_mini, dataOdhad){
  
  dataOdhad = dataOdhad[[1]]
  velkost   = dim(data_mini)[1]
  
  odhad_mi = dataOdhad[1:velkost]
  odhad_ni = dataOdhad[(1+velkost):(2*velkost)]
  
  odhad_mi = odhad_mi + data_mini[1]
  odhad_ni = odhad_ni + data_mini[2]
  
  data = data.frame(cbind(odhad_mi, odhad_ni))
  colnames(data)[1] = "mi"
  colnames(data)[2] = "ni"
  
  return(data)
}





#
# Funkcia pre vykreslenie novych odhadnutych dat
#
# parametre:
#          param: su to parametre elipsy pre vykreslenie
#                 krivky elipsy
# odhadnute_mini: su to odhadnute data mini
#       iteracia: ciselny udaj o kolku iteraciu ide
#
#         vystup: graf
# 
plotHatData = function(param, odhadnute_mini, iteracia){
  
  # premenne vyuzivane v celom tele kodu
  # 
  B = param[[1]]
  C = param[[2]]
  D = param[[3]]
  F = param[[4]]
  G = param[[5]]
  
  int  = getXIntervalForElipse(B,C,D,F,G)
  data = odhadnute_mini
  
  # pomocna funkcia pre vypis do grafu
  #
  str = function(x){
    if(x>=0) return("+")
    else(return("-"))
  }
  
  plot = ggplot() +
    stat_function(data = int, aes(x = x), fun = getElipse_m,
                  args = list(B=B,C=C,D=D,F=F,G=G)) +
    stat_function(data = int, aes(x = x), fun = getElipse_p,
                  args = list(B=B,C=C,D=D,F=F,G=G)) +
    geom_point(aes(x = data$mi, y = data$ni)) +
    annotate("text", x = -Inf, y = Inf, hjust = -.10, vjust = 2.2, 
             label = TeX(sprintf("$\\mu^2 %s %.f \\nu^2 %s %.f \\mu \\nu 
                                 %s %.f \\mu %s %.f \\nu %s %.f$", 
                                 str(B), abs(B),
                                 str(C), abs(C),
                                 str(D), abs(D),
                                 str(F), abs(F),
                                 str(G), abs(G)
             )), size = 4, parse = TRUE) +
    
    annotate("text", x = -Inf, y = Inf, hjust = -.10, vjust = 1.2,
             label = sprintf("iteracia: %.f", iteracia), size = 4, 
             parse = TRUE)
  plot
}




#
# Funkcia pre vykreslenie odhadnutej elipsy
#
# parametre:
#         param: su to parametre elipsy pre vykreslenie
#                krivky elipsy
#    paramOdhad: odhadnute parametre pre elipsu
#        parApr: vstupne data ro sigma delta
#                do prvej iteracie. Ku nim by
#                sme sa mali dostat aproximaciou
#
#         vystup: graf
# 
plotHatElipse = function(param, paramOdhad, parApr){
  
  B = param[[1]]
  C = param[[2]]
  D = param[[3]]
  F = param[[4]]
  G = param[[5]]
  
  B_hat = paramOdhad[[4]][1]
  C_hat = paramOdhad[[4]][2]
  D_hat = paramOdhad[[4]][3]
  F_hat = paramOdhad[[4]][4]
  G_hat = paramOdhad[[4]][5]
  
  # pomocna funkcia pre vypis do grafu
  #
  str = function(x){
    if(x>=0) return("+")
    else(return("-"))
  }
  
  int  = getXIntervalForElipse(B,C,D,F,G)
  int2 = getXIntervalForElipse(B_hat, C_hat, D_hat, F_hat, G_hat)
  
  plot = ggplot() +
    stat_function(data = int, aes(x = x), fun = getElipse_m,
                  args = list(B=B,C=C,D=D,F=F,G=G)) +
    stat_function(data = int, aes(x = x), fun = getElipse_p,
                  args = list(B=B,C=C,D=D,F=F,G=G)) +
    stat_function(data = int2, aes(x = x), fun = getElipse_m, color = "red",
                  args = list(B=B_hat,C=C_hat,D=D_hat,F=F_hat,G=G_hat)) +
    stat_function(data = int2, aes(x = x), fun = getElipse_p, color = "red",
                  args = list(B=B_hat,C=C_hat,D=D_hat,F=F_hat,G=G_hat)) +
    annotate("text", x = -Inf, y = Inf, hjust = -.10, vjust = 2.2, 
             label = TeX(sprintf("odhad:   $\\ro$ = %.4f,  $\\sigma^2$ = %.4f,  $\\delta$ = %.4f",
                                 paramOdhad[1], paramOdhad[2], paramOdhad[3])), size = 4, parse = TRUE)
  plot
}








#
# Funkcia pre maticu odhadnutych dat theta
#
# parametre:
#           theta_tr: data su odhadnute hodnoty thety 
#                     je to vystup z funkcie odhad_mi_ni_theta
#            theta_0: je to vystup z predchadzajucej iteracie
#
#   vystup: dataframe odhadnutej thety. To su odhadovane 
#           parametre pre elipsu
#
#
odhadnute_theta = function(theta_0, theta_tr){
  
  data = theta_0 + theta_tr
  
  return(data)
}





#
# Funkcia pre odhad novych parametrov
#
# parametre:
#       param: funkcia vracajuca parametre od uzivatela
#             - ro
#             - sigmas
#             - delta
#   generujPriblizenie: je to vystup z funkcie 
#             generujPriblizenie, je to ulozene v liste
#      vypis: ci chceme vypisovat na konzolu odhadnute 
#             parametre. Defaultne je nastavene na FALSE.
#             
# vystup: list (ro, sigma, delta, theta), theta je matica
#         v ktorej su parametre elispy.
# 
param_nove = function(param, generujPriblizenie, vypis = F){
  
  ro    = param[[1]]
  
  ro_odhad    = generujPriblizenie[[2]][1,1]
  sigma_odhad = generujPriblizenie[[2]][2,1]
  delta_odhad = generujPriblizenie[[2]][3,1]
  
  ro_nove    = ro + ro_odhad
  sigma_nove = sigma_odhad
  delta_nove = delta_odhad
  
  theta_0  = generujPriblizenie[[3]]
  theta_tr = generujPriblizenie[[4]]
  
  theta_nove = theta_0 + theta_tr
  
  
  # Volitelna moznost, ci chceme vypisovat na konzolu
  # parametre, alebo nie.
  # 
  if(vypis != FALSE){
    cat(sprintf("%.6f  %.6f  %.6f  %.6f  %.6f  %.6f  %.6f  %.6f",
                theta_nove[1],
                theta_nove[2],
                theta_nove[3],
                theta_nove[4],
                theta_nove[5],
                ro_nove,
                sigma_nove, 
                delta_nove))
    cat("\n")
  }
  
  data = list("ro" = ro_nove, "sigmaS" = sigma_nove, 
              "delta" = delta_nove, "theta" = theta_nove)
  
  return(data)
}





#
# Funkcia pre aproximaciu dat
#
# parametre:
#         par: vystup z funkcie paramElipse
#             - ro
#             - sigmas
#             - delta
#             - tetha
#      parApr: volitelny parameter aproximacie pre 
#              prvu iteraciu pre ro, sigma, delta
#     velkost: kolko dat chcem aproximovat
#        iter: pocet iteracii ak je tam 0
#              tak len vykresli odhad
#        plot: ci mame vykreslovat kazdy graf
#              alebo iba prvy zasumenie a posledy
#              pre odhadnute data. Defaultne je na FALSE.
#       vypis: ci chceme vypisovat na konzolu odhadnute 
#              parametre. Defaultne je nastavene na FALSE. 
#             
#
aproxData = function(par, parApr, velkost, iter, plot = F, vypis = F){

  # pocitanie iteracii pre legendu do grafov
  iteracia = 1
  
  # toto je na vypis diagonalnych prvkov matic s_0 a odhad Q_22. Su to 
  # kovariacne matice pre rozptyl.
  # 
  minque = data.frame(data = matrix(data = NA, nrow = 1, ncol = 3))
  Q22    = data.frame(data = matrix(data = NA, nrow = 1, ncol = 5))
  
  xy = generujData(par, velkost, vypis)[[1]]
  
  # osetrenie ci je vo vystupe z funkcie generujData singularna matica.
  # Ak vystupnou hodnotou funkcie generujData je parameter FALSE, tak
  # sa ukoncuje vykonavanie tejto funkcie.
  # 
  if(isFALSE(xy)) {return(FALSE)} else{xy}
  
  showParamElipsa(par, vypis)
  
  gc()
  
  if(iter > 0){
    dataMiNi   = xy
    paramVstup = paramVstupne(parApr[1],parApr[2],parApr[3])
    odhad      = generujPriblizenie(paramVstup, dataMiNi, xy, velkost)
    
    # osetrenie ci je vo vystupe z funkcie generujPriblizenie 
    # singularna matica. Ak vystupnou hodnotou funkcie 
    # generujPriblizenie je parameter FALSE, tak
    # sa ukoncuje vykonavanie tejto funkcie.
    # 
    if(isFALSE(odhad)) {return(FALSE);break} else{odhad}
    
    noveMiNi = odhadnute_mini(dataMiNi, odhad)
    
    # Vypisanie cisla iteracie.
    # 
    if(vypis != FALSE){
      cat(sprintf("%2d    ",1))
    }
    param = param_nove(paramVstup, odhad, vypis)
    if(plot == TRUE) show(plotHatData(par, noveMiNi,iteracia))
    
    if(iter > 1){
      for (i in 1:(iter-1)) {
    
        iteracia = iteracia + 1
        odhad    = generujPriblizenie(param, noveMiNi, xy, velkost)
      
        # osetrenie ci je vo vystupe z funkcie generujPriblizenie 
        # singularna matica. Ak vystupnou hodnotou funkcie 
        # generujPriblizenie je parameter FALSE, tak
        # sa ukoncuje vykonavanie tejto funkcie.
        # 
        if(isFALSE(odhad)) {return(FALSE);break} else{odhad}
        
        noveMiNi = odhadnute_mini(noveMiNi, odhad)
      
        # Vypisanie cisla iteracie.
        # 
        if(vypis != FALSE){
          cat(sprintf("%2d    ", (i+1)))
        }
        param = param_nove(param, odhad, vypis)
        if(plot == TRUE) show(plotHatData(par, noveMiNi,iteracia))
        
        gc()
        
      }
      
      # osetrenie ci je vo vystupe z funkcie generujPriblizenie 
      # singularna matica. Ak vystupnou hodnotou funkcie 
      # generujPriblizenie je parameter FALSE, tak
      # sa ukoncuje vykonavanie tejto funkcie.
      # 
      if(isFALSE(odhad)) {return(FALSE);break} else{odhad}
    }
    
    # Parametre pre vypis diagonaly inverznej matice pre s_0 
    # a diagonaly pre maticu odhad Q_22
    # 
    minqueR = matrix(data = odhad[[5]], ncol = 3, nrow = 1)
    Q22R    = matrix(data = diag(odhad[[6]]), ncol = 5, nrow = 1)
  }
  
  # 
  # Ak dame vypis FALSE tak nebude na konzolu pisat nic. Ani odhad
  # parametrov ani grafy. Iba pocet iteracii. 
  # Je to na zrychlenie vystupu. 
  # 
  if(vypis != FALSE){if(plot != TRUE)show(plotHatData(par, noveMiNi,iteracia))}
  if(vypis != FALSE){show(plotHatElipse(par, param, parApr))}
  
  # dataframe na ulozenie odhadnutych dat na testovanie.  
  # 
  paramFinal = data.frame("oC"      = param$theta[1],
                          "oD"      = param$theta[2],
                          "oE"      = param$theta[3],
                          "oF"      = param$theta[4],
                          "oG"      = param$theta[5],
                          "oRo"     = param$ro[1],
                          "osigmaS" = param$sigmaS[1],
                          "odelta"  = param$delta[1])
  
  minque     = data.frame("min1" = minqueR[1,1], 
                          "min2" = minqueR[1,2],
                          "min3" = minqueR[1,3])

  Q22        = data.frame("Q_1" = Q22R[1,1],
                          "Q_2" = Q22R[1,2],
                          "Q_3" = Q22R[1,3],
                          "Q_4" = Q22R[1,4],
                          "Q_5" = Q22R[1,5])
  
  # spojenie dataframov kde v prvom su ulozene parametre pre
  # generovanie dat na elipse. V druhom su koncecne odhadnute 
  # parametre. Su zaokruhlene na 10 desatinnych miest.
  # V tretom je ulozena diagonala z odhadu Q_0.
  # V stvrtom je ulozena diagonala z s_0.
  # 
  vystup = as.vector(cbind(par, paramFinal, minqueR, Q22R), mode = "numeric")
  vystup = round(vystup, digits = 10 )
  
  invisible(vystup)
}






#
# Funkcia pre odhad parametrov modelu z realnych dat
#
# parametre:
# 
#        data: vstupne data upravene list s parametrom
#              dataframe, nazov stlpcov x,y
#                            x          y
#                   1 5.543802 -0.3628816
#                   2 4.934941  1.7297207
#                   3 3.529854  3.8182488
#                   4 3.101714  4.4199204
#                       ...       ... 
#      parApr: volitelny parameter aproximacie pre 
#              prvu iteraciu pre ro, sigma, delta
#              defaultne je nastaveny na FALSE.
#        iter: pocet iteracii ak je tam 0
#              tak len vykresli odhad
#        plot: ci mame vykreslovat kazdy graf
#              alebo iba prvy zasumenie a posledy
#              pre odhadnute data. Defaultne je na FALSE.
#       vypis: ci chceme vypisovat na konzolu odhadnute 
#              parametre. Defaultne je nastavene na FALSE. 
#             
#
odhadZRealDat = function(data, iter, parApr = F,  plot = F, vypis = F){
  
  xy      = data
  velkost = dim(data)[[1]]
  if(isFALSE(parApr)) {parApr = c(0,1,0)} else{parApr}

  # pocitanie iteracii pre legendu do grafov
  iteracia = 1
  
  # toto je na vypis diagonalnych prvkov matic s_0 a odhad Q_22. Su to 
  # kovariacne matice pre rozptyl.
  # 
  minque = data.frame(data = matrix(data = NA, nrow = 1, ncol = 3))
  Q22    = data.frame(data = matrix(data = NA, nrow = 1, ncol = 5))
  
  gc()
  
  if(iter > 0){
    dataMiNi   = xy
    paramVstup = paramVstupne(parApr[1],parApr[2],parApr[3])
    odhad      = generujPriblizenie(paramVstup, dataMiNi, xy, velkost)
    
    # osetrenie ci je vo vystupe z funkcie generujPriblizenie 
    # singularna matica. Ak vystupnou hodnotou funkcie 
    # generujPriblizenie je parameter FALSE, tak
    # sa ukoncuje vykonavanie tejto funkcie.
    # 
    if(isFALSE(odhad)) {
      print("vo vystupe sa nachadza singularna matica")
      print("ukoncenie vypoctu odhadu")
      return(FALSE);break} else{odhad}
    
    noveMiNi = odhadnute_mini(dataMiNi, odhad)
    
    # Vypisanie cisla iteracie.
    # 
    if(vypis != FALSE){
      cat(sprintf("%2d    ",1))
    }
    param = param_nove(paramVstup, odhad, vypis)
    
    if(iter > 1){
      for (i in 1:(iter-1)) {
        
        iteracia = iteracia + 1
        odhad    = generujPriblizenie(param, noveMiNi, xy, velkost)
        
        # osetrenie ci je vo vystupe z funkcie generujPriblizenie 
        # singularna matica. Ak vystupnou hodnotou funkcie 
        # generujPriblizenie je parameter FALSE, tak
        # sa ukoncuje vykonavanie tejto funkcie.
        # 
        if(isFALSE(odhad)) {
          print("vo vystupe sa nachadza singularna matica")
          print("ukoncenie vypoctu odhadu")
          return(FALSE);break} else{odhad}
        
        noveMiNi = odhadnute_mini(noveMiNi, odhad)
        
        # Vypisanie cisla iteracie.
        # 
        if(vypis != FALSE){
          cat(sprintf("%2d    ", (i+1)))
        }
        param = param_nove(param, odhad, vypis)
        
        gc()
        
      }
      
      # osetrenie ci je vo vystupe z funkcie generujPriblizenie 
      # singularna matica. Ak vystupnou hodnotou funkcie 
      # generujPriblizenie je parameter FALSE, tak
      # sa ukoncuje vykonavanie tejto funkcie.
      # 
      if(isFALSE(odhad)) {
        print("vo vystupe sa nachadza singularna matica")
        print("ukoncenie vypoctu odhadu")
        return(FALSE);break} else{odhad}
    }
    
    # Parametre pre vypis diagonaly inverznej matice pre s_0 
    # a diagonaly pre maticu odhad Q_22
    # 
    minqueR = matrix(data = odhad[[5]], ncol = 3, nrow = 1)
    Q22R    = matrix(data = diag(odhad[[6]]), ncol = 5, nrow = 1)
  }
  
  # dataframe na ulozenie odhadnutych dat na testovanie.  
  # 
  paramFinal = data.frame("oC"      = param$theta[1],
                          "oD"      = param$theta[2],
                          "oE"      = param$theta[3],
                          "oF"      = param$theta[4],
                          "oG"      = param$theta[5],
                          "oRo"     = param$ro[1],
                          "osigmaS" = param$sigmaS[1],
                          "odelta"  = param$delta[1])
  
  minque     = data.frame("min1" = minqueR[1,1], 
                          "min2" = minqueR[1,2],
                          "min3" = minqueR[1,3])
  
  Q22        = data.frame("Q_1" = Q22R[1,1],
                          "Q_2" = Q22R[1,2],
                          "Q_3" = Q22R[1,3],
                          "Q_4" = Q22R[1,4],
                          "Q_5" = Q22R[1,5])
  
  # spojenie dataframov kde v prvom su koncecne odhadnute 
  # parametre. Su zaokruhlene na 10 desatinnych miest.
  # V druhom je ulozena diagonala z odhadu Q_0.
  # V tretom je ulozena diagonala z s_0.
  # 
  vystup = as.vector(cbind(paramFinal, minqueR, Q22R), mode = "numeric")
  vystup = round(vystup, digits = 10 )
  
  invisible(vystup)
}






##################### uprava ##########################################





# generovanie bodov na elipse
# https://stackoverflow.com/questions/41820683/how-to-plot-ellipse-given-a-general-equation-in-r
# https://www.r-bloggers.com/fitting-an-ellipse-to-point-data/


plotElipseAndData = function(B,C,D,F,G, interval, data){
  int = interval
  
  plot = ggplot() +
    stat_function(data = int, aes(x = x), fun = getElipse_m, 
                  args = list(B=B,C=C,D=D,F=F,G=G)) + 
    stat_function(data = int, aes(x = x), fun = getElipse_p,
                  args = list(B=B,C=C,D=D,F=F,G=G)) +
    geom_point(aes(x = data[,1], y = data[,2]))
  return(plot)
}




# Generovanie zasumenych dat. Je to pre rozdelene vtorky
# lebo do zasumenia pojdu len po castiach. Lebo ak mam 
# vzorku napriklad 6500 pozorovani, tak mi to nespracuje
# lebo mam malu ramku.
# 
generujDataPoCastiach = function(param, data){
  
  velkost = dim(data)[1]
  
  B       = param[[1]]
  C       = param[[2]]
  D       = param[[3]]
  F       = param[[4]]
  G       = param[[5]]
  ro      = param[[6]]
  sigma   = param[[7]]
  delta   = param[[8]]
  
  # generovanie dat na elipse
  dataOnElipse = data
  
  # v nasledujucej casti sa vykonava zasumenie vygenerovanzch
  # dat na elipse
  #
  V = V(ro, sigma, velkost)
  W = W(delta, velkost, V)
  B = B(W)
  
  # osetrenie ci je vo vystupe z funkcie Q_0 singularna matica
  # 
  if(isFALSE(B)) {return(FALSE);break} else{B}
  
  dataZasumene = genData(dataOnElipse, B)
  
  return(dataZasumene)
}
# 
# par  = paramElipsa(3,-2,-5,-4,10, 0.001,0.003,0.0001)
# data = generujData(par,100)
# data[[1]]
# data[[2]]








































