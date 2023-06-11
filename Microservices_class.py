import pandas as pd
from skimpy import clean_columns
class Microservices:
    df = pd.DataFrame(data=None)
    def __init__(self, path):
        tempdf = pd.read_csv(path, nrows=100)
        Microservices.df = clean_columns(tempdf)

    def displayDataFrame(self):
        print(Microservices.df)
    
    def getNumericColumnsOnly(self):
        numerics = ['int16', 'int32', 'int64',
                    'float16', 'float32', 'float64']
        df = self.df.select_dtypes(include=numerics)
        clean_df = clean_columns(df)
        return clean_df.columns.tolist()
    
    def getAllColumnsName(self):
        clean_df = clean_columns(self.df)
        return clean_df.columns.tolist()
        # Columns = self.df.columns.values.tolist()
        # return Columns

    def getdataframe(self):
        return self.df

