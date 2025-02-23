# -*- coding: utf-8 -*-
"""UBER_II

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rmm41784W95HXXBbyOSdOQWKh9bVJxaw
"""

import warnings
warnings.filterwarnings("ignore")
import os
import numpy as np
import pandas as pd
import seaborn as sns
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from xgboost import plot_importance, plot_tree
from sklearn.model_selection import train_test_split
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV,TimeSeriesSplit

df = pd.read_csv("/content/Uber.csv")

df.head()

df.shape

df.describe()

df.info()

df.isnull().sum()

df['date'] = pd.to_datetime(df['date'])

df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

df

months_count = df['month'].value_counts()
plt.pie(months_count, labels=months_count, autopct='%1.2f%%', startangle=90)
plt.title('Months Distribution')
plt.show()

df['dispatching_base_number'].unique()

df['date_ordinal'] = df['date'].apply(lambda date: date.toordinal())

df = pd.get_dummies(df, columns=['dispatching_base_number'], drop_first=True)

x = df.drop(columns=['date','trips','day','month','year'])
y = df['trips']

plt.figure(figsize=(20, 8))
plt.plot(df['trips'],linewidth = 1, color='darkslateblue')
plt.xticks(rotation=30,ha='right')
plt.show()

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
y_pred

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R^2 Score:", r2_score(y_test, y_pred))

plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred, alpha=0.3)
plt.xlabel('Actual Trips')
plt.ylabel('Predicted Trips')
plt.title('Actual vs Predicted Trips')
plt.show()

x_test

pred = model.predict(x_test)
pred

y_predo = model.predict(x_testo)
y_predo

xgb_param_grid = {
'n_estimators': [100, 200, 300],
'max_depth': [3, 6, 9],
'learning_rate': [0.01, 0.1, 0.3],
'subsample': [0.6, 0.8, 1.0],
'colsample_bytree': [0.6, 0.8, 1.0]
}

tscv = TimeSeriesSplit(n_splits=5)

xgb_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)

xgb_grid_search = GridSearchCV(
    estimator=xgb_model,
    param_grid=xgb_param_grid,
    cv=tscv,
    scoring='neg_mean_absolute_percentage_error',
    n_jobs=-1,
    verbose=2
)
xgb_grid_search.fit(x_train, y_train)

print("Best XGBoost parameters:", xgb_grid_search.best_params_)

xgb_predict = xgb_grid_search.best_estimator_.predict(x_test)

xgb_mape = mean_absolute_percentage_error(y_test, xgb_predict)
print(f'XGBoost MAPE:\t\t{xgb_mape:.2%}')

