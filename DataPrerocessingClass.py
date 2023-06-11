import pandas as pd

import Microservices_class

class preprocessing(Microservices_class.Microservices):

    datasetBeforePreprocessing = pd.DataFrame(data=None)

    def __init__(self):
        self.datasetBeforePreprocessing = Microservices_class.Microservices.df

    def getDatasetBeforePreprocessing(self):
        return self.datasetBeforePreprocessing

    def update_dataframe(self, path):
        self.df.to_csv(path, index=False)
    
    def getNumberOfRowCount(self):
        return self.df.shape[0]

    def getNumberOfcolumnCount(self):
        return self.df.shape[1]
