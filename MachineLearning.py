import Microservices_class
import pandas as pd
import statistics
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
import numpy as np
from sklearn import datasets, linear_model, metrics
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import confusion_matrix
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import sys
import os
class MachineLearningClass(Microservices_class.Microservices):

    datasetForMachineLearning = pd.DataFrame(data=None)

    def __init__(self,PreProcessedDataset):
        self.datasetForMachineLearning = PreProcessedDataset
        self.HandleNullValues()
    def setDataFrameForMachineLearning(self,tempdf):
        self.datasetForMachineLearning = tempdf
    
    def getAllColumnsName(self):
        Columns = list(self.datasetForMachineLearning.columns.values.tolist())
        return Columns

    def getDataFrame(self):
        return self.datasetForMachineLearning

    def getNumberOfRowCount(self):
        return self.datasetForMachineLearning.shape[0]

    def HandleNullValues(self):

        li2 = self.datasetForMachineLearning.columns.tolist()
        for i in li2:
            self.datasetForMachineLearning[i] = pd.to_numeric(self.datasetForMachineLearning[i], errors='ignore')
        for i in li2:
            percent_missing = self.datasetForMachineLearning[i].isnull().sum() * 100 / len(self.datasetForMachineLearning)
            if (percent_missing > 80):
                self.datasetForMachineLearning.drop(i, inplace=True, axis=1)
        
        li3 = self.datasetForMachineLearning.columns.tolist()
        for i in li3:
            if (self.datasetForMachineLearning[i].dtype.kind in 'biufc'):
                meanval = self.datasetForMachineLearning[i].mean()
                self.datasetForMachineLearning[i].fillna(meanval, inplace=True)
            else:
                valu = self.datasetForMachineLearning[i].mode(dropna=True)
                self.datasetForMachineLearning[i].fillna(valu[0], inplace=True)
    
    def linear_regression(self,col, test_size, state):
        try:
            X = self.datasetForMachineLearning.drop([col], axis=1)
            y = self.datasetForMachineLearning[col]
            dfobj = X.select_dtypes(include=['object'])
            dfobj1 = X.select_dtypes(include=np.number)
            if not dfobj.empty:
                #dfobj.to_numpy()
                labelencoder_X = LabelEncoder()
                for i in dfobj.columns:
                    dfobj[i] = labelencoder_X.fit_transform(dfobj[i])
                li = self.datasetForMachineLearning.columns.tolist()
                li1 = dfobj.columns.tolist()
                for i in li1:
                    for j in li:
                        if i == j:
                            X[i] = dfobj[j]
                            break
            if self.datasetForMachineLearning[col].dtypes == 'object':
                y = labelencoder_X.fit_transform(y)
            else:
                y = y.astype(int)
                y = y

            # splitting X and y into training and testing sets

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size,
                                                                random_state=state)
            reg = linear_model.LinearRegression()
            reg.fit(X_train, y_train)
            y_pred = reg.predict(X_test)
            r2_score = reg.score(X_test, y_test)
            r2_score = r2_score*100
            mse = mean_squared_error(y_test, y_pred)
            # print(mse)
            # print("Accuracy", r2_score, '%')
            baseline_mse = 0
            baseline_r2_score = 0

            # Create a line plot
            fig = go.Figure()

            # Add a trace for the accuracy line
            fig = go.Figure(data=[
                go.Bar(name='Accuracy', x=[r2_score], y=[
                       'Accuracy'], orientation='h', marker=dict(color='rgb(35,139,69)')),
                go.Bar(name='MSE', x=[mse], y=['mean_squared_error'],
                       orientation='h', marker=dict(color='rgb(102,194,164)')),
            ], layout=go.Layout(
                title="Model Evaluation Metrics"
            ))

            # Show chart
            return fig
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    
    def logistic_regression(self,col, test_size, state, f1_score_average):
        try:

            X = self.datasetForMachineLearning.drop([col], axis=1)
            y = self.datasetForMachineLearning[col]
            dfobj = X.select_dtypes(include=['object'])
            dfobj1 = X.select_dtypes(include=np.number)
            if not dfobj.empty:
                #dfobj.to_numpy()
                labelencoder_X = LabelEncoder()
                for i in dfobj.columns:
                    dfobj[i] = labelencoder_X.fit_transform(dfobj[i])
                li = self.datasetForMachineLearning.columns.tolist()
                li1 = dfobj.columns.tolist()
                for i in li1:
                    for j in li:
                        if i == j:
                            X[i] = dfobj[j]
                            break
            if self.datasetForMachineLearning[col].dtypes == 'object':
                y = labelencoder_X.fit_transform(y)
            else:
                y = y.astype(int)
                y = y
            logr = linear_model.LogisticRegression()
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size,
                                                                random_state=state)
            logr.fit(X_train, y_train)
            predictions = logr.predict(X_test)
            #confusion_matrix = confusion_matrix(y_true, y_pred)
            conf_matrix = confusion_matrix(y_true=y_test, y_pred=predictions)
            acc = accuracy_score(y_test, y_pred=predictions)
            precision = precision_score(
                y_test, predictions, average=f1_score_average, zero_division=0)
            recall = recall_score(y_test, predictions,
                                  average=f1_score_average, zero_division=0)
            F1score = 2 * (precision * recall) / (precision + recall)
            f1 = f1_score(y_test, y_pred=predictions, average=f1_score_average)

            # Create figure with two subplots
            fig = make_subplots(rows=1, cols=2)

            # Add first trace to first subplot
            fig.add_trace(go.Heatmap(
                z=conf_matrix,
                x=["Predicted Positive", "Predicted Negative"],
                y=["True Positive", "True Negative"],
                colorscale='Greens'
            ))

            # Add third trace to second subplot
            fig.add_trace(go.Bar(name='Recall', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          recall], y=['Recall'], orientation='h', marker=dict(color='rgb(178,226,226)')))

            # Add third trace to second subplot
            fig.add_trace(go.Bar(name='F1 Score', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          F1score], y=['F1'], orientation='h', marker=dict(color='rgb(102,194,164)')))

            # Add second trace to second subplot
            fig.add_trace(go.Bar(name='precision', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          precision], y=['Precision'], orientation='h', marker=dict(color='rgb(144, 238, 144)')))

            # Add second trace to second subplot
            fig.add_trace(go.Bar(name='Accuracy', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          acc], y=['Accuracy'], orientation='h', marker=dict(color='rgb(35,139,69)')))


#             fig.update(coloraxis=None)

#             fig.update_layout(xaxis_title='X-axis Title', yaxis_title='Y-axis Title', title='Figure Title')
#             fig.update_layout(width=800, height=600)
            return fig
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Random_forest(self,col, test_size, state, f1_score_average):
        try:

            X = self.datasetForMachineLearning.drop([col], axis=1)
            y = self.datasetForMachineLearning[col]
            dfobj = X.select_dtypes(include=['object'])
            dfobj1 = X.select_dtypes(include=np.number)
            if not dfobj.empty:
                labelencoder_X = LabelEncoder()
                for i in dfobj.columns:
                    dfobj[i] = labelencoder_X.fit_transform(dfobj[i])
                li = self.datasetForMachineLearning.columns.tolist()
                li1 = dfobj.columns.tolist()
                for i in li1:
                    for j in li:
                        if i == j:
                            X[i] = dfobj[j]
                            break
            if self.datasetForMachineLearning[col].dtypes == 'object':
                y = labelencoder_X.fit_transform(y)
            else:
                y = y.astype(int)
                y = y
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=state)

            rf_model = RandomForestClassifier(
                n_estimators=50, max_features="auto", random_state=state)
            rf_model.fit(X_train, y_train)
            predictions = rf_model.predict(X_test)
            acc = accuracy_score(y_test, y_pred=predictions)
            precision = precision_score(
                y_test, predictions, average=f1_score_average, zero_division=0)
            recall = recall_score(y_test, predictions,
                                  average=f1_score_average, zero_division=0)
            F1score = 2 * (precision * recall) / (precision + recall)
            f1 = f1_score(y_test, y_pred=predictions, average=f1_score_average)
            conf_matrix = confusion_matrix(y_true=y_test, y_pred=predictions)
            # Create figure with two subplots
            fig = make_subplots(rows=1, cols=2)

            # Add first trace to first subplot
            fig.add_trace(go.Heatmap(
                z=conf_matrix,
                x=["Predicted Positive", "Predicted Negative"],
                y=["True Positive", "True Negative"],
                colorscale='Greens'
            ))

            # Add third trace to second subplot
            fig.add_trace(go.Bar(name='Recall', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          recall], y=['Recall'], orientation='h', marker=dict(color='rgb(178,226,226)')))

            # Add third trace to second subplot
            fig.add_trace(go.Bar(name='F1 Score', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          F1score], y=['F1'], orientation='h', marker=dict(color='rgb(102,194,164)')))

            # Add second trace to second subplot
            fig.add_trace(go.Bar(name='precision', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          precision], y=['Precision'], orientation='h', marker=dict(color='rgb(144, 238, 144)')))

            # Add second trace to second subplot
            fig.add_trace(go.Bar(name='Accuracy', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          acc], y=['Accuracy'], orientation='h', marker=dict(color='rgb(35,139,69)')))

            return fig
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def KNN(self,col, test_size, state, neighbours, f1_score_average):
        try:

            X = self.datasetForMachineLearning.drop([col], axis=1)
            y = self.datasetForMachineLearning[col]
            dfobj = X.select_dtypes(include=['object'])
            dfobj1 = X.select_dtypes(include=np.number)
            if not dfobj.empty:
                #dfobj.to_numpy()
                labelencoder_X = LabelEncoder()
                for i in dfobj.columns:
                    dfobj[i] = labelencoder_X.fit_transform(dfobj[i])
                li = self.datasetForMachineLearning.columns.tolist()
                li1 = dfobj.columns.tolist()
                for i in li1:
                    for j in li:
                        if i == j:
                            X[i] = dfobj[j]
                            break
            if self.datasetForMachineLearning[col].dtypes == 'object':
                y = labelencoder_X.fit_transform(y)
            else:
                y = y.astype(int)
                y = y

            X_train, X_test, Y_train, Y_test = train_test_split(
                X, y, test_size=test_size, random_state=state)
            knn = KNeighborsClassifier(n_neighbors=neighbours).fit(X_train, Y_train)
            predictions = knn.predict(X_test)  # Predictions on Testing data
            acc = accuracy_score(Y_test, y_pred=predictions)
            precision = precision_score(
                Y_test, predictions, average=f1_score_average, zero_division=0)
            recall = recall_score(Y_test, predictions,
                                  average=f1_score_average, zero_division=0)
            F1score = 2 * (precision * recall) / (precision + recall)
            conf_matrix = confusion_matrix(y_true=Y_test, y_pred=predictions)
            # Create figure with two subplots
            fig = make_subplots(rows=1, cols=2)

            # Add first trace to first subplot
            fig.add_trace(go.Heatmap(
                z=conf_matrix,
                x=["Predicted Positive", "Predicted Negative"],
                y=["True Positive", "True Negative"],
                colorscale='Greens'
            ))

            # Add third trace to second subplot
            fig.add_trace(go.Bar(name='Recall', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          recall], y=['Recall'], orientation='h', marker=dict(color='rgb(178,226,226)')))

            # Add third trace to second subplot
            fig.add_trace(go.Bar(name='F1 Score', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          F1score], y=['F1'], orientation='h', marker=dict(color='rgb(102,194,164)')))

            # Add second trace to second subplot
            fig.add_trace(go.Bar(name='precision', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          precision], y=['Precision'], orientation='h', marker=dict(color='rgb(144, 238, 144)')))

            # Add second trace to second subplot
            fig.add_trace(go.Bar(name='Accuracy', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          acc], y=['Accuracy'], orientation='h', marker=dict(color='rgb(35,139,69)')))

            return fig
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    def Naive_Bayes(self,col,test_size,randomstate,f1_score_average):
        try:

            X = self.datasetForMachineLearning.drop([col], axis=1)
            y = self.datasetForMachineLearning[col]
            dfobj=X.select_dtypes(include=['object'])
            dfobj1=X.select_dtypes(include=np.number)
            if not dfobj.empty:
                #dfobj.to_numpy()
                labelencoder_X = LabelEncoder()
                for i in dfobj.columns:
                    dfobj[i] = labelencoder_X.fit_transform(dfobj[i])
                li = self.datasetForMachineLearning.columns.tolist()
                li1=dfobj.columns.tolist()
                for i in li1:
                    for j in li:
                        if i==j:
                            X[i] = dfobj[j]
                            break
            if self.datasetForMachineLearning[col].dtypes == 'object':
                    y = labelencoder_X.fit_transform(y)
            else:
                y=y.astype(int)
                y = y

            X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=test_size, random_state=randomstate)

            # training the model on training set
            gnb = GaussianNB()
            gnb.fit(X_train, Y_train)

            # making predictions on the testing set
            predictions = gnb.predict(X_test)
            acc = accuracy_score(Y_test, y_pred=predictions)
            precision = precision_score(
                Y_test, predictions, average=f1_score_average, zero_division=0)
            recall = recall_score(Y_test, predictions,
                                  average=f1_score_average, zero_division=0)
            F1score = 2 * (precision * recall) / (precision + recall)
            conf_matrix = confusion_matrix(y_true=Y_test, y_pred=predictions)
            # Create figure with two subplots
            fig = make_subplots(rows=1, cols=2)

            # Add first trace to first subplot
            fig.add_trace(go.Heatmap(
                z=conf_matrix,
                x=["Predicted Positive", "Predicted Negative"],
                y=["True Positive", "True Negative"],
                colorscale='Greens'
                ))

            # Add third trace to second subplot
            fig.add_trace(go.Bar(name='Recall',xaxis='x2', yaxis='y2',showlegend=False, x=[recall], y=['Recall'], orientation='h', marker=dict(color='rgb(178,226,226)')))  

            # Add third trace to second subplot
            fig.add_trace(go.Bar(name='F1 Score',xaxis='x2', yaxis='y2',showlegend=False, x=[F1score], y=['F1'], orientation='h', marker=dict(color='rgb(102,194,164)')))

            # Add second trace to second subplot
            fig.add_trace(go.Bar(name='precision',xaxis='x2', yaxis='y2',showlegend=False, x=[precision], y=['Precision'], orientation='h', marker=dict(color='rgb(144, 238, 144)')))

            # Add second trace to second subplot
            fig.add_trace(go.Bar(name='Accuracy',xaxis='x2', yaxis='y2',showlegend=False ,x=[acc], y=['Accuracy'], orientation='h', marker=dict(color='rgb(35,139,69)')))

            return fig
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def descion_tree(self,col, test_size, randomstate, f1_score_average):
        try:

            X = self.datasetForMachineLearning.drop([col], axis=1)
            y = self.datasetForMachineLearning[col]
            dfobj = X.select_dtypes(include=['object'])
            dfobj1 = X.select_dtypes(include=np.number)
            if not dfobj.empty:
                #dfobj.to_numpy()
                labelencoder_X = LabelEncoder()
                for i in dfobj.columns:
                    dfobj[i] = labelencoder_X.fit_transform(dfobj[i])
                li = self.datasetForMachineLearning.columns.tolist()
                li1 = dfobj.columns.tolist()
                for i in li1:
                    for j in li:
                        if i == j:
                            X[i] = dfobj[j]
                            break
            if self.datasetForMachineLearning[col].dtypes == 'object':
                y = labelencoder_X.fit_transform(y)
            else:
                y = y.astype(int)
                y = y

            X_train, X_test, Y_train, Y_test = train_test_split(
                X, y, test_size=test_size, random_state=randomstate)

            # training the model on training set
            clf = DecisionTreeClassifier()

            # Fit the model to the training data
            clf.fit(X_train, Y_train)

            # making predictions on the testing set
            predictions = clf.predict(X_test)
            acc = accuracy_score(Y_test, y_pred=predictions)
            precision = precision_score(
                Y_test, predictions, average=f1_score_average, zero_division=0)
            recall = recall_score(Y_test, predictions,
                                  average=f1_score_average, zero_division=0)
            F1score = 2 * (precision * recall) / (precision + recall)
            conf_matrix = confusion_matrix(y_true=Y_test, y_pred=predictions)
            # Create figure with two subplots
            fig = make_subplots(rows=1, cols=2)

            # Add first trace to first subplot
            fig.add_trace(go.Heatmap(
                z=conf_matrix,
                x=["Predicted Positive", "Predicted Negative"],
                y=["True Positive", "True Negative"],
                colorscale='Greens'
            ))

            # Add third trace to second subplot
            fig.add_trace(go.Bar(name='Recall', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          recall], y=['Recall'], orientation='h', marker=dict(color='rgb(178,226,226)')))

            # Add third trace to second subplot
            fig.add_trace(go.Bar(name='F1 Score', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          F1score], y=['F1'], orientation='h', marker=dict(color='rgb(102,194,164)')))

            # Add second trace to second subplot
            fig.add_trace(go.Bar(name='precision', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          precision], y=['Precision'], orientation='h', marker=dict(color='rgb(144, 238, 144)')))

            # Add second trace to second subplot
            fig.add_trace(go.Bar(name='Accuracy', xaxis='x2', yaxis='y2', showlegend=False, x=[
                          acc], y=['Accuracy'], orientation='h', marker=dict(color='rgb(35,139,69)')))

            return fig
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def DisplayDataset(self):
        print(self.datasetForMachineLearning)
