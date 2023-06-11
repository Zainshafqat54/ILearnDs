import Microservices_class
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
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Response

class rawDataVisualization(Microservices_class.Microservices):

    def __init__(self):
        self.df = Microservices_class.Microservices.df

    def visualize_corr_btw_attr(self):
        try:
            import matplotlib.pyplot as plt
            print('CSV File Read Successfully...............\n\n')
            numerics = ['int16', 'int32', 'int64',
                        'float16', 'float32', 'float64']
            df = self.df.select_dtypes(include=numerics)
            plt.clf()
            plt.cla()
            matplotlib.rcParams['figure.dpi'] = 100
            matplotlib.rcParams['figure.figsize'] = (10.5,10)
            fig = plt.figure(num=None)
            fig.set_facecolor("aliceblue")
            ax = plt.subplot(1, 1, 1, aspect='equal')
            df = df.corr(numeric_only=True)
            c = corrplot.Corrplot(df)
            c.plot(colorbar=True, method='square', shrink=.9,
                   rotation=45, fontsize=10, binarise_color=True,ax=ax)
            # c.plot(background="white")
            plt.tight_layout()
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            return Response(output.getvalue(), mimetype='image/png')
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Visualize_null_Val_Percentage(self):
        try:
            import matplotlib.pyplot as plt
            print('CSV File Read Successfully...............\n\n')
            if self.df.isnull().sum().sum() != 0:
                na_df = (self.df.isnull().sum() / len(self.df)) * 100
                na_df = na_df.drop(na_df[na_df == 0].index).sort_values(ascending=False)
                missing_data = pd.DataFrame({'Missing Values Ratio %': na_df})
                missing_data['Columns'] = missing_data.index
                # Figure Size
                plt.clf()
                plt.cla()
                fig, ax = plt.subplots(figsize=(9,6))
                fig.set_facecolor("aliceblue")
                # Horizontal Bar Plot
                bars = ax.barh(missing_data.iloc[:, 1], missing_data.iloc[:, 0], color='crimson')
                for bar in bars:
                    bar.set_height(0.3)
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)

                # Add padding between axes and labels
                # ax.xaxis.set_tick_params(pad=20, labelsize=15)
                # ax.yaxis.set_tick_params(pad=20, labelsize=15)

                for i, v in enumerate(missing_data.iloc[:, 0]):
                    ax.text(v + 1.5, i, str(str(round(v, 2)) + '%'), color='red', fontsize=15)

                # Add x,y gridlines
                # ax.grid(b=True, linestyle='-.', linewidth=0.5, alpha=0.2,color="aliceblue")

                # Show top values
                ax.invert_yaxis()

                # Add Plot Title
                # ax.set_title('Columns Having Null Values', fontdict={'fontsize': 25}, pad=20)

                ax.set_xlabel('')
                ax.set_ylabel('')

                # Show Plot
                plt.tight_layout()
                output = io.BytesIO()
                FigureCanvas(fig).print_png(output)
                return Response(output.getvalue(), mimetype='image/png')
            else:
                print('No Missing Values Found.')
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def visualize_attr_all_value_count(self, columnToVisualize):
        try:
            import matplotlib.pyplot as plt
            print('CSV File Readed Successfully...............\n\n')
            df = self.df.astype(str)
            plt.clf()
            plt.cla()
            lst = list(df[columnToVisualize].value_counts()[:10])
            max_index = lst.index(max(lst))
            explode_value = tuple([.06 if i != max_index else 0.2 for i in range(len(list(lst)))])
            fig = (df[columnToVisualize].value_counts()[:10]).plot(kind='pie', figsize=(8, 5.5), autopct='%1.2f%%',
                                                             shadow=False, explode=explode_value, pctdistance=0.65,
                                                             labeldistance=1.1)
            # draw circle
            centre_circle = plt.Circle((0, 0), 0.50, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            plt.title(str(columnToVisualize.capitalize()),
                      fontsize=20, pad=10)
            plt.ylabel("")
            plt.xlabel("")
            plt.tight_layout()
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            return Response(output.getvalue(), mimetype='image/png')
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def visualize_all_attr_stats(self, columnToVisualize):
        try:
            import matplotlib.pyplot as plt
            df = self.df
            print('CSV File Readed Successfully...............\n\n')
            describe_num_df = df.describe(include=['int64', 'float64']).apply(
                lambda s: s.apply(lambda x: format(x, 'g')))
            describe_num_df = describe_num_df.apply(pd.to_numeric)
            describe_num_df.reset_index(inplace=True)
            describe_num_df = describe_num_df[describe_num_df['index'] != 'count']
            plt.clf()
            plt.cla()
            for i in describe_num_df.columns:
                if columnToVisualize == i:
                    
                    if i in ['index']:
                        continue
                    fig, ax = plt.subplots(figsize=(8,5.5))
                    ax = sns.set_context("notebook", font_scale=1.5, rc={
                                         "lines.linewidth": 4.5})
                    ax = sns.barplot(
                        x="index", y=i, data=describe_num_df, edgecolor='black')
                    ax.set(ylim=(min(describe_num_df[i].tolist()), max(
                        describe_num_df[i].tolist())))
                    plt.title(str(i.capitalize()), fontsize=30,pad=10)
                    plt.ylabel('')
                    plt.xlabel('')
                    # ax.get_figure().savefig((path + '/' + str(i) + ".jpg"))
                    plt.tight_layout()

                    # plt.show()
                    output = io.BytesIO()
                    FigureCanvas(fig).print_png(output)
            return Response(output.getvalue(), mimetype='image/png')
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def visualize_all_attr_distribution(self, columnToVisualize):
        try:
            import matplotlib.pyplot as plt
            df = self.df
            print('CSV File Readed Successfully...............\n\n')
            rqrd_columns = df.select_dtypes(
                include=np.number).columns.tolist()
            for i in rqrd_columns:
                if columnToVisualize == i:
                    plt.clf()
                    plt.cla()
                    f, (ax_box, ax_hist) = plt.subplots(
                        2, sharex=True, gridspec_kw={"height_ratios": (6, 6)}, figsize=(8, 5.5))
                    mean = int(df[i].mean())
                    median = int(df[i].median())
                    mode = int(df[i].mode().values[0])
                    if mean < median:
                        distribution_Result = "Left Skewed"
                    if mean == median:
                        distribution_Result = "Normal Distribution"
                    if mean > median:
                        distribution_Result = "Right Skewed"
                    sns.set(style="darkgrid")
                    flierprops = dict(
                        marker='o', markersize=10, markeredgecolor='black', markerfacecolor='red', alpha=0.5)
                    sns.boxplot(data=df, x=i, ax=ax_box , linewidth=2, width=0.5,
                                color='lightgrey', flierprops=flierprops, orient="h")
                    ax_box.axvline(mean, color='r', linestyle='--')
                    ax_box.axvline(median, color='g', linestyle='-')
                    ax_box.axvline(mode, color='b', linestyle='-')
                    sns.histplot(data=df, x=i, ax=ax_hist, kde=True)
                    ax_hist.axvline(mean, color='r', linestyle='--', label="Mean")
                    ax_hist.axvline(median, color='g',
                                    linestyle='-', label="Median")
                    ax_hist.axvline(mode, color='b', linestyle='-', label="Mode")
                    ax_hist.text(0.35, 1.2, distribution_Result,
                                 transform=ax_hist.transAxes, fontsize='20', color='slategrey', weight='bold')
                    ax_hist.legend()
                    ax_box.set(xlabel=i)
                    fig = plt.gcf()
                    plt.tight_layout()
                    output = io.BytesIO()
                    FigureCanvas(fig).print_png(output)
            return Response(output.getvalue(), mimetype='image/png')
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def visualize_all_attr_Outliers(self, columnToVisualize):
        try:
            import matplotlib.pyplot as plt
            df = self.df
            sns.set(style="darkgrid")
            for i in df.select_dtypes(include=np.number).columns.tolist():
                if i == columnToVisualize:
                    plt.clf()
                    plt.cla()
                    fig, ax = plt.subplots(figsize=(8, 5.5))
                    flierprops = dict(
                        marker='o', markersize=10, markeredgecolor='black', markerfacecolor='red', alpha=0.5)
                    # sns.set(rc={'figure.figsize': (15, 8)})
                    # box plot of the variable height
                    ax = sns.boxplot(df[i], linewidth=2, width=0.5,
                                     color='lightgrey', flierprops=flierprops, orient="h")
                    # xtick, label, and title
                    plt.xticks(fontsize=14)
                    plt.title(str(i.capitalize()), fontsize=30, )
                    plt.tight_layout()
                    # plt.show()
                    output = io.BytesIO()
                    FigureCanvas(fig).print_png(output)
            return Response(output.getvalue(), mimetype='image/png')
        except BaseException as e:
            print('The exception occurs : {}'.format(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    def NoMissingValFoundFigure(self):
        plt.clf()
        plt.cla()
        fig = plt.figure(figsize=(10, 5), facecolor='#EFEFEF')
        plt.tick_params(left=False, right=False, labelleft=False,
                        labelbottom=False, bottom=False)
        plt.text(0.2, 0.5, 'No Missing Value Found!', dict(size=30))
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
