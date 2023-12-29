import pandas as pd 
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import classification_report as report
import statsmodels.api as sm 
from statsmodels.formula.api import ols



#READ DATA INTO DATAFRAME
file_path = ''

df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'])
# print(df.head(10))

df['Trend'] = np.nan
df['Trend'] = df['Trend'].astype(object)



#CREATE 'TREND' COLUMN AND AD LABEL FOR EACH ROW
df.loc[0, 'Trend'] = 'Bullish'
for x in range(1, len(df)):
    if df['NASDAQ'].iloc[x] > df['NASDAQ'].iloc[x - 1]:
        df.loc[x, 'Trend'] = 'Bullish'
    else:
        if df['NASDAQ'].iloc[x] < df['NASDAQ'].iloc[x - 1]:
            df.loc[x, 'Trend'] = 'Bearish'

# print(df['Trend'].head(10))


#SENTIMMENT ANALYSIS
headlines = df['Headline']
analysis = SentimentIntensityAnalyzer()     #instance of SentimentIntensityAnalyzer
stm_score = headlines.apply(lambda x: analysis.polarity_scores(x))  #lambda method applied to each headlines individually
df['Sentiment'] = stm_score.tolist()    #assign scores specifically to the new column
# print(df['Sentiment']).head(10)
df['compound'] = df['Sentiment'].apply(lambda x: 'positive' if x['compound'] > 0.7 
            else 'negative' if x['compound'] < -0.7 else 'neutral') #new compund column for organization
qualitative_compound = df['compound']
# print(df['compound'].tail(20))




#LINEAR REGRESSION
apple = df['AAPL'] 
df['compound'] = df['Sentiment'].apply(lambda x: x['compound']) #quantitative version of compount scores
stm_results = df['compound']
df_analysis = pd.merge(apple, stm_results, left_index=True, right_index=True, how='inner')
print(df_analysis.head(10))
print(apple.head(10))
print(stm_results.head(10))

results = ols("APPL ~ compound", data=df_analysis).fit()



#LOGISTIC REGRESSION
x = df['Trend']
y = df['compound']

log_analysis = pd.merge(x, y, left_index=True, right_index=True, how='inner')

x = log_analysis.drop('Trend', axis=1)
y = log_analysis['Trend']

x = pd.get_dummies(x, prefix=['compound'], drop_first=True)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=40)

log_model = LogisticRegression()
log_model.fit(x_train, y_train)

y_predict = log_model.predict(x_test)
label_encoder = LabelEncoder()
y_test_encoded = label_encoder.fit_transform(y_test)
y_predict_encoded = label_encoder.transform(y_predict)


apple = df['AAPL'] 
nasdaq = df['NASDAQ']
nya = df['NYA']
spx = df['SPX']
dji = df['DJI']

min_length = min(len(apple), len(nasdaq), len(nya), len(spx), len(dji))

apple = apple[:min_length]
nasdaq = nasdaq[:min_length]
nya = nya[:min_length]
spx = spx[:min_length]
dji = dji[:min_length]

df_aapl_analysis = pd.concat([apple, nasdaq, nya, spx, dji], axis=1, join='inner')
# print(df_aapl_analysis.head(10))
df_aapl_analysis.dropna(inplace=True)



# results = ols("APPL ~ NASDAQ + NYA + SPX + DJI", data=df_aapl_analysis).fit()
# print(results.summary())


#seperate x and y values
y = df_aapl_analysis['AAPL']
x = df_aapl_analysis.drop(['AAPL'], axis=1)

# print(y.head(5))
# print(x.head(5))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=40)

model = LinearRegression()
model.fit(x_train, y_train)
y_predict = model.predict(x_test)
model.score(x_test, y_test)
print(model.score)