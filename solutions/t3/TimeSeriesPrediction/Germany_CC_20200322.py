# This code was specificly tuned for "Germany_CC_20200322.png" image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from prophet import Prophet
from datetime import datetime
import holidays
import seaborn as sns

from prophet.plot import add_changepoints_to_plot

def diff(col):
    colout = np.zeros(len(col))
    col = col.to_numpy()
    for i in range(len(col)-1):
        colout[i] = col[i+1]-col[i]
    return colout

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'same') / w

data = pd.read_csv('OxCGRT_latest.csv',low_memory=False)
# Preview the first 5 lines of the loaded data
country = data[data['CountryName']=='Germany']
sc = country['ConfirmedCases']
confirmedpd = diff(sc)
confirmedpd = moving_average(confirmedpd,7)

newdf = pd.DataFrame(columns=['Date', 'AverageConfirmedCases'])
newdf['Date'] = country['Date']
newdf['AverageConfirmedCases'] = confirmedpd.tolist()
newdf.dropna(subset=['AverageConfirmedCases'], inplace=True)

policy_date = 20200322
next_policy_date = 20200422
df_renamed = newdf.rename(columns = {'AverageConfirmedCases': 'y', 'Date': 'ds'}, inplace = False)
df_real = df_renamed[(df_renamed['ds'] <= next_policy_date) & (df_renamed['ds'] > policy_date)]
df_real['ds'] = df_real['ds'].apply(lambda x: str(x)[0:4]+'-'+str(x)[4:6]+'-'+str(x)[6:])
# df_real.plot.scatter(x='ds',y='y')
# plt.xticks(rotation='vertical')
# plt.show()

df_renamed = df_renamed[df_renamed['ds'] <= policy_date]
df_renamed['floor'] = 0 # cannot be less than zero


df_renamed['ds'] = df_renamed['ds'].apply(lambda x: str(x)[0:4]+'-'+str(x)[4:6]+'-'+str(x)[6:])
de_holidays = holidays.DE()
holidays_df = pd.DataFrame()
holidays_df['ds'] = df_renamed['ds']
holidays_df['holiday'] = df_renamed['ds'].apply(lambda x: de_holidays.get(x))
holidays_df = holidays_df.dropna()
m = Prophet(changepoint_range=0.9, changepoint_prior_scale=0.2, yearly_seasonality=1, holidays=holidays_df) # , yearly_seasonality=10
m.add_country_holidays(country_name='DE')
m.fit(df_renamed)
print(m.train_holiday_names)

future = m.make_future_dataframe(periods=30)
future['floor'] = 0 # cannot be less than zero
# future.tail()

# Python
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))

# Python

str_policy_date = str(policy_date)[0:4]+'-'+str(policy_date)[4:6]+'-'+str(policy_date)[6:]
next_str_policy_date = str(next_policy_date)[0:4]+'-'+str(next_policy_date)[4:6]+'-'+str(next_policy_date)[6:]
df_for = forecast[(forecast['ds'] <= datetime.strptime(next_str_policy_date, '%Y-%m-%d')) &
                  (forecast['ds'] > datetime.strptime(str_policy_date, '%Y-%m-%d'))]
df_real['ds'] = df_real['ds'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
# df_real = df_real.join(df_for[['ds', 'yhat']].set_index('ds'), on='ds')

realvalue = df_real['y'].to_numpy()
predvalue = df_for['yhat'].to_numpy()
sum_save = 0
for i in range(30):
    sum_save = sum_save + (predvalue[i]-realvalue[i])

fig1 = m.plot(forecast)
sns.scatterplot(ax=fig1.axes[0], data=df_real, x='ds', y='y')
fig1.legend(labels=['Confirmed Cases before closing schools','predicted trend','Confidence interval','Confirmed Cases after closing schools'])
fig1.axes[0].set_ylabel('Confirmed Cases')
fig1.axes[0].set_xlabel('Date')

plt.vlines(datetime.strptime(str_policy_date, '%Y-%m-%d'),0,5000,colors='r')
str_policy_date = '2020-03-16'
plt.vlines(datetime.strptime(str_policy_date, '%Y-%m-%d'),0,5000,colors='g',label='Workplace close')
# str_policy_date = '2020-12-16'
# plt.vlines(datetime.strptime(str_policy_date, '%Y-%m-%d'),0,5000,colors='b',label='StayAtHomeRequired')
plt.savefig('Germany_CC_' + str(policy_date), dpi=1200)
plt.show()


