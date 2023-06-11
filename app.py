import CreateNeuralNetworkScript
import Visualize_Correlation
import main
from flask import send_file
import io
import json
from flask import Response, render_template, request, jsonify
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import plotly
import plotly.express as px
matplotlib.use('Agg')
import os
app = Flask(__name__)

MicroServicesObject = main.Microservices_class.Microservices(
    "heart_failure_clinical_records_dataset.csv")

preprocessingInstance=main.DataPrerocessingClass.preprocessing()
DataCleaningInstance=main.DataCleaningClass.DataCleaning(preprocessingInstance)
DataReductionInstance=main.DataReductionClass.DataReduction(preprocessingInstance)
MachineLearningObj = main.MachineLearning.MachineLearningClass(
    DataCleaningInstance.GetDatasetPreprocessed())
@app.route("/")
def openLandingPage():
  return render_template('index.html') 

@app.route("/Data_quality_assessment")
def openDataQualityAssessmentPage():
  return render_template('Data_quality_assessment.html')


@app.route("/MicroservicesModulesOptions")
def MicroservicesModulesOptions():
   return render_template('MicroservicesModulesOption.html')

@app.route("/MachineLearning")
def MachineLearning():
   print(DataCleaningInstance.GetDatasetPreprocessed())
   MachineLearningObj.setDataFrameForMachineLearning(
       DataCleaningInstance.GetDatasetPreprocessed())
   print(MachineLearningObj.getDataFrame())
   return render_template('MachineLearning.html')

@app.route("/BuildDeepLearningModel")
def BuildDeepLearningModel():
  return render_template('BuildingDeepLearningModel.html')

@app.route('/download')
def download():
   df = DataCleaningInstance.GetDatasetPreprocessed()
   caldf = df.to_csv(index=False, header=True)
   buf_str = io.StringIO(caldf)
   return send_file(io.BytesIO(buf_str.read().encode("utf-8")), mimetype="text/csv", download_name="data.csv")


app.config['SECRET_KEY'] = 'secretkey'


# class CSVUploadForm(FlaskForm):

#    csv_file = FileField('Upload CSV file')
#    submit = SubmitField('Submit')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
   if request.method == 'POST':
      result = request.form
      # print("Yesssssssssss")
      print(result)
   # form = CSVUploadForm()
   # if request.form.get('file') is None:
   #    print('No file selected')
   else:
      file = request.files['file']
      print(file.filename)
   
   if form.validate_on_submit():
       # Get the CSV file from the request
       csv_file = request.files['csv_file']
       # Do something with the CSV file, such as saving it to the database
       print('File uploaded successfully')
     #   return 'File uploaded successfully'
   else:
      print("Error uploading a file")
   return render_template('MicroservicesModulesOption.html')




'''
quality assessment  starts from here 
'''

@app.route('/visualization_corr', methods=['GET'])
def plot_corr():
   # main.UploadDataSet("churn_data.csv")   
   png = main.callingRawDataVisualizationClassFunc('correlation','')
   return png



@app.route('/visualization_NullValue', methods=['GET'])
def plot_null_val_percentage():
   # main.UploadDataSet("churn_data.csv")
   png = main.callingRawDataVisualizationClassFunc('null_val', '')
   if png is None:
      png=main.RawDataVisualizationClass.rawDataVisualization.NoMissingValFoundFigure(
          MicroServicesObject)
   return png


@app.route('/visualization_ValueCount/<name>', methods=['GET'])
def plot_value_count(name):
   png = main.callingRawDataVisualizationClassFunc('value_count', name)
   return png


@app.route('/visualization_Statistics/<name>', methods=['GET'])
def plot_stats(name):
   # main.UploadDataSet("churn_data.csv")
   png = main.callingRawDataVisualizationClassFunc('stats', name)
   return png


@app.route('/visualization_Distribution/<name>', methods=['GET'])
def plot_distribution(name):
   # main.UploadDataSet("churn_data.csv")
   png = main.callingRawDataVisualizationClassFunc('distribution', name)
   return png


@app.route('/visualization_Outliers/<name>', methods=['GET'])
def plot_outliers(name):
   # main.UploadDataSet("churn_data.csv")
   png = main.callingRawDataVisualizationClassFunc('outliers', name)
   return png

@app.route('/getNumericColumns', methods=['GET'])
def getNumericColumnNames():
   # obj = main.UploadDataSet("churn_data.csv")
   pythondata = main.RawDataVisualizationClass.rawDataVisualization.getNumericColumnsOnly(
       MicroServicesObject)
   return json.dumps(pythondata)


@app.route('/getAllColumns', methods=['GET'])
def getAllColumnNames():
   pythondata = main.RawDataVisualizationClass.rawDataVisualization.getAllColumnsName(
       MicroServicesObject)
   return json.dumps(pythondata)


'''
preprocessing starts from here 
'''

@app.route("/DataPreprocessing", methods=("POST", "GET"))
def openDataPreProcessingPage():
  DataCleaningInstance.replacingAmbigiousValuesWithNan()
  df = DataCleaningInstance.GetDatasetPreprocessed()
  return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/resetPreProcessing", methods=("POST", "GET"))
def resetPreProcessing():
  DataCleaningInstance.replacingAmbigiousValuesWithNan()
  df = DataCleaningInstance.GetDatasetPreprocessed()
  return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route("/DisplayTop10Rows", methods=("POST", "GET"))
def DisplayTop10Rows():
  Tempdf = DataCleaningInstance.GetDatasetPreprocessed()
  df = Tempdf.head(10)
  return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/DisplayLast10Rows", methods=("POST", "GET"))
def DisplayLast10Rows():
  TempDf = DataCleaningInstance.GetDatasetPreprocessed()
  df = TempDf.tail(10)
  return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/DisplayFullDataset", methods=("POST", "GET"))
def DisplayFullDataset():
  df = DataCleaningInstance.GetDatasetPreprocessed()
  return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route("/DisplayRand10Rows", methods=("POST", "GET"))
def DisplayRand10Rows():
  df = DataCleaningInstance.GetDatasetPreprocessed()
  df = df.sample(10)
  return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/ReplaceNullValWithUpperOne", methods=("POST", "GET"))
def ReplaceNullValWithUpperOne():
   DataCleaningInstance.replacing_Null_Values_With_upperOnes()
   df = DataCleaningInstance.GetDatasetPreprocessed()
   return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/ReplaceNullValWithLowerOne", methods=("POST", "GET"))
def ReplaceNullValWithLowerOne():
   DataCleaningInstance.replacing_Null_Values_With_LowerOnes()
   df = DataCleaningInstance.GetDatasetPreprocessed()
   return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/ReplaceNullValWithMean", methods=("POST", "GET"))
def ReplaceNullValWithMean():
   DataCleaningInstance.replacing_Null_Values_with_Mean()
   df = DataCleaningInstance.GetDatasetPreprocessed()
   return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/ReplaceNullValWithMax", methods=("POST", "GET"))
def ReplaceNullValWithMax():
   DataCleaningInstance.replacing_Null_Values_with_Max()
   df = DataCleaningInstance.GetDatasetPreprocessed()
   return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route("/ReplaceNullValWithMin", methods=("POST", "GET"))
def ReplaceNullValWithMin():
   DataCleaningInstance.replacing_Null_Values_with_Min()
   df = DataCleaningInstance.GetDatasetPreprocessed()
   return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/DropNullValByRow", methods=("POST", "GET"))
def DropNullValByRow():
   DataCleaningInstance.Dropping_Null_values_By_row()
   df = DataCleaningInstance.GetDatasetPreprocessed()
   return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/DropNullValByColumn", methods=("POST", "GET"))
def DropNullValByColumn():
   DataCleaningInstance.Dropping_Null_values_By_Column()
   df = DataCleaningInstance.GetDatasetPreprocessed()
   return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route("/DropNullVal", methods=("POST", "GET"))
def DropNullVal():
   if request.method == 'POST':
      result = request.form
      keys = list(result.keys())
      KeyValue = list(result.values())
      DataCleaningInstance.Dropping_Null_values(
          KeyValue[0], KeyValue[1])
      df = DataCleaningInstance.GetDatasetPreprocessed()
      return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/getAllColumnsName", methods=("POST", "GET"))
def getAllColumnsName():
   ColumnsList = DataCleaningInstance.getAllColumnsName()
 
   return json.dumps(ColumnsList)


@app.route("/getRowcount", methods=("POST", "GET"))
def getRowcount():
   NumberOfRows = DataCleaningInstance.getNumberOfRowCount()
   return json.dumps(NumberOfRows)


@app.route("/getColumncount", methods=("POST", "GET"))
def getColumncount():
   NumberOfColumns = DataCleaningInstance.getNumberOfcolumnCount()
   return json.dumps(NumberOfColumns)

@app.route("/RemoveAmbiguityURLEmoji", methods=("POST", "GET"))
def RemoveAmbiguityURLEmoji():
   if request.method == 'POST':
      result = request.form.getlist('RemoveAmbiguityUrls_EmojisColumnName')
      DataCleaningInstance.remove_urls_emojis_special_characters(result)
      df = DataCleaningInstance.GetDatasetPreprocessed()
      return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/RemoveAmbiguityHTMLTags", methods=("POST", "GET"))
def RemoveAmbiguityHTMLTags():
   if request.method == 'POST':
      result = request.form.getlist('RemoveAmbiguityHTMLTagColumnName')
      DataCleaningInstance.remove_html_tags(result)
      df = DataCleaningInstance.GetDatasetPreprocessed()
      return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/RemoveAmbiguityColumnSpace", methods=("POST", "GET"))
def RemoveAmbiguityColumnSpace():
   DataCleaningInstance.remove_spaces_between_cols()
   df = DataCleaningInstance.GetDatasetPreprocessed()
   return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route("/DropDuplicates", methods=("POST", "GET"))
def DropDuplicates():
   if request.method == 'POST':
      ColumnsName = request.form.getlist('DropDuplicateColumns')
      result = request.form
      # print(result)
      keys = list(result.keys())
      KeyValue = list(result.values())
      # print('keys', keys)
      # print('keyValue', KeyValue)
      DataCleaningInstance.drop_duplicates(ColumnsName,KeyValue[1])
      df = DataCleaningInstance.GetDatasetPreprocessed()
      return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/replaceColVal", methods=("POST", "GET"))
def replaceColVal():
   if request.method == 'POST':
      result = request.form
      # print(result)
      keys = list(result.keys())
      KeyValue = list(result.values())
      DataCleaningInstance.replaceColumnName(KeyValue[0], KeyValue[1])
      df = DataCleaningInstance.GetDatasetPreprocessed()
      return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/replaceRowVal", methods=("POST", "GET"))
def replaceRowVal():
   if request.method == 'POST':
      result = request.form
      keys = list(result.keys())
      KeyValue = list(result.values())
      print(keys)
      print(KeyValue)
      DataCleaningInstance.replaceCellvalue(KeyValue[0], KeyValue[1], KeyValue[2])
      df = DataCleaningInstance.GetDatasetPreprocessed()
      return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/dropColumn", methods=("POST", "GET"))
def dropColumn():
   if request.method == 'POST':
      ColumnsName = request.form.getlist('dropColumnName')
      print(ColumnsName)
      DataCleaningInstance.drop_Column(ColumnsName)
      df = DataCleaningInstance.GetDatasetPreprocessed()
      return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/dropRow", methods=("POST", "GET"))
def dropRow():
   if request.method == 'POST':
      result = request.form
      keys = list(result.keys())
      KeyValue = list(result.values())
      print(keys)
      print(KeyValue)
      DataCleaningInstance.drop_Rows(KeyValue[0], KeyValue[1])
      df = DataCleaningInstance.GetDatasetPreprocessed()
      return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/featureSelectionViaChiSquare", methods=("POST", "GET"))
def featureSelectionViaChiSquare():
   if request.method == 'POST':
      result = request.form
      keys = list(result.keys())
      KeyValue = list(result.values())
      print(keys)
      print(KeyValue)
   DataCleaningInstance.FeatureSelectionVia_Chi_Square(KeyValue[0], int(KeyValue[1]))
   df = DataCleaningInstance.GetDatasetPreprocessed()
   # print(df)
   return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route("/Normalization", methods=("POST", "GET"))
def Normalization():
   DataCleaningInstance.normalization()
   df = DataCleaningInstance.GetDatasetPreprocessed()
   return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

# @app.route('/DisplayDataframe', methods=("POST", "GET"))
# def displayDataframe():
#    df = MicroServicesObject.getdataframe()
#    print(df.head())
#    return render_template('DataPreprocessing.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


# ---------------------MachineLearning-------------------------

@app.route("/<name>", methods=['POST', 'GET'])
def MachineLearningAlgorithm(name):
   if request.method == 'POST':
      result = request.form
      keys = list(result.keys())
      KeyValue = list(result.values())
      # print(name)
      #  MachineLearningObj.HandleNullValues()
      if (name == 'li'):
          figure = MachineLearningObj.linear_regression(
              KeyValue[0], float(KeyValue[1]), int(KeyValue[2]))
      if (name == 'lg'):
          figure = MachineLearningObj.logistic_regression(
              KeyValue[0], float(KeyValue[1]), int(KeyValue[2]), KeyValue[3])
      if (name == 'rf'):
          figure = MachineLearningObj.Random_forest(
              KeyValue[0], float(KeyValue[1]), int(KeyValue[2]), KeyValue[3])
      if (name == 'knn'):
          figure = MachineLearningObj.KNN(
              KeyValue[0], float(KeyValue[1]), int(KeyValue[2]), int(KeyValue[4]), KeyValue[3])
      if (name == 'dt'):
          figure = MachineLearningObj.descion_tree(
              KeyValue[0], float(KeyValue[1]), int(KeyValue[2]), KeyValue[3])
      if (name == 'Nb'):
          figure = MachineLearningObj.Naive_Bayes(
              KeyValue[0], float(KeyValue[1]), int(KeyValue[2]), KeyValue[3])
    # fgure=MachineLearningObj.linear_regression('churn', 0.4, 1)
    # fgure = MachineLearningObj.logistic_regression(
    #    'churn', 0.7, 2, 'weighted')
    # fgure = MachineLearningObj.Random_forest(
    #    'churn', 0.7, 2, 'weighted')
    # fgure = MachineLearningObj.KNN(
    #    'churn', 0.7, 2, 4, 'macro')
    # fgure = MachineLearningObj.Naive_Bayes(
    #    'churn', 0.7,1,'macro')
    # fgure = MachineLearningObj.descion_tree(
    #    'churn', 0.7, 1, 'macro')
      # Convert the figure to JSON
      plot_json = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
      # Render the template
      return render_template('MachineLearning.html', plot_json=plot_json)
   return render_template('MachineLearning.html')


@app.route('/getAllColumnsNameForMachineLearning', methods=['GET'])
def getAllColumnsNameForMachineLearning():
   #  MachineLearningObj.HandleNullValues()
    pythondata = MachineLearningObj.getAllColumnsName()
    return json.dumps(list(pythondata))


@app.route('/getRowcountForMachineLearning', methods=['GET'])
def getRowcountForMachineLearning():
   #  MachineLearningObj.HandleNullValues()
    pythondata = MachineLearningObj.getNumberOfRowCount()
    return json.dumps((pythondata))



'''Build Deep Learning Model'''

@app.route('/download_file/<FileName>')
def download_file(FileName):
        directory = 'E:\fyp1\WebAppFlask'
        path = os.path.join(directory, FileName)
        return send_file(path, as_attachment=True)

form_data = {}

@app.route('/Get-Input-Values-OF-Form', methods=['POST'])
def Get_Input_Values_OF_Form():
    global form_data
    form_data = request.get_json()
    print('type ', type(form_data))
    print('Received form data:', form_data)
    # Store the form data in a dictionary or database
    return jsonify({'message': 'Form data submitted successfully!'})

@app.route('/Create-Structure/<name>', methods=['POST'])
def handle_Create_Structure(name):
    form_class = name
    if form_class == 'ANN_Form':
        print("_________________ANN______________________________")
        CreateNeuralNetworkScript.create_and_save_ann(
            int((list(form_data.values()))[0]), int((list(form_data.values()))[1]), int((list(form_data.values()))[2]),int((list(form_data.values()))[3]))

        fileName = "ann_model.py"  # Specify the name of the file to be downloaded
        return jsonify({'file_name': fileName})

    elif form_class == 'CNN_Form':
        print("_________________CNN______________________________")

        # Call the function to handle form2
        CreateNeuralNetworkScript.create_and_save_cnn(
            int((list(form_data.values()))[0]), int((list(form_data.values()))[1]), int((list(form_data.values()))[2]),int((list(form_data.values()))[3]))

        fileName = "cnn_model.py"  # Specify the name of the file to be downloaded
        return jsonify({'file_name': fileName})
    
    elif form_class == 'RNN_Form':
        print("_________________RNN______________________________")
        CreateNeuralNetworkScript.create_and_save_rnn(
            int((list(form_data.values()))[0]), int((list(form_data.values()))[1]), int((list(form_data.values()))[2]),int((list(form_data.values()))[3]))

        fileName = "rnn_structure.py"  # Specify the name of the file to be downloaded
        return jsonify({'file_name': fileName})
    else:
        print("______________ERROR________________________________________")

    return jsonify({'status': ""})


if __name__ == "__main__":
  app.run('0.0.0.0',debug=True)