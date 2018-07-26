# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 09:13:35 2018

@author: patelj
"""

import pandas as pd

FILE_PATH_INPUT = 'C:/Users/patelj/Documents/Project/Predictive-Model---Claires/Jayraj-Patel-Model/NA - Predictive Model/2018/1. Data Processing/Input Data/'

FILE_PATH_OUTPUT = 'C:/Users/patelj/Documents/Project/Predictive-Model---Claires/Jayraj-Patel-Model/NA - Predictive Model/2018/1. Data Processing/Output Data/'

# Import required datasets from excel
promo_df = pd.read_excel(FILE_PATH_INPUT+'NA Promo Data.xlsm', sheetname='Promo_Data')
hol_df = pd.read_excel(FILE_PATH_INPUT+'NA Holiday Data.xlsm', sheetname='Holiday_Data')
sales_df = pd.read_excel(FILE_PATH_INPUT+'Output Sales.xlsx', sheetname='Sales_Sorted')
store_hours_df = pd.read_excel(FILE_PATH_INPUT+'Updated Store Hours.xlsm', sheetname='Formatted')





### Assign the right data types to the features. for example, store number should be categorical

sales_df['Store Number'] = sales_df.Store_Number.astype('category')



###############################################################################################

#### extract week, day of the week from transaction date

def extract_dayofweek(date):
    return date.dayofweek

def extract_weeknum(date):
    return date.week


###########################################################################################
    
######### Join various data frames to get one unified dataframe ################ 
sales_storeHours_df = pd.merge(sales_df, store_hours_df,
                 how='left', on=['Store_Number','Transaction_Date'])
sales_storeHours_df.shape

hol_df.fillna('None', inplace=True) ### fill NA with None

sales_storeHours_hol_df = pd.merge(sales_storeHours_df, hol_df,
                 how='left', on=['Store_Number','Transaction_Date'])
sales_storeHours_hol_df.shape


sales_storeHours_hol_promo_df = pd.merge(sales_storeHours_hol_df, promo_df,
                 how='left', on=['Store_Number','Transaction_Date'])
sales_storeHours_hol_promo_df.shape



sales_storeHours_hol_promo_df['Day_of_Week']  = sales_storeHours_hol_promo_df.Transaction_Date.apply(extract_dayofweek)
sales_storeHours_hol_promo_df['Week_Num'] = sales_storeHours_hol_promo_df.Transaction_Date.apply(extract_weeknum)
###############################################################################

###### Merge the weather data into main dataframe #############################
#weather_cols = ['Airport_Code', 'Transaction_Date', 'rain', 'snow', 'meantempi', 
#       'meandewpti', 'meanwindspdi', 'humidity', 'precipi']

#weather_subset_df = weather_df[weather_cols]
#weather_subset_df = pd.merge(weather_subset_df,store_airportCode_df, how='left', on=['Airport_Code'])

### convert Transaction Date to Datetime object

#weather_subset_df.Transaction_Date = pd.to_datetime(weather_subset_df.Transaction_Date)
#sales_storeHours_hol_promo_weather_df = pd.merge(sales_storeHours_hol_promo_df, weather_subset_df, how='left', on=['Store_Number','Transaction_Date'])
#sales_storeHours_hol_promo_weather_df.shape
###############################################################################

#### filter out any records with open hours less than 0 ###

#sales_storeHours_hol_promo_weather_df = sales_storeHours_hol_promo_weather_df.loc[sales_storeHours_hol_promo_df['Open Hours']>0,:]

######## save the dataframe ##############################

writer = pd.ExcelWriter(FILE_PATH_OUTPUT+'Sales-StoreHours-Hol-Promo.xlsx')
sales_storeHours_hol_promo_df.to_excel(writer,'Data')
writer.save()
