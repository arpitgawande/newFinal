
# coding: utf-8

# In[2]:

# Common Imports
#Pandas for creating dataframes
import pandas as pd
#Sklearn
from sklearn import preprocessing
#OS moduled for file oprations
import os
#CSV module
import csv
#SKlearn SVM
from sklearn import svm


# In[3]:

#Folder Base Path
base_path = 'converted/test2/'


# In[38]:

first = True

ip_dict = dict()
sample_path = base_path+'samples/'
#Cluster Path
#cluster_path = base_path+'attack_ip_cluster/2/'
sample_count = 1;
first = True;
dfList = []
for filename in os.listdir(sample_path):
    tdf = pd.read_csv(sample_path+filename, index_col=0)
    #Filter Columns
    tdf = tdf[['ip.dst', 'ip.proto', 'sniff_timestamp', 'sample']]
    #Remove null destinations
    tdf = tdf[tdf['ip.dst'].notnull()]
    #Rename Columns
    tdf.columns = ['ip', 'proto', 'time_stamp', 'sample']
    #Get count for each ip
    df = tdf.groupby(['ip', 'proto']).size().unstack().fillna(0).astype(int)
    df['sample'] = filename
    dfList.append(df)    


# In[45]:

#Group all the flow for an IP address for SVM training algorithm.
df1 = pd.concat(dfList).sort_index()
df1 = df1.reset_index().set_index(['ip','sample'])
indexValues = df1.index.get_level_values(0)


# In[80]:

#Use SVM to train on every destination IP
svm_dict = dict()
for i in indexValues:
    X_train = df1.loc[i].values
    # fit the model
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    clf.
    clf.fit(X_train)
    svm_dict[i] = clf


# In[90]:

#Predict for the give destination if it is normal or not
svm_dict['192.168.0.7'].predict([[0,0,1,1]])

