
# coding: utf-8

# In[2]:

# Common Imports

#Pandas for creating dataframes
import pandas as pd
#Sklearn
from sklearn import preprocessing
#K-means clustering algo
from sklearn.cluster import KMeans
#OS moduled for file oprations
import os
#CSV module
import csv


# In[3]:

#Folder Base Path
base_path = 'converted/test2/'


# In[8]:

#Cluster Path
#Normal
sample_path = base_path+'samples/'
cluster_path = base_path+'ip_cluster/'
#Attack
#sample_path = base_path+'attack_samples/2/'
#cluster_path = base_path+'attack_ip_cluster/2/'


# In[9]:

first = True
ip_dict = dict()
sample_count = 1;
for filename in os.listdir(sample_path):
    tdf = pd.read_csv(sample_path+filename, index_col=0)
    #Filter Columns
    t = tdf[['ip.dst', 'ip.proto', 'sniff_timestamp', 'sample']]
    #Remove null destinations
    t = t[t['ip.dst'].notnull()]
    #Rename Columns
    t.columns = ['ip', 'proto', 'time_stamp', 'sample']
    #Get count for each ip
    df = t.groupby(['ip', 'proto']).size().unstack().fillna(0).astype(int)
    #Select TCP and UDP as only fetures (TCP:6, UDP:17)
    #df = df[[6,17]]
    #Get value matrix
    X = df.values
    #Create scaling
    scaler = preprocessing.StandardScaler().fit(X)
    #Transform Traning data
    X_trans = scaler.transform(X)
    #Define Number of Clusters
    cluster_count = 6
    #Data Fitting using K-means
    if first:
        kmeans = KMeans(n_clusters=cluster_count)
        kmeans.fit(X_trans)
        centroids_array=kmeans.cluster_centers_
    else:
        kmeans = KMeans(n_clusters=cluster_count, init=centroids_array)
        kmeans.fit(X_trans)
    #Attaching label/cluster to IP
    ip_series = pd.Series(df.index, name='ip')
    label_series = pd.Series(kmeans.labels_, name='label')
    ip_label_df = pd.concat([ip_series, label_series], axis=1).set_index('ip')
    if not os.path.exists(cluster_path):
        os.makedirs(cluster_path)
    ip_label_df.to_csv(cluster_path+str(sample_count))
    sample_count += 1


# In[10]:

#Cluster Assignment
from itertools import groupby
ip_dict = dict()

for filename in os.listdir(cluster_path):
    with open(cluster_path+filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ip'] in ip_dict:
                #print(row['ip'],ip_dict[row['ip']])
                ip_dict[row['ip']] = ip_dict[row['ip']] + [row['label']]
            else:
                ip_dict[row['ip']] = [row['label']]


# In[15]:

#Find how many time destination has been assigned a given cluster
ip_cluster_dict = dict()
for key, value in ip_dict.items():
    ip_cluster_dict[key] = {k: len(list(group)) for k, group in groupby(value)}


# In[ ]:



