import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler 
from sklearn.pipeline import make_pipeline
import seaborn as sns


FILE_PATH_INPUT = 'C:/Users/aripiralas/GitHub/Predictive-Modeling/Predictive-Model---Claires/UK-Sales_Predictive_Model/2. Clustering/Input_Data/'

FILE_PATH_OUTPUT = 'C:/Users/aripiralas/GitHub/Predictive-Modeling/Predictive-Model---Claires/UK-Sales_Predictive_Model/2. Clustering/Output_Data/'

sales_df = pd.read_excel(FILE_PATH_INPUT+'Sales-StoreHours-Hol-Promo-Weather.xlsx', sheetname='Data')

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

#### run the Kmeans algorithm for K in (1,20) ######
### Step 1: standardize all the columns using standardscaler inbuilt Sklearn method ###
### step 2: Run Kmeans clustering algorithm on the standardized dataframe ###

pipe_StdSca_KMeans = [make_pipeline(StandardScaler(),KMeans(random_state=123, n_clusters=clusters, init= 'k-means++', n_init=50, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, copy_x=True, n_jobs=1, algorithm='auto')) for clusters in range(1,21)]

score = [est.fit(sales_agg_df).score(sales_agg_df) for est in pipe_StdSca_KMeans]
cluster_list = [est.fit_predict(sales_agg_df) for est in pipe_StdSca_KMeans]

######### end #######################################################################


## elbow curve ###

xrange = list(range(1,21))
plt.figure(1,figsize=(12,8))
sns.set_style("darkgrid")
ax = sns.pointplot(x=xrange,y=score)
ax.set(xlabel='# of Clusters',ylabel='Score', title="Elbow Curve")
plt.savefig(FILE_PATH_OUTPUT+'Elbow_curve.png')       
plt.show()

## end elbow curve ###

#### plot sales vs qty by cluster to invesitage how many clusters work for our stores ####
 
sales_agg_df['Cluster'] = cluster_list[3]
sales_agg_df.Cluster = sales_agg_df.Cluster.astype('category')
sales_agg_df.Cluster.value_counts()

plt.figure(1,figsize=(12,8))
sns.set_style("darkgrid")

fg = sns.FacetGrid(data=sales_agg_df[['Sales','Quantity','Cluster']], hue='Cluster', hue_order=sales_agg_df.Cluster.unique().sort(), aspect=1.61)
fg.map(plt.scatter, 'Sales', 'Quantity').add_legend()
plt.savefig(FILE_PATH_OUTPUT+'Sales vs Qty-Kmeans.png')

#######################################################################################

## conclusion: Analyzing the elbow curve and plots between Sales vs Quantity, 4 clusters are sufficient for the stores in UK

######### save the clustering analysis #################
cluster_df = pd.DataFrame(cluster_list)
cluster_df = cluster_df.transpose()
cluster_df.columns = list(range(1,21))    

cluster_df.to_csv(FILE_PATH_OUTPUT+'Clustering-kmeans.csv')
sales_agg_df.to_csv(FILE_PATH_OUTPUT+'Sales_agg_cluster-k4.csv')

########################################################################################
