install.packages("plm")
install.packages("Formula")
install.packages("stargazer")
install.packages("readxl")

# -----------------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------------

setwd("C:\\Users\\filip\\Desktop\\AE project")
Sys.setenv(LANG = "en")
options(scipen=999)

library("MASS")
library("sandwich")
library("zoo")
library("car")
library("lmtest")
library("Formula")
library("plm")
library("stargazer")
library("readxl")

####################
CO2 <- read_excel("CO2_data.xlsx", col_names = TRUE)
head(CO2)
summary(CO2)


