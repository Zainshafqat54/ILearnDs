import Microservices_class
import RawDataVisualizationClass
import DataPrerocessingClass
import DataCleaningClass
import DataReductionClass
import DataTransformationClass
import MachineLearning
def UploadDataSet(path):
    MicroServicesObj=Microservices_class.Microservices(path)
    return MicroServicesObj

def callingRawDataVisualizationClassFunc(functToCall, columntoVisualize):
    RawDataInstance = RawDataVisualizationClass.rawDataVisualization()
    if functToCall == 'correlation':
        return (RawDataInstance.visualize_corr_btw_attr())
    elif functToCall == 'null_val':
        return RawDataInstance.Visualize_null_Val_Percentage()
    elif functToCall == 'value_count':
        return RawDataInstance.visualize_attr_all_value_count(columntoVisualize)
    elif functToCall == 'stats':
        return RawDataInstance.visualize_all_attr_stats(columntoVisualize)
    elif functToCall == 'distribution':
        return RawDataInstance.visualize_all_attr_distribution(columntoVisualize)
    elif functToCall == 'outliers':
        return RawDataInstance.visualize_all_attr_Outliers(columntoVisualize)
    else:
        print("No Function call Matches")

# def getColumnsList():
#     Microservices_class.Microservices.

# UploadDataSet(r"C:\Users\MOON COMPUTER\Desktop\House_Rent_Dataset.csv")
# UploadDataSet(r"D:\Anas Degree\sem 7\FYP\Datasets\BankChurners.csv")
# UploadDataSet(r"D:\Anas Degree\sem 7\FYP\Datasets\heart_failure_clinical_records_dataset.csv")
# UploadDataSet(r"D:\Anas Degree\sem 7\FYP\Datasets\TrainingData.csv")


# callingRawDataVisualizationClassFunc('correlation')

# DataPreprocessingInstance=DataPrerocessingClass.preprocessing()
# DataCleaningInstance=DataCleaningClass.DataCleaning(DataPreprocessingInstance)
# DataCleaningInstance.remove_spaces_between_cols()

# DataReductionInstance=DataReductionClass.DataReduction(DataPreprocessingInstance)
# DataReductionInstance.Feature_Selection_via_univariate_statistical_tests('price_range',30)

# DataTransformationIntance=DataTransformationClass.DataTransformation(DataPreprocessingInstance)
# DataTransformationIntance.Data_normalization()