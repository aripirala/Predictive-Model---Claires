# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 10:41:07 2018

@author: patelj
"""

import pandas as pd
import numpy as np
from sklearn.datasets import make_blobs
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler 
from sklearn.pipeline import make_pipeline
import seaborn as sns


FILE_PATH_INPUT = 'C:/Users/patelj/Documents/Project/Predictive-Model---Claires/Jayraj-Patel-Model/NA - Predictive Model/2018/2. Clustering/Input Data/'

FILE_PATH_OUTPUT = 'C:/Users/patelj/Documents/Project/Predictive-Model---Claires/Jayraj-Patel-Model/NA - Predictive Model/2018/2. Clustering/Output Data/'

sales_df = pd.read_excel(FILE_PATH_INPUT+'Sales-StoreHours-Hol-Promo.xlsx', sheetname='Data')

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


km = KMeans(n_clusters=4, init='k-means++', n_init=10)
km.fit(sales_agg_df)
x = km.fit_predict(sales_agg_df)

sales_agg_df["Cluster"]= x
sales_agg_df.sort_values(["Cluster"])


plt.figure(1,figsize=(16,16))
sns.set_style("darkgrid")
sns.lmplot('Sales', # Horizontal axis
           'Quantity', # Vertical axis
           data=sales_agg_df, # Data source
           fit_reg=False, # Don't fix a regression line
           hue="Cluster", # Set color
           scatter_kws={"marker": "D", # Set marker style
                        "s": 50})
sns.set_context("poster")
plt.savefig(FILE_PATH_OUTPUT+'Sales vs Qty-Kmeans.png')

#Conclusion: Store 6349 is an outlier
sales_agg_df.to_csv(FILE_PATH_OUTPUT+'Sales_agg_cluster-k4.csv')
