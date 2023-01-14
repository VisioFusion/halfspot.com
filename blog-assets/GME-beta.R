# Load required packages
library(Hmisc)
library(MASS)
library(L1pack)

# Set up the data
gme = read.csv('GME-SP500.csv')
gme$gmeret = log(gme$gme / Lag(gme$gme))
gme$spret = log(gme$sp500 / Lag(gme$sp500))
gme$Date = as.Date(gme$Date)
gme21 = gme[gme$Date > as.Date('2020-12-31'),]

# Scatter plot
png('GME-vs-SP500.png')
plot(gme21$spret, gme21$gmeret, xlab = "S&P 500 Returns", ylab = "GME Returns",
     main = "GME vs S&P 500 (1-Jan-2021 to 16-Mar-2021)")
dev.off()

# Naive OLS
ols = lm(gmeret ~ spret, data = gme21)
summary(ols)

# OLS with two outliers removed
outliers = as.Date(c('2021-01-27', '2021-02-02'))
ols_sans_outliers = lm(gmeret ~ spret, data = gme21[! gme21$Date %in% outliers,])
summary(ols_sans_outliers)

# Least Absolute Deviation (LAD) regression
L1 = lad(gmeret ~ spret, data = gme21)
summary(L1)

# Robust regression using bisquare method
bisquare = rlm(gmeret ~ spret, data = gme21, psi=psi.bisquare)
summary(bisquare)

