import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import sys
import os
import shutil
import matplotlib
from biokit.viz import corrplot
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask
import io


def getListOfColumnsOfDataFrame(df_Path):
    df = pd.read_csv(df_Path)
    return list(df.columns)

def Correlation(df_Path):
    try:
        df=pd.read_csv(df_Path)
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df = df.select_dtypes(include=numerics)
        print('CSV File Read Successfully...............\n\n')
        print(df)
        plt.clf()
        matplotlib.rcParams['figure.dpi'] = 180
        matplotlib.rcParams['figure.figsize'] = (6, 6)
        fig = plt.figure(num=None, facecolor='white', figsize=(12, 6))
        ax = plt.subplot(1, 1, 1, aspect='equal', facecolor='white')
        df = df.corr(numeric_only=True)
        c = corrplot.Corrplot(df)
        c.plot(colorbar=True, method='square', shrink=.9, rotation=45, fontsize=10, binarise_color=True,ax=ax)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
        # plt.show()
    except BaseException as e:
        print('The exception: {}'.format(e))


def Visualize_null_Val_Percentage(df_Path):
    try:
        df = pd.read_csv(df_Path)
        print('CSV File Read Successfully...............\n\n')
        if df.isnull().sum().sum() != 0:
            na_df = (df.isnull().sum() / len(df)) * 100
            na_df = na_df.drop(na_df[na_df == 0].index).sort_values(
                ascending=False)
            missing_data = pd.DataFrame({'Missing Values Ratio %': na_df})
            missing_data['Columns'] = missing_data.index
            # Figure Size
            fig, ax = plt.subplots()
            # Horizontal Bar Plot
            bars = ax.barh(
                missing_data.iloc[:, 1], missing_data.iloc[:, 0], color='crimson')
            # Remove axes splines
            for s in ['top', 'bottom', 'left', 'right']:
                ax.spines[s].set_visible(False)
            # Add padding between axes and labels
            ax.xaxis.set_tick_params(pad=20, labelsize=15)
            ax.yaxis.set_tick_params(pad=20, labelsize=15)
            for i, v in enumerate(missing_data.iloc[:, 0]):
                ax.text(v + 1.5, i, str(str(round(v, 2)) + '%'),
                        color='red', fontsize=15)
            # Add x,y gridlines
            ax.grid(b=True, color='grey', linestyle='-.',
                    linewidth=0.5, alpha=0.2)
            # Show top values
            ax.invert_yaxis()
            # Add Plot Title
            ax.set_title('Columns Having Null Values',
                         fontdict={'fontsize': 25}, pad=20)
            ax.set_xlabel('Null Values Percentage%',
                          labelpad=20, fontdict={'fontsize': 15})
            ax.set_ylabel('Column Name', labelpad=20,
                          fontdict={'fontsize': 15})
            # Show Plot
            plt.tight_layout()
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            return Response(output.getvalue(), mimetype='image/png')
            # plt.show()
        else:
            print('No Missing Values Found.')
    except BaseException as e:
        print('The exception: {}'.format(e))


def visualize_attr_all_value_count(df_Path,columnToVisualize):
    try:
         df = pd.read_csv(df_Path)
         df=df.astype(str)
         print('CSV File Readed Successfully...............\n\n')
        #  print(df)
         Columns = df.columns.values.tolist()
        #  print(Columns)
         plt.clf()
         for i in range(len(Columns)):
            print(columnToVisualize)
            if columnToVisualize == Columns[i]:
                # print("Yesssssssssssssss")
                # print("------")
                # print(df[Columns[i]].value_counts()[:10])
                lst = list(df[Columns[i]].value_counts()[:10])
                print('list= ',lst)
                print('columnName',Columns[i])
                print((df[Columns[i]].value_counts()[:10]))
                max_index = lst.index(max(lst))
                explode_value = tuple(
                    [.06 if i != max_index else 0.2 for i in range(len(list(lst)))])
                fig = (df[Columns[i]].value_counts()[:10]).plot(kind='pie', figsize=(6, 6), autopct='%.1f%%',shadow=False, explode=explode_value, pctdistance=0.65,labeldistance=1.1)
                # draw circle
                centre_circle = plt.Circle((0, 0), 0.50, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(centre_circle)
                plt.xlabel(str(Columns[i]), fontsize=30)
                plt.ylabel("")
                plt.tight_layout()
                output = io.BytesIO()
                FigureCanvas(fig).print_png(output)
                return Response(output.getvalue(), mimetype='image/png')
    except BaseException as e:
        print('The exception occurs : {}'.format(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def visualize_all_attr_stats(df_Path,columnToVisualize):
    try:
        df = pd.read_csv(df_Path)
        print('CSV File Readed Successfully...............\n\n')
        describe_num_df = df.describe(include=['int64', 'float64']).apply(
            lambda s: s.apply(lambda x: format(x, 'g')))
        describe_num_df = describe_num_df.apply(pd.to_numeric)
        describe_num_df.reset_index(inplace=True)
        describe_num_df = describe_num_df[describe_num_df['index'] != 'count']
        plt.clf()
        for i in describe_num_df.columns:
            if columnToVisualize == i:
                if i in ['index']:
                    continue
                fig, ax = plt.subplots()
                ax = sns.set_context("notebook", font_scale=1.5, rc={
                                     "lines.linewidth": 4.5})
                ax = sns.barplot(
                    x="index", y=i, data=describe_num_df, edgecolor='black')
                ax.set(ylim=(min(describe_num_df[i].tolist()), max(
                    describe_num_df[i].tolist())))
                plt.xlabel(i)
                plt.ylabel('Value')
                # ax.get_figure().savefig((path + '/' + str(i) + ".jpg"))
                plt.tight_layout()

                # plt.show()
                output = io.BytesIO()
                FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    except BaseException as e:
         print('The exception: {}'.format(e))


def visualize_all_attr_distribution(df_Path):
    try:
        df = pd.read_csv(df_Path)
        print('CSV File Readed Successfully...............\n\n')
        # path = 'Dataset_all_attr_distribution'
        # Create_directory(path)
        rqrd_columns = df.select_dtypes(
            include=np.number).columns.tolist()
        for i in rqrd_columns:
            f, (ax_box, ax_hist) = plt.subplots(
                2, sharex=True, gridspec_kw={"height_ratios": (6, 6)})
            mean = int(df[i].mean())
            median = int(df[i].median())
            mode = int(df[i].mode().values[0])
            if mean < median:
                distribution_Result = "Left Skewed"
            if mean == median:
                distribution_Result = "Normal Distribution"
            if mean > median:
                distribution_Result = "Right Skewed"
            sns.boxplot(data=df, x=i, ax=ax_box)
            ax_box.axvline(mean, color='r', linestyle='--')
            ax_box.axvline(median, color='g', linestyle='-')
            ax_box.axvline(mode, color='b', linestyle='-')
            sns.histplot(data=df, x=i, ax=ax_hist, kde=True)
            ax_hist.axvline(mean, color='r', linestyle='--', label="Mean")
            ax_hist.axvline(median, color='g',
                            linestyle='-', label="Median")
            ax_hist.axvline(mode, color='b', linestyle='-', label="Mode")
            ax_hist.text(0.7, 0.4, distribution_Result,
                         transform=ax_hist.transAxes, fontsize='10')
            ax_hist.legend()
            ax_box.set(xlabel=i)
            fig = plt.gcf()
            # fig.set_size_inches(18.5, 13)
            # fig.savefig((path + '/' + str(i) + ".png"))
            plt.tight_layout()
            # plt.show()
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            break
        return Response(output.getvalue(), mimetype='image/png')
    except BaseException as e:
         print('The exception: {}'.format(e))


def visualize_all_attr_Outliers(df_Path):
    try:
        df = pd.read_csv(df_Path)
        for i in df.select_dtypes(include=np.number).columns.tolist():
            fig, ax = plt.subplots()
            flierprops = dict(
                marker='o', markersize=10, markeredgecolor='black', markerfacecolor='red', alpha=0.5)
            # sns.set(rc={'figure.figsize': (15, 8)})
            sns.set(style="darkgrid")
            # box plot of the variable height
            ax = sns.boxplot(df[i], linewidth=2, width=0.5,
                             color='lightgrey', flierprops=flierprops, orient="h")
            # xtick, label, and title
            plt.xticks(fontsize=14)
            plt.title('Distribution of ' + str(i), fontsize=30, )
            plt.tight_layout()
            # plt.show()
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            break
        return Response(output.getvalue(), mimetype='image/png')
    except BaseException as e:
         print('The exception: {}'.format(e))