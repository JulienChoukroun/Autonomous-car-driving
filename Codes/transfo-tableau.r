# Authors: Julien Choukroun, Jessica Gourdon, Luc Sagnes

# This code is used to create the dataset.

library(dplyr)

options("digits" = 13)

getwd()
vitesse=read.csv(file="data9.csv", sep=';',na.string="NA")

image=read.csv(file="time_images9.csv", sep=";", na.string="NA")

# The image/time file starts ealier than the speed/steering/time file so the first values of the image/time file are deleted.

mintime=min(vitesse$Time)

image <- image %>%
  filter(Time>=mintime)

# The image/time file ends later than the speed/steering/time file so the last values of the image/time file are deleted. 

maxtime=max(vitesse$Time)

image <- image %>%
  filter(Time<=maxtime)

# For each image data, we take the data in time that has the closest time.

sizeimage=length(image$Time)
sizevitesse=length(vitesse$Time)

# We do the first step manually to initialize the vitesse2 dataframe.
timeimage=image$Time[1]
distmin=min(abs(timeimage-vitesse$Time))
for (j in 1 : sizevitesse){
   if(abs(timeimage-vitesse$Time[j])==distmin){
      vit2=vitesse$Time[j]
      ind2=which(vitesse$Time %in% vit2)
      vitesse2 <- vitesse[ind2,]
      break
   }
}

# We loop on the rest.
for (i in 2:sizeimage){
   timeimage=image$Time[i]
   distmin=min(abs(timeimage-vitesse$Time))
   for (j in 1 : sizevitesse){
      if(abs(timeimage-vitesse$Time[j])==distmin){
         vit=vitesse$Time[j]
         ind=which(vitesse$Time %in% vit)
         vitesse2 <- rbind(vitesse2,vitesse[ind,])
         break
      }
   }
}

tableaufinal <- image %>%
   mutate(vitesses=vitesse2$Vitesse, angles= vitesse2$Angle )

# We put the time in the last column.

tableaufinal <- tableaufinal[, c(1,3,4,2)]
tableaufinal <- tableaufinal %>%
   filter(vitesses>0)

#setwd("C:\Users\cevat\Documents\Polytech\MAM4\ProjetVoitures\Dataset\csv")
write.csv2(tableaufinal,file="Database9.csv")
