import numpy as np
import pandas as pd
from datetime import datetime
from scipy.stats import ttest_ind, ttest_rel
import scipy.stats as st


#read both datasets into a pandas dataframe
df_sales = pd.read_csv('')
df_feedback = pd.read_csv('')

print(df_sales.head(5)) 
print(df_feedback.head(5))



#convert date column in both datasets into a pandas dataframe object
df_sales_date = df_sales[['date']]
df_feedback_date = df_feedback[['date']]

print(df_sales_date.head(5))
print(df_feedback_date.head(5))


#two-tail: the data is not related
#independent: it is unknown if the data may skew in favor of one platform or another 
#H_0: There is no signficant different in average customer satisfaction between products
def feedback_analysis(df_feedback):

    #convert the feedback scores into 2D np.array    
    feedback_score = df_feedback['feedback_score']
    ios_score = feedback_score[df_feedback['product'] == 'iOS']
    android_score = feedback_score[df_feedback['product'] == 'Android']
    feedback_score_array = np.array([ios_score, android_score])


    #check the variance equality
    equal = True
    if feedback_score_array[0].std() > feedback_score_array[1].std():
        if (feedback_score_array[0].std() / feedback_score_array[1].std() > 2):
            equal = False

        else:
            if (feedback_score_array[1].std() / feedback_score_array[0].std()) > 2:
                equal = False


    #run the test and return result
    sampleT = ttest_ind(feedback_score_array[0], feedback_score_array[1], equal_var = equal)
    result = sampleT.pvalue
    print(f'The p-value customer feedback is: {result}')

    if result > .05:
        print('Accept the null hypothesis: there is no significant difference in average customer satisfaction between products')
    else:
        print('Reject the null hypothesis: there is a significant difference in average customer satisfaction between products')



#one tail t_test: expectation for the sales to improve given the implementation of a marketing campaign
#independent t_test: originally paired, but unequal sales resulted in a switch to independent t_test woth false equal variance
#H_0: There is no signficant different in sales after the marketing campaign
def sales_analysis(df_sales):

    #uniform and isolate the sales between March 1-31, 2023
    df_sales['date'] = pd.to_datetime(df_sales['date'])
    campaign_start = pd.to_datetime('3/1/23')
    campaign_end = pd.to_datetime('3/31/23')

    pre_campaign_sales = (df_sales['date'] < campaign_start)
    post_campaign_sales = (df_sales['date'] > campaign_end)

    pre_campaign_data = df_sales[pre_campaign_sales]
    post_campaign_data = df_sales[post_campaign_sales]


    #convert to np arrays
    pre_campaign_array = np.array(pre_campaign_data['sales'])
    post_campaign_array = np.array(post_campaign_data['sales'])


    #evaluate variance equality
    equal = True
    if pre_campaign_array.std() > post_campaign_array.std():
        if (pre_campaign_array.std() / post_campaign_array .std() > 2):
            equal = False

    else:
        if (post_campaign_array.std() / pre_campaign_array.std()) > 2:
            equal = False


    #run the test and return the results
    sampleT = ttest_ind(pre_campaign_array, post_campaign_array, equal_var = equal)
    result = sampleT.pvalue
    result = result / 2
    print(f'The p-value for sales analysis is: {result}')

    if result > .05:
        print('Accept the null hypothesis: there is no significant difference in sales after the marketing campaign')
    else:
        print('Reject the null hypothesis: there is a significant difference in sales after the marketing campaign')



#independent t-test: the datasets across the months are not paired
#two-tailed: it is unclear if there is an expected sales changes based on the season on one direction, thus a two-tailed
#H_0: There is no signficant different in sales based on seasonality
def seasonal_analysis(df_sales):

    #uniform and isolate the summer (June-August) sales and the winter (December-February) sales
    df_sales['date'] = pd.to_datetime(df_sales['date'])
    summer_start_sales = pd.to_datetime('6/1/2023')
    summer_end_sales = pd.to_datetime('8/31/2023')
    winter_start_sales = pd.to_datetime('12/1/2022')
    winter_end_sales = pd.to_datetime('2/28/2023')

    summer_sales = (df_sales['date'] > summer_start_sales) & (df_sales['date'] < summer_end_sales)
    winter_sales = (df_sales['date'] > winter_start_sales) & (df_sales['date'] < winter_end_sales)

    winter_sales_data = df_sales[winter_sales]['sales']
    summer_sales_data = df_sales[summer_sales]['sales']


    #convert the data to np.arrays
    winter_sales_array = np.array(winter_sales_data)
    summer_sales_array = np.array(summer_sales_data)

    #evaluate variance equality
    equal = True
    if winter_sales_array.std() > summer_sales_array.std():
        if (winter_sales_array.std() / summer_sales_array .std() > 2):
            equal = False

    else:
        if (summer_sales_array.std() / winter_sales_array.std()) > 2:
            equal = False


    #run the test and return the result
    sampleT = ttest_ind(winter_sales_array, summer_sales_array, equal_var=equal)
    result = sampleT.pvalue
    print(f'The p-value for seasonal analysis is: {result}')

    if result > 0.05:
        print('Accept the null hypothesis: there is no significant difference in sales between summer and winter')
    else:
        print('Reject the null hypothesis: there is a significant difference in sales between summer and winter')



#use one way ANOVA
#H_0: There is no signficant difference in consistency of sales across the specified months
def consistency_analysis(df_feedback):

    #standardize dates
    df_feedback['date'] = pd.to_datetime(df_feedback['date'])

    #isloate Jan, May, Spet, and Dec feedback scores
    january_data = df_feedback[df_feedback['date'].dt.month == 1]['feedback_score']
    may_data = df_feedback[df_feedback['date'].dt.month == 5]['feedback_score']
    september_data = df_feedback[df_feedback['date'].dt.month == 9]['feedback_score']
    december_data = df_feedback[df_feedback['date'].dt.month == 12]['feedback_score']


    #run the oneway ANOVA test
    result = st.f_oneway(january_data, may_data, september_data, december_data)
    print(result)

    if result.pvalue > 0.05:
        print('Accept the null hypothesis: there is no significant difference in consistency across the specified the months')
    else:
        print('Reject the null hypothesis: there is a significant difference in consistency across the specified the months')



#independent t_test: since the data is independent of each other
#two-_tailed: there is no indication that the data is would skew only higher or lower
#H_0: There is no signficant difference in relationship between the level of sales and feedback scores
def corr_analysis(df_feedback, df_sales):

    df_combined_high = pd.merge(df_feedback[df_feedback['feedback_score'] > 5], df_sales, how = 'inner')
    df_combined_low = pd.merge(df_feedback[df_feedback['feedback_score'] < 6], df_sales, how = 'inner')

    #convert sales and feedback_score to arrays
    df_combined_low_data = df_combined_low[['sales','feedback_score']]
    df_combined_high_data = df_combined_high[['sales','feedback_score']]


    #convert to an np array
    df_high_array = np.array(df_combined_high_data)
    df_low_array = np.array(df_combined_low_data)


    #check the variance equality
    equal = True
    if df_high_array.std() > df_low_array.std():
        if (df_high_array.std() / df_low_array .std() > 2):
            equal = False

    else:
        if (df_low_array.std() / df_high_array.std()) > 2:
            equal = False


    #run the test and print the results
    result = ttest_ind(df_high_array, df_low_array, equal_var=equal)

    print(result.pvalue[0])
    print(result.pvalue[1])

    if result.pvalue[0] > 0.05:
        print('Accept the null hypothesis: there is no significant difference in sales and high feedback scores')
    else:
        print('Reject the null hypothesis: there is a significant difference in sales and high feedback scores')


    if result.pvalue[1] > 0.05:
        print('Accept the null hypothesis: there is no significant difference in sales and low feedback scores')
    else:
        print('Reject the null hypothesis: there is a significant difference in sales and low feedback scores')


    print('Conclusion:'
    'The result here indicates that the relationship between low feedback scores and sales is significant. Sales can be expected'
    'to be low as long as the feedback scores are low; this seems to indicate that poor feedback scores, assuming they are made public'
    'or reflect future purchases in some manner result in fewer sales. Conversely, a high feedback score does not seems to be significant'
    'enough (although the relationship is borderline) to increase further sales. The company seems to be in a position where it is'
    'punished for poor feedback scores and marginally, if at all, rewarded for high feedback scores.')



feedback_analysis(df_feedback)
sales_analysis(df_sales)
seasonal_analysis(df_sales)
consistency_analysis(df_feedback)
corr_analysis(df_feedback, df_sales)