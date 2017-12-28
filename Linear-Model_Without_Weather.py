import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler 
from sklearn.pipeline import make_pipeline
import numpy as np
import seaborn as sns
from sklearn.model_selection import GridSearchCV


FILE_PATH = 'W:/B&M/Store Segmentation/Predictive Model/EU - Model/UK/'

# Import required datasets from excel
promo_df = pd.read_excel(FILE_PATH+'Promo_Data.xlsm', sheetname='Promo_Data')
hol_df = pd.read_excel(FILE_PATH+'Holiday_Data.xlsm', sheetname='Holiday_Data')
sales_df = pd.read_excel(FILE_PATH+'Sales_Data.xlsm', sheetname='Sales_Data')
store_hours_df = pd.read_excel(FILE_PATH+'Store_Hours_Data.xlsm', sheetname='Store_Hours')
weather_df = pd.read_csv(FILE_PATH+'weather_vF2.csv', parse_dates = True )

### Assign the right data types to the features. for example, store number should be categorical

sales_df['Store_Number'] = sales_df.Store_Number.astype('category')



###############################################################################################

#### extract week, day of the week from transaction date

def extract_dayofweek(date):
    return date.dayofweek

def extract_weeknum(date):
    return date.week

######### Data processing & clustering analysis ######################################

cluster_columns = ['Store_Number', 'Transaction_Count', 'Sales',
       'Quantity', 'Gross_Margin']

sales_agg_df = sales_df[cluster_columns].groupby(by='Store_Number').sum().reset_index()

sales_agg_df['ADS'] = sales_agg_df.Sales/sales_agg_df.Transaction_Count
sales_agg_df['UPT'] = sales_agg_df.Quantity/sales_agg_df.Transaction_Count
sales_agg_df['AUR'] = sales_agg_df.Sales/sales_agg_df.Quantity

pipe1_StdSca_KMeans = [make_pipeline(StandardScaler(),KMeans(random_state=123, n_clusters=clusters, init= 'k-means++', n_init=50, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, copy_x=True, n_jobs=1, algorithm='auto')) for clusters in range(1,20)]

score = [est.fit(sales_agg_df).score(sales_agg_df) for est in pipe1_StdSca_KMeans]
cluster_list = [est.fit_predict(sales_agg_df) for est in pipe1_StdSca_KMeans]



# plt.plot(range(1,20),score)
 
sales_agg_df['Cluster'] = cluster_list[2]
sales_agg_df.Cluster = sales_agg_df.Cluster.astype('category')

fig = sales_agg_df.plot.scatter(x='Sales', y='Quantity', color= sales_agg_df.Cluster,figsize=(12,8), s=50)
fig.show()


sns.set(style="darkgrid", color_codes=True)



g = sns.jointplot("Sales", "Quantity", data=sales_agg_df, kind="scatter",
                   hue="Cluster", size=7)

pd.DataFrame(cluster, columns = ['cluster']).cluster.value_counts()

#######################################################################################

# Join data 
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

sales_storeHours_hol_promo_cluster_df = pd.merge(sales_storeHours_hol_promo_df, sales_agg_df[['Store_Number','Cluster']],
                 how='left', on=['Store_Number'])
sales_storeHours_hol_promo_cluster_df.shape

features = ['Transaction_Date', 'Transaction_Count',
        'Open Hours', 'Labour Hours',
       'Holiday_Event', 'Holiday_Period', 'Promo', 'Sales_Promo', 'Cluster']

response = 'Sales'


data_df = sales_storeHours_hol_promo_cluster_df[features]
data_df['Day_of_Week']  = data_df.Transaction_Date.apply(extract_dayofweek)
data_df['Week_Num'] = data_df.Transaction_Date.apply(extract_weeknum)

#### filter out any records with open hours less than 0 ###

data_df = data_df.loc[data_df['Open Hours']>0,:]

#####################

data_df.Day_of_Week = data_df.Day_of_Week.astype('category')
data_df.Week_Num = data_df.Week_Num.astype('category')

data_df.drop(['Transaction_Date'],axis=1,inplace=True)

data_df.drop(['Transaction_Count'],axis=1,inplace=True)


response_df = sales_storeHours_hol_promo_cluster_df.loc[sales_storeHours_hol_promo_cluster_df['Open Hours']>0,response] 


data_dummy_df = pd.get_dummies(data_df)


#### Model 1 #########

from sklearn.model_selection import train_test_split

train_X, test_X, train_y, test_y = train_test_split(data_dummy_df, response_df, 
                                                    train_size=0.75, 
                                                    random_state=123,
                                                    )

#### linear model without weather data ########
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

np.random.seed(123)
LM = LinearRegression()
LM.fit(train_X,train_y).score(test_X,test_y)

test_pred = LM.predict(test_X)

print('Coefficients: \n', LM.coef_)
# The mean squared error
print(" Root Mean squared error: %.2f"
      % np.sqrt(mean_squared_error(test_y, test_pred)))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(test_y, test_pred))


#### model with weather data incorporated #########


