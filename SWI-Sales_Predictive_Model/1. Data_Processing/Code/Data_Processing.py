"""
Created on Wed Jan 24 09:30:09 2018

@author: HintonP
"""

import pandas as pd

FILE_PATH_INPUT = 'W:/B&M/Store Segmentation/Pete/Learning/Git/Predictive-Model---Claires/SWI-Sales_Predictive_Model/1. Data_Processing/Input_Data/'

FILE_PATH_OUTPUT = 'W:/B&M/Store Segmentation/Pete/Learning/Git/Predictive-Model---Claires/SWI-Sales_Predictive_Model/1. Data_Processing/Output_Data/'

#### Import required datasets from excel ###########################################################
promo_df = pd.read_excel(FILE_PATH_INPUT+'Promo_Data.xlsm', sheetname='Promo_Data')
hol_df = pd.read_excel(FILE_PATH_INPUT+'Holiday_Data.xlsm', sheetname='Holiday_Data')
sales_df = pd.read_excel(FILE_PATH_INPUT+'Sales_Data.xlsm', sheetname='Sales_Data')
store_hours_df = pd.read_excel(FILE_PATH_INPUT+'Store_Hours_Data.xlsm', sheetname='Store_Hours')
#weather_df = pd.read_csv(FILE_PATH_INPUT+'weather_vF2.csv', parse_dates = True )
store_airportCode_df = pd.read_csv(FILE_PATH_INPUT+'Branch_AirportCode_mapping.csv')

#### Rename columns in weather df ##################################################################

#weather_df.rename(columns = {'City':'Airport_Code', 'Date':'Transaction_Date'}, inplace=True)

### Assign the right data types to the features. for example, store number should be categorical

sales_df['Store_Number'] = sales_df.Store_Number.astype('category')

#### Extract week, day of the week from transaction date ###########################################

def extract_dayofweek(date):
    return date.dayofweek

def extract_weeknum(date):
    return date.week
  
#### Join various data frames to get one unified dataframe #########################################
    
sales_storeHours_df = pd.merge(sales_df, store_hours_df,
                 how='left', on=['Store_Number','Transaction_Date'])
sales_storeHours_df.shape

hol_df.fillna('None', inplace=True) #### fill NA with None

sales_storeHours_hol_df = pd.merge(sales_storeHours_df, hol_df,
                 how='left', on=['Store_Number','Transaction_Date'])
sales_storeHours_hol_df.shape

sales_storeHours_hol_promo_df = pd.merge(sales_storeHours_hol_df, promo_df,
                 how='left', on=['Store_Number','Transaction_Date'])
sales_storeHours_hol_promo_df.shape

sales_storeHours_hol_promo_df['Day_of_Week']  = sales_storeHours_hol_promo_df.Transaction_Date.apply(extract_dayofweek)

sales_storeHours_hol_promo_df['Week_Num'] = sales_storeHours_hol_promo_df.Transaction_Date.apply(extract_weeknum)

#### Filter out any records with open hours less than 0 ############################################

sales_storeHours_hol_promo_df = sales_storeHours_hol_promo_df.loc[sales_storeHours_hol_promo_df['Open Hours']>0,:]

#### Save the dataframe ############################################################################

writer = pd.ExcelWriter(FILE_PATH_OUTPUT+'Sales-StoreHours-Hol-Promo.xlsx')
sales_storeHours_hol_promo_df.to_excel(writer,'Data')
writer.save()

############################ Add Weather #######################################
################################################################################
#
####### Merge the weather data into main dataframe #############################
#weather_cols = ['Airport_Code', 'Transaction_Date', 'rain', 'snow', 'meantempi', 
#       'meandewpti', 'meanwindspdi', 'humidity', 'precipi']
#
#weather_subset_df = weather_df[weather_cols]
#weather_subset_df = pd.merge(weather_subset_df,store_airportCode_df, how='left', on=['Airport_Code'])
#
#sales_storeHours_hol_promo_weather_df = pd.merge(sales_storeHours_hol_promo_df, weather_subset_df, how='left', on=['Store_Number','Transaction_Date'])
#
################################################################################
#
##### filter out any records with open hours less than 0 ###
#
#sales_storeHours_hol_promo_weather_df = sales_storeHours_hol_promo_weather_df.loc[sales_storeHours_hol_promo_df['Open Hours']>0,:]
#
######### save the dataframe ##############################
#
#writer = pd.ExcelWriter(FILE_PATH_OUTPUT+'Sales-StoreHours-Hol-Promo-Weather.xlsx')
#sales_storeHours_hol_promo_weather_df.to_excel(writer,'Data')
#writer.save()