import pandas as pd
import numpy as np



FILE_PATH_INPUT = 'C:/Users/aripiralas/GitHub/Predictive-Modeling/Predictive-Model---Claires/UK-Sales_Predictive_Model/2016/7. LM with Weather + Ridge/Input_Data/'

FILE_PATH_OUTPUT = 'C:/Users/aripiralas/GitHub/Predictive-Modeling/Predictive-Model---Claires/UK-Sales_Predictive_Model/2016/7. LM with Weather + Ridge/Output_Data/'

# Import required datasets from excel
sales_storeHours_hol_promo_weather_df = pd.read_excel(FILE_PATH_INPUT+'Sales-StoreHours-Hol-Promo-Weather.xlsx', sheetname='Data')
sales_agg_df = pd.read_csv(FILE_PATH_INPUT+'Sales_agg_cluster-k4.csv')

### Assign the right data types to the features. for example, store number should be categorical

sales_storeHours_hol_promo_weather_df['Store_Number'] = sales_storeHours_hol_promo_weather_df.Store_Number.astype('category')

###############################################################################################

#### extract week, day of the week from transaction date

def extract_dayofweek(date):
    return date.dayofweek

def extract_weeknum(date):
    return date.week

######### Data processing & clustering analysis ######################################


sales_storeHours_hol_promo_weather_cluster_df = pd.merge(sales_storeHours_hol_promo_weather_df, sales_agg_df[['Store_Number','Cluster']],
                 how='left', on=['Store_Number'])
sales_storeHours_hol_promo_weather_cluster_df.shape

#### filter out any records with open hours less than 0 ###
sales_storeHours_hol_promo_weather_cluster_df = sales_storeHours_hol_promo_weather_cluster_df.loc[sales_storeHours_hol_promo_weather_cluster_df['Open Hours']>0,:]

### drop rows with NA
sales_storeHours_hol_promo_weather_cluster_df.dropna(inplace=True)
############################################################

### remove data for closed stores ####################################################

closed_stores_list = [156, 146, 345, 380, 113, 325, 499, 184, 237, 385, 93, 76, 521, 78, 137, 173, 475, 420, 462, 548, 513] 

sales_storeHours_hol_promo_weather_cluster_df = sales_storeHours_hol_promo_weather_cluster_df.loc[np.logical_not(sales_storeHours_hol_promo_weather_cluster_df.Store_Number.isin(closed_stores_list)),:]


######################################################################################


features = ['Transaction_Date', 'Transaction_Count','Open Hours', 'Labour Hours', 'Holiday_Event', 'Holiday_Period', 'Promo', 'Sales_Promo', 'Cluster','rain','snow', 'meantempi', 'meandewpti', 'meanwindspdi', 'humidity', 'precipi']

response = 'Sales'

response_df = sales_storeHours_hol_promo_weather_cluster_df[response]
data_df = sales_storeHours_hol_promo_weather_cluster_df[features]
data_df['Day_of_Week']  = data_df.Transaction_Date.apply(extract_dayofweek)
data_df['Week_Num'] = data_df.Transaction_Date.apply(extract_weeknum)


######################## convert various elements into category type #######

data_df.Day_of_Week = data_df.Day_of_Week.astype('category')
data_df.Week_Num = data_df.Week_Num.astype('category')
data_df.Cluster =  data_df.Cluster.astype('category')

############################################################################

data_df.drop(['Transaction_Date'],axis=1,inplace=True)

data_df.drop(['Transaction_Count'],axis=1,inplace=True)



data_dummy_df = pd.get_dummies(data_df)

############################################################################

###Drop unimportant (beta = 0) columns identified through Lasso ##########

lasso_output_df = pd.read_csv(FILE_PATH_INPUT + 'Lasso_Weather_Output.csv', skiprows = 2, header = None, engine = 'python')

lasso_output_df.columns = ['Alpha_0.1','Alpha_1','Alpha_10','Features']


zero_features = lasso_output_df.Features[lasso_output_df['Alpha_0.1']==0]
zero_features_bool = [x not in ['Day_of_Week_2', 'Week_Num_20', 'Week_Num_27', 'Week_Num_29'] for x in list(zero_features)]  #### dont drop seasonality related columns


### drop the insigficant columns identified through lasso model ###
data_dummy_lasso_drop_df = data_dummy_df.drop(list(zero_features[zero_features_bool]), axis=1)

############################################################################

#### Model 1 #########

from sklearn.model_selection import train_test_split

train_X, test_X, train_y, test_y = train_test_split(data_dummy_lasso_drop_df, response_df, 
                                                    train_size=0.75, 
                                                    random_state=123,
                                                    )


########## End ########################################


###### model after standardizing the data ##########
#
#from sklearn.pipeline import make_pipeline
#from sklearn.preprocessing import StandardScaler
#from sklearn.model_selection import GridSearchCV
#from sklearn.linear_model import Lasso
#
#
#Est_StdSca_LM = make_pipeline(StandardScaler(),Lasso(random_state=123, max_iter=5000))
#
#Est_StdSca_LM_params = {'lasso__alpha':[.1,1,10]                    
#        }
#
#Est_grid = GridSearchCV(Est_StdSca_LM, param_grid=Est_StdSca_LM_params, cv=5,verbose=3)
#
#Est_grid.fit(train_X,train_y).score(test_X,test_y)


###################End ####################################


from sklearn.linear_model import Ridge
np.random.seed(123)

#### create a list of Lasso Estimators with various L1 penalties--i.e. alpha values
Est_StdSca_Ridge_list = [Ridge(normalize=False,max_iter=5000, alpha=a, random_state=123) for a in [0.1,1,10]]

#### store the output in the lists for each estimator 
ridge_coeff = []
ridge_score = []
ridge_params = []
ridge_intercept = []
for est in Est_StdSca_Ridge_list:
    print(est.get_params())
    score = est.fit(train_X,train_y).score(test_X,test_y)
    print("Score: ",score)
    print('Coeff:\n',est.coef_)
    ### append to the list
    ridge_coeff.append(est.coef_)
    ridge_score.append(score) ### Generalization error; Not training error
    ridge_params.append(est.get_params())
    ridge_intercept.append(est.intercept_)

##### print the score for alpha = 0.1 ####
from sklearn.metrics import mean_squared_error, r2_score
    
test_pred = Est_StdSca_Ridge_list[0].predict(test_X)
print(" Root Mean squared error: %.2f"
      % np.sqrt(mean_squared_error(test_y, test_pred)))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(test_y, test_pred))

### Conclusion ######
### Lasso with alpha = 0.1 seems to be working fine ###
### Root Mean squared error: 563.28   
### Variance score: 0.743                          ####   



###### Output the coefficients into a file #####

ridge_coeff_df = pd.DataFrame(ridge_coeff).transpose()
ridge_coeff_df['Features'] =  test_X.columns

ridge_intercept_df = pd.DataFrame(ridge_intercept).transpose()
ridge_intercept_df['Features'] = 'Intercept'

ridge_score_df = pd.DataFrame(ridge_score).transpose()
ridge_score_df['Features'] = 'Score'


ridge_output_df = pd.merge(ridge_score_df, ridge_intercept_df,how="outer")
ridge_output_df = pd.merge(ridge_output_df,ridge_coeff_df,how="outer")
   

ridge_output_df.columns = ['Alpha_0.1', 'Alpha_1', 'Alpha_10', 'Features']

ridge_output_df.to_csv(FILE_PATH_OUTPUT+'Ridge_Weather_Output.csv',index=False)
