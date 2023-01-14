s <- 0.8
u1 <- 1.01
d1 <- 0.99
u2 <- 5.00
d2 <- 0.70

util<-function(x){
2+log(x-s)
}

risk_aversion <- function(x){
1/(x-s)
}

Eutil<-function(w){
w1 <-w
w2 <- 1-w
p1 <- 0.5
p2 <- 0.5
q1 <- 1-p1
q2 <- 1-p2
p1*p2*util(w1*u1+w2*u2)+p1*q2*util(w1*u1+w2*d2)+q1*p2*util(w1*d1+w2*u1)+q1*q2*util(w1*d1+w2*d2)
}

opt_wt <- function(){
## w d1 + (1-w)d2 = s    =>    w(d1-d2)= (s-d2)
wmin <- (s-d2)/(d1-d2)
result<- optimize(Eutil,interval=c(wmin+0.001,1),maximum=TRUE)
wstar <-result$maximum
utility<-result$objective
low <- wstar*d1 +(1-wstar)*d2
cat("d1=", d1, "Weight in safe asset=", wstar, "Exp Util=", utility, "\n")
cat("Lowest wealth=", low, " At this point risk aversion=", risk_aversion(low), "\n")
}

opt_wt()

d1 <- 0.90
opt_wt()

u1 <- 1.15
d1 <- 0.85
opt_wt()

curve(risk_aversion,0.85,3)


