# kreslenie grafov z realnych dat




plot1 = function(data,odhad){
  p1 = ggplot() +
    geom_point(aes(x = data[odhad[1,17]:odhad[1,18],1],
                   y = data[odhad[1,17]:odhad[1,18],2]), alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[1,17]:odhad[1,18]),1],
                   y = data[-c(odhad[1,17]:odhad[1,18]),2]), alpha = 0.2,color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[1,17],odhad[1,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[1,17]),
                                                 sprintf("koniec\nn = %d",odhad[1,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  
  p2 = ggplot() +
    geom_point(aes(x = data[odhad[2,17]:odhad[2,18],1],
                   y = data[odhad[2,17]:odhad[2,18],2]), alpha = 0.2,color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[2,17]:odhad[2,18]),1],
                   y = data[-c(odhad[2,17]:odhad[2,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[2,17],odhad[2,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[2,17]),
                                                 sprintf("koniec\nn = %d",odhad[2,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p3 = ggplot() +
    geom_point(aes(x = data[odhad[3,17]:odhad[3,18],1],
                   y = data[odhad[3,17]:odhad[3,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[3,17]:odhad[3,18]),1],
                   y = data[-c(odhad[3,17]:odhad[3,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[3,17],odhad[3,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[3,17]),
                                                 sprintf("koniec\nn = %d",odhad[3,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p4 = ggplot() +
    geom_point(aes(x = data[odhad[4,17]:odhad[4,18],1],
                   y = data[odhad[4,17]:odhad[4,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[4,17]:odhad[4,18]),1],
                   y = data[-c(odhad[4,17]:odhad[4,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[4,17],odhad[4,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[4,17]),
                                                 sprintf("koniec\nn = %d",odhad[4,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p5 = ggplot() +
    geom_point(aes(x = data[odhad[5,17]:odhad[5,18],1],
                   y = data[odhad[5,17]:odhad[5,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[5,17]:odhad[5,18]),1],
                   y = data[-c(odhad[5,17]:odhad[5,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[5,17],odhad[5,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[5,17]),
                                                 sprintf("koniec\nn = %d",odhad[5,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p6 = ggplot() +
    geom_point(aes(x = data[odhad[6,17]:odhad[6,18],1],
                   y = data[odhad[6,17]:odhad[6,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[6,17]:odhad[6,18]),1],
                   y = data[-c(odhad[6,17]:odhad[6,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[6,17],odhad[6,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[6,17]),
                                                 sprintf("koniec\nn = %d",odhad[6,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p7 = ggplot() +
    geom_point(aes(x = data[odhad[7,17]:odhad[7,18],1],
                   y = data[odhad[7,17]:odhad[7,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[7,17]:odhad[7,18]),1],
                   y = data[-c(odhad[7,17]:odhad[7,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[7,17],odhad[7,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[7,17]),
                                                 sprintf("koniec\nn = %d",odhad[7,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  plot = grid.arrange(p1,p2,p3,p4,p5,p6,p7,ncol = 2, bottom = "veækosù segmentu pre odhad parametrov je pribliûne 15% zo vzorky")
  
  return(plot)
}



plot2 = function(data,odhad){
  p1 = ggplot() +
    geom_point(aes(x = data[odhad[8,17]:odhad[8,18],1],
                   y = data[odhad[8,17]:odhad[8,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[8,17]:odhad[8,18]),1],
                   y = data[-c(odhad[8,17]:odhad[8,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[8,17],odhad[8,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[8,17]),
                                                 sprintf("koniec\nn = %d",odhad[8,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  
  p2 = ggplot() +
    geom_point(aes(x = data[odhad[9,17]:odhad[9,18],1],
                   y = data[odhad[9,17]:odhad[9,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[9,17]:odhad[9,18]),1],
                   y = data[-c(odhad[9,17]:odhad[9,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[9,17],odhad[9,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[9,17]),
                                                 sprintf("koniec\nn = %d",odhad[9,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p3 = ggplot() +
    geom_point(aes(x = data[odhad[10,17]:odhad[10,18],1],
                   y = data[odhad[10,17]:odhad[10,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[10,17]:odhad[10,18]),1],
                   y = data[-c(odhad[10,17]:odhad[10,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[10,17],odhad[10,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[10,17]),
                                                 sprintf("koniec\nn = %d",odhad[10,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p4 = ggplot() +
    geom_point(aes(x = data[odhad[11,17]:odhad[11,18],1],
                   y = data[odhad[11,17]:odhad[11,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[11,17]:odhad[11,18]),1],
                   y = data[-c(odhad[11,17]:odhad[11,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[11,17],odhad[11,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[11,17]),
                                                 sprintf("koniec\nn = %d",odhad[11,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p5 = ggplot() +
    geom_point(aes(x = data[odhad[12,17]:odhad[12,18],1],
                   y = data[odhad[12,17]:odhad[12,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[12,17]:odhad[12,18]),1],
                   y = data[-c(odhad[12,17]:odhad[12,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[12,17],odhad[12,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[12,17]),
                                                 sprintf("koniec\nn = %d",odhad[12,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p6 = ggplot() +
    geom_point(aes(x = data[odhad[13,17]:odhad[13,18],1],
                   y = data[odhad[13,17]:odhad[13,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[13,17]:odhad[13,18]),1],
                   y = data[-c(odhad[13,17]:odhad[13,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[13,17],odhad[13,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[13,17]),
                                                 sprintf("koniec\nn = %d",odhad[13,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  

  
  plot = grid.arrange(p1,p2,p3,p4,p5,p6,ncol = 2, bottom = "veækosù segmentu pre odhad parametrov je pribliûne 30% zo vzorky")
  
  return(plot)
}





plot3 = function(data,odhad){
  p1 = ggplot() +
    geom_point(aes(x = data[odhad[14,17]:odhad[14,18],1],
                   y = data[odhad[14,17]:odhad[14,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[14,17]:odhad[14,18]),1],
                   y = data[-c(odhad[14,17]:odhad[14,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[14,17],odhad[14,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[14,17]),
                                                 sprintf("koniec\nn = %d",odhad[14,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  
  p2 = ggplot() +
    geom_point(aes(x = data[odhad[15,17]:odhad[15,18],1],
                   y = data[odhad[15,17]:odhad[15,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[15,17]:odhad[15,18]),1],
                   y = data[-c(odhad[15,17]:odhad[15,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[15,17],odhad[15,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[15,17]),
                                                 sprintf("koniec\nn = %d",odhad[15,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p3 = ggplot() +
    geom_point(aes(x = data[odhad[16,17]:odhad[16,18],1],
                   y = data[odhad[16,17]:odhad[16,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[16,17]:odhad[16,18]),1],
                   y = data[-c(odhad[16,17]:odhad[16,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[16,17],odhad[16,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[16,17]),
                                                 sprintf("koniec\nn = %d",odhad[16,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p4 = ggplot() +
    geom_point(aes(x = data[odhad[17,17]:odhad[17,18],1],
                   y = data[odhad[17,17]:odhad[17,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[17,17]:odhad[17,18]),1],
                   y = data[-c(odhad[17,17]:odhad[17,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[17,17],odhad[17,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[17,17]),
                                                 sprintf("koniec\nn = %d",odhad[17,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p5 = ggplot() +
    geom_point(aes(x = data[odhad[18,17]:odhad[18,18],1],
                   y = data[odhad[18,17]:odhad[18,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[18,17]:odhad[18,18]),1],
                   y = data[-c(odhad[18,17]:odhad[18,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[18,17],odhad[18,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[18,17]),
                                                 sprintf("koniec\nn = %d",odhad[18,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)

  
  
  plot = grid.arrange(p1,p2,p3,p4,p5,ncol = 2, bottom = "veækosù segmentu pre odhad parametrov je pribliûne 45% zo vzorky")
  
  return(plot)
}




plot4 = function(data,odhad){
  p1 = ggplot() +
    geom_point(aes(x = data[odhad[19,17]:odhad[19,18],1],
                   y = data[odhad[19,17]:odhad[19,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[19,17]:odhad[19,18]),1],
                   y = data[-c(odhad[19,17]:odhad[19,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[19,17],odhad[19,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[19,17]),
                                                 sprintf("koniec\nn = %d",odhad[19,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p2 = ggplot() +
    geom_point(aes(x = data[odhad[20,17]:odhad[20,18],1],
                   y = data[odhad[20,17]:odhad[20,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[20,17]:odhad[20,18]),1],
                   y = data[-c(odhad[20,17]:odhad[20,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[20,17],odhad[20,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[20,17]),
                                                 sprintf("koniec\nn = %d",odhad[20,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p3 = ggplot() +
    geom_point(aes(x = data[odhad[21,17]:odhad[21,18],1],
                   y = data[odhad[21,17]:odhad[21,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[21,17]:odhad[21,18]),1],
                   y = data[-c(odhad[21,17]:odhad[21,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[21,17],odhad[21,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[21,17]),
                                                 sprintf("koniec\nn = %d",odhad[21,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p4 = ggplot() +
    geom_point(aes(x = data[odhad[22,17]:odhad[22,18],1],
                   y = data[odhad[22,17]:odhad[22,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[22,17]:odhad[22,18]),1],
                   y = data[-c(odhad[22,17]:odhad[22,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[22,17],odhad[22,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[22,17]),
                                                 sprintf("koniec\nn = %d",odhad[22,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  
  plot = grid.arrange(p1,p2,p3,p4,ncol = 2, bottom = "veækosù segmentu pre odhad parametrov je pribliûne 60% zo vzorky")
  
  return(plot)
}




plot5 = function(data,odhad){
  p1 = ggplot() +
    geom_point(aes(x = data[odhad[23,17]:odhad[23,18],1],
                   y = data[odhad[23,17]:odhad[23,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[23,17]:odhad[23,18]),1],
                   y = data[-c(odhad[23,17]:odhad[23,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[23,17],odhad[23,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[23,17]),
                                                 sprintf("koniec\nn = %d",odhad[23,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p2 = ggplot() +
    geom_point(aes(x = data[odhad[24,17]:odhad[24,18],1],
                   y = data[odhad[24,17]:odhad[24,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[24,17]:odhad[24,18]),1],
                   y = data[-c(odhad[24,17]:odhad[24,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[24,17],odhad[24,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[24,17]),
                                                 sprintf("koniec\nn = %d",odhad[24,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  p3 = ggplot() +
    geom_point(aes(x = data[odhad[25,17]:odhad[25,18],1],
                   y = data[odhad[25,17]:odhad[25,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[25,17]:odhad[25,18]),1],
                   y = data[-c(odhad[25,17]:odhad[25,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[25,17],odhad[25,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[25,17]),
                                                 sprintf("koniec\nn = %d",odhad[25,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  plot = grid.arrange(p1,p2,p3,ncol = 2, bottom = "veækosù segmentu pre odhad parametrov je pribliûne 75% zo vzorky")
  
  return(plot)
}



plot6 = function(data,odhad){
  p1 = ggplot() +
    geom_point(aes(x = data[odhad[26,17]:odhad[26,18],1],
                   y = data[odhad[26,17]:odhad[26,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[26,17]:odhad[26,18]),1],
                   y = data[-c(odhad[26,17]:odhad[26,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[26,17],odhad[26,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok\nn = %d",odhad[26,17]),
                                                 sprintf("koniec\nn = %d",odhad[26,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)
  
  
  p2 = ggplot() +
    geom_point(aes(x = data[odhad[27,17]:odhad[27,18],1],
                   y = data[odhad[27,17]:odhad[27,18],2]),alpha = 0.2, color = "#B71C1C") +
    geom_point(aes(x = data[-c(odhad[27,17]:odhad[27,18]),1],
                   y = data[-c(odhad[27,17]:odhad[27,18]),2]),alpha = 0.2, color = "black") +
    xlab("x") + ylab("y") +
    geom_label_repel(data = data[c(1,odhad[27,17],odhad[27,18]),],
                     aes(x = x, y = y, label = c("zaËiatok dataframe",
                                                 sprintf("zaËiatok odhadu\nn = %d",odhad[27,17]),
                                                 sprintf("koniec odhadu\nn = %d",odhad[27,18]))),
                     box.padding = unit(1.5, "lines"),
                     point.padding = unit(1.5, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2)

  
  plot = grid.arrange(p1,p2,ncol = 2, bottom = "veækosù segmentu pre odhad parametrov je pribliûne 90% zo vzorky") 
    
  
  return(plot)
}





plot7 = function(data,odhad){
  p1 = ggplot(data = data) +
    geom_point(aes(x = x, y = y),alpha = 0.2, color = "#B71C1C") +
    xlab("x") + ylab("y")  +
    geom_label_repel(data = data[1:3,],
                     aes(x = x[1:3], y = y[1:3], label = c("zaËiatok dataframe",
                                                           "zaËiatok odhadu",
                                                           "koniec odhadu")),
                     box.padding = unit(2, "lines"),
                     point.padding = unit(2, 'lines'),
                     colour = "black", 
                     fill = "grey",
                     fontface = "bold", 
                     size = 2.9)
   
  return(p1)
}













