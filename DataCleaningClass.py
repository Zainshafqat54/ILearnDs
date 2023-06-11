import DataPrerocessingClass
import re as re
import statistics
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split

class DataCleaning:

    def __init__(self, preprocesingInstance):
        self.df = preprocesingInstance.datasetBeforePreprocessing

    def setDataSet(self, preprocesingInstance):
        self.df = preprocesingInstance.datasetBeforePreprocessing
    
    def replacingAmbigiousValuesWithNan(self):
        self.df = self.df.astype(str)
        # Replace infinite updated data with nan
        self.df.replace([np.inf, -np.inf], np.NaN, regex=True ,inplace=True)
        # Replace blank spaces with nan
        self.df.replace(r'^\s*$', np.NaN, regex=True, inplace=True)
        # Replcae Null with nan
        self.df.replace(r'Null', np.NaN, inplace=True)
        # Replcae na with nan
        self.df.replace(r'na', np.NaN, inplace=True)
        # Replcae nan with NaN
        self.df.replace(r'nan', np.NaN, inplace=True)
        self.settingDataSetType()

    def getDataset(self):
        return self.df

    def replacing_Null_Values_With_upperOnes(self):
        self.df.fillna(method='pad', inplace=True)

    def replacing_Null_Values_With_LowerOnes(self):
        self.df.fillna(method='bfill', inplace=True)

    def replacing_Null_Values_with_Max(self):
        li2 = self.df.columns.tolist()
        li3 = self.df.columns.tolist()
        for i in li3:
            if (self.df[i].dtype.kind in 'biufc'):
                maxval = self.df[i].max()
                self.df[i].fillna(maxval, inplace=True)
            else:
                valu = statistics.mode(self.df[i])
                self.df[i].fillna(valu, inplace=True)
    
    def replacing_Null_Values_with_Min(self):
        li2 = self.df.columns.tolist()
        li3 = self.df.columns.tolist()
        for i in li3:
            if (self.df[i].dtype.kind in 'biufc'):
                maxval = self.df[i].min()
                self.df[i].fillna(maxval, inplace=True)
            else:
                valu = statistics.mode(self.df[i])
                self.df[i].fillna(valu, inplace=True)

    def replacing_Null_Values_with_Mean(self):
        li2 = self.df.columns.tolist()
        li3 = self.df.columns.tolist()
        for i in li3:
            if (self.df[i].dtype.kind in 'biufc'):
                maxval = self.df[i].mean()
                self.df[i].fillna(maxval, inplace=True)
            else:
                valu = statistics.mode(self.df[i])
                self.df[i].fillna(valu, inplace=True)

    def Dropping_Null_values(self,Axis,How):
        self.df.dropna(axis=Axis,how=How,inplace=True)
        self.df.reset_index(drop=True,  inplace=True)


    def remove_urls_emojis_special_characters(self,ColumnNameList):
        if ColumnNameList:
            self.df = self.df.astype(str)
            if ColumnNameList[0] == 'ALLCOLUMNS' or 'ALLCOLUMNS' in ColumnNameList:
                ColumnsName = self.df.columns.tolist()
                for i in ColumnsName:
                    self.df[i] = self.df[i].str.replace('[^A-Za-z0-9.,]', ' ', flags=re.UNICODE)
                self.replacingAmbigiousValuesWithNan()
                self.settingDataSetType()
            else:
                for i in ColumnNameList:               
                    self.df[i] = self.df[i].str.replace(
                            '[^A-Za-z0-9.,]', ' ', flags=re.UNICODE)
                self.replacingAmbigiousValuesWithNan()
                self.settingDataSetType()


    def remove_tags(self,string):
        result = re.sub('<.*?>', '', string)
        return result

    def remove_html_tags(self, ColumnNameList):
        if ColumnNameList:
            self.df = self.df.astype(str)
            if ColumnNameList[0] == 'ALLCOLUMNS' or 'ALLCOLUMNS' in ColumnNameList:
                ColumnsName = self.df.columns.tolist()
                for i in ColumnsName:
                    self.df[i] = self.df[i].apply(lambda cw: self.remove_tags(cw))
                self.replacingAmbigiousValuesWithNan()
                self.settingDataSetType()
            else:               
                for i in ColumnNameList:
                    self.df[i] = self.df[i].apply(lambda cw: self.remove_tags(cw))
                self.replacingAmbigiousValuesWithNan()
                self.settingDataSetType()
                    

    def drop_duplicates(self, ColumnNameList,keep):
        if keep=='None':
            keep=False
        if ColumnNameList:
            if ColumnNameList[0] == 'ALLCOLUMNS' or 'ALLCOLUMNS' in ColumnNameList:
                self.df = self.df.drop_duplicates(keep=keep, ignore_index=True)
                self.df.reset_index(drop=True,  inplace=True)
            else:
                self.df = self.df.drop_duplicates(
                    subset=ColumnNameList, keep=keep,ignore_index=True)
                self.df.reset_index(drop=True,  inplace=True)

    def remove_spaces_between_cols(self):
        self.df.columns = self.df.columns.str.replace(' ', '_')

    def GetDatasetPreprocessed(self):
        return self.df
    
    def getAllColumnsName(self):
        return self.df.columns.tolist()


    def replaceColumnName(self,ColumnToReplace,ColumnReplaceWith):
        self.df.rename(columns = {ColumnToReplace:ColumnReplaceWith}, inplace = True)
    
    def replaceCellvalue(self,ColumnName,RowIndex,Value):
        # print(self.df.at[RowIndex, ColumnName])
        self.df.at[int(RowIndex), ColumnName] = Value


    def drop_Column(self,ColumnList):
        self.df.drop(labels=ColumnList, axis=1,inplace=True)

    def drop_Rows(self,rangeFrom,rangeTo):
        self.df.drop(labels=range(int(rangeFrom), int(rangeTo)), axis=0,  inplace=True)
        self.df.reset_index(drop=True,  inplace=True)

    def settingDataSetType(self):
        li2=self.df.columns.tolist()
        for i in li2:
            self.df[i]=pd.to_numeric(self.df[i], errors='ignore')
    

    # Data Transformation

    def drop_null_values(self):
        newdf = self.df
        li2 = newdf.columns.tolist()
        for i in li2:
            percent_missing = newdf[i].isnull().sum() * 100 / len(newdf)
            if (percent_missing > 70):
                newdf.drop(i, inplace=True, axis=1)
        newdf = newdf.dropna()
        self.df = newdf

    def FeatureSelectionVia_Chi_Square(self, col, no_cols_you_want):
        try:

            self.drop_null_values()
            if (no_cols_you_want > len(self.df.columns.tolist())):
                no_cols_you_want = len(self.df.columns.tolist())
            # print(self.df)
            newdf3 = self.df
            newdf3 = newdf3.iloc[1:, :]
            li2 = newdf3.columns.tolist()
            count_row = newdf3.shape[0]
            for i in li2:
                newdf3[i] = pd.to_numeric(newdf3[i], errors='ignore')
            X = newdf3.drop([col], axis=1)
            y = newdf3[col]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.33, random_state=1)

            # Getting cols with object and integer datatypes in data set

            dfobj = newdf3.select_dtypes(include=['object'])
            lii2 = dfobj.columns.tolist()
            totalcategoricalcols = len(dfobj.axes[1])
            categoricalcols = 0
            feasturelist = []

            # For categorical values

            if not dfobj.empty:
                # prepare input data
                oe = OrdinalEncoder()
                oe.fit(dfobj)
                X_enc = oe.transform(dfobj)

                # prepare target
                if newdf3[col].dtypes == 'object':
                    le = LabelEncoder()
                    le.fit(y)
                    y_enc = le.transform(y)
                else:
                    y = y.astype(int)
                    y_enc = y
                X_train_enc, X_test_enc, y_train_enc, y_test_enc = train_test_split(
                    X_enc, y_enc, test_size=0.33, random_state=1)
                # feature selection

                def select_features(X_train, y_train, X_test):
                    fs = SelectKBest(score_func=chi2, k='all')
                    fs.fit(X_train, y_train)
                    X_train_fs = fs.transform(X_train)
                    X_test_fs = fs.transform(X_test)
                    return X_train_fs, X_test_fs, fs
                # feature selection
                X_train_fs, X_test_fs, fs = select_features(
                    X_train_enc, y_train_enc, X_test_enc)
                # what are scores for the features
                for i in range(len(fs.scores_)):
                    feasturelist.append(fs.scores_[i])

            # Now getting features from numerical data

            dfobj2 = X.select_dtypes(include=np.number)
            # apply SelectKBest class to extract best features
            bestfeatures = SelectKBest(score_func=chi2, k=no_cols_you_want/2)
            dfobj2[dfobj2 < 0] = 0
            # prepare target
            if newdf3[col].dtypes == 'object':
                le = LabelEncoder()
                le.fit(y)
                y_train_enc = le.transform(y)
            else:
                y = y.astype(int)
                y_train_enc = y

            fit = bestfeatures.fit(dfobj2, y_train_enc)
            dfscores = pd.DataFrame(fit.scores_)
            dfcolumns = pd.DataFrame(dfobj2.columns)
            # concat two dataframes for better visualization
            featureScores = pd.concat([dfcolumns, dfscores], axis=1)
            # naming the dataframe columns
            featureScores.columns = ['Specs', 'Score']
            cl = featureScores['Specs']
            dfcolumns1 = featureScores.nlargest(no_cols_you_want, 'Score')
            df3 = pd.DataFrame()
            numer = []
            for i in dfcolumns1['Specs']:
                numer.append(i)
            numericalcolfeatures = []
            for i in dfcolumns1['Score']:
                numericalcolfeatures.append(i)

            # concating features list of both numeiracl and categorical
            listtt = numericalcolfeatures + feasturelist

            # finding best on basis of features
            maxi1 = 0
            colmns = []  # creating list for final cols
            feasturelist2 = feasturelist.copy()
            # In this loop we are getting name of cols according to their scores in decending order
            for i in range(len(listtt)):
                maxi1 = max(listtt)
                # Checking if maximum is exist in categorical or not
                exist_count = feasturelist.count(maxi1)
                if exist_count > 0:  # This will search in categorical col
                    # Finding index of max value
                    index1 = feasturelist.index(maxi1)
                    for i in lii2:  # lii2 is a list of categorical cols
                        if index1 == lii2.index(i):
                            # getting features with max preference in data set
                            colmns.append(i)
                    # Removing max value for finding next maximum
                    listtt.remove(max(listtt))
                else:  # This will search in numerical col
                    index2 = numericalcolfeatures.index(
                        maxi1)  # Finding index of max value
                    for i in numer:  # numer is a list of numerical cols
                        if index2 == numer.index(i):
                            # getting features with max preference in data set
                            colmns.append(i)
                    # Removing max value for finding next maximum
                    listtt.remove(max(listtt))
            # Appending column in a dataframe
            df5 = pd.DataFrame()
            counter = 0
            for i in colmns:
                if (counter >= no_cols_you_want):
                    break
                if i == col:  # Checking if the target col exist is list or not if exist then we will skip this iteration and will not add it to dataframe
                    can = []
                else:
                    df5[i] = newdf3[i]
                    counter += 1
            self.df = df5
            self.df.reset_index(drop=True,  inplace=True)
        except:
            print("Error ocuured")

    def normalization(self):
        # print("runned-----")
        self.settingDataSetType()
        newdf1 = self.df.select_dtypes(include=np.number)
        li = newdf1.columns.tolist()
        li1 = self.df.columns.tolist()
        normalized_df = (newdf1-newdf1.min())/(newdf1.max()-newdf1.min())
        for i in li1:
            for j in li:
                if i == j:
                    self.df[i] = normalized_df[j]
                    break

    def getNumberOfRowCount(self):
        return self.df.shape[0]

    def getNumberOfcolumnCount(self):
        return self.df.shape[1]

    # def getFeaturedDataset(self):
    #     return self.df
