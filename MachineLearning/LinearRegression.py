import pandas as pd 
import quandl, math, datetime
import numpy as np 
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt 
from matplotlib import style 
from matplotlib import use
use('TkAgg')
style.use("ggplot")
## Dataset
df = quandl.get("WIKI/GOOGL")
df = df[["Adj. Open","Adj. High", "Adj. Low", "Adj. Close", "Adj. Volume"]]

df["HL_PCT"] = (df["Adj. High"] - df["Adj. Close"]) / df["Adj. Close"] * 100
df["PCT_change"] = (df["Adj. Close"] - df["Adj. Open"]) / df["Adj. Open"] * 100
df = df[["Adj. Close", "HL_PCT", "PCT_change", "Adj. Volume"]]

## Select our future label, the column datathat we are going to predict
forecast_col ="Adj. Close"
## Fill NA (not a number) with a value
df.fillna(-99999, inplace=True)
## Specify how many days in the future in the future our predection is going to be
forecast_out = (int(math.ceil(0.01*len(df))))

## Create the label column, with the data that we already know of adj close each amount of days
## by shifting up the rows of the adj close
df["Label"] = df[forecast_col].shift(-forecast_out)


## Features of the dataset
X = np.array(df.drop(["Label"], 1))

## Standarize the colums array
##X = preprocessing.scale(X)

X_lately = X[-forecast_out:]
X = X[:-forecast_out]
print(X)
print(X_lately)

df.dropna(inplace=True)
## Label of the dataset
Y = np.array(df["Label"])

## Shuffle the arrays and return into two different groups 
## One for training and outher for testig 
## The relation between columns is maintined 
## The only thing that changes is the order
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2)

## Specifies the classifier algorithm
clf = LinearRegression()
## Train the classifier with some date
clf.fit(X_train,Y_train)
## Test the classifier with the test group
accuracy = clf.score(X_test, Y_test)

##Predict the lately values
forecast_set = clf.predict(X_lately)

 
##----------------------PRE-PlOTTING PREPARATION ----------------------- 
## ----------------X= time Y = price
df["Forecast"] = np.nan

##Last day we have stored
last_date = df.iloc[-1].name
##Last date in seconds
last_unix = last_date.timestamp()
one_day = 86400 ## seconds of a day
##n Next day
next_unix = last_unix + one_day
for i in forecast_set:
    ## tansform into actual day
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    ## For each new day, create all columns null, and then add the forecast column to the 
    df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]


print(forecast_set, accuracy, forecast_out)

## Ploting into a graph
df["Adj. Close"].plot()
df["Forecast"].plot()
plt.legend(loc=4)
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()
