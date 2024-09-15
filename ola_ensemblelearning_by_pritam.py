# -*- coding: utf-8 -*-
"""OLA_EnsembleLearning_by_Pritam.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1M4aHbhqtnz3lcSEYHb9A0PbVNsE5UVWL
"""

# Importing the required libraries
# Pandas and Numpy libraries will be used for data manipulations, Matplotlib and Seaborn will be used for data visualizations which will be required for Analysis.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/content/ola_driver_scaler.csv')
df.head()

df.shape   # There are 19104 records of data with 14 features

df.info() # let's look at the datatype for all the features

# Convert date columns
df['Dateofjoining'] = pd.to_datetime(df['Dateofjoining'])
df['LastWorkingDate'] = pd.to_datetime(df['LastWorkingDate'])
df['MMM-YY'] = pd.to_datetime(df['MMM-YY'])

# Convert categorical columns
df['City'] = df['City'].astype('category')

df.info()

df.drop('Unnamed: 0', axis=1, inplace=True)

df.head()

df.isna().sum()   # Age, Gender and LastWorkingDate have Nan/missing values

from sklearn.impute import KNNImputer

# Selecting only the numerical columns
numerical_cols = ['Age']
imputer = KNNImputer(n_neighbors=5)

# Applying KNN imputation
df[numerical_cols] = imputer.fit_transform(df[numerical_cols])

# Mode imputation for Gender
df['Gender'].fillna(df['Gender'].mode()[0], inplace=True)

# Handling LastWorkingDate
# If LastWorkingDate is missing, it indicates the driver is still working or will have target = 0,
# We'll impute the Nan values with 0
df['LastWorkingDate'].fillna(0, inplace=True)

# Also let's perform target encoding on the "City" feature
df['City'] = df.groupby('City')['Total Business Value'].transform('mean')

df['target'] = df['LastWorkingDate'].apply(lambda x: 1 if x!=0 else 0)

df.loc[:5, 'target']

df.isna().sum() # Removed all the missing values for the features

# Let's drop the LastWorkingDate feature a we have already created the target column.
df.drop('LastWorkingDate', axis=1, inplace=True)

df.describe(include=np.number)

"""### **Univariate Analysis**"""

# Continuous variables
numerical_cols = df.select_dtypes(include=['number']).columns
for col in numerical_cols:
    plt.figure(figsize=(8, 4))
    sns.histplot(df[col], kde=True)
    plt.title(f'Distribution of {col}')
    plt.show()

# Categorical variables
categorical_cols = df.select_dtypes(include=['category']).columns
for col in categorical_cols:
    plt.figure(figsize=(8, 4))
    sns.countplot(x=col, data=df)
    plt.title(f'Countplot of {col}')
    plt.show()

"""**1. Driver_ID:**
Range: The Driver_ID ranges from 1 to 2788, with a mean around 1415. This indicates that the dataset contains 2788 unique drivers.

**2. Age:**
Mean Age: The average age of the drivers is approximately 34.67 years, with a standard deviation of about 6.25 years.
Range: The youngest driver is 21 years old, while the oldest is 58 years old.
Interquartile Range (IQR): The middle 50% of drivers are between 30 and 39 years old.
Insight: The age distribution is fairly spread, with most drivers being in their 30s. Younger and older drivers are present, but they form a smaller portion of the dataset.

**3. Income:**
Mean Income: The average monthly income is approximately ₹65,652, with a significant variation (standard deviation of ₹30,914).
Range: Income varies widely from ₹10,747 to ₹188,418.
IQR: The middle 50% of drivers earn between ₹42,383 and ₹83,969.
Insight: The income distribution is skewed, with some drivers earning significantly more than others. This could be due to differences in experience, location, or business value generated.

**4. Total Business Value:**
Mean Business Value: The average total business value generated is approximately ₹571,662, with a very high standard deviation of ₹1,128,312.
Range: The business value ranges from a negative value (loss) of ₹-6,000,000 to a maximum of approximately ₹33,747,720.
IQR: The middle 50% of drivers generated between ₹0 and ₹699,700 in business value.
Insight: The business value has a very large range, with some drivers generating extremely high or negative values. The presence of negative values could indicate refunds, cancellations, or adjustments like EMI deductions. The high variance suggests that the drivers' performance varies significantly.

**5. Quarterly Rating:**
Mean Rating: The average quarterly rating is around 2.01, with a standard deviation of 1.01.
Range: Ratings range from 1 (lowest) to 4 (highest).
IQR: The majority of drivers have a rating between 1 and 3.
Insight: The ratings are relatively low on average, with no drivers achieving the highest possible rating (which might be 5 if the scale goes higher). This suggests room for improvement in driver performance.

**6. Target:**
Mean Target: The mean value is 0.0846, indicating that about 8.46% of the drivers have left the company (target = 1).
Insight: The dataset is highly imbalanced, with a small percentage of drivers leaving the company. This will need to be addressed during model training to avoid bias toward the majority class.

### **Bivariate Analysis**
"""

# Relationship between Income and Total Business Value
sns.scatterplot(x='Income', y='Total Business Value', hue='Gender', data=df)
plt.title('Income vs. Total Business Value')
plt.show()

"""The scatter plot reveals a positive relationship between Income and Total Business Value across both genders. The plot also highlights the presence of outliers and some level of income clustering among the majority of drivers. However, there doesn’t appear to be a significant gender disparity in this relationship.







"""

numerical_features = ['Age', 'Income', 'Total Business Value', 'Quarterly Rating']

plt.figure(figsize=(15, 10))
for i, feature in enumerate(numerical_features, 1):
    plt.subplot(2, 2, i)
    sns.boxplot(x=df[feature], color='green')
    plt.title(f'Boxplot of {feature}')
plt.show()

"""**Age:**
The Age feature has a relatively symmetric distribution with a median age around 34-35 years.
There are a few outliers on the higher end, with ages above 50. However, these are minimal and may not significantly impact the model.
The interquartile range (IQR) shows that most of the data is concentrated between 30 and 40 years.

**Income:**
The Income feature is slightly skewed to the right, with a median around 60,000 to 70,000.
There are several outliers, primarily on the higher end, with incomes exceeding 125,000. These could represent higher-income drivers or anomalies.
The bulk of the data falls between 40,000 and 90,000, as indicated by the IQR.

**Total Business Value:**
The Total Business Value feature has a significant number of outliers, indicating that there is a wide variance in the business value generated by drivers.
The distribution is highly skewed to the right, with many values clustered near zero, and a few extreme outliers.
This suggests that while most drivers generate relatively low business value, a few drivers contribute exceptionally high amounts.

**Quarterly Rating:**
The Quarterly Rating feature is relatively well-distributed, with ratings ranging from 1 to 4.
There are no significant outliers, and the distribution appears relatively uniform, with a slight concentration around the median value of 2.
This suggests that driver performance, as measured by the quarterly rating, is fairly consistent across the dataset.
"""

plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, cmap='PiYG', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

"""**Low Correlation with Target:**
Most features have a very weak correlation with the target variable (Driver Attrition).

The highest correlations are with:

**Quarterly Rating:** -0.26 (moderately negative correlation).

**Total Business Value:** -0.14 (weak negative correlation).

**Income:** -0.10 (weak negative correlation).
Other variables like Age, Grade, and City show almost no correlation with the target.


**Strong Feature-Feature Correlations:**

**Income and Grade:** Very strong positive correlation of 0.78. This indicates that as a driver’s grade increases, their income also tends to increase.

**Income and Total Business Value:** Strong correlation of 0.78. Higher income is associated with higher business value.

**Joining Designation and Grade:** Strong correlation of 0.56. The designation at joining is tied to the grade.

**Date of Joining and Age:** Moderate negative correlation of -0.29 suggests that older drivers tend to have joined the company earlier.

**Date of Joining and MMM-YY (likely representing the month of joining)** show a moderately strong correlation of 0.34.


"""

# Though Gradient Boosting and Random Forest are not greatly affected by strongly correlated features, we can still remove some features to avoid redundancy and
# to make the model as effecient and simpler as possible
df.drop(['Grade', 'Total Business Value'], axis=1, inplace=True)

# Let's handle the outliers in the numerical features
from scipy import stats

numerical_features = ['Age', 'Income', 'Quarterly Rating']  # Currently avaliable numerical features
z_scores = np.abs(stats.zscore(df[numerical_features]))
outliers = np.where(z_scores > 3)
df = df[~(z_scores > 3).any(axis=1)]

df.shape       # Records present in the data after removing the outliers

# Quarterly rating increase
df['Quarterly_Rating_Increase'] = df.groupby('Driver_ID')['Quarterly Rating'].diff().fillna(0).apply(lambda x: 1 if x > 0 else 0)

# Monthly income increase
df['Monthly_Income_Increase'] = df.groupby('Driver_ID')['Income'].diff().fillna(0).apply(lambda x: 1 if x > 0 else 0)

df.head()

df.info()

# SMOTE cannot be applied to features of timestamp datatype, since ML expect numerical data we'll convert these
# features to numerical representation (eg. Unix timestamp)

df['Dateofjoining'] = df['Dateofjoining'].astype(int) / 10**9
df['MMM-YY'] = df['MMM-YY'].astype(int) / 10**9

df.head()

"""### **Model Building**"""

# Before building and training the model let's split the data into train and test
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(df.drop('target', axis=1), df['target'], test_size=0.3, random_state=42)  # 70% training and 30% testing

X_train.shape, y_train.shape

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

X_train.shape, y_train.shape

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

X_train.head()

"""#### **Train a Model using Bagging (Random Forest)**"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV       # GridSearch will basically run all combinations of the given hyperparameters and choose the best one
                                                       # and is computationally expensive

# Let's try for various parameters
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf = RandomForestClassifier(random_state=42)

# Use GridSearchCV to find the best parameters
# In the below line n_jobs parameter when set to -1 allows for parallel processing and verbose parameter is responsible for showing training related info
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

print("Best Parameters for Random Forest:", grid_search.best_params_)
print("Best CV Score for Random Forest:", grid_search.best_score_)

# Predict using the best model
best_rf = grid_search.best_estimator_
y_pred_rf = best_rf.predict(X_test)

"""#### **Train a Model using Boosting (Gradient Boosting)**"""

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV  # RandomSearch will basically choose random combinations of hyperparameters based on the
                                                        # n_iter (specifies the number of combinations) parameter and is computationally less expensive

# Let's try for various parameters
param_grid = {
    'n_estimators': [25, 50, 100],
    'learning_rate': [0.01, 0.1],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

gb = GradientBoostingClassifier(random_state=42)

# Use GridSearchCV to find the best parameters
random_search = RandomizedSearchCV(estimator=gb, param_distributions=param_grid, n_iter=10, cv=5, n_jobs=-1, verbose=2)
random_search.fit(X_train, y_train)

print("Best Parameters for Gradient Boosting:", random_search.best_params_)
print("Best CV Score for Gradient Boosting:", random_search.best_score_)

# Predict using the best model
best_gb = random_search.best_estimator_
y_pred_gb = best_gb.predict(X_test)

"""### **Model Evaluation**"""

from sklearn.metrics import classification_report, roc_auc_score, roc_curve

# Random Forest Classification Report
print("Random Forest Classification Report:")
print(classification_report(y_test, y_pred_rf))

# Gradient Boosting Classification Report
print("Gradient Boosting Classification Report:")
print(classification_report(y_test, y_pred_gb))

"""Imbalance Issue: Class 1 (minority class) has significantly fewer samples (476) compared to Class 0 (5223), leading to poor performance for Class 1 in both models.

**Random Forest:**

Class 0 (majority): High precision (0.92), recall (0.95), and F1-score (0.93), showing good performance for predicting the majority class.
Class 1 (minority): Poor precision (0.15), recall (0.10), and F1-score (0.12), indicating struggles with detecting the minority class.
Macro Avg: Low score (0.53) due to poor performance on the minority class.
Weighted Avg: Decent score (0.87), influenced by the majority class's performance.

**Gradient Boosting:**

Class 0: Similar high performance to Random Forest, with slightly better F1-score (0.94).
Class 1: Better precision (0.21) but still low recall (0.15) and F1-score (0.17), meaning it struggles less but still performs poorly on minority class.
Macro Avg: Slight improvement (0.56) compared to Random Forest, but still low overall.
Weighted Avg: Similar to Random Forest (0.87), mainly driven by Class 0.
Conclusion:
Both models handle the majority class well but struggle with the minority class due to class imbalance. Gradient Boosting performs slightly better on the minority class, but both models could benefit from addressing the imbalance
"""

# ROC AUC Score for Random Forest
roc_auc_rf = roc_auc_score(y_test, best_rf.predict_proba(X_test)[:, 1])
print(f"Random Forest ROC AUC Score: {roc_auc_rf}")

# ROC AUC Score for Gradient Boosting
roc_auc_gb = roc_auc_score(y_test, best_gb.predict_proba(X_test)[:, 1])
print(f"Gradient Boosting ROC AUC Score: {roc_auc_gb}")

# Plotting the ROC Curve
fpr_rf, tpr_rf, _ = roc_curve(y_test, best_rf.predict_proba(X_test)[:, 1])
fpr_gb, tpr_gb, _ = roc_curve(y_test, best_gb.predict_proba(X_test)[:, 1])

plt.figure(figsize=(8, 6))
plt.plot(fpr_rf, tpr_rf, label=f'Random Forest (AUC = {roc_auc_rf:.2f})')
plt.plot(fpr_gb, tpr_gb, label=f'Gradient Boosting (AUC = {roc_auc_gb:.2f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random Chance')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()

"""
**Insight:**

The Gradient Boosting model (AUC = 0.82) outperforms the Random Forest model (AUC = 0.79) based on the ROC curve, indicating better performance in distinguishing between the two classes.
Both models perform significantly better than random chance (dashed line), but neither achieves perfect classification.

**Recommendation:**
Gradient Boosting is preferable due to its higher AUC score, but both models could benefit from further tuning or class imbalance treatment (e.g. class weighting) to improve recall, especially for the minority class."""
