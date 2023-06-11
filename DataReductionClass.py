import DataPrerocessingClass
import sklearn
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split

class DataReduction:

    def __init__(self, preprocesingInstance):
        self.df = preprocesingInstance.datasetBeforePreprocessing

    # def Feature_Selection_via_univariate_statistical_tests(self,col,no_cols_you_want):
    #     collen = len(self.df.axes[1])
    #     while (collen < no_cols_you_want):
    #         print('please enter col number less then total cols')
    #         no_cols_you_want = int(input())

    #     X = self.df.drop([col], axis=1)
    #     y = self.df[col]
    #     # apply SelectKBest class to extract top 10 best features
    #     bestfeatures = SelectKBest(score_func=chi2, k=no_cols_you_want)
    #     fit = bestfeatures.fit(X, y)
    #     dfscores = pd.DataFrame(fit.scores_)
    #     dfcolumns = pd.DataFrame(X.columns)
    #     # concat two dataframes for better visualization
    #     featureScores = pd.concat([dfcolumns, dfscores], axis=1)
    #     featureScores.columns = ['Specs', 'Score']  # naming the dataframe columns
    #     cl = featureScores['Specs']
    #     dfcolumns1 = featureScores.nlargest(no_cols_you_want, 'Score')
    #     df3 = pd.DataFrame()
    #     for i in dfcolumns1['Specs']:
    #         df3[i] = self.df[i]
    #     # print(featureScores.nlargest(no_cols_you_want, 'Score'))  # print 10 best features
    #     print(df3)

    # def Feature_Selection_via_Feature_importance(self, col, no_cols_you_want):
    #     collen = len(self.df.axes[1])
    #     while (collen < no_cols_you_want):
    #         print('please enter col number less then total cols')
    #         no_cols_you_want = int(input())
    #     X = self.df.drop([col], axis=1)
    #     y = self.df[col]
    #     model = ExtraTreesClassifier()
    #     model.fit(X, y)
    #     print(model.feature_importances_)  # use inbuilt class feature_importances of tree based classifiers
    #     # plot graph of feature importances for better visualization
    #     feat_importances = pd.Series(model.feature_importances_, index=X.columns)
    #     feat_importances.nlargest(no_cols_you_want).plot(kind='barh')
    #     colname = feat_importances.nlargest(no_cols_you_want).index.tolist()
    #     df4 = pd.DataFrame()
    #     for i in colname:
    #         df4[i] = self.df[i]
    #         # print(i)
    #     return df4

    def drop_null_values(self):
        newdf=self.df
        li2 = newdf.columns.tolist()
        for i in li2:
            percent_missing = newdf[i].isnull().sum() * 100 / len(newdf)
            if (percent_missing > 70):
                newdf.drop(i, inplace=True, axis=1)
        newdf = newdf.dropna()
        self.df = newdf

    
    def featureselection(self, col, no_cols_you_want):
        
        self.drop_null_values()
        # print(self.df)
        newdf3=self.df
        newdf3 = newdf3.iloc[1:, :]
        li2=newdf3.columns.tolist()
        count_row = newdf3.shape[0]
        for i in li2:
            newdf3[i]=pd.to_numeric(newdf3[i], errors='ignore')
        X = newdf3.drop([col], axis=1)
        y = newdf3[col]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
        
        #Getting cols with object and integer datatypes in data set
        
        dfobj=newdf3.select_dtypes(include=['object'])
        lii2=dfobj.columns.tolist()
        totalcategoricalcols = len(dfobj.axes[1])
        categoricalcols=0
        feasturelist=[]
        
        
        
        
        #For categorical values
        
        if not dfobj.empty:
            # prepare input data
            oe = OrdinalEncoder()
            oe.fit(dfobj)
            X_enc = oe.transform(dfobj)
            
            # prepare target
            if newdf3[col].dtypes=='object':
                le = LabelEncoder()
                le.fit(y)
                y_enc = le.transform(y)
            else:
                y=y.astype(int)
                y_enc = y
            X_train_enc, X_test_enc, y_train_enc, y_test_enc = train_test_split(X_enc, y_enc, test_size=0.33, random_state=1)
            # feature selection
            def select_features(X_train, y_train, X_test):
                fs = SelectKBest(score_func=chi2, k=no_cols_you_want)
                fs.fit(X_train, y_train)
                X_train_fs = fs.transform(X_train)
                X_test_fs = fs.transform(X_test)
                return X_train_fs, X_test_fs, fs
            # feature selection
            X_train_fs, X_test_fs, fs = select_features(X_train_enc, y_train_enc, X_test_enc)
            # what are scores for the features
            for i in range(len(fs.scores_)):
                feasturelist.append(fs.scores_[i])

    
        
        
        # Now getting features from numerical data
        
        dfobj2=X.select_dtypes(include=np.number)
        #apply SelectKBest class to extract best features
        bestfeatures = SelectKBest(score_func=chi2, k=no_cols_you_want/2)
        dfobj2[dfobj2 < 0] = 0
        # prepare target
        if newdf3[col].dtypes=='object':
            le = LabelEncoder()
            le.fit(y)
            y_train_enc = le.transform(y)
        else:
            y=y.astype(int)
            y_train_enc = y

        fit = bestfeatures.fit(dfobj2,y_train_enc)
        dfscores = pd.DataFrame(fit.scores_)
        dfcolumns = pd.DataFrame(dfobj2.columns)
        #concat two dataframes for better visualization 
        featureScores = pd.concat([dfcolumns,dfscores],axis=1)
        featureScores.columns = ['Specs','Score']  #naming the dataframe columns
        cl=featureScores['Specs']
        dfcolumns1=featureScores.nlargest(no_cols_you_want,'Score')
        df3 = pd.DataFrame()
        numer=[]
        for i in dfcolumns1['Specs']:
            numer.append(i)
        numericalcolfeatures=[]
        for i in dfcolumns1['Score']:
            numericalcolfeatures.append(i)
        
        #concating features list of both numeiracl and categorical
        listtt=numericalcolfeatures + feasturelist
        
        #finding best on basis of features
        maxi1=0
        colmns=[]#creating list for final cols
        feasturelist2 = feasturelist.copy()
        #In this loop we are getting name of cols according to their scores in decending order
        for i in range(len(listtt)):
            maxi1=max(listtt)
            exist_count = feasturelist.count(maxi1)#Checking if maximum is exist in categorical or not
            if exist_count > 0:#This will search in categorical col
                index1=feasturelist.index(maxi1)#Finding index of max value 
                for i in lii2:#lii2 is a list of categorical cols
                    if index1==lii2.index(i):
                        colmns.append(i)# getting features with max preference in data set
                listtt.remove(max(listtt))#Removing max value for finding next maximum
            else:#This will search in numerical col
                index2=numericalcolfeatures.index(maxi1)#Finding index of max value 
                for i in numer:#numer is a list of numerical cols
                    if index2==numer.index(i):
                        colmns.append(i)# getting features with max preference in data set
                listtt.remove(max(listtt))#Removing max value for finding next maximum
        #Appending column in a dataframe
        df5 = pd.DataFrame()
        counter=0
        for i in colmns:
            if(counter>=no_cols_you_want):
                break
            if i==col:#Checking if the target col exist is list or not if exist then we will skip this iteration and will not add it to dataframe
                can=[]
            else:    
                df5[i]=newdf3[i]
                counter+=1
        self.df= df5

    def getFeaturedDataset(self):
        return self.df
