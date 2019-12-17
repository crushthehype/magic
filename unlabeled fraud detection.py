#!/usr/bin/env python
# coding: utf-8
# data -> 'https://www.kaggle.com/ntnu-testimon/banksim1#bs140513_032310.csv'

"""K-means Clustering"""
# In Machine Learning, the types of Learning can broadly be classified into three types: 
# 1. Supervised Learning, 
# 2. Unsupervised Learning and 
# 3. Semi-supervised Learning. 
# Algorithms belonging to the family of Unsupervised Learning have no variable to predict tied to the data. 
# Instead of having an output, the data only has an input which would be multiple variables that describe the data. 
# This is where clustering comes in.


# Clustering is the task of grouping together a set of objects in a way that objects...
# ...in the same cluster are more similar to each other than to objects in other clusters. 
# Similarity is a metric that reflects the strength of relationship between two data objects


# K-Means falls under the category of centroid-based clustering. 
# A centroid is a data point (imaginary or real) at the center of a cluster. 
# In centroid-based clustering, clusters are represented by a central vector or a centroid. 
# This centroid might not necessarily be a member of the dataset. 
# Centroid-based clustering is an iterative algorithm in which the notion of similarity is derived...
# ...by how close a data point is to the centroid of the cluster.

# Import packages
import pandas as pd 
import numpy as np
import seaborn as sn 
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, silhouette_score, homogeneity_score, roc_auc_score, roc_curve
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import MiniBatchKMeans, DBSCAN
from sklearn.preprocessing import LabelEncoder

# Read the dataset and clean it
df = pd.read_csv('FraudData.csv')
df.head()
df.tail()
df.info()
df = df[['gender', 'category', 'amount', 'fraud']]
df['gender'] = df['gender'].replace("'", "", regex = True)
df['category'] = df['category'].replace("'", "", regex = True)
df.head(3)
df.tail(3)

# Calculate the ratio of fraud and non-fraud transactions
occ = df['fraud'].value_counts() # occurance count
ratio_cases = (occ/len(df.index))
print(f'Ratio of fraudulent cases: {ratio_cases[1]}\nRatio of non-fraudulent cases: {ratio_cases[0]}')

# Group the data by category to see either there is something unusual
print(df.groupby('category').mean())
print(df.gender.value_counts())

# Drop the unwanted genders (E & U), we want explore M & F, which is male and female
df = df.drop(df[(df.gender == "E") | (df.gender == "U")].index)
df.gender.unique()

# Create a dataframe with fraud and non-fraud data
df_fraud = df.loc[df.fraud ==1]
df_non_fraud = df.loc[df.fraud ==0]

# Inspect the created db's
df_fraud.head()
df_fraud.info()
df_non_fraud.head()
df_non_fraud.info()

# Plot a histogram of the amounts in fraud and non-fraud data
plt.hist(df_fraud.amount, alpha = 0.5, label = 'fraud')
plt.hist(df_non_fraud.amount, alpha = 0.5, label = 'non-fraud')
plt.xlabel('amount')
plt.legend()
plt.show()

# Encode and transform the data on the gender param
le = LabelEncoder()
gender = le.fit_transform(df.gender)


df['M'] = pd.get_dummies(df.gender)['M']
df = pd.concat([df, pd.get_dummies(df.category, drop_first=True)],axis=1)
y = df.fraud.copy()
df.drop(['gender', 'fraud', 'category'], axis=1, inplace=True)
df.head()
df.tail()
df.isnull().sum()
df.shape
y.shape
cols = df.columns

# For ML algorithms using distance based metrics, it is crucial to always scale your data, as features using different scales will distort your results. 
# K-means uses the Euclidean distance to assess distance to cluster centroids, therefore you first need to scale your data before continuing to implement the algorithm.
# In mathematics, the Euclidean distance or Euclidean metric is the "ordinary" straight-line distance between two points in Euclidean space.

# Get the float values of df
X = np.array(df).astype(np.float)

# Define the scaler and apply to the data
# Scale generally means to change the range of the values, the shape and distribution doesn't change.
# ML algorithms perform better or converge faster when features are relatively similar scale ...
#...and/or close to normally distributed.
# For each value in feature MinMaxScaler substracts the minimum value in the feature and divides it...
# ... by the range. The range is the difference between the original maximum and original minimum.
# (!) MinMaxScaler does not reduce the importance of outliers, this is critical for us working without labels.

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_scaled.shape


"""Kmeans Method"""
# Define the model
kmeans = MiniBatchKMeans(n_clusters=8, random_state=0)
# Fit the model to scale the data
kmeans.fit(X_scaled)

# The model has now been fit to the data. 
# Is it any good for flagging fraud? 
# We need to figure out the right number of clusters to use.
# let's apply the Elbow method and see what the optimal number of clusters should be based on this method.


"""Elbow Method"""
# An Elbow method is designed to help us find the appropriate number of clusters to use in a dataset.
# More precisely, it plots the percentage of variance explained by the clusters against the number of clusters.

# Define the range of clusters to try
clustno = range(1,12)

# Run the MiniBatch Kmeans over the number of clusters
kmeans = [MiniBatchKMeans(n_clusters=i) for i in clustno]

# Obtain sthe score for model
score = [kmeans[i].fit(X_scaled).score(X_scaled) for i in range(len(kmeans))]

# Plot the models and their respective score
plt.plot(clustno, score)
plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.show()


"""Detecting Outliers"""
# Split the data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size = 0.3, random_state =0)

# Define K-means model
kmeans = MiniBatchKMeans(n_clusters =3, random_state = 42).fit(X_train)

# Obtain predictions and calculate distance from cluster centroid
# np.linalg.norm: returns the vector norm, the vector of distance for each datapoint to their assigned cluster
X_test_clusters = kmeans.predict(X_test)
X_test_clusters_centers = kmeans.cluster_centers_
dist = [np.linalg.norm(x-y) for x,y in zip(X_test, X_test_clusters_centers[X_test_clusters])]

# Create fraud predictions based on outlier clusters
# Choose the prcentile carefully. Lowering it will make the model identify more false-positives

km_y_pred = np.array(dist)
km_y_pred[dist >= np.percentile(dist, 95)] = 1
km_y_pred[dist < np.percentile(dist, 95)] = 0
np.unique(km_y_pred)
np.unique(X_test_clusters)


"""Checking model results"""
# AUROC - Area Under the Receiver Operating Characteristics
# AUC-ROC - is a performance measurment for classification problem at various thrasholds settings.
# It tells us how much model is capable of distinguishing between classes
# The higher the AUC (Area Under the Curve), the better the model is at predicting 0s as 0s and 1s as 1s.
# Obtain the ROC_auc_score
print(roc_auc_score(y_test, km_y_pred))

# Create confusion matrix
# A confusion matrix is a summary of prediction results on classification problem.
# The Confusion Matrix shows the ways in which a classification model is confused when it makes predictions.
# The matrix also gives us insight what types of errors that are being made.
km_cm = confusion_matrix(y_test, km_y_pred)
print('Confusion Matrix:\n', km_cm)
print('Classifcation Report:\n', classification_report(y_test, km_y_pred))
# Plot confusion Matrix
fig, ax = plot_confusion_matrix(conf_mat=km_cm,
                                show_absolute=True,
                                show_normed=True,
                                colorbar=True)
plt.show()

# TN   FP
# FN   TP

# Actual NO, Predicted NO = TN (true negatives); not a fraudulent case, we correctly predicted it's not a fraudulent case
# Actual NO, Predicted YES = FP (false positives); not a fraudulent case, we incorrectly predicted that it's a fraudulent case
# Actual YES, Predicted NO = FN (false negatives); fraudulent case, we predicted incorrectly as a non-fraudulent case
# Actual YES, Predicted YES = TP (true positives); fraudulent case, we predicted it correctly as a fraudulent case


# Accuracy = TP+TN/TP+TN+FP+FN
# Recall = TP/TP+FN, Recall can be defined as the ratio of the total number of correctly classified positive examples divide to the total number of positive examples
# Precision = TP/TP+FP, tells us about then it predicts yes, how often it is

# High recall, low precision means that most of the positive examples are correctlty recognized (low FN), but there's a lot of false positives (FP)
# Low recall, high precision means we miss a lot of positive examples (high FN), those we predict are indeed positive (low FP)
