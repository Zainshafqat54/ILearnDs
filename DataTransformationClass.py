import DataPrerocessingClass
import numpy as np
class DataTransformation:

    def __init__(self, preprocesingInstance):
        self.df = preprocesingInstance.datasetBeforePreprocessing

    def Data_normalization(self):
        self.df = self.df.select_dtypes(include=np.number)
        li = self.df.columns.tolist()
        li1 = self.df.columns.tolist()
        normalized_df = (self.df - self.df.min()) / (self.df.max() - self.df.min())
        for i in li1:
            for j in li:
                if i == j:
                    self.df[i] = normalized_df[j]
                    break
        print(self.df)